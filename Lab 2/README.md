# Interactive Prototyping: The Clock of Pi

Does it feel like time is moving strangely during this semester?

For our first Pi project, we will pay homage to the [timekeeping devices of old](https://en.wikipedia.org/wiki/History_of_timekeeping_devices) by making simple clocks.

It is worth spending a little time thinking about how you mark time, and what would be useful in a clock of your own design.

**Please indicate anyone you collaborated with on this Lab here.**
Be generous in acknowledging their contributions! And also recognizing any other influences (e.g. from YouTube, Github, Twitter) that informed your design. 

## Prep

[Lab prep](prep.md) is extra long this week! Make sure you read it over in time to prepare for lab on Thursday.

### Get your kit
If you are remote but in the US, let the teaching team know you need the parts mailed.

If you are in New York, you can come to the campus and pick up your parts. If you have not picked up your parts by Thursday lab you should come to Tata 351.

### Set up your Lab 2

1. [Pull changes from the Interactive Lab Hub](https://github.com/FAR-Lab/Developing-and-Designing-Interactive-Devices/blob/2021Fall/readings/Submitting%20Labs.md#to-pull-lab-updates) so that you have your own copy of Lab 2 on your own lab hub. (This may have to be done again at the start of lab on Thursday.)
  
  If you are organizing your Lab Hub through folder in local machine, go to terminal, cd into your Interactive-Lab-Hub folder and run:

  ```
  Interactive-Lab-Hub $ git remote add upstream https://github.com/FAR-Lab/Interactive-Lab-Hub.git
  Interactive-Lab-Hub $ git pull upstream Fall2021
  Interactive-Lab-Hub $ git add .
  Interactive-Lab-Hub $ git commit -m'merge'
  Interactive-Lab-Hub $ git push
  ```
  Your local and remote should now be up to date with the most recent files.

2. Go to the [lab prep page](prep.md) to inventory your parts and set up your Pi before the lab session on Thursday.


## Overview
For this assignment, you are going to 

A) [Connect to your Pi](#part-a)  

B) [Try out cli_clock.py](#part-b) 

C) [Set up your RGB display](#part-c)

D) [Try out clock_display_demo](#part-d) 

E) [Modify the code to make the display your own](#part-e)

F) [Make a short video of your modified barebones PiClock](#part-f)

G) [Sketch and brainstorm further interactions and features you would like for your clock for Part 2.](#part-g)

## The Report
This readme.md page in your own repository should be edited to include the work you have done. You can delete everything but the headers and the sections between the \*\*\***stars**\*\*\*. Write the answers to the questions under the starred sentences. Include any material that explains what you did in this lab hub folder, and link it in the readme.

Labs are due on Mondays. Make sure this page is linked to on your main class hub page.

## Part A. 
### Connect to your Pi
Just like you did in the lab prep, ssh on to your pi. Once you get there, create a Python environment by typing the following commands.

```
ssh pi@<your Pi's IP address>
...
pi@ixe00:~ $ virtualenv circuitpython
pi@ixe00:~ $ source circuitpython/bin/activate
(circuitpython) pi@ixe00:~ $ 

```
### Setup Personal Access Tokens on GitHub
The support for password authentication of GitHub was removed on August 13, 2021. That is, in order to link and sync your own lab-hub repo with your Pi, you will have to set up a "Personal Access Tokens" to act as the password for your GitHub account on your Pi when using git command, such as `git clone` and `git push`.

Following the steps listed [here](https://docs.github.com/en/github/authenticating-to-github/keeping-your-account-and-data-secure/creating-a-personal-access-token) from GitHub to set up a token. Depends on your preference, you can set up and select the scopes, or permissions, you would like to grant the token. This token will act as your GitHub password later when you use the terminal on your Pi to sync files with your lab-hub repo.

## Part B. 
### Try out the Command Line Clock
Clone your own lab-hub repo for this assignment to your Pi and change the directory to Lab 2 folder (remember to replace the following command line with your own GitHub ID):

```
(circuitpython) pi@ixe00:~$ git clone https://github.com/<YOURGITID>/Interactive-Lab-Hub.git
(circuitpython) pi@ixe00:~$ cd Interactive-Lab-Hub/Lab\ 2/
```
Depends on the setting, you might be asked to provide your GitHub user name and password. Remember to use the "Personal Access Tokens" you just set up as the password instead of your account one!


Install the packages from the requirements.txt and run the example script `cli_clock.py`:

```
(circuitpython) pi@ixe00:~/Interactive-Lab-Hub/Lab 2 $ pip install -r requirements.txt
(circuitpython) pi@ixe00:~/Interactive-Lab-Hub/Lab 2 $ python cli_clock.py 
02/24/2021 11:20:49
```

The terminal should show the time, you can press `ctrl-c` to exit the script.
If you are unfamiliar with the Python code in `cli_clock.py`, have a look at [this Python refresher](https://hackernoon.com/intermediate-python-refresher-tutorial-project-ideas-and-tips-i28s320p). If you are still concerned, please reach out to the teaching staff!


## Part C. 
### Set up your RGB Display
We have asked you to equip the [Adafruit MiniPiTFT](https://www.adafruit.com/product/4393) on your Pi in the Lab 2 prep already. Here, we will introduce you to the MiniPiTFT and Python scripts on the Pi with more details.

<img src="https://cdn-learn.adafruit.com/assets/assets/000/082/842/large1024/adafruit_products_4393_iso_ORIG_2019_10.jpg" height="200" />

The Raspberry Pi 4 has a variety of interfacing options. When you plug the pi in the red power LED turns on. Any time the SD card is accessed the green LED flashes. It has standard USB ports and HDMI ports. Less familiar it has a set of 20x2 pin headers that allow you to connect a various peripherals.

<img src="https://maker.pro/storage/g9KLAxU/g9KLAxUiJb9e4Zp1xcxrMhbCDyc3QWPdSunYAoew.png" height="400" />

To learn more about any individual pin and what it is for go to [pinout.xyz](https://pinout.xyz/pinout/3v3_power) and click on the pin. Some terms may be unfamiliar but we will go over the relevant ones as they come up.

### Hardware (you have done this in the prep)

From your kit take out the display and the [Raspberry Pi 4](https://cdn-shop.adafruit.com/1200x900/4296-13.jpg)

Line up the screen and press it on the headers. The hole in the screen should match up with the hole on the raspberry pi.

<p float="left">
<img src="https://cdn-learn.adafruit.com/assets/assets/000/087/539/medium640/adafruit_products_4393_quarter_ORIG_2019_10.jpg?1579991932" height="200" />
<img src="https://cdn-learn.adafruit.com/assets/assets/000/082/861/original/adafruit_products_image.png" height="200">
</p>

### Testing your Screen

The display uses a communication protocol called [SPI](https://www.circuitbasics.com/basics-of-the-spi-communication-protocol/) to speak with the raspberry pi. We won't go in depth in this course over how SPI works. The port on the bottom of the display connects to the SDA and SCL pins used for the I2C communication protocol which we will cover later. GPIO (General Purpose Input/Output) pins 23 and 24 are connected to the two buttons on the left. GPIO 22 controls the display backlight.

We can test it by typing 
```
(circuitpython) pi@ixe00:~/Interactive-Lab-Hub/Lab 2 $ python screen_test.py
```

You can type the name of a color then press either of the buttons on the MiniPiTFT to see what happens on the display! You can press `ctrl-c` to exit the script. Take a look at the code with
```
(circuitpython) pi@ixe00:~/Interactive-Lab-Hub/Lab 2 $ cat screen_test.py
```

#### Displaying Info with Texts
You can look in `stats.py` for how to display text on the screen!

#### Displaying an image

You can look in `image.py` for an example of how to display an image on the screen. Can you make it switch to another image when you push one of the buttons?



## Part D. 
### Set up the Display Clock Demo
Work on `screen_clock.py`, try to show the time by filling in the while loop (at the bottom of the script where we noted "TODO" for you). You can use the code in `cli_clock.py` and `stats.py` to figure this out.

### How to Edit Scripts on Pi
Option 1. One of the ways for you to edit scripts on Pi through terminal is using [`nano`](https://linuxize.com/post/how-to-use-nano-text-editor/) command. You can go into the `screen_clock.py` by typing the follow command line:
```
(circuitpython) pi@ixe00:~/Interactive-Lab-Hub/Lab 2 $ nano screen_clock.py
```
You can make changes to the script this way, remember to save the changes by pressing `ctrl-o` and press enter again. You can press `ctrl-x` to exit the nano mode. There are more options listed down in the terminal you can use in nano.

Option 2. Another way for you to edit scripts is to use VNC on your laptop to remotely connect your Pi. Try to open the files directly like what you will do with your laptop and edit them. Since the default OS we have for you does not come up a python programmer, you will have to install one yourself otherwise you will have to edit the codes with text editor. [Thonny IDE](https://thonny.org/) is a good option for you to install, try run the following command lines in your Pi's ternimal:

  ```
  pi@ixe00:~ $ sudo apt install thonny
  pi@ixe00:~ $ sudo apt update && sudo apt upgrade -y
  ```

Now you should be able to edit python scripts with Thonny on your Pi.


## Part E.
### Modify the barebones clock to make it your own

Does time have to be linear?  How do you measure a year? [In daylights? In midnights? In cups of coffee?](https://www.youtube.com/watch?v=wsj15wPpjLY)
I collaborated this design with a teammate, Kaiyuan Deng (kd487) whom we together came up with multiple solutions and implement one of them into Pi. The other solution spaces are placed in Part G as part of sketches and brainstorming.
- Intro to truman clock: it is a functional clock that tells about four stages in a typical day, morning, afternoon, evening and night. By default, we set up four equal length of time scale (6 hours) for each stage, and they evenly divide 24 hours with a different color. For example, in the morning, we display "Good morning" with a light green color that represents a fresh, clean and healthy start of the day. It begins at 6am and last until 12pm, excluding the instant time of 12pm. We display "Good afternoon" with a light orange color that represents a recharging, exciting state to refresh user's mind. It begins at 12pm and lasts until 6pm, excluding 6pm. We then display "Good evening" with a darker blue that shows the after hours, when sun goes down and when user finishes a day. It begins at 6pm and lasts until 12am. Lastly, "Good night" stands for showing the last stage of a day where user will rest for the day, with a dark purple scheme that showcases the sleeping mode. It begins at 12am and lasts until 6am, the next day when a new round of the truman clock operates.
- The time doesn't have to linear because even though in default setting we set up four equal length of time scale to be 6 hours, the clock can vary based on the length of the day and night. For instance, the day will be longer for summer (meaning that there will be longer hours for "Good morning" and "Good afternoon" stages), while the day will be shorter for winter (meaning that there will be longer hours for "Good evening" and "Good night" stages.)
- To measure a year, we thought about changing the color schemes as the time went by. For spring and summer, the clock will be displayed with more vibrant, light colors, while in autumn and winter, the clock can visualize in darker or deeper colors.
- Some pictures representing our design are shown as:
![image](https://user-images.githubusercontent.com/61665501/134278602-4f0a2c3c-9925-4b35-8920-0bfaa841a1af.png)
![image](https://user-images.githubusercontent.com/61665501/134278628-42790da0-3848-402c-a331-a8225b90cb5d.png)
![image](https://user-images.githubusercontent.com/61665501/134278645-c570335e-a55f-4f8c-9166-7282eaf67b3b.png)
![image](https://user-images.githubusercontent.com/61665501/134278660-cba5b22a-62a4-47bc-ac3c-d17bb607155e.png)


Can you make time interactive? You can look in `screen_test.py` for examples for how to use the buttons.
- We plan to make the time interactive now only based on time flies. We don't plan to use the buttons for now. So the scale of each time stage will reduce in colors as the time flies. The background color is black, by default. For instance, for morning stage, the green scale will decrease as the time flies from 6am to 12pm, and it will change directly into blue after 12pm, and so on. Here are some screenshots from the design ideas we planned:

![image](https://user-images.githubusercontent.com/61665501/134278906-9f30b3f6-f679-465a-95dc-bf39f08248f4.png)
![image](https://user-images.githubusercontent.com/61665501/134278918-45a2e42a-cbd3-41f2-967f-3e5b26eb84c2.png)
![image](https://user-images.githubusercontent.com/61665501/134386442-4ceaaee1-be3b-42d2-98e3-e90571f1390a.png)
![image](https://user-images.githubusercontent.com/61665501/134377333-fad36559-5fd0-430b-b006-9b2dce98f2d3.png)


**We strongly discourage and will reject the results of literal digital or analog clock display.**

\*\*\***A copy of your code should be in your Lab 2 Github repo.**\*\*\*
- the code is in truman_clock.py file.

After you edit and work on the scripts for Lab 2, the files should be upload back to your own GitHub repo! You can push to your personal github repo by adding the files here, commiting and pushing.

```
(circuitpython) pi@ixe00:~/Interactive-Lab-Hub/Lab 2 $ git add .
(circuitpython) pi@ixe00:~/Interactive-Lab-Hub/Lab 2 $ git commit -m 'your commit message here'
(circuitpython) pi@ixe00:~/Interactive-Lab-Hub/Lab 2 $ git push
```

After that, Git will ask you to login to your GitHub account to push the updates online, you will be asked to provide your GitHub user name and password. Remember to use the "Personal Access Tokens" you set up in Part A as the password instead of your account one! Go on your GitHub repo with your laptop, you should be able to see the updated files from your Pi!


## Part F. 
## Make a short video of your modified barebones PiClock

\*\*\***Take a video of your PiClock.**\*\*\*
- link to the video: https://youtu.be/GuJpIU0WzvE


## Part G. 
## Sketch and brainstorm further interactions and features you would like for your clock for Part 2.
Here are some of the additional sketches and brainstorming we thought about:
1. we think of adding the meditation activities to each stage to remind users of their wellness. This can incorporate a voice assistant audio that instructs a short meditation session at the beginning of each stage. Users can control if they want to pause or leave the mediation by pressing the buttons on the left.
- morning: ![image](https://user-images.githubusercontent.com/61665501/134385602-7cde8fe2-430e-4419-a234-f5bd2615a097.png)
- afternoon: ![image](https://user-images.githubusercontent.com/61665501/134385639-b8b8e8d9-0bf5-4e1f-9bfc-4e79efdb0f71.png)
- evening: ![image](https://user-images.githubusercontent.com/61665501/134385696-4045c2d4-9452-492d-959b-bfc113ece208.png)
- when the meditation is done: ![image](https://user-images.githubusercontent.com/61665501/134385746-fb55d2af-7f09-421b-8c51-4127ba6296bb.png)


# Prep for Part 2

1. Pick up remaining parts for kit.

2. Look at and give feedback on the Part G. for at least 2 other people in the class (and get 2 people to comment on your Part G!)

# Lab 2 Part 2

Pull Interactive Lab Hub updates to your repo.

Modify the code from last week's lab to make a new visual interface for your new clock. You may [extend the Pi](Extending%20the%20Pi.md) by adding sensors or buttons, but this is not required.

As always, make sure you document contributions and ideas from others explicitly in your writeup.

You are permitted (but not required) to work in groups and share a turn in; you are expected to make equal contribution on any group work you do, and N people's group project should look like N times the work of a single person's lab. What each person did should be explicitly documented. Make sure the page for the group turn in is linked to your Interactive Lab Hub page. 

***Update of Lab2 Design.***
1. I collaborated with Kaiyuan Deng (kd487) on this lab and we were able to receive some thoughtful feedback from during the Thursday lab session. We debriefed as the following: 
- The idea of adding meditation possibly to the truman clock design is cool. It adds more awareness of wellness and maintaining healthy life. But it will depend on if the audio is actually feasible for this lab. 
- In the next iterations, think about whether users would feel stressed to see the time loss, and possibly redesign each stage as a progress bar.


2. **New Truman Clock: Designing a day with ascending progress**
- Introduction: Truman clock a functional clock that tells about four stages in a typical day, from morning, afternoon, evening to night. By default, we set up four equal length of time scale (6 hours) for each stage, and they evenly divide 24 hours with a different color. 
- Morning: we display "Good morning" with a light green color that represents a fresh, clean and healthy start of the day. It begins at the sunrise and lasts until 12pm, excluding the instant time of 12pm. By default, the screen is black, and at the time of actual sunrise, the screen started to proceed with the green color with a percentage shown in the middle as the time goes to 12pm. 
- Afternoon: we display "Good afternoon" with a light orange color that represents a recharging, exciting state to refresh user's mind. It begins at 12pm and lasts until the time of sunset, excluding the sunset time. By default, the screen is black, and at the time of 12pm, the screen started to proceed with the orange color with a percentage shown in the middle as the time goes to the sunset. 
- Evening: we then display "Good evening" with a darker blue that shows the after hours, when sun goes down and when user finishes a day. It begins at 6pm and lasts until 12am, excluding the point of 12am. By default, the screen is black, and at the time of 6pm, the screen started to proceed with the blue color with a percentage shown in the middle as the time goes to 12am. 
- Lastly, "Good night" stands for showing the last stage of a day where user will rest for the day, with a dark purple scheme that stands for the sleeping mode. It begins at 12am and lasts until 6am, the next day when a new round of the truman clock operates. 
- Proximity feature: we introduced the proximity sensor feature that tells the actual real time when user puts their palm on the sensor, the screen will switch to a new screen showing the actual time formatting with date, plus real-time “hour+minute+second”. The actual-time screen will last around five seconds and automatically switch back to proceeding progress bar. 
- Significance: based on our feedback, we hope that people using this clock will find a more **relaxing** way to check out the time at a day. Rather than looking at the actual time format, they are shown the primary screens of each stage (morning, afternoon, evening and night) with different colors of progress bar where they would be able to have a sense about the approximate time of the day. In some cases, people need to check out the actual time, so what they can do is simply to put their palm on the sensor and the screen will switch to showing the actual time, in the format of date, plus real-time “hour+minute+second”.
- Here are the images of the iterated sketch for the new truman clock:

3. Video of the Truman Clock:
