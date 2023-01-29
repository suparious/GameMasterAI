import pyautogui
import pydirectinput
import time
import mss
import gc
import threading
from dataclasses import dataclass
from random import randint
# bring in customized variables
import config
# bring in custom functions
from functions import autoRun
from functions import rotate
from functions import checkHealth
from functions import checkInventory
from functions import unstuck
from functions import checkForResource
from functions import closeMenu

# quality of life settings for developers
pyautogui.FAILSAFE = config.failsafe
pydirectinput.FAILSAFE = config.failsafe

@dataclass
class RunEnv():
  gameWindows = pyautogui.getWindowsWithTitle(config.gameTitle)
  bagCheckDelayMax = config.bagCheckDelayMax
  debug = config.debug
  forwardMoveKey = config.forwardMoveKey
  reverseMoveKey = config.reverseMoveKey
  autorunKey = config.autorunKey
  actionKey = config.actionKey
  failsafe = config.failsafe
  fowardMoveTotal = config.fowardMoveTotal
  flipMouseMove = config.flipMouseMove
  flip = config.flip
  runtime_images_folder = config.runtime_images_folder
  images_folder = config.images_folder
  weaponSelect1 = config.weaponSelect1
  weaponSelect2 = config.weaponSelect2
  weaponSelectDelay = config.weaponSelectDelay
  combatKey1 = config.combatKey1
  combatKey1delay1 = config.combatKey1delay1
  combatKey1delay2 = config.combatKey1delay2
  combatKey2 = config.combatKey2
  combatKey2delay1 = config.combatKey2delay1
  combatKey2delay2 = config.combatKey2delay2
  combatKey3 = config.combatKey3
  combatKey3delay1 = config.combatKey3delay1
  combatKey3delay2 = config.combatKey3delay2
  hotbarKey1 = config.hotbarKey1
  takePots = config.takePots
  emote_list = config.emote_list
  fuckedMax = config.fuckedMax
  maxStuck = config.maxStuck
  prone = config.prone
  sct = mss.mss()
  startTime = time.time()
  bagCheckDelay = 0
  sctGrab = ""
  stopped = True
  currentFoward = 0
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
  
def startup(env):
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
    checkForResource(env)
    checkHealth(env)
    autoRun(env)
    gc.collect()

# Define main loop
def finish(env):
  env.startTime = time.time()  
  ### Main loop
  print("Possible bag full, stopping. Weight:", env.bagWeight,"%")
  closeMenu()
  pyautogui.press(env.weaponActivate)
  time.sleep(.3)
  if not stopped:
    pydirectinput.press(env.autorunKey)
    stopped = True
  time.sleep(.3)
  pyautogui.press(env.prone)
  time.sleep(.3)
  # Clean garbage
  gc.collect()
  print("End of main loop")

# Configure threading
runenv = RunEnv()

startupThread = threading.Thread(name='startup', target=startup(runenv))
captureLoop = threading.Thread(name='capture', target=capture(runenv))
finishThread = threading.Thread(name='finish', target=finish(runenv))

startupThread.run()
captureLoop.start()
finishThread.start()
