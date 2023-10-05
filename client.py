import RPi.GPIO as GPIO
import os
import pygame as game
import pygame.camera
import sys
import time
import sys
import time
import socket
from PIL import Image

# Network settings
port=8888 
address="192.168.42.1" #server ip
#address="127.0.0.1" 	#local testing ip

size=width, height=  1024, 768	#image size
scale=width, height= 40, 10
timer=0

PIN_DETECT=15			#pin for blink detection signal

# GPIO settings

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN_DETECT, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
print 'GPIO init OK'
input_state1 = True
last_state1 = True

# pygame settings
	
game.init()
game.camera.init()
screen=game.display.set_mode(size)
print 'Pygame init OK'

# camera settings
camera1=game.camera.Camera("/dev/video0", size )
print 'Camera init OK'

# images settings
backimage=('/boot/blink/blackscreenjpg')
captimage=('/boot/blink/captured.jpg')
sendimage=('/boot/blink/sendeded.jpg')



# Show blackscreen 
print("Show black screen\n")
os.system('sudo fbi -d /dev/fb0 -T 1 -a -noverbose '+backimage)  

#create an INET, STREAMing socket
try:
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	print 'Socket Created'
  	s.connect((address, port))
except socket.error:
	print 'Failed to create socket'
	sys.exit()
     

try:
	while (True):	#infinite loop
		last_state1 = input_state1
		input_state1 = GPIO.input(PIN_DETECT) 		
		if ((input_state1)and(not last_state1)):
			camera1.start()		# shot image
			image1=""
			buffer=""
			print 'Blink detected!'
			image1=camera1.get_image()
			camera1.stop()
			
			print 'Captured'
			#pygame.image.save(image1,captimage)
			#os.system('sudo fbi -d /dev/fb0 -T 1 -a -noverbose '+captimage)  
			
			print 'Saved, try to send...'
			
			buffer=pygame.image.tostring(image1,'RGB')	# convert to string buffer
			try:
				s.sendall(buffer)			# send buffer
				print ("Sended"+str(sys.getsizeof(buffer)))	
				
			except:
				print("Falied to send image")
				
					
		time.sleep(0.2)		#Pause for next blink detection loop

except KeyboardInterrupt:
	camera1.stop()
	s.close()


s.close()
