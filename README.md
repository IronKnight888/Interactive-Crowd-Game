# Interactive Crowd Game (Ping Pong)
This repository is the first implementation of our interactive game (Ping-Pong in this case) for large audiences. The game was featured during an assembly at our school and it received a lot of good feedback. Over a 1,000 people participated in the game with two sides competing against each other: left and right. 

It would be very much appreciated if you tell us about how you used this project at vartanyildiz@gmail.com or vedicpatel@gmail.com

Link to Video: https://www.youtube.com/watch?v=OcLmcevJgVQ
[![IMAGE_ALT](https://img.youtube.com/vi/OcLmcevJgVQ/maxresdefault.jpg)](https://www.youtube.com/watch?v=OcLmcevJgVQ)

## How it Works
We were able to create an interactive game on this large of a scale with the use of smartphone flashlights and two cameras up on stage. In order for either of the sides to controll their respective paddle, they had to turn on their smartphone flashlights and point them towards the cameras on stage. One camera was positioned on the left while the other on the right and with the captured feed, our program calculated a brightness value between 0-100 of each side. The paddle in-game would then adjust according to the value. With a higher value, the paddle moves up and with a lower value it moves down. 

## Requirements and Necessities
- 2 Cameras- we plan to add support for more (and less) cameras in the future. In our case we used two Sony 1080p broadcasting cameras.
    ### Dependencies
    - OpenCV
    - NumPy
    - Matplotlib

## How to Run
1. Open up command prompt and cd into the directory of your choice
2. Clone this respository
```
git clone https://github.com/artavasdes/Light-Ping-Pong
```
3. Cd into the repository
```
cd Light-Ping-Pong
```
4. Plug in the two cameras
5. Run one of the three python files depending on your camera setup
```
python 1_camera.py
```
```
python 2_camera.py
```
```
python 4_camera.py
```
Or use the following command to record a video of all the camera feed
```
python 2_camera.py --save_video True
```
To see a list of possible commands
```
python 2_camera.py --help
```

6. A unity window for ping pong will automatically open up
7. Follow the prompts for a quick callibration
8. Go ahead and click "play" in the Ping Pong window

### Notes on Command Line Arguments
* Light Range: This command can be accessed by using the argument like so:
```
python 1_camera.py --light_range 140 255
```
The numbers are on a grayscale range so only values between 0-255 are allowed or else an error will occur. The first value represents the low threshold while the second value represents the high threshold. So in this case, only pixels between 140-255 on grayscale will be considered light pixels. It is recommended to adjust these values prior to use, but we have found the default values (140-255) to be adequate. Originally, we had our low threshold value set lower than 140, but due to light from the projector we decided to increase it, thus reducing unwanted interference.

## Unity Game
As of now, there are three gamemodes available to play:
1. Classic Normal- ball moves at a constant speed
2. Classic Hard- ball speeds up by 5% on each successful hit
3. Flashlight Normal- nothing can be seen on screen except for a small radius around the ball
4. Flashlight Hard- Combination of classic hard and flashlight normal

There is also a manual mode available which can be toggled in the main menu. By enabling it, the paddles can be controlled with the following keys respectively: 'W', 'S', Up Arrow and Down Arrow.

## Acknowledgments
Udp Communication code between Python and Unity was borrowed from Siliconifier's [Python-Unity-Socket-Communication](https://github.com/Siliconifier/Python-Unity-Socket-Communication)
