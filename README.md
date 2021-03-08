# autoCar
autoCar was an attempt at a miniature self driving car. It used a Haar Cascade Classifier to identify the shape of a miniature traffic light, then used the monocular vision method in this [study](https://ieeexplore.ieee.org/document/1336478?tp=&arnumber=1336478&url=http:%2F%2Fieeexplore.ieee.org%2Fxpls%2Fabs_all.jsp%3Farnumber%3D1336478) to determine the distance to the traffic light. To do this first the piCam needed to be calibrated, this was done using OpenCV's provided library for [camera calibration](https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_calib3d/py_calibration/py_calibration.html). After this was done we received the undistorted camera matrix, which was essential to use in the distance calculation to get somewhat accurate results. After this was done, a simple P controller was run with the distance and motor output, the closer the object got to the light, the more it slowed down to ensure smooth deceleration. A more complicated controller was not used as the motors were not powerful enough to cause any sort of oscillation at when the car stopped, thus it was adequate enough to use a P controller.

# Images of the Car
![front](https://imgur.com/a/hS3T4y2)

### Credits
This project was inspired by Zheng Wang's [similar project](https://zhengludwig.wordpress.com/projects/self-driving-rc-car/) using an RC Car and was extended with some features removed to be run on a car that I made myself
