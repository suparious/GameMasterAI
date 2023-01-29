### Define functions
def screenshot(env, region):
  import mss

  print("capturing screen:", region)
  env.sctImg = env.sct.grab(region)
  env.sctPNG = mss.tools.to_png(env.sctImg.rgb, env.sctImg.size)
  # save to file if debugging is enabled
  if env.debug:
    filename = env.runtime_images_folder+"/capture_screen.png".format(region)
    print("Saving to ", filename)
    mss.tools.to_png(env.sctImg.rgb, env.sctImg.size, output=filename)

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