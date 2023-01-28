import pyautogui
import pydirectinput
import time
import random
import mss
import numpy as np
from PIL import Image
import gc
import os.path
import cv2

import config

pyautogui.FAILSAFE = False
pydirectinput.FAILSAFE = False

# Global Variables
# Default movement state on startup
stopped = True
# Default movement count in seconds
currentFoward = 0
# Set the initial start time
startTime = ""
sctImg = ""
stuckTracker = 0
mssRegion = ""
full_screen = ""
area_title = ""
inventory_bar = ""
sct = ""
found = False
fucked = 0
bagWeight = 0
bagCheckDelay = 0
shotType = "debug"
combat = False
inventory_load = 0

# Define main loop
def main():
  print("RibRub Bot v", config.version)
  global stopped
  global currentFoward
  global startTime
  global sctImg
  global stuckTracker
  global mssRegion
  global area_title
  global inventory_bar
  global full_screen
  global sct
  global found
  global bagWeight
  global inventory_load

  # Find the Window titled as per the configuration
  gameWindows = pyautogui.getWindowsWithTitle(config.gameTitle)
  for window in gameWindows:
    if window.title == (config.gameTitle):
      gameWindow = window
      break
  # Select that Windowas
  gameWindow.activate()

  # Move your mouse to the center of the game window
  centerW = gameWindow.left + (gameWindow.width/2)
  centerH = gameWindow.top + (gameWindow.height/2)
  pyautogui.moveTo(centerW, centerH)

  # Bring to focus the window under the cursor
  time.sleep(.1)
  pyautogui.click()
  time.sleep(.1)

  # Making tuple with data from the window for later use
  full_screen = (gameWindow.left, gameWindow.top,
    gameWindow.width, gameWindow.height)
  if config.screen_size == "1080p":
    area_title = {"mon": 1, "top": gameWindow.top + 52, "left": gameWindow.left + 810,
      "width": 300, "height": 15}
    inventory_bar = {"mon": 1, "top": gameWindow.top + 86, "left": gameWindow.left + 990,
      "width": 546, "height": 6}
  if config.screen_size == "1440p":
    area_title = {"mon": 1, "top": gameWindow.top + 65, "left": gameWindow.left + 1040,
      "width": 500, "height": 25}
  # dynamic screen
  mssRegion = {"mon": 1, "top": gameWindow.top, "left": gameWindow.left + round(
    gameWindow.width/3), "width": round(gameWindow.width/3)*2, "height": gameWindow.height}

  # Prep screenshots, walk forward and log time
  sct = mss.mss()
  startTime = time.time()

  # Select weapon
  print("Select primary weapon")
  pyautogui.press(config.weaponSelect1)
  time.sleep(config.weaponSelectDelay)

  # Main bot loop, runs forever use CTRL+C to turn it off
  while True:
    #save_shot("area", area_title)
    #time.sleep(1)
    save_shot("dash", full_screen)
    combatFocus()
    # Clean garbage
    gc.collect()
  print("End of main loop")

def save_shot(name, region):
  global sctImg
  global mssRegion
  global full_screen
  global area_title
  global inventory_bar

  ## Save current screenshot
  #filename = "debug/save_shot-"+name+".png".format(**mssRegion)
  #sctImg = sct.grab(mssRegion)
  ## Save to the picture file
  #mss.tools.to_png(sctImg.rgb, sctImg.size, output=filename)
  #print(filename)

  ## Save current screenshot
  #filename = "debug/save_shot-"+name+"-full.png".format(full_screen)
  #sctImg = sct.grab(full_screen)
  ## Save to the picture file
  #mss.tools.to_png(sctImg.rgb, sctImg.size, output=filename)
  #print(filename)

  # Save current screenshot
  filename = config.runtime_images_folder+"/shot-"+name+".png".format(region)
  sctImg = sct.grab(region)
  # Save to the picture file
  mss.tools.to_png(sctImg.rgb, sctImg.size, output=filename)
  #print(filename)

def combatFocus():
  global full_screen

  save_shot("focus", full_screen)
  aggro_bar = config.images_folder+"/combat1.png".format(full_screen)
  focus_shot = config.runtime_images_folder+"/shot-focus.png".format(full_screen)
  focus_location = pyautogui.locate(aggro_bar, focus_shot, grayscale=True, confidence=.7)
  if focus_location is not None:
    print("Focusing target")
    focus = pyautogui.center(focus_location)
    focus_x, focus_y = focus
    pyautogui.click(focus_x, focus_y)
    #print("x:", focus_x, "y:", focus_y)
  time.sleep(.5)

def on_exists(fname: str) -> None:
  if os.path.isfile(fname):
    newfile = f"{fname}.old"
    print(f"{fname} -> {newfile}")
    os.rename(fname, newfile)

# Execute the loop
if __name__ == '__main__':
    main()
