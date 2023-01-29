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

