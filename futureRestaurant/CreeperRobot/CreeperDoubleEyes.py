from SimpleCV import Camera, Display,Color
import SimpleCV
from time import sleep
import requests
from CreeperLegs import MotorDriver
 
lostingtime = 0 # Tracking how long it is lost the way

direction = 0 #0:Straight, #1:Left, #2:Right #3: Reverse

ifRightEyeSees = False # Tracking if right eye can see
ifLeftEyeSees = False # Tracking if left eye can see

rightEye = SimpleCV.Camera(1)
leftEye  = SimpleCV.Camera(0)

legs = MotorDriver()

#myDisplay = Display(resolution=(640,480))

#while not myDisplay.isDone():
while True:
    rightView = rightEye.getImage().resize(320,240)
    leftView  = leftEye.getImage().resize(320,240)

    #check if right eye can see
    dist = rightView.colorDistance(Color.BLACK).dilate(2)
    segmentedRight = dist.binarize(80)
    cropSegmented = segmentedRight.crop(0,80,320,80)
    blobs = cropSegmented.findBlobs(minsize = 300);
    if blobs:
        blobs.draw(width=3)
        ifRightEyeSees = True
    else :
        ifRightEyeSees = False

    #check if left eye can see
    dist = leftView.colorDistance(Color.BLACK).dilate(2)
    segmentedLeft = dist.binarize(80)
    cropSegmented = segmentedLeft.crop(0,80,320,80)
    blobs = cropSegmented.findBlobs(minsize = 300);
    if blobs:
        blobs.draw(width=3)
        ifLeftEyeSees = True
    else:
        ifLeftEyeSees = False
    
    #Determine which direction to go
    if ifLeftEyeSees == True and ifRightEyeSees == True :
       #Both eye see, go straight
       direction = 0
       #r = requests.get('http://127.0.0.1/powerleft/0.3')
       #r = requests.get('http://127.0.0.1/powerright/0.3')
       legs.setMotorRight(0.8)
       legs.setMotorLeft(0.8)
       print "Go Straight"
    elif ifLeftEyeSees == True and ifRightEyeSees == False:
        #Only right eye sees, go right
       direction = 2 
       #r = requests.get('http://127.0.0.1/powerleft/-0.3')
       #r = requests.get('http://127.0.0.1/powerright/0.3')
       legs.setMotorRight(0.8);
       legs.setMotorLeft(0)
       print "Go Left"
    elif ifLeftEyeSees == False and ifRightEyeSees == True :
       #Only feft eye sees, go left
       direction = 1
       #r = requests.get('http://127.0.0.1/powerleft/0.3')
       #r = requests.get('http://127.0.0.1/powerright/-0.3')
       legs.setMotorRight(0)
       legs.setMotorLeft(0.8)
       print "Go Right"
    else:
        #Both eye cannot see
        print "Cannot find way"
        if direction==1:
            #If previously go left, turn right
            legs.setMotorRight(0)
            legs.setMotorLeft(0.8)
            #r = requests.get('http://127.0.0.1/powerleft/-0.2')
            #r = requests.get('http://127.0.0.1/powerright/0.4')
            direction = 2
        elif direction==2:
            #If previously go Right, turn left
            legs.setMotorRight(0.8)
            legs.setMotorLeft(0)
            #r = requests.get('http://127.0.0.1/powerleft/0.4')
            #r = requests.get('http://127.0.0.1/powerright/-0.2')
            direction = 1
        elif direction == 0:
            #If Previously go Straight, reverse a bit
            legs.setMotorRight(-0.8)
            legs.setMotorLeft(-0.8)
            #r = requests.get('http://127.0.0.1/powerleft/-0.3')
            #r = requests.get('http://127.0.0.1/powerright/-0.3')
            direction = 3 
        else:
            #If Previously go reverse, move forward a bit
            legs.setMotorRight(0.8)
            legs.setMotorLeft(0.8)
            #r = requests.get('http://127.0.0.1/powerleft/0.3')
            #r = requests.get('http://127.0.0.1/powerright/0.3')
            direction = 0 
            
        lostingtime = lostingtime + 0.2
        sleep(lostingtime)

        #r = requests.get('http://127.0.0.1/brake')
        legs.exit()
        sleep(0.5)
        
    #left_combined = leftView.sideBySide(segmentedLeft,side="bottom") 
    #right_combined = rightView.sideBySide(segmentedRight,side="bottom")
    #img_combined = left_combined.sideBySide(right_combined,side='right')


    #cropSegmented.save(myDisplay)
    #img_combined.save(myDisplay)

    sleep(.1)