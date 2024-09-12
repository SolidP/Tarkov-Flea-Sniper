import pyautogui
import time
import keyboard

def buy_top_item_max():

    print ("--- Buy attempt")
    # Move the mouse to the first position (example coordinates)
    pyautogui.moveTo(1768, 178)
    # Click the left mouse button
    pyautogui.click()

    # Move the mouse to the second position (example coordinates)
    pyautogui.moveTo(1150, 490)
    # Click the left mouse button
    pyautogui.click()

    # Press the 'Y' key
    pyautogui.press('y')

canRefresh: bool = True

def refresh(t: float):
    print (f"--- canRefresh is {'TRUE' if canRefresh else 'FALSE'}")
    
    if not canRefresh:
        print ("--- Waiting for canRefresh...")

    while not canRefresh:
        time.sleep(0.1)

    print ("--- Refresh!")
    pyautogui.press("f5")
    time.sleep(t)

    return True


def start_refresh_wait():
    canRefresh = False

    time.sleep(3)
    
    canRefresh = True