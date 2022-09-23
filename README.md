# Interactive Crowd Game (Ping Pong)
This repository is the first implementation of our interactive game (Ping-Pong in this case) for large audiences. The game was featured during an assembly at our school and it received a lot of good feedback. Over a 1,000 people participated in the game with two sides competing against each other: left and right. 

**New**: Future improvements are currently in the works

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
1. Plug in the two cameras
2. Run the main python file
```
python main.py
```
Or use the following command to record a video of all the camera feed
```
python main.py --save_video True
```
To see a list of possible commands
```
python main.py --help
```

3. A unity window for ping pong will automatically open up
4. Follow the prompts for a quick callibration
5. Go ahead and click "play" in the Ping Pong window

## Acknowledgments
Udp Communication code between Python and Unity was borrowed from Siliconifier's [Python-Unity-Socket-Communication](https://github.com/Siliconifier/Python-Unity-Socket-Communication)
