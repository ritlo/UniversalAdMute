from PIL import ImageGrab

def simpleScreenshot():
    screenshot = ImageGrab.grab()
    return screenshot