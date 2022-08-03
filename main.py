from waveGenerator import WaveGen
import os

title = """\n\033[36m      .o.       ooooo     ooo  .oooooo..o ooooooooooooo oooooooooooo ooooo      ooo 
\033[36m     .888.      `888'     `8' d8P'    `Y8 8'   888   `8 `888'     `8 `888b.     `8' 
\033[36m    .8"888.      888       8  Y88bo.           888       888          8 `88b.    8  
\033[36m   .8' `888.     888       8   `"Y8888o.       888       888oooo8     8   `88b.  8  
\033[36m  .88ooo8888.    888       8       `"Y88b      888       888    "     8     `88b.8  
\033[36m .8'     `888.   `88.    .8'  oo     .d8P      888       888       o  8       `888  
\033[36mo88o     o8888o    `YbodP'    8""88888P'      o888o     o888ooooood8 o8o        `8"""
title2 = "\033[32m- Hide Your Secret Message in Audio Wave File -\033[37m"

def choose(op):
    if op not in ['1','2','3']:
        return
    
    if op == '3':
        exit()
    
    if op == '1':       # Encode
        secretMessage = input("\033[33mWrite a message: \n\033[37m")
        filename = input("\033[33mName the audio wave file: \033[37m")
        wg.encode(secretMessage, filename)
        input("\n[Press Enter]")

    if op == '2':       # Decode
        audioFileName = input("Name the audio wave file (only if is in the same folder): ")
        wg.decode(audioFileName)
        input("\n[Press Enter]")


def main():
    while True:
        os.system('cls')
        print(title)
        print('\n' + title2)
        operation = input("\n\nPress:\n1) Generate an audio wave file with a secret message\n2) Decode Secret Message from audio .wav file\n3) Quit\n\n>> ")
        choose(operation)

wg = WaveGen()
main()