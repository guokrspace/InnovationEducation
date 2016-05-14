# InnovationEducation
This repo includes a serial of lessons that aims for children to experience and enjoy the process of innovation. 

## Innovation Box One: Future Restaurant
### 1. Introduction:
This is a restaurant without waiters or waitress, nor providing any food. It is rather a virtual playground with VR devices that Children can play and have a lot of fun. Although it dose not provide any food, it does serve extremely nutritious drinks by Robots so the children wont get disturbed.

### 2. The Robot
The robot follows tha desigated road that is confined with two black lines. The core of the robot is a Raspberry Pi computer with a USB camera. The software will process the image taken by the camera then determine go straight, left or right. This sounds, but we failed millon times achieving the goal. The solutions that failed are,
- One Camera follow one line
The issue is that the motors speed cannot be accurately controlled, when the robot turns, the angel it turns is too wide so the line will be out of view very quickly, therefore, it will often gets out of control.

- Two Cameras follow one line
It seems to be very smart solution, with two eyes, it can easily determine which way to go based on which eyes sees the line or both eyes see the line. However, the problem is that with two cameras, the image process time increased significantly, the delay makes the robot to be out of control. The problem of 1) still exist.

- One Cameras follow a road confined by two lines
The idea is that if it sees nothing, it just go straight, otherwise, the robot will bounce when it sees the line. However, it is very difficult to determine which direction to do, right or left when it was going straight and suddenly sees a black line. 

### 3. Computer Vision and Algorithm
- The program language is [Python](www.python.org)
- The Computer Vision library we used is called [Simple CV](). 
- The algorithm
--
### Finally it works!


