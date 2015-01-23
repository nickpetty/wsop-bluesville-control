dmxStatus = open("config","r+").read().rstrip()
print dmxStatus
open('config', 'w').write('1')
