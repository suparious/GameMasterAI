### Define functions
def screenshot(env, region, name, file):
  import mss
  from PIL import Image
  import numpy as np

  #print("capturing screen:", region)
  env.sctImg = Image.fromarray(np.array(env.sct.grab(region)))
  env.sctGrab = env.sct.grab(region)
  env.sctPNG = mss.tools.to_png(env.sctGrab.rgb, env.sctGrab.size)
  #env.sctImg = Image.fromarray(np.array(sct.grab(env.mssRegion)))
  
  # save to file if debugging is enabled
  if env.debug or file:
    filename = env.runtime_images_folder+"/shot-"+name+".png".format(region)
    print("Saving to ", filename)
    mss.tools.to_png(env.sctGrab.rgb, env.sctGrab.size, output=filename)


def autoRun(env):
  import time
  import pydirectinput
  pydirectinput.FAILSAFE = env.failsafe
  from functions import unstuck
  from functions import rotate
  from functions import checkInventory

  checkInventory(env)
  unstuck(env)
  rotate(env)
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
      screenshot(env, env.full_screen, "fucked_up", True)
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
    #random_emote(env)
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
  from functions import combatActivate

  screenshot(env, env.mssRegion, "checkHealth", False)

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
  from functions import checkForResource

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
  screenshot(env, env.mssRegion, "combatActivate", False)

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
        #TODO make a fucntion to replace this, add a cooldown timer
        pyautogui.press(env.hotbarKey1)
        time.sleep(.3)
  pyautogui.press(env.weaponSelect1)
  time.sleep(0.5)
  env.fucked = 0
  env.startTime = time.time()
  env.currentFoward = 0
  checkHealth(env)
  checkForResource(env)

def combatFocus(env):
  import pyautogui
  pyautogui.FAILSAFE = env.failsafe

  screenshot(env, env.full_screen, "combatFocus", False)
  aggro_bar = env.images_folder+"/combat1.png".format(env.full_screen)
  #focus_shot = config.runtime_images_folder+"/shot-focus.png".format(full_screen)
  focus_location = pyautogui.locate(aggro_bar, env.sctImg, grayscale=True, confidence=.65)
  if focus_location is not None:
    focus = pyautogui.center(focus_location)
    focus_x, focus_y = focus
    print("Focusing target, x:", focus_x, "y:", focus_y)
    pyautogui.moveTo(focus_x, focus_y)
    pyautogui.click(focus_x, focus_y)

def random_emote(env):
  import random
  import time
  import pydirectinput
  pydirectinput.FAILSAFE = env.failsafe

  emote = random.choice(env.emote_list)
  print("Emoting:", emote)
  time.sleep(1)
  pydirectinput.press(env.reverseMoveKey)
  time.sleep(0.1)
  pydirectinput.press('return')
  time.sleep(0.1)
  pydirectinput.write('./'+emote)
  time.sleep(0.1)
  pydirectinput.press('return')

def checkInventory(env):
  from PIL import Image
  import numpy as np
  import cv2
  import pydirectinput
  pydirectinput.FAILSAFE = env.failsafe
  from functions import closeMenu

  if env.bagCheckDelay >= env.bagCheckDelayMax:
    pydirectinput.press('tab')
    screenshot(env, env.inventory_bar, "inventory", True)
    closeMenu(env)
    # Check Inventory percentage
    inventory_bar_raw = cv2.imread(env.runtime_images_folder+"/shot-inventory.png", 1)
    alpha = 2.25 # Contrast control (1.0-3.0)
    beta = 0 # Brightness control (0-100)
    enhancement = cv2.convertScaleAbs(inventory_bar_raw, alpha=alpha, beta=beta)
    cv2.imwrite(env.runtime_images_folder+"/shot-inventory_enhanced.png", enhancement)
    inventory_bar_enhanced = Image.open(env.runtime_images_folder+"/shot-inventory_enhanced.png")
    inventory_bar_bw = inventory_bar_enhanced.convert('1', dither=Image.NONE)
    inventory_bar_bw.save(env.runtime_images_folder+"/shot-inventory_bw.png")
    count_pixels = cv2.imread(env.runtime_images_folder+"/shot-inventory_bw.png")
    n_white_pix = np.sum(count_pixels == 255)
    n_black_pix = np.sum(count_pixels == 0)
    total_pix = n_white_pix + n_black_pix
    env.bagWeight = round(n_white_pix / total_pix * 100)
    print('Inventory load:', env.bagWeight, '%')
    env.bagCheckDelay = 0
  env.bagCheckDelay += 1

def closeMenu(env):
  import pyautogui
  import pydirectinput
  pyautogui.FAILSAFE = env.failsafe
  pydirectinput.FAILSAFE = env.failsafe
  from functions import screenshot
  
  screenshot(env, env.mssRegion, "closeMenu", False)
  if pyautogui.locate("imgs/modes0.png", env.sctImg, grayscale=True, confidence=.8) is not None:
    print("closing menu")
    pydirectinput.press('esc')
  if pyautogui.locate("imgs/inventory0.png", env.sctImg, grayscale=True, confidence=.8) is not None:
    print("closing menu")
    pydirectinput.press('esc')

def unstuck(env):
  import time
  import pydirectinput
  pydirectinput.FAILSAFE = env.failsafe

  while env.fucked >= env.fuckedMax:
    print("We are fucked")
    pydirectinput.press('return')
    pydirectinput.write('/unstuck')
    pydirectinput.press('return')
    env.fucked = 0
    env.startTime = time.time()
    env.currentFoward = 0

def checkForResource(env):
  import time
  import pyautogui
  import pydirectinput
  pyautogui.FAILSAFE = env.failsafe
  pydirectinput.FAILSAFE = env.failsafe
  from functions import screenshot

  screenshot(env, env.mssRegion, "checkForResource", False)
  # Find the image on screen, in that region
  if pyautogui.locate("imgs/e1.png", env.sctImg, grayscale=True, confidence=.7) is not None:
    # If not stopped, stop
    if not env.stopped:
      pydirectinput.press(env.autorunKey)
    #print("Stopping. Distance:", round(env.currentFoward), "m, Weight:", env.bagWeight,"%")
    #pydirectinput.keyDown(env.reverseMoveKey)
    #time.sleep(.1)
    #pydirectinput.keyUp(env.reverseMoveKey)
    env.stopped = True
    env.found = True
    env.fucked = 0
    env.startTime = time.time()
    env.currentFoward = 0
  else:
    env.found = False
  while env.found:
    # Interact with detected object
    #print("Pressing Action Key")
    pyautogui.press(env.actionKey)
    time.sleep(0.1)
    # Get a new Screenshot
    screenshot(env, env.mssRegion, "checkForResource", False)
    # Check the status of the interaction
    if pyautogui.locate("imgs/two1.png", env.sctImg, grayscale=True, confidence=.7) is None:
      print("Waiting for object")
      waiting = True
      while waiting:       
        time.sleep(0.5)
        screenshot(env, env.mssRegion, "checkForResource", False)
        if pyautogui.locate("imgs/two1.png", env.sctImg, grayscale=True, confidence=.7) is None:
          waiting = True
        else:
          waiting = False
        # If stuckTracker hits the maxStuck limit, move the mouse
        if env.stuckTracker == env.maxStuck:
          pydirectinput.move(5, 0, relative=True)
          env.stuckTracker = 0
        env.stuckTracker += 1
      # Check for additional resources
      screenshot(env, env.mssRegion, "checkForResource", False)
      if pyautogui.locate("imgs/e1.png", env.sctImg, grayscale=True, confidence=.7) is not None:
        print("Found another object")
        env.found = True
      else:
        env.found = False
    if pyautogui.locate("imgs/e1.png", env.sctImg, grayscale=True, confidence=.7) is None:
      env.found = False
      # If stuckTracker hits the maxStuck limit, move the mouse
    env.startTime = time.time()
    env.currentFoward = 0