import sys
import struct
from bitarray import bitarray
import numpy as np

class WaveGen:

    def __init__(self, frequency=440, channels=2):
        
        self.SAMPLE_RATE = 44100
        self.BIT_FOR_SAMPLE = 16
        self.FREQUENCY = frequency
        self.CHANNELS = channels
        self.TIME = 1

        self.bitArray = b''

    
    def bitMessage(self, line):
        bitLine = ''
        for c in line:
            bitLine += bin(ord(c))[2:].zfill(8)
        return bitLine
    
    
    def intToByte(self, n, lenght=4):
        l, f = '<', ''
        if (lenght == 2): f = 'h'
        else: f = 'i'
        
        bitValue = struct.pack(l+f, n)
        self.bitArray += bitValue

        
    def ChunkID(self):
        self.bitArray += b'RIFF'

    
    def ChunkSize(self):
        size = 36 + ((self.SAMPLE_RATE * self.TIME) * self.CHANNELS * self.BIT_FOR_SAMPLE // 8)    # NumSamples * NumChannels * BitperSample/8
        self.intToByte(size)

    
    def Format(self):
        self.bitArray += b'WAVE'

    
    def SubChunk1ID(self):
        self.bitArray += b'fmt '

    
    def SubChunk1Size(self):
        self.intToByte(16)

    
    def AudioFormat(self):
        self.intToByte(1, lenght=2)


    def NumChannels(self):
        self.intToByte(self.CHANNELS, lenght=2)


    def SampleRate(self):
        self.intToByte(self.SAMPLE_RATE)

    
    def ByteRate(self):
        byteRate = self.SAMPLE_RATE * self.CHANNELS * self.BIT_FOR_SAMPLE // 8
        self.intToByte(byteRate)

    
    def BlockAlign(self):
        blockAlaign = self.CHANNELS * self.BIT_FOR_SAMPLE // 8  # NumChannels * BitsPerSamples//8
        self.intToByte(blockAlaign, lenght=2)
    

    def BitPerSample(self):
        self.intToByte(self.BIT_FOR_SAMPLE, lenght=2)
    
    
    def Subchunk2ID(self):
        self.bitArray += b'data'


    def Subchunk2Size(self):
        size = (self.SAMPLE_RATE * self.TIME) * self.CHANNELS * self.BIT_FOR_SAMPLE // 8
        self.intToByte(size)

    
    def AppendAudioData(self, secretMessage):
        secret = self.bitMessage(secretMessage + '#1991#')
        if (len(secret) > (self.SAMPLE_RATE)):
            print("\033[31mMessage too long.")
            return False     

        self.data = np.linspace(0, self.TIME, (self.SAMPLE_RATE * self.TIME), endpoint=True)
        signal = np.sin(2 * np.pi * self.FREQUENCY * self.data)
        signal *= 32767
        signal = np.int16(signal)
        
        for i in range(len(secret)):
            if secret[i] == '1':
                signal[i] = signal[i] | 1                           # change LSB with 1
            elif secret[i] == '0':
                signal[i] = signal[i] & ~1                          # change LSB with 0
        
        for s in signal:
            self.intToByte(s)
        
        return True
    

    def WriteItDown(self, filename):
        with open(filename + '.wav', 'wb') as f:
            f.write(self.bitArray)

    
    def encode(self, secretMessage, filename):
        print("\033[33mEncoding message...")
        self.bitArray = b''                     # reset the array

        self.ChunkID()
        self.ChunkSize()
        self.Format()
        self.SubChunk1ID()
        self.SubChunk1Size()
        self.AudioFormat()
        self.NumChannels()
        self.SampleRate()
        self.ByteRate()
        self.BlockAlign()
        self.BitPerSample()
        self.Subchunk2ID()
        self.Subchunk2Size()
        
        if self.AppendAudioData(secretMessage):          # encoding message...       
            self.WriteItDown(filename)
            print("\033[32mDone.\033[37m")
        else:
            print("\033[31mEncoding Failed\033[37m")
    
    
    def decode(self, filename):
        if filename[-4:] != '.wav':
            filename = filename + '.wav'

        index = 44
        bitsLine, decription = '', ''

        try:
            data = open(filename, "rb").read()
            sampleRate = int.from_bytes(data[24:28], byteorder=sys.byteorder)   # 44100

            for _ in range(sampleRate):
                value = int.from_bytes(data[index:index+4], byteorder=sys.byteorder, signed=True)
                lsb = bin(value).lstrip('-0b').rjust(8, '0')[-1]
                bitsLine += lsb
                index += 4

                if len(bitsLine) == 8:                      # entire byte reached
                    decription += chr(int(bitsLine, 2))     # write char
                    bitsLine = ''                           # reset the 8-bitsLine
                    if decription[-6:] == '#1991#':         # search for the end string
                        break

            secretMessage = decription[:-6]
            if len(secretMessage) == 0 or decription[-6:] != '#1991#':
                print("\033[31mMessage not found.\033[37m")
            else:
                print(f"\n\033[32mMessage found:\033[37m\n\n'{secretMessage}'\n\n\033[33m*** End of Message ***\033[37m")
        
        except FileNotFoundError as e:
            print(f"\033[31m{e}\033[37m")
        