from tkinter import *
from tkinter import ttk
import time
from pyautogui import * 
import pyautogui 
import pyscreeze

from pynput.keyboard import Key, Listener

pyscreeze.USE_IMAGE_NOT_FOUND_EXCEPTION = False
 

# 1 event page
# 2 event fight
# 3 event moving left
# 4 event moving right
current_state = 1


clicks = 0
loop = False
after_id = ''
 
def event_page():
    global current_state,loop,clicks
    if not loop:
        return
    location = pyautogui.locateOnScreen('event_fight.png', confidence=0.9)
    if location != None:
        pyautogui.click(location)
        current_state = 2
        clicks = 0
        after_id = root.after(1000,start_fight)    
    else:
        if current_state == 4:
            event_right()
        else:
            event_left()

def start_fight():
    global loop
    if not loop:
        return
    location = pyautogui.locateOnScreen('fight_skip.png', grayscale=False)   
    if location != None:
        pyautogui.click(location)
        after_id = root.after(10000,check_win)    
    else:
        after_id = root.after(1000,start_fight)    

def check_win():
    global clicks
    global loop
    if not loop:
        return
    location = pyautogui.locateOnScreen('win_button.png', confidence=0.9)   
    if location != None:
        pyautogui.click(location)
        if current_state == 2:
           clicks = 0
           after_id = root.after(10000,event_page)
    else:
        clicks += 1
        if clicks >= 5:
           after_id = root.after(10000,event_page)
        else:    
            after_id = root.after(1000,check_win)    


def event_left():
    global clicks,current_state
    global loop
    if not loop:
        return
    location = pyautogui.locateOnScreen('move_left.png', confidence=0.9)
    if location != None:
        pyautogui.click(location)
        clicks += 1
        label["text"] = clicks
        if clicks >= 13:
            current_state = 4
    after_id = root.after(1000,event_page)

def event_right():
    global clicks,current_state
    global loop
    if not loop:
        return
    location = pyautogui.locateOnScreen('move_right.png', confidence=0.9)
    if location != None:
        pyautogui.click(location)
        clicks -= 1
        label["text"] = clicks
        if clicks <= 0:
            current_state = 3
    after_id = root.after(1000,event_page)

def check_keys(key):
    global loop
    if not loop:
        return
    if key == Key.esc:
        click_button()

listener = Listener(on_press = check_keys)   
listener.start()


def click_button():
    global loop
    loop = not loop
    if loop:
        btn["text"] = f"Stop"
        event_page()
    else:
        btn["text"] = f"Start"

root = Tk()
root.title("title")
root.geometry("300x250+600+500")    # устанавливаем размеры окна
label = Label(text="0")
label.pack()
btn = ttk.Button(text="Start", command=click_button)
btn.pack()

root.mainloop()