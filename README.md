# Voice Assisted Billiards System (VABS)
NEU Capstone Project

This project involved creating a variation on billiards that would be accessible for anyone regardless of physical capability. The overall components are as follows:

**1. The Sphero**

![Sphero](https://target.scene7.com/is/image/Target/GUEST_21437067-5bb5-4bd5-ad0c-f8f250a0be94?wid=488&hei=488&fmt=pjpeg)

The Sphero will be used in place of a regular cue ball. It is slightly larger, but is able to be controlled via bluetooth. Custom functions for controlling the Sphero have been written.

**2. The Camera**

 ![Intel Realsense](https://images-na.ssl-images-amazon.com/images/I/41MpF-1GVmL._AC_SY450_.jpg)
 
 The Intel Realsense D415 will take images of the pool table from the top of a mount and feed them into our written library which will detect the location of the Sphero in the image.
 
 **3. The Projector**
 
 Based on the location of the Sphero as well as some known offset values, a compass is projected around the Sphero showing the direction the Sphero currently will shoot in.
 
 **4. The App (Currently unfinished)**
 
 The idea was for the app to control everything. The user would speak or just input a command such as "Move 45 degrees" or "Shoot with full power". Over bluetooth, that signal would be sent to our module, where a signal to the Sphero rotates it, the compass is reprojected with the new direction, then the Sphero will fire if that is the given command. 
