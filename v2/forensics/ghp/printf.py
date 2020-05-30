import os
from ctypes import *


def run_windows():
	
	msvcrt = cdll.msvcrt
	message_string = "Hello Windows!\n"
	msvcrt.printf("Success: %s", message_string)


def run_linux():
	
	libc = CDLL("libc.so.6")
	message_string = "Hello Linux!\n"
	libc.printf("Success: %s", message_string)
	

def main():
	
	if os.name == 'nt':
		run_windows()
	else:
		run_linux()
		
		
if __name__ == '__main__':
	main()
