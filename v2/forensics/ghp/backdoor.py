import sys
from ctypes import *
from my_debugger_defines import *

kernel32 = windll.kernel32
PAGE_EXECUTE_READWRITE = 0x00000040
PROCESS_ALL_ACCESS = (0x000F0000 | 0x00100000 | 0xFFF)
VIRTUAL_MEM = (0x1000 | 0x2000)

# This is the original executable #
path_to_exe = "C:\\calc.exe"

startupinfo = STARTUPINFO()
process_information = PROCESS_INFORMATION()
creation_flags = CREATE_NEW_CONSOLE
startupinfo.dwFlags = 0x1
startupinfo.wShowWindow = 0x0
startupinfo.cb = sizeof(startupinfo)

kernel32.CreateProcessA(path_to_exe, None, None, None, None, creation_flags, None, None, byref(startupinfo), byref(process_information))

pid = process_information.dwProcessId
