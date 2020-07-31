import base64
import colorama
from colorama import init
from pyfiglet import figlet_format
import socket
import sys
from termcolor import cprint
import threading
import os

def main():

    def getoption():
        option =input("\n\t ENTER OPTION: ")
        callfile(option)

    def callfile(option):
        if option == '1':
            os.system("python3 server.py")
        elif option == '2':
            os.system("python3 client.py ")
        else:
            print("\n\t INVALID INPUT")
            getoption()

    colorama.init()
    cprint(figlet_format('PROXIMITY', font="standard"), "cyan")

    print("\n\t 1) Start a new Chat-Room")
    print("\t 2) Join existing Chat-Room")

    getoption()

main()