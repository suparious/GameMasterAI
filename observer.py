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
import threading
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from random import randint
import config

pyautogui.FAILSAFE = False
pydirectinput.FAILSAFE = False

@dataclass
class RunEnv():
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
  bagCheckDelay = config.bagCheckDelayMax
  shotType = "debug"
  combat = False

  gameWindows = pyautogui.getWindowsWithTitle(config.gameTitle)
  
def capture_setup(env):
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

# Define the capture loop
def capture(env):
  # begin capture loop
  while True:
    capture_screen(env.full_screen)
    time.sleep(0.4)

# Define main loop
def main(env):
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


  # Find the Window titled as per the configuration
  
  for window in env.gameWindows:
    if window.title == (config.gameTitle):
      gameWindow = window
      break
  ## Select that Windowas
  #gameWindow.activate()

  

  # Making tuple with data from the window for later use
  
  

  # Prep screenshots and set elapsed time counter
  sct = mss.mss()
  startTime = time.time()

  # Select weapon
  print("Select primary weapon")
  pyautogui.press(config.weaponSelect1)
  time.sleep(config.weaponSelectDelay)

  ### Main loop

  
  time.sleep(.3)
  # Clean garbage
  gc.collect()
  print("End of main loop")

### Define functions
def capture_screen(region):
  global sctImg
  global sctPNG
  sct = mss.mss()
  sctImg = sct.grab(region)
  sctPNG = mss.tools.to_png(sctImg.rgb, sctImg.size)

def save_shot(name, region):
  global sctImg
  global sctPNG

  # Save current screenshot
  #filename = config.runtime_images_folder+"/shot-"+name+".png".format(region)
  sctImg = sct.grab(region)
  # Save to the picture file
  #mss.tools.to_png(sctImg.rgb, sctImg.size, output=filename)
  sctPNG = mss.tools.to_png(sctImg.rgb, sctImg.size)
  #print(filename)

def autoRun():
  global stopped
  global startTime
  global currentFoward

  # Check autorun state
  if stopped:
    print("Auto-run activating")
    pydirectinput.press(config.forwardMoveKey)
    pydirectinput.press(config.autorunKey)
    stopped = False
    startTime = time.time()
    currentFoward = 0

# Define mouse rotate function
def rotate():
  global currentFoward
  global startTime
  global stopped
  global fucked

  checkHealth()
  if fucked >= 2:
    #toggle run
    print("could toggle run now")
  # Rotate if you reach the max move time (config.fowardMoveTotal)
  if currentFoward >= config.fowardMoveTotal:
    fucked += 1
    print("Rotating:", fucked, "Distance:", round(currentFoward))
    save_shot("fucked", full_screen)
    if not stopped:
      pydirectinput.press('space')
      time.sleep(.2)
      pydirectinput.press(config.autorunKey)
      stopped = True
      startTime = time.time()
      currentFoward = 0
    # sync-up the auto-run state by using a combat skill
    #print("Pressing light attack key")
    #pydirectinput.click()
    #random_emote()
    # Rotate the camera
    for i in range(0, config.flipMouseMove, round(config.flipMouseMove/5)):
      # Moving the mouse a 5th of the total move amount
      pydirectinput.move(round(config.flipMouseMove/5)
                         * (config.flip), 0, relative=True)
      # Wait for .3 seconds
      time.sleep(.3)
    config.flip *= -1

# Define resouce check function
def checkForResource():
  global sctImg
  global stopped
  global sct
  global mssRegion
  global stuckTracker
  global found
  global fucked
  global currentFoward
  global startTime
  global bagWeight

  # Take a screenshot
  sctImg = Image.fromarray(np.array(sct.grab(mssRegion)))
  # Find the image on screen, in that region
  if pyautogui.locate("imgs/e1.png", sctImg, grayscale=True, confidence=.7) is not None:
    # If not stopped, stop
    if not stopped:
      pydirectinput.press(config.autorunKey)
    print("Stopping. Distance:", round(currentFoward), "m, Weight:", bagWeight,"%")
    pydirectinput.keyDown(config.reverseMoveKey)
    time.sleep(.1)
    pydirectinput.keyUp(config.reverseMoveKey)
    stopped = True
    found = True
    fucked = 0
    startTime = time.time()
    currentFoward = 0
  else:
    found = False

  while found:
    checkHealth()
    # Interact with detected object
    pyautogui.press(config.actionKey)
    print("Pressing Action Key")
    # Get a new Screenshot
    sctImg = Image.fromarray(np.array(sct.grab(mssRegion)))
    # Check the status of the interaction
    if pyautogui.locate("imgs/two1.png", sctImg, grayscale=True, confidence=.8) is None:
      print("Waiting for object")
      waiting = True
      while waiting:       
        time.sleep(0.5)
        sctImg = Image.fromarray(np.array(sct.grab(mssRegion)))
        if pyautogui.locate("imgs/two1.png", sctImg, grayscale=True, confidence=.8) is None:
          waiting = True
        else:
          waiting = False
        # If stuckTracker hits the maxStuck limit, move the mouse
        if stuckTracker == config.maxStuck:
          pydirectinput.move(5, 0, relative=True)
          stuckTracker = 0
        stuckTracker += 1
      # Check for additional resources
      sctImg = Image.fromarray(np.array(sct.grab(mssRegion)))
      if pyautogui.locate("imgs/e1.png", sctImg, grayscale=True, confidence=.7) is not None:
        print("Found another object")
        found = True
      else:
        found = False
    if pyautogui.locate("imgs/e1.png", sctImg, grayscale=True, confidence=.7) is None:
      found = False
      # If stuckTracker hits the maxStuck limit, move the mouse
    startTime = time.time()
    currentFoward = 0
    time.sleep(1)

# Define health check function
def checkHealth():
  global sctImg
  global sct
  global mssRegion
  global currentFoward
  global startTime
  global combat
  global fucked

  # Take a screenshot
  sctImg = Image.fromarray(np.array(sct.grab(mssRegion)))
  # Find the image on screen, in that region
  if pyautogui.locate("imgs/health1.png", sctImg, grayscale=True, confidence=.65) is not None:
    print("Combat Detected")
    combat = True
    fucked = 0
  else:
    if pyautogui.locate("imgs/health3.png", sctImg, grayscale=True, confidence=.65) is not None:
      print("Combat Detected")
      combat = True
      fucked = 0
    else:
      combat = False
  while combat:
    fucked = 0
    currentFoward = 0
    startTime = time.time()
    combatActivate()

def combatActivate():
  global sctImg
  global sct
  global mssRegion
  global stopped
  global combat
  global bagWeight
  global currentFoward
  global found
  global fucked
  global startTime

  # If not in a stopped state, set as stopped
  if not stopped:
    stopped = True
    pydirectinput.press(config.autorunKey)
  print("Stopping. Distance:", round(currentFoward), "m, Weight:", bagWeight,"%")
  pydirectinput.keyDown(config.reverseMoveKey)
  time.sleep(.1)
  pydirectinput.keyUp(config.reverseMoveKey)
  combatFocus()
  print("Pressing Combat Keys")
  pyautogui.press(config.weaponSelect1)
  time.sleep(config.weaponSelectDelay)
  pyautogui.press(config.combatKey2)
  time.sleep(config.combatKey2delay1)
  pyautogui.press(config.combatKey1)
  time.sleep(config.combatKey1delay1)
  #pyautogui.press(config.combatKey3)
  #time.sleep(config.combatKey3delay1)
  found = True

  # Get a fresh screenshot
  sctImg = Image.fromarray(np.array(sct.grab(mssRegion)))
  if pyautogui.locate("imgs/health1.png", sctImg, grayscale=True, confidence=.65) is not None:
    print("Combat still detected...")
    combatFocus()
    save_shot("combat", full_screen)
    pyautogui.press(config.weaponSelect2)
    time.sleep(config.weaponSelectDelay)
    pyautogui.press(config.combatKey1)
    time.sleep(config.combatKey1delay2)
  else:
    if pyautogui.locate("imgs/health3.png", sctImg, grayscale=True, confidence=.65) is not None:
      print("Combat still detected...")
      combatFocus()
      save_shot("combat", full_screen)
    else:
      print("End of Combat")
      combat = False
      if config.takePots:
        pyautogui.press(config.hotbarKey1)
        time.sleep(.3)
  pyautogui.press(config.weaponSelect1)
  time.sleep(0.5)
  fucked = 0
  startTime = time.time()
  currentFoward = 0
  checkHealth()
  checkForResource()

# Check if we are fucked
def unstuck():
  global fucked
  global startTime
  global currentFoward

  while fucked >= config.fuckedMax:
    print("We are fucked")
    pydirectinput.press('return')
    pydirectinput.write('/unstuck')
    pydirectinput.press('return')
    fucked = 0
    startTime = time.time()
    currentFoward = 0

def closeMenu():
  sctImg = Image.fromarray(np.array(sct.grab(mssRegion))) 
  if pyautogui.locate("imgs/modes0.png", sctImg, grayscale=True, confidence=.8) is not None:
    print("closing menu")
    pydirectinput.press('esc')
  if pyautogui.locate("imgs/inventory0.png", sctImg, grayscale=True, confidence=.8) is not None:
    print("closing menu")
    pydirectinput.press('esc')

def inventoryCheck():
  global sctImg
  global inventory_bar
  global bagWeight
  global bagCheckDelay

  if bagCheckDelay >= config.bagCheckDelayMax:
    pydirectinput.press('tab')
    save_shot("inventory", inventory_bar)
    closeMenu()

    # Check Inventory percentage
    inventory_bar_raw = cv2.imread(config.runtime_images_folder+"/shot-inventory.png", 1)
    alpha = 2.25 # Contrast control (1.0-3.0)
    beta = 0 # Brightness control (0-100)
    enhancement = cv2.convertScaleAbs(inventory_bar_raw, alpha=alpha, beta=beta)
    cv2.imwrite(config.runtime_images_folder+"/shot-inventory_enhanced.png", enhancement)
    inventory_bar_enhanced = Image.open(config.runtime_images_folder+"/shot-inventory_enhanced.png")
    inventory_bar_bw = inventory_bar_enhanced.convert('1', dither=Image.NONE)
    inventory_bar_bw.save(config.runtime_images_folder+"/shot-inventory_bw.png")
    count_pixels = cv2.imread(config.runtime_images_folder+"/shot-inventory_bw.png")
    n_white_pix = np.sum(count_pixels == 255)
    n_black_pix = np.sum(count_pixels == 0)
    total_pix = n_white_pix + n_black_pix
    bagWeight = round(n_white_pix / total_pix * 100)
    print('Inventory load:', bagWeight, '%')
    bagCheckDelay = 0
  bagCheckDelay += 1

def random_emote():
  emote = random.choice(config.emote_list)
  print("Emoting:", emote)
  time.sleep(1)
  pydirectinput.press(config.reverseMoveKey)
  time.sleep(0.1)
  pydirectinput.press('return')
  time.sleep(0.1)
  pydirectinput.write('./'+emote)
  time.sleep(0.1)
  pydirectinput.press('return')

def combatFocus():
  global full_screen

  save_shot("focus", full_screen)
  aggro_bar = config.images_folder+"/combat1.png".format(full_screen)
  focus_shot = config.runtime_images_folder+"/shot-focus.png".format(full_screen)
  focus_location = pyautogui.locate(aggro_bar, focus_shot, grayscale=True, confidence=.65)
  if focus_location is not None:
    focus = pyautogui.center(focus_location)
    focus_x, focus_y = focus
    print("Focusing target, x:", focus_x, "y:", focus_y)
    pyautogui.moveTo(focus_x, focus_y)
    pyautogui.click(focus_x, focus_y)

# Configure threading

captureLoop = threading.Thread(name='')

# Execute the main loop
if __name__ == '__main__':
    main()
