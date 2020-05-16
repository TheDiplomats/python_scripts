import optparse
import ftplib
import sys
from threading import *
from socket import *


screenlock = Semaphore(value=1)

def anonLogin(hostname):
	try:
		ftp = ftplib.FTP(hostname)
		ftp.login('anonymous', 'me@your.com')
		screenlock.acquire()
		print '\n[*] ' + str(hostname) +\
			' FTP Anonymous Logon Succeeded'
		ftp.quit()
		return True
	except Exception, e:
		screenlock.acquire()
		print '\n[-] ' + str(hostname) +\
		' FTP Anonymous Logon failed'
		return False
	finally:
		screenlock.release()


def main():
	parser = optparse.OptionParser('usage %prog '+\
		'-H <target host>')
	parser.add_option('-H', dest="tgtHost", type="string", \
		help='specify target hosts separated by a comma')
	(options, args) = parser.parse_args()
	tgtHosts = str(options.tgtHost).split(',')

	if not len(sys.argv) > 1:
		print '[!] You must specify a target host(s).'
		print parser.usage
		exit(0)

	else:
		setdefaulttimeout(1)
		for host in tgtHosts:
			t = Thread(target=anonLogin, args=(host,))
			t.start()

		
if __name__ == '__main__':
	main()
