### Define functions
def screenshot(env, region, name):
  import mss
  from PIL import Image
  import numpy as np

  print("capturing screen:", region)
  env.sctImg = Image.fromarray(np.array(env.sct.grab(region)))
  env.sctGrab = env.sct.grab(region)
  env.sctPNG = mss.tools.to_png(env.sctGrab.rgb, env.sctGrab.size)
  #env.sctImg = Image.fromarray(np.array(env.sct.grab(env.mssRegion)))
  
  # save to file if debugging is enabled
  if env.debug:
    filename = env.runtime_images_folder+"/shot-"+name+".png".format(region)
    print("Saving to ", filename)
    mss.tools.to_png(env.sctGrab.rgb, env.sctGrab.size, output=filename)


def autoRun(env):
  import time
  import pydirectinput
  pydirectinput.FAILSAFE = env.failsafe

  # Check autorun state
  if env.stopped:
    print("Auto-run activating")
    pydirectinput.press(env.forwardMoveKey)
    pydirectinput.press(env.autorunKey)
    env.stopped = False
    env.startTime = time.time()
    env.currentFoward = 0

def rotate(env):
  import time
  import pydirectinput
  pydirectinput.FAILSAFE = env.failsafe

  if env.fucked >= 2:
    #toggle run
    print("Getting bored")
  # Rotate if you reach the max move time (config.fowardMoveTotal)
  if env.currentFoward >= env.fowardMoveTotal:
    env.fucked += 1
    print("Rotating:", env.fucked, "Distance:", round(env.currentFoward))
    if env.debug:
      print("Screenshotting the shit show")
      #save_shot("fucked", env.full_screen)
    if not env.stopped:
      pydirectinput.press('space')
      time.sleep(.2)
      pydirectinput.press(env.autorunKey)
      env.stopped = True
      env.startTime = time.time()
      env.currentFoward = 0
    # sync-up the auto-run state by using a combat skill
    #print("Pressing light attack key")
    #pydirectinput.click()
    #random_emote()
    # Rotate the camera
    for i in range(0, env.flipMouseMove, round(env.flipMouseMove/5)):
      # Moving the mouse a 5th of the total move amount
      pydirectinput.move(round(env.flipMouseMove/5)
                         * (env.flip), 0, relative=True)
      # Wait for .3 seconds
      time.sleep(.3)
    env.flip *= -1

# Define health check function
def checkHealth(env):
  import time
  import pyautogui
  pyautogui.FAILSAFE = env.failsafe
  from functions import screenshot

  screenshot(env, env.mssRegion, "checkHealth")

  # Find the image on screen, in that region
  if pyautogui.locate("imgs/health1.png", env.sctImg, grayscale=True, confidence=.65) is not None:
    print("Combat Detected")
    env.combat = True
    env.fucked = 0
  else:
    if pyautogui.locate("imgs/health3.png", env.sctImg, grayscale=True, confidence=.65) is not None:
      print("Combat Detected")
      env.combat = True
      env.fucked = 0
    else:
      env.combat = False
  while env.combat:
    env.fucked = 0
    env.currentFoward = 0
    env.startTime = time.time()
    combatActivate(env)

def combatActivate(env):
  import time
  import pyautogui
  import pydirectinput
  pyautogui.FAILSAFE = env.failsafe
  pydirectinput.FAILSAFE = env.failsafe
  from functions import screenshot
  from functions import combatFocus

  # If not in a stopped state, set as stopped
  if not env.stopped:
    env.stopped = True
    pydirectinput.press(env.autorunKey)
  print("Stopping. Distance:", round(env.currentFoward), "m, Weight:", env.bagWeight,"%")
  pydirectinput.keyDown(env.reverseMoveKey)
  time.sleep(.1)
  pydirectinput.keyUp(env.reverseMoveKey)
  combatFocus(env)
  print("Pressing Combat Keys")
  pyautogui.press(env.weaponSelect1)
  time.sleep(env.weaponSelectDelay)
  pyautogui.press(env.combatKey2)
  time.sleep(env.combatKey2delay1)
  pyautogui.press(env.combatKey1)
  time.sleep(env.combatKey1delay1)
  #pyautogui.press(env.combatKey3)
  #time.sleep(env.combatKey3delay1)
  env.found = True

  # Get a fresh screenshot
  screenshot(env, env.mssRegion, "combatActivate")

  if pyautogui.locate("imgs/health1.png", env.sctImg, grayscale=True, confidence=.65) is not None:
    print("Combat still detected...")
    combatFocus(env)
    pyautogui.press(env.weaponSelect2)
    time.sleep(env.weaponSelectDelay)
    pyautogui.press(env.combatKey1)
    time.sleep(env.combatKey1delay2)
  else:
    if pyautogui.locate("imgs/health3.png", env.sctImg, grayscale=True, confidence=.65) is not None:
      print("Combat still detected...")
      combatFocus(env)
    else:
      print("End of Combat")
      combat = False
      if env.takePots:
        pyautogui.press(env.hotbarKey1)
        time.sleep(.3)
  pyautogui.press(env.weaponSelect1)
  time.sleep(0.5)
  env.fucked = 0
  env.startTime = time.time()
  env.currentFoward = 0
  checkHealth(env)

def combatFocus(env):
  import pyautogui
  pyautogui.FAILSAFE = env.failsafe

  screenshot(env, env.full_screen, "combatFocus")
  aggro_bar = env.images_folder+"/combat1.png".format(env.full_screen)
  #focus_shot = config.runtime_images_folder+"/shot-focus.png".format(full_screen)
  focus_location = pyautogui.locate(aggro_bar, env.sctImg, grayscale=True, confidence=.65)
  if focus_location is not None:
    focus = pyautogui.center(focus_location)
    focus_x, focus_y = focus
    print("Focusing target, x:", focus_x, "y:", focus_y)
    pyautogui.moveTo(focus_x, focus_y)
    pyautogui.click(focus_x, focus_y)