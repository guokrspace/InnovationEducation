from SimpleCV import Camera, Display,Color
import SimpleCV
from time import sleep
import requests

forwardpowerLevel = '1'
reversepowerLevel = '-1'

RIGHT = 2
LEFT = 1
FORWARD = 3
BACKWARD = 4

direction = FORWARD


def goRight():
    print "Go Right"
    direction = RIGHT
    r = requests.get('http://127.0.0.1/powerleft/' + forwardpowerLevel)
    r = requests.get('http://127.0.0.1/powerright/'+ reversepowerLevel)
def goLeft():
    print "Go Left"
    direction = LEFT
    r = requests.get('http://127.0.0.1/powerleft/'+ reversepowerLevel)
    r = requests.get('http://127.0.0.1/powerright/'+ forwardpowerLevel)
def goStraight():
    print "Go Straight"
    direction = RIGHT
    r = requests.get('http://127.0.0.1/powerleft/'+ forwardpowerLevel)
    r = requests.get('http://127.0.0.1/powerright/'+ forwardpowerLevel)
def goBackward():
    direction = Backward
    print "Go Backward"
    r = requests.get('http://127.0.0.1/powerleft/'+ reversepowerLevel)
    r = requests.get('http://127.0.0.1/powerright/'+ reversepowerLevel)
def brake():
    print "Stop"
    r = requests.get('http://127.0.0.1/brake')

viewPortCenterLowThres = 160 
viewPortCenterHighThres = 160
isLookingForRoad = False
#0:Straight, #1:Left, #2:Right #3: Reverse

#myCamera = SimpleCV.Camera(0)
myCamera = Camera(prop_set{"width":320,"height":240})
myDisplay = Display(resolution=(320,480))

xArr = [];
deltaArr = [];
segments = [];
while not myDisplay.isDone():
#while True:
    del xArr[:]
    del deltaArr[:]
    img = myCamera.getImage().resize(320,240)
    img_output = img

    #Binarize
    dist = img.colorDistance(Color.BLACK).dilate(2)
    segmented = dist.binarize(80)
    
    #Divide the view into 6 parts vertically
    for i in range(0,5):
        y = i * 40
        cropSegment = segmented.crop(0,y,320,40)
        blobs = cropSegment.findBlobs(minsize = 300)
        if blobs:
            blobs.draw(width=3)
            xArr.append(blobs[0].x)
        img_output = img_output.sideBySide(cropSegment,side="bottom")


    #See nothing or only see one part, go straight
    if sum(xArr)==0 or len(xArr) == 1:
        goStraight()
        continue

    #print xArr
    #if go straight, then follow the line direction   
    #get the delta array
    for i in range(len(xArr)-1):
        deltaArr.append(xArr[i]-xArr[i+1])

    #print deltaArr
    if direction == FORWARD:

        print deltaArr;
        if sum(deltaArr)/len(deltaArr) > 0:
            goRight()
        elif sum(deltaArr)/len(deltaArr) < 0:
            goLeft()
        else:
            goStraight() 
        # if x2 != 0:
        #     if x2 > viewPortCenterHighThres :
        #         goRight()
        #     elif x2 < viewPortCenterHighThres:
        #         goLeft()
        # elif x1 != 0:
        #     if x1 > viewPortCenterHighThres :
        #         goRight()
        #     elif x1 < viewPortCenterHighThres:
        #         goLeft()
        # elif x0 != 0:
        #     if x0 > viewPortCenterHighThres :
        #         goRight()
        #     elif x0 < viewPortCenterHighThres:
        #         goLeft()
    
    #if was going left,then bounce right
    elif direction == LEFT:
        goRight()
        
    #if was going right, then bounce left
    elif direction == RIGHT:
        goLeft()    
        
        # if blobs:
        #     blobs.draw(width=3)
        #     for blob in blobs:
        #         print direction
        #         print blob.x
        #         if direction == FORWARD:
        #         #First saw in the left side, turn right
        #             if blob.x<viewPortCenterLowThres:
        #                 goRight()
        #         #First saw in the right side, turn left
        #             elif blob.x>viewPortCenterHighThres:
        #                 goLeft()
        #             else :                      
        #                 print "Should not get here"
        #                 brake()
        #         elif direction == LEFT:
        #             goRight()
        #         elif direction == RIGHT:
        #             goLeft()        
        #         break
        # else:
        #     goStraight()


        # #r = requests.get('http://127.0.0.1/brake')
        # sleep(1)
            
    img_output.save(myDisplay)

    sleep(.1)
