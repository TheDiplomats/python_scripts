import crypt


def testPass(cryptPass):
	salt = cryptPass[0:2]
	dictFile = open('dictionary.txt', 'r')
	for word in dictfile.readlines():
		word = word.strip('\n')
		cryptWord1 = crypt.crypt(word, salt)
		if(cryptWord1 == cryptPass):
			print "[*] Password found: " + word + '\n'
			return
	print "[!] Password not found"
	return
	

def main():
	passfile = open("passwords.txt")
	for line in passfile.readlines():
		if ':' in line:
			user = line.split()
			cryptPass = line.split(':')[1].strip(' ')
			print "[*] Cracking password for: " + user
			testPass(cryptPass)
			

if __name__ == "__main__":
	main()
