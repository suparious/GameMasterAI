import pyautogui
import pydirectinput
import time
import mss
import gc
import threading
from dataclasses import dataclass
from random import randint

import cv2
import numpy as np
from PIL import Image
import random

# bring in customized variables
import config
# bring in custom functions
from functions import screenshot
from functions import autoRun

# quality of life settings for developers
pyautogui.FAILSAFE = False
pydirectinput.FAILSAFE = False

@dataclass
class RunEnv():
  sct = mss.mss()
  gameWindows = pyautogui.getWindowsWithTitle(config.gameTitle)
  bagCheckDelay = config.bagCheckDelayMax
  debug = config.debug
  forwardMoveKey = config.forwardMoveKey
  autorunKey = config.autorunKey
  failsafe = config.failsafe
  stopped = True
  currentFoward = 0
  startTime = time.time()
  sctImg = ""
  sctPNG = ""
  stuckTracker = 0
  mssRegion = ""
  full_screen = ""
  area_title = ""
  inventory_bar = ""
  found = False
  fucked = 0
  bagWeight = 0
  shotType = "debug"
  combat = False
  
 
  
def capture_setup(env):
  print("RibRub Bot v", config.version)
  # Iterate through available windows, until we find the gameTitle
  for window in env.gameWindows:
    if window.title == (config.gameTitle):
      # set the matching window
      gameWindow = window
      # stop looking after we found a match
      break
  
  # define the screensize dimentions based on the matching window
  env.full_screen = (gameWindow.left, gameWindow.top, gameWindow.width, gameWindow.height)
  # for 1080p screens
  if config.screen_size == "1080p":
    env.area_title = {"mon": 1, "top": gameWindow.top + 52, "left": gameWindow.left + 810,
      "width": 300, "height": 15}
    env.inventory_bar = {"mon": 1, "top": gameWindow.top + 86, "left": gameWindow.left + 990,
      "width": 536, "height": 6}
  # for 1440p screens
  if config.screen_size == "1440p":
    env.area_title = {"mon": 1, "top": gameWindow.top + 65, "left": gameWindow.left + 1040,
      "width": 500, "height": 25}
  # for dynamic percentage-based screen
  env.mssRegion = {"mon": 1, "top": gameWindow.top, "left": gameWindow.left + round(
    gameWindow.width/3), "width": round(gameWindow.width/3)*2, "height": gameWindow.height}
  
  # Select the matching Window
  gameWindow.activate()
  # Move your mouse to the center of the game window
  centerW = gameWindow.left + (gameWindow.width/2)
  centerH = gameWindow.top + (gameWindow.height/2)
  pyautogui.moveTo(centerW, centerH)
  # Bring to focus the window under the cursor
  time.sleep(.1)
  pyautogui.click()
  time.sleep(.1)
  # Select weapon
  print("Select primary weapon")
  pyautogui.press(config.weaponSelect1)
  time.sleep(config.weaponSelectDelay)

# Define the capture loop
def capture(env):
  # begin capture loop
  while env.bagWeight < 90:
    env.currentFoward += (time.time() - env.startTime)
    screenshot(env, env.full_screen)
    autoRun(env)
    time.sleep(0.4)

# Define main loop
def main(env):
  env.startTime = time.time()  

  ### Main loop
  print("Starting main loop")
  time.sleep(10)

  # Clean garbage
  gc.collect()
  print("End of main loop")



# Configure threading
runenv = RunEnv()

screen_setup = threading.Thread(name='capture_setup', target=capture_setup(runenv))
captureLoop = threading.Thread(name='capture', target=capture(runenv))
mainLoop = threading.Thread(name='main', target=main(runenv))

screen_setup.run()
captureLoop.start()
mainLoop.start()
