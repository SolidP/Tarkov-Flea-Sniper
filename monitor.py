from PIL import Image
import pyautogui
import pytesseract
import time
import cv2
import numpy as np

def preprocess_image(image):
    # Convert PIL image to OpenCV format (numpy array)
    image_np = np.array(image)
    
    # Convert to grayscale
    gray_image = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)
    
    # Apply adaptive thresholding to get a binary image
    thresh_image = cv2.adaptiveThreshold(
        gray_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
        cv2.THRESH_BINARY_INV, 11, 2
    )
    
    # Convert back to PIL image
    preprocessed_image = Image.fromarray(thresh_image)
    
    return preprocessed_image
bank_region = (1520, 64, 105, 25)
price_region = (1334, 154, 160, 34)
notif_region = (630, 120, 1, 1)

def take_screenshot(region=None):
    screenshot = pyautogui.screenshot(region=region)
    
    return screenshot

def detect_numbers_in_image(image):
    detected_text = pytesseract.image_to_string(image, config='--psm 8 -c tessedit_char_whitelist=0123456789')
    
    return detected_text.strip()

def check_top_item_price(min_price, max_price):
    top_item_price = int(detect_numbers_in_image(take_screenshot(price_region)))
    time.sleep(0.2)
    print (f"--- Top item price is: {top_item_price} rub.")

    if top_item_price >= min_price and top_item_price <= max_price:
        return True
    else:
        return False

def is_notification_shown():
    print ("Checking for notification...")
    color = take_screenshot(notif_region).getpixel((0,0))
    
    if color[0] != 255:
        print ("--- Notification Shown")
        return False
    else:
        print ("--- Clear")
        return True

def is_bank_in_treshold(treshold):
    return True # Shit's unstable cuz of the tesseract
    print ("Checking if bank's money is in treshold...")
    money = int(detect_numbers_in_image(take_screenshot(bank_region)))

    print (f"--- Bank has: {money} rub.")

    if money > int(treshold):
        return True
    else:
        if money == 0:
            return True
        else:
            return False
    