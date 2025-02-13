# Observant Systems


For lab this week, we focus on creating interactive systems that can detect and respond to events or stimuli in the environment of the Pi, like the Boat Detector we mentioned in lecture. 
Your **observant device** could, for example, count items, find objects, recognize an event or continuously monitor a room.

This lab will help you think through the design of observant systems, particularly corner cases that the algorithms needs to be aware of.

## Prep

1.  Pull the new Github Repo.
2.  Install VNC on your laptop if you have not yet done so. This lab will actually require you to run script on your Pi through VNC so that you can see the video stream. Please refer to the [prep for Lab 2](https://github.com/FAR-Lab/Interactive-Lab-Hub/blob/Fall2021/Lab%202/prep.md), we offered the instruction at the bottom.
3.  Read about [OpenCV](https://opencv.org/about/), [MediaPipe](https://mediapipe.dev/), and [TeachableMachines](https://teachablemachine.withgoogle.com/).
4.  Read Belloti, et al.'s [Making Sense of Sensing Systems: Five Questions for Designers and Researchers](https://www.cc.gatech.edu/~keith/pubs/chi2002-sensing.pdf).

### For the lab, you will need:

1. Raspberry Pi
1. Webcam 
1. Microphone (if you want to have speech or sound input for your design)

### Deliverables for this lab are:
1. Show pictures, videos of the "sense-making" algorithms you tried.
1. Show a video of how you embed one of these algorithms into your observant system.
1. Test, characterize your interactive device. Show faults in the detection and how the system handled it.

## Overview
Building upon the paper-airplane metaphor (we're understanding the material of machine learning for design), here are the four sections of the lab activity:

A) [Play](#part-a)

B) [Fold](#part-b)

C) [Flight test](#part-c)

D) [Reflect](#part-d)

---

### Part A
### Play with different sense-making algorithms.

#### OpenCV
A more traditional method to extract information out of images is provided with OpenCV. The RPI image provided to you comes with an optimized installation that can be accessed through python. We included 4 standard OpenCV examples: contour(blob) detection, face detection with the ``Haarcascade``, flow detection (a type of keypoint tracking), and standard object detection with the [Yolo](https://pjreddie.com/darknet/yolo/) darknet.

Most examples can be run with a screen (e.g. VNC or ssh -X or with an HDMI monitor), or with just the terminal. The examples are separated out into different folders. Each folder contains a ```HowToUse.md``` file, which explains how to run the python example. 

Following is a nicer way you can run and see the flow of the `openCV-examples` we have included in your Pi. Instead of `ls`, the command we will be using here is `tree`. [Tree](http://mama.indstate.edu/users/ice/tree/) is a recursive directory colored listing command that produces a depth indented listing of files. Install `tree` first and `cd` to the `openCV-examples` folder and run the command:

```shell
pi@ixe00:~ $ sudo apt install tree
...
pi@ixe00:~ $ cd openCV-examples
pi@ixe00:~/openCV-examples $ tree -l
.
├── contours-detection
│   ├── contours.py
│   └── HowToUse.md
├── data
│   ├── slow_traffic_small.mp4
│   └── test.jpg
├── face-detection
│   ├── face-detection.py
│   ├── faces_detected.jpg
│   ├── haarcascade_eye_tree_eyeglasses.xml
│   ├── haarcascade_eye.xml
│   ├── haarcascade_frontalface_alt.xml
│   ├── haarcascade_frontalface_default.xml
│   └── HowToUse.md
├── flow-detection
│   ├── flow.png
│   ├── HowToUse.md
│   └── optical_flow.py
└── object-detection
    ├── detected_out.jpg
    ├── detect.py
    ├── frozen_inference_graph.pb
    ├── HowToUse.md
    └── ssd_mobilenet_v2_coco_2018_03_29.pbtxt
```

The flow detection might seem random, but consider [this recent research](https://cseweb.ucsd.edu/~lriek/papers/taylor-icra-2021.pdf) that uses optical flow to determine busy-ness in hospital settings to facilitate robot navigation. Note the velocity parameter on page 3 and the mentions of optical flow.

Now, connect your webcam to your Pi and use **VNC to access to your Pi** and open the terminal. Use the following command lines to try each of the examples we provided:
(***it will not work if you use ssh from your laptop***)

```
pi@ixe00:~$ cd ~/openCV-examples/contours-detection
pi@ixe00:~/openCV-examples/contours-detection $ python contours.py
...
pi@ixe00:~$ cd ~/openCV-examples/face-detection
pi@ixe00:~/openCV-examples/face-detection $ python face-detection.py
...
pi@ixe00:~$ cd ~/openCV-examples/flow-detection
pi@ixe00:~/openCV-examples/flow-detection $ python optical_flow.py 0 window
...
pi@ixe00:~$ cd ~/openCV-examples/object-detection
pi@ixe00:~/openCV-examples/object-detection $ python detect.py
```

**\*\*\*Try each of the following four examples in the `openCV-examples`, include screenshots of your use and write about one design for each example that might work based on the individual benefits to each algorithm.\*\*\***
- The first example: **Contour** in which this detection can be used to detect the borders of objects, hence we can use it to draw the outlines of objects in our images. The outlines can be extracted to draw a sketch of the objects in the original image. 
![image](https://user-images.githubusercontent.com/61665501/139780534-30717bd7-6ae6-4dba-82eb-33755ab8e9c4.png)

- The second example: **facial detection**, TODO: the user (Yehao) put your screenshots in; if there is a face in the image/video feeds, then greet the person with “why so serious?”
- The third example: **optical flow**, tracking the trajectory of moving objects.
![image](https://user-images.githubusercontent.com/61665501/139780562-1f18de31-bb73-4246-b0db-0c35e0b14141.png)

- The fourth example: **object detection**, adopting object detection to build an educational application for identifying different animals.
![image](https://user-images.githubusercontent.com/61665501/139780636-b6361414-ad3c-4ca2-b341-68ca9da1aceb.png)


#### MediaPipe

A more recent open source and efficient method of extracting information from video streams comes out of Google's [MediaPipe](https://mediapipe.dev/), which offers state of the art face, face mesh, hand pose, and body pose detection.

![Alt Text](mp.gif)

To get started, create a new virtual environment with special indication this time:

```
pi@ixe00:~ $ virtualenv mpipe --system-site-packages
pi@ixe00:~ $ source mpipe/bin/activate
(mpipe) pi@ixe00:~ $ 
```

and install the following.

```
...
(mpipe) pi@ixe00:~ $ sudo apt install ffmpeg python3-opencv
(mpipe) pi@ixe00:~ $ sudo apt install libxcb-shm0 libcdio-paranoia-dev libsdl2-2.0-0 libxv1  libtheora0 libva-drm2 libva-x11-2 libvdpau1 libharfbuzz0b libbluray2 libatlas-base-dev libhdf5-103 libgtk-3-0 libdc1394-22 libopenexr23
(mpipe) pi@ixe00:~ $ pip3 install mediapipe-rpi4 pyalsaaudio
```

Each of the installs will take a while, please be patient. After successfully installing mediapipe, connect your webcam to your Pi and use **VNC to access to your Pi**, open the terminal, and go to Lab 5 folder and run the hand pose detection script we provide:
(***it will not work if you use ssh from your laptop***)


```
(mpipe) pi@ixe00:~ $ cd Interactive-Lab-Hub/Lab\ 5
(mpipe) pi@ixe00:~ Interactive-Lab-Hub/Lab 5 $ python hand_pose.py
```

Try the two main features of this script: 1) pinching for percentage control, and 2) "[Quiet Coyote](https://www.youtube.com/watch?v=qsKlNVpY7zg)" for instant percentage setting. Notice how this example uses hardcoded positions and relates those positions with a desired set of events, in `hand_pose.py` lines 48-53. 

**\*\*\*Consider how you might use this position based approach to create an interaction, and write how you might use it on either face, hand or body pose tracking.\*\*\***
- Body pose tracking can be used to track the body movement during a workout session. Based on the movements, we can give meaningful feedback to the users to facilitate their workout. 

(You might also consider how this notion of percentage control with hand tracking might be used in some of the physical UI you may have experimented with in the last lab, for instance in controlling a servo or rotary encoder.)



#### Teachable Machines
Google's [TeachableMachines](https://teachablemachine.withgoogle.com/train) might look very simple. However, its simplicity is very useful for experimenting with the capabilities of this technology.

![Alt Text](tm.gif)

To get started, create and activate a new virtual environment for this exercise with special indication:

```
pi@ixe00:~ $ virtualenv tmachine --system-site-packages
pi@ixe00:~ $ source tmachine/bin/activate
(tmachine) pi@ixe00:~ $ 
```

After activating the virtual environment, install the requisite TensorFlow libraries by running the following lines:
```
(tmachine) pi@ixe00:~ $ cd Interactive-Lab-Hub/Lab\ 5
(tmachine) pi@ixe00:~ Interactive-Lab-Hub/Lab 5 $ sudo chmod +x ./teachable_machines.sh
(tmachine) pi@ixe00:~ Interactive-Lab-Hub/Lab 5 $ ./teachable_machines.sh
``` 

This might take a while to get fully installed. After installation, connect your webcam to your Pi and use **VNC to access to your Pi**, open the terminal, and go to Lab 5 folder and run the example script:
(***it will not work if you use ssh from your laptop***)

```
(tmachine) pi@ixe00:~ Interactive-Lab-Hub/Lab 5 $ python tm_ppe_detection.py
```


(**Optionally**: You can train your own model, too. First, visit [TeachableMachines](https://teachablemachine.withgoogle.com/train), select Image Project and Standard model. Second, use the webcam on your computer to train a model. For each class try to have over 50 samples, and consider adding a background class where you have nothing in view so the model is trained to know that this is the background. Then create classes based on what you want the model to classify. Lastly, preview and iterate, or export your model as a 'Tensorflow' model, and select 'Keras'. You will find an '.h5' file and a 'labels.txt' file. These are included in this labs 'teachable_machines' folder, to make the PPE model you used earlier. You can make your own folder or replace these to make your own classifier.)

**\*\*\*Whether you make your own model or not, include screenshots of your use of Teachable Machines, and write how you might use this to create your own classifier. Include what different affordances this method brings, compared to the OpenCV or MediaPipe options.\*\*\***
- Here's a screenshot of our try on teachable machine: ![image](https://user-images.githubusercontent.com/61665501/139779261-278a7393-1819-4798-8848-8b91c698ac7e.png)
- Compared to the OpenCV and MediaPipe options, teachable meachine has:
1. An intuitive graphical interface for a user to collect data, train the model, and see the model performance. 
2. Probabilities for each class which helps the user understand how the prediction is made. 
3. platform for classifying data of different modalities, including images and sounds.

*Don't forget to run ```deactivate``` to end the Teachable Machines demo, and to reactivate with ```source tmachine/bin/activate``` when you want to use it again.*


#### Filtering, FFTs, and Time Series data. (optional)
Additional filtering and analysis can be done on the sensors that were provided in the kit. For example, running a Fast Fourier Transform over the IMU data stream could create a simple activity classifier between walking, running, and standing.

Using the accelerometer, try the following:

**1. Set up threshold detection** Can you identify when a signal goes above certain fixed values?

**2. Set up averaging** Can you average your signal in N-sample blocks? N-sample running average?

**3. Set up peak detection** Can you identify when your signal reaches a peak and then goes down?

**\*\*\*Include links to your code here, and put the code for these in your repo--they will come in handy later.\*\*\***
- Here is the link to our code (**part1.py**): https://github.com/angelachen-19/Interactive-Lab-Hub/blob/e42ee11433f5deb405fea869e78be7e475eb80b6/Lab%205/part1.py


### Part B
### Construct a simple interaction.

Pick one of the models you have tried, pick a class of objects, and experiment with prototyping an interaction.
This can be as simple as the boat detector earlier.
Try out different interaction outputs and inputs.

**\*\*\*Describe and detail the interaction, as well as your experimentation here.\*\*\***
- In this part, we created a very simple interaction that allows user to make a "yeah" pose in front of the camera. In this experiment, we adopted Google's MediaPipe that offers the hand pose detection. When a hand is shown the "yeah" gesture with both index and middle fingers up, the camera will be able to recognize the pose and display a "yeah" text on the screen that confirms the accurate information detected.
- A video showing the hand interaction with the system: https://youtu.be/R4UWQaEk4B8.

### Part C
### Test the interaction prototype

Now flight test your interactive prototype and **note down your observations**:
For example:
1. When does it what it is supposed to do?
- When the user makes the “yeah” gesture at a certain distance from the camera.
2. When does it fail?
- when the user’s hand is too far away from the camera.
- when two hands are detected by the camera.
- when the user keeps the pose for a quite short of time
3. When it fails, why does it fail?
- because The system fails when the user’s hand is too far away from the camera because we coded for absolute distance between fingertips rather than relative distances. When the user’s hand is too far, the absolute distance may fall beyond the threshold, and thus fail to trigger the shooting action.
- The system fails when two hands are detected by the camera because the tracking of fingertips under such circumstances becomes unstable, which makes the calculation of distances between fingertips inaccurate.
- The system fails when the user keeps the gesture only for a very short time period because the camera is taking a picture at around 12fps and it may not capture the moment when the user makes the gesture.

4. Based on the behavior you have seen, what other scenarios could cause problems?
- If there are multiple people in the same picture, they may make the “yeah” gesture at the same time, and this can make tracking gestures difficult for the system.

**\*\*\*Think about someone using the system. Describe how you think this will work.\*\*\***
1. Are they aware of the uncertainties in the system?
- User is able to be aware of the uncertainties (such as hand placed in the marginal area to be detected by camera) in the system
2. How bad would they be impacted by a miss classification?
- User will be asked to do again, to make sure their palm and "yeah" pose is fully detected by the camera.
3. How could change your interactive system to address this?
- We planned to modify our code to consider the marginzalied uncetainty to make the system more flexible.
4. Are there optimizations you can try to do on your sense-making algorithm.
- adding more code and set up the margins so that the algorithm can detect more areas with higher accuracy


### Part D
### Characterize your own Observant system

Now that you have experimented with one or more of these sense-making systems **characterize their behavior**.
During the lecture, we mentioned questions to help characterize a material:
* What can you use X for?
* What is a good environment for X?
* What is a bad environment for X?
* When will X break?
* When it breaks how will X break?
* What are other properties/behaviors of X?
* How does X feel?

**\*\*\*Include a short video demonstrating the answers to these questions.\*\*\***
the video: https://youtu.be/R6-CVpC9aQI


### Part 2.

Following exploration and reflection from Part 1, finish building your interactive system, and demonstrate it in use with a video.
**\*\*\*Include a short video demonstrating the finished result.\*\*\***
- **Rock-Scissors-Paper!** Do you know this game?! Yes we all do. For this lab, we, Kaiyuan Deng (kd487), Angela Chen (ac2689), Yehao Zhang (yz2444), and Zhengxing Xue (zx252) together to create a fun and new version of this game through sense-making systems that are taught in this lab session. 
- Sense-making system: OpenCV and MediaPipe
- Update and feedback from Part 1: we acknowledged that the sense-making system will not be able to detect more than one hand, but since we wanted to create the game that involves two players (two hands) interacting together with the camera, we modified the code and now it's updated as **part2.py** (https://github.com/angelachen-19/Interactive-Lab-Hub/blob/286db9d3969d6c9d5ab0cde9f39901768106d73c/Lab%205/part2.py)
- **Game instruction**: two players place their hands in front of the camera and made a pose of either rock, scissor or paper during each round. The MediaPipe will detect both hands‘ locations, and we adopted OpenCV to display and print the each round's result on the screen (in gray blue colors). The rule of the game is based on:
1) scissor > paper
2) paper > rock
3) rock > scissor
4) draw and even game when both hands display the same results, scissor = scissor, paper = paper, and rock = rock.
For the player who wins twice out of the three rounds in total, he or she will be the winner for the game!

- Here's a video to our game playing: **https://youtu.be/YqvtDnU0N14**
- Photos from user testing: 
1) round one: ![image](https://user-images.githubusercontent.com/61665501/140824087-f5c4ca1b-8359-47eb-a9f2-04e307493409.png)
2) round two: ![image](https://user-images.githubusercontent.com/61665501/140824154-09cc7339-35e7-426c-a7fd-7d23d124c3d6.png)
3) round three: ![image](https://user-images.githubusercontent.com/61665501/140824176-cc95640d-66d7-4f7e-9e5e-f653ff18871d.png)

- User testing and feedback
1) we found that when parts of two hands overlapped, the camera cannot detect them and produce the game result. At the same time, it's optimal to have two hands placed in the middle of the camera detection area so that it can quickly sense the objects. In our future iteration, we'd love improve our code in order to avoid the errors made by overlapping.
2) we also noticed that the background setting requires high brightness. During our testing, the camera initially faced the backlight area and the hands were darkened when shown on the screen. The camera sometimes wouldn't able to detect the hands if the background is too dark. In our future iteration, we want to increase the range of brightness detection for the camera.
