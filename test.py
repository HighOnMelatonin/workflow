from getpass import getpass



password = getpass()

raw = open('test.txt','w')
print(password, file = raw)
raw.close()


    
