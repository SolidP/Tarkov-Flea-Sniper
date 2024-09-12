import os
import pyautogui
import tkinter as tk
import time
import keyboard
import threading

from tkinter import messagebox
from tkinter import font
from monitor import take_screenshot, detect_numbers_in_image, check_top_item_price, is_notification_shown, is_bank_in_treshold
from buyer import buy_top_item_max, refresh, start_refresh_wait

preset_wires = [0, 16000]
preset_bolts = [0, 28500]
preset_eslamps = [0, 51111]

def select_price_preset(preset=[0, 0]):
    min_price_entry.delete(0, tk.END)
    min_price_entry.insert(0, preset[0])
    max_price_entry.delete(0, tk.END)
    max_price_entry.insert(0, preset[1])

isActive = False

def install_font(font_path):
    if os.name == 'nt':  # Check if the OS is Windows
        from ctypes import windll
        windll.gdi32.AddFontResourceW(font_path)  # Add the font to the system
        windll.user32.SendMessageW(0xFFFF, 0x001D, 0, 0)  # Notify Windows of the font change

install_font('Jovanny Lemonad - Bender.otf')
install_font('Jovanny Lemonad - Bender-Bold.otf')

# Function to update the Text widget with new output
def log_message(message):
    text_output.insert(tk.END, message + '\n')
    text_output.yview(tk.END)  # Scroll to the end of the text widget

def toggle_mode():
    global isActive
    isActive = not isActive
    log_message(f"Mode toggled. New mode: {'ACTIVE' if isActive else 'INACTIVE'}")
    update_mode_label()

def update_mode_label():
    if isActive:
        mode_label.config(text="Mode: ACTIVE", fg="green")
    else:
        mode_label.config(text="Mode: INACTIVE", fg="red")

def _main_loop():
    global isActive
    while True:
        if isActive:
            try:
                log_message("====== LOOP ======")
                # Refresh the page
                log_message("Refreshing..")
                if refresh(float(refresh_rate.get())):
                    # Check for price
                    # if not is_bank_in_treshold(bank_treshold.get()):
                    #     pyautogui.press("esc")
                    #     log_message("Money is below the treshold, deactivating...")
                    #     isActive = False
                    #     update_mode_label()
                    #     continue
                    if not is_notification_shown():
                        pyautogui.press("esc")
                    log_message("Checking the price of the top item...")
                    if check_top_item_price(int(min_price_entry.get()), int(max_price_entry.get())):  # Is in range
                        buy_top_item_max()
                        another_buy_attempt()
                    else:
                        start_refresh_wait()  # Disabling the button for 3 seconds
                        log_message("Item was not in range")
                else:
                    time.sleep(0.1)
            except Exception as e:
                log_message(f"An error occurred: {e}")
                time.sleep(5)
        else:
            time.sleep(0.1)

def another_buy_attempt():
    global isActive
    keepBuying = True

    while keepBuying and isActive:
        log_message("Trying to keep buying")
        time.sleep(float(refresh_rate.get()))
        # if not is_bank_in_treshold(bank_treshold.get()):
        #     pyautogui.press("esc")
        #     log_message("Money is below the treshold, deactivating...")
        #     isActive = False
        #     update_mode_label()
        #     return
        if not is_notification_shown():
            pyautogui.press("esc")
        if check_top_item_price(int(min_price_entry.get()), int(max_price_entry.get())):
            buy_top_item_max()
        else:
            keepBuying = False
            log_message("Ending the Keep Buying loop")
            return

def wait_for_numpad_enter():
    keyboard.add_hotkey('end', toggle_mode)  # Toggle mode when enter is pressed
    # Start the main loop in a separate thread
    threading.Thread(target=_main_loop, daemon=True).start()

# Create the main window
root = tk.Tk()
root.configure(bg='black')
root.title("Tarkov Flea Sniper")

custom_font = font.Font(family="Bender", size=14)
custom_font_bold = font.Font(family="Bender", size=14, weight='bold')

tk.Label(root, 
         bg = 'black',
         fg = '#C5C3B2',
         text="Minimum Price:",
         font=custom_font,
         justify = 'right').grid(row=0, column=0, padx=10, pady=10,sticky='e')
min_price_entry = tk.Entry(root,
                           bg = 'black',
                           fg = '#EEECD6',
                           highlightbackground = '#4B4F50',
                           highlightcolor = '#4B4F50',
                           highlightthickness = 1,
                           insertbackground = '#EEECD6',
                           insertwidth = 1,
                           relief = 'flat',
                           font=custom_font,
                           selectbackground='#7E9BC0')
min_price_entry.insert(0, 0)
min_price_entry.grid(row=0, column=1, padx=10, pady=10,sticky='w')

tk.Label(root, 
         bg = 'black',
         fg = '#C5C3B2',
         text="Maximum Price:",
         font=custom_font,
         justify = 'right').grid(row=1, column=0, padx=10, pady=10,sticky='e')
max_price_entry = tk.Entry(root,
                           bg = 'black',
                           fg = '#EEECD6',
                           highlightbackground = '#4B4F50',
                           highlightcolor = '#4B4F50',
                           highlightthickness = 1,
                           insertbackground = '#EEECD6',
                           insertwidth = 1,
                           relief = 'flat',
                           font=custom_font,
                           selectbackground='#7E9BC0')
max_price_entry.insert(0, 30000)
max_price_entry.grid(row=1, column=1, padx=10, pady=10,sticky='w')

tk.Label(root, 
         bg = 'black',
         fg = '#C5C3B2',
         text="Refresh Time:",
         font=custom_font,
         justify = 'right').grid(row=2, column=0, padx=10, pady=10,sticky='e')
refresh_rate = tk.Entry(root,
                        bg = 'black',
                        fg = '#EEECD6',
                        highlightbackground = '#4B4F50',
                        highlightcolor = '#4B4F50',
                        highlightthickness = 1,
                        insertbackground = '#EEECD6',
                        insertwidth = 1,
                        relief = 'flat',
                        font=custom_font,
                        selectbackground='#7E9BC0')
refresh_rate.insert(0, str(0.6))
refresh_rate.grid(row=2, column=1, padx=10, pady=10,sticky='w')

# Create the Text widget for terminal output
text_output = tk.Text(root,
                      bg='black',
                      fg='#C5C3B2',
                      font=custom_font,
                      height=10,
                      width=80,
                      wrap='word',
                      state='normal')
text_output.grid(row=9, column=0, columnspan=2, padx=10, pady=10)

# Mode label
mode_label = tk.Label(root, 
                      bg = 'black',
                      text="Mode: INACTIVE", 
                      fg="red",
                      font=custom_font_bold,
                      justify = 'left')
mode_label.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

# Mode label
help_label = tk.Label(root, 
                      bg = 'black',
                      text="Press (END) to toggle", 
                      fg="#C5C3B2",
                      font=custom_font_bold,
                      justify = 'left')
help_label.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

# Start the mode toggle listener and main loop
wait_for_numpad_enter()

# Start Tkinter main loop
root.mainloop()
