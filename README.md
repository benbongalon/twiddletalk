# TwiddleTalk #

Demo of a virtual assistant (personal chatbot) running on your mobile phone that you can silently converse with, using a Twiddler for input.

You type messages on the Twiddler one-handed keyboard while the bot responds by speaking. Wear earphones to keep the conversation private. With enough practise, you can converse without ever looking at your phone's screen. Imagine being able to do this: 

- during meetings
- while walking
- lying in bed in the dark 

This is an alpha release and the bot is not intelligent: it simply says the word or individual letters you typed depending on the mode you select. It will be enhanced in the next releases.

This project is developed with Kivy and Plyer. Here's a video demo:

[![Author using Twiddler3 wirelessly connected to Samsung Galaxy S8 via bluetooth](https://img.youtube.com/vi/otnWRTZA5KU/0.jpg)](https://www.youtube.com/watch?v=otnWRTZA5KU "TwiddleTalk demo")


## Prerequisites ##

1. [Twiddler](https://twiddler.tekgear.com/) one-handed keyboard
2. Mobile phone -- only tested on Android so far
3. Computer -- to download TwiddleTalk and copy to your phone
4. USB cable

## Running ##

You can first try out TwiddleTalk on your computer. You can skip this step, but clone this repository on your computer so you can trasfer it to your phone. 

### Windows ###

1. Install espeak - http://espeak.sourceforge.net/
2. Clone this repository
3. Install Kivy - http://kivy.org/#download
4. Run kivy.bat
5. `pip install plyer`
6. `python TwiddleTalk/main.py`

### OSX ###

1. Clone this repository
2. Install Kivy - http://kivy.org/#download
3. `pip install plyer`
4. `python TwiddleTalk/main.py`

### Linux ###

1. Install espeak or flite from your distro's repositories
2. Clone this repository
3. Install Kivy - http://kivy.org/#download
4. `pip install plyer`
5. `python TwiddleTalk/main.py`


### Android ###

1. If you haven't done so, clone this repository on your computer.
2. Connect the phone to your computer via a USB cable.
3. Create a folder called *'kivy'* in your phone's internal storage. (**NOTE:** */sdcard* is the root of the internal storage.)
4. Copy the *TwiddleTalk* folder that you cloned into the phone's *'kivy'* folder. After the transfer, it's path should be */sdcard/kivy/TwiddleTalk*.

On your phone:

5. Install Kivy Launcher from Google Play
6. Run the Kivy Launcher. You should now see TwiddleTalk as a project.
7. Tap the TwiddleTalk item.


### How to use TwiddleTalk ###

- on start, the default mode is to say each character (letter) you type
- type the Escape key to toggle between SAY_LETTERS and SAY_WORDS
- in SAY_WORDS mode, the program says the completed word after you type a whitespace (Space, Tab, Enter)
- press RESET to start over
- press EXIT to quit


### License ###

The code is licensed under the [MIT License](LICENSE.md).


