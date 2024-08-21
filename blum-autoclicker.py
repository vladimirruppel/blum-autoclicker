import time
import random
import pygetwindow as gw
import pyautogui
import cv2 as cv
from pynput.mouse import Button, Controller

BLUM_WINDOW_NAME = 'TelegramDesktop'
MAIN_MENU_ACTIVE_PLAY_BUTTON_PATH = 'Screenshot_1.png'
RESULTS_MENU_ACTIVE_PLAY_BUTTON_PATH = 'Screenshot_2.png'

class BlumController:
    def __init__(self):
        self.mouse = Controller()
    
    def scroll_down(self, steps_count):
        self.mouse.scroll(0, -steps_count)

    def click(self):
        self.mouse.press(Button.left)
        self.mouse.release(Button.left)

    def move(self, x, y):
        self.mouse.position = (x, y)

class BlumWindow:
    def __init__(self):
        blumWindows = gw.getWindowsWithTitle(BLUM_WINDOW_NAME)
        if bool(blumWindows):
            self.window = blumWindows[0]
            self.isDefined = True
        else:
            self.isDefined = False

    def focus(self):
        self.window.activate()

    # returns position of top left corner
    def getPosition(self):
        return self.window.topleft

    def getCenterAppPosition(self):
        pos = self.getPosition()
        x = pos.x + self.window.width // 2
        y = pos.y + self.window.height // 2
        return (x, y)

class Timer:
    def start(self, duration):
        self.end_time = time.perf_counter() + duration

    def isElapsed(self):
        return time.perf_counter() >= self.end_time
        
def playGame(window, controller, chance_to_miss):
    print("Starting the game...")

    timer = Timer()
    window_handler = window.window
    game_area = (
        window_handler.left, window_handler.top, window_handler.width, window_handler.height
    )

    timer.start(30.0)
    while not timer.isElapsed():
        scrn = pyautogui.screenshot(region=game_area)

        width, height = scrn.size
        for x in range(0, width, 20):
            for y in range(0, height, 20):
                r, g, b = scrn.getpixel((x, y))
                if (b in range(0, 125)) and (r in range(102, 220)) and (g in range(200, 255)):
                    screen_x = window_handler.left + x + 4
                    screen_y = window_handler.top + y + 1

                    # попадание
                    if (100 - random.randint(1, 100) > chance_to_miss):
                        controller.move(screen_x, screen_y)
                        controller.click()    
                    else:
                        controller.move(screen_x + 10, screen_y + 5)
                    time.sleep(random.uniform(0.001, 0.005))

    print("The game is ended")

def main():
    chance_to_miss = 50 # шанс промазать по цветочку (в %)
    controller = BlumController()
    blum_window = BlumWindow()
    if blum_window.isDefined:
        blum_window.focus()
        time.sleep(0.5)
        
        # Scroll down to reveal buttons
        controller.move(*blum_window.getCenterAppPosition())
        time.sleep(0.1)
        controller.scroll_down(random.randint(20, 24))
        
        # Locate and click the "Play" button in the main menu
        time.sleep(0.2)
        mmbtn_location = pyautogui.locateCenterOnScreen(MAIN_MENU_ACTIVE_PLAY_BUTTON_PATH, confidence=0.9)
        if mmbtn_location:
            print(f"Found button at {mmbtn_location}")
            controller.move(*mmbtn_location)
            time.sleep(0.1)
            controller.click()
            while True:
                playGame(blum_window, controller, chance_to_miss)
                print("Lil chill...")
                time.sleep(random.uniform(5, 6.5))
                rmbtn_location = pyautogui.locateCenterOnScreen(RESULTS_MENU_ACTIVE_PLAY_BUTTON_PATH, confidence=0.9)
                print(f"Found result menu button at {rmbtn_location}")
                controller.move(*rmbtn_location)
                time.sleep(0.1)
                controller.click()
                
            
        else:
            print("Main menu Play button not found.")
    else:
        print('Blum window is not open')
        
if __name__ == '__main__':
    main()
