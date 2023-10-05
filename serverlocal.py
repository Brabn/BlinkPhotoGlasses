import socket
import sys
from thread import *
import pygame as game
import time
import subprocess
import os
from PIL import Image
 
interval=2.0
showtime=10

print "Blink detection server\nversion 1.65"
# Network settings

port=8888
host=''
address="127.0.0.1" 	#local testing ip
#address="192.168.42.1" #server ip


size=width, height= 1024, 768	#image size
scale=width, height=40, 10
timer = 0
previousImage = ""
image = ""
rimage = ""
message=[]

# images settings
eyeimage3=("/boot/blink/eye3.jpg")
eyeimage2=("/boot/blink/eye2.jpg")
eyeimage=("/boot/blink/eye.jpg")
backimage =("/boot/blink/blackscreen.jpg")
recievedimage=("/boot/blink/recieved")

# Show blackscreen
''' 
print("Show black screen")
os.system('sudo fbi -T 1 -a -noverbose '+backimage)
#os.system('sudo python /boot/blink/fbitest.py')
#time.sleep(5)
'''

# pygame settings

game.init()
#screen=game.display.set_mode(size)
#game.display.set_caption('Socket Raspi Camera Viewer')
print 'Pygame init OK'
 

s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
print 'Socket created'
 
#Start listening on socket
s.listen(4)
print 'Socket now listening'






#device list
maxdevice=3
devicecount=-1
showimage=False
showimageN=-1
deviceid=[0,0,0]
lasttime=[0,0,0]
currtime=[0,0,0]
comptime=[0,0,0]
rimage=["","",""]

# Begin timers
for d in range(0, maxdevice-1):
	lasttime[d]=time.time()
	currtime[d]=time.time()
	comptime[d]=0

print("Waiting for connection...\n")


def showimg(img):
	global backimage
	print("Show back screen")
	os.system('sudo fbi -T 1 -a -noverbose '+img)

#Function for handling connections.
def clientthread(conn,devicenumber):
    global showimage
    global showimageN
    global lasttime
    global currtime
    global comptime
    global rimage
    global recievedimage
    global devicecount
    global game
    currdevice=devicecount
    print 'Connected device number #'+str(currdevice)+', IP '+str(devicenumber)
    
    lasttime[currdevice]=currtime[currdevice]
    currtime[currdevice]=time.time()
    comptime[currdevice]=currtime[currdevice]-lasttime[currdevice]
   
    string=""
    message=[]
    full_string=""
    bufsize=0

    while True:		#infinite loop for listening this connection
	string=conn.recv(1024*1024)

	if (string==''):
		
    		break
	else:
		bufsize+=sys.getsizeof(string)
    		message.append(string)
		
	
	
	full_string="".join(message)
        print '.',
	if (int(bufsize)>=2359316):		#max size for 1027x768 image = 2359317-1
			
			lasttime[currdevice]=currtime[currdevice]
			currtime[currdevice]=time.time()
			comptime[currdevice]=currtime[currdevice]-lasttime[currdevice] 
			print ("Blink from device "+str(currdevice)+"(data "+str(sys.getsizeof(full_string)))
			full_string="".join(message)
                     
			
			try:
				rimage[currdevice]=game.image.fromstring(full_string,size,'RGB')
				game.image.save(rimage[currdevice],recievedimage+str(currdevice)+'.jpg')
				os.system('sudo fbi -T 1 -a -noverbose '+eyeimage2)
				time.sleep(0.2)
				os.system('sudo fbi -T 1 -a -noverbose '+eyeimage)

			except:
				print ("image not saved")
			for d in range(1, devicecount+1):
				print ("blink inerval "+str(d-1)+"-"+str(d)+'='+str(currtime[d-1]-currtime[d]))
				if (abs(currtime[d-1]-currtime[d])<=interval):
					showimage=True
					showimageN=d
					os.system('sudo fbi -T 1 -a -noverbose '+recievedimage+str(d-1)+'.jpg')
					time.sleep(showtime)
					os.system('sudo fbi -T 1 -a -noverbose '+recievedimage+str(d)+'.jpg')
					time.sleep(showtime)
					os.system('sudo fbi -T 1 -a -noverbose '+eyeimage)
					
			if (devicecount>1):
				if (abs(currtime[0]-currtime[devicecount])<=interval):
					showimage=True
					showimageN=d
					os.system('sudo fbi -T 1 -a -noverbose '+recievedimage+str(0)+'.jpg')
					time.sleep(showtime)
					os.system('sudo fbi -T 1 -a -noverbose '+recievedimage+str(devicecount)+'.jpg')
					time.sleep(showtime)
					os.system('sudo fbi -T 1 -a -noverbose '+eyeimage)
			string=""
			message=[]
			full_string=""
			bufsize=0;


	
 
#now keep talking with the client
os.system('sudo fbi -T 1 -a -noverbose '+eyeimage)
showimage=True
pygameinit=False
while 1:
    
    if (not pygameinit):
    	game.init()
        pygameinit=True
    
    if showimage:
	showimage=False
	
    #wait to accept a connection - blocking call
    conn, addr = s.accept()
    
    #print 'Try to connect from ' + addr[0] + ':' + str(addr[1])
    devicenumber=int(addr[0].split('.')[3])
    acceptconnection=True
    for d in deviceid:
	#print 'List: ' + str(d) + ' <- ' + str(devicenumber)
	if (d==devicenumber):
		acceptconnection=False
		break
    if (acceptconnection):
	deviceid[devicecount]=devicenumber
    	devicecount=devicecount+1 
	os.system('sudo fbi -T 1 -a -noverbose '+eyeimage3)
	time.sleep(2)
	os.system('sudo fbi -T 1 -a -noverbose '+eyeimage)
					
    	#start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
    	start_new_thread(clientthread ,(conn,devicenumber,))
game.quit()
s.close()