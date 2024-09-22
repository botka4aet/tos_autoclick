from tkinter import *
from tkinter import ttk
from pyautogui import * 
import pyautogui 
import pyscreeze

from pynput.keyboard import Key, Listener
import datetime

pyscreeze.USE_IMAGE_NOT_FOUND_EXCEPTION = False
 
#-3 - закрыть крусейд
#-2 - не определено
#-1 - главное меню
# 0 - битва эвент
# 1 - битва эвент, ожидание победы
# 2 - карта эвента 
# 10 - битва арена
# 11 - битва арена, ожидание победы
# 12 - меню арены, поиск сундуков
# 13 - меню арены, поиск битвы
# 20 - битва сюжет
# 21 - битва сюжет, ожидание победы
# 22 - карта сюжета 
# 30 - битва покорение
# 31 - битва покорение, ожидание победы
# 32 - карта покорения 
current_state = -2
target_state = 0

time_crusade_pause = datetime.time(2, 55, 0, 0)
time_crusade_resume = datetime.time(3, 0, 0, 0)

clicks = 0
loop = False
after_id = ''

def search_location():
    location = pyautogui.locateOnScreen('event_map.png', grayscale=False)   
    if location != None:
        return 2
    location = pyautogui.locateOnScreen('main_arena.png', grayscale=False)   
    if location != None:
        return -1
    location = pyautogui.locateOnScreen('story_map.png', grayscale=False)   
    if location != None:
        return 22
    location = pyautogui.locateOnScreen('arena_fight.png', grayscale=False)   
    if location != None:
        return 12
    location = pyautogui.locateOnScreen('win_button.png', confidence=0.9)    
    if location != None:
        pyautogui.click(location)
    return -2

def eloop():
    global current_state,loop,clicks,target_state,time_crusade_pause,time_crusade_resume
    if time_crusade_pause <= datetime.datetime.now().time() <= time_crusade_resume:
        sleep(5*60)
        location = pyautogui.locateOnScreen('event_close.png', grayscale=False)
        if location != None:
            pyautogui.click(location)
            current_state = -2
    if not loop:
        return
    
    location = pyautogui.locateOnScreen('win_button.png', confidence=0.9)    
    if location != None:
        pyautogui.click(location)
        current_state += 1
        sleep(5)

    while current_state == -2:
        current_state = search_location()

### Выбор карты
    if current_state == -1:
        current_state = -2
        if target_state == 0:
            location = pyautogui.locateOnScreen('main_event.png', grayscale=False)   
            if location != None:
                pyautogui.click(location)
        elif target_state == 1:
            location = pyautogui.locateOnScreen('main_arena.png', grayscale=False)   
            if location != None:
                pyautogui.click(location)
        elif target_state == 2:
            location = pyautogui.locateOnScreen('main_story.png', grayscale=False)   
            if location != None:
                pyautogui.click(location)
        elif target_state == 3:
            location = pyautogui.locateOnScreen('main_crusade.png', grayscale=False)   
            if location != None:
                pyautogui.click(location)
### Битва                
    elif current_state % 10 == 0:
        location = pyautogui.locateOnScreen('fight_skip.png', grayscale=False)   
        if location != None:
            pyautogui.click(location)
            current_state += 1
            clicks = 0
### Меню эвента               
    elif current_state == 2:
        location = pyautogui.locateOnScreen('event_fight.png', confidence=0.9)    
        if location != None:
            pyautogui.click(location)
            current_state = 0
            clicks = 0
        else:
            clicks += 1
            if 0 <= clicks < 15:
                location = pyautogui.locateOnScreen('move_left.png', confidence=0.9)
                if location != None:
                    pyautogui.click(location)
            elif clicks == 15:
                target_state = 1
                location = pyautogui.locateOnScreen('event_close.png', grayscale=False)
                if location != None:
                    pyautogui.click(location)
                    current_state = -2
                    clicks = 0
            label["text"] = clicks
### Меню арены               
    elif current_state == 12:
        location = pyautogui.locateOnScreen('arena_open.png', confidence=0.9)    
        if location != None:
            pyautogui.click(location)
            current_state -= 1
        else:
            current_state = 13 
    elif current_state == 13:
        location = pyautogui.locateOnScreen('arena_empty.png', confidence=0.9)    
        if location == None:
            target_state = 0
            location = pyautogui.locateOnScreen('arena_close.png', confidence=0.9)    
            if location != None:
                current_state = -2
                pyautogui.click(location)
        else:
            location = pyautogui.locateOnScreen('arena_fight.png', confidence=0.9)    
            if location != None:
                current_state -= 3
                pyautogui.click(location)
    elif current_state % 10 == 1:
        clicks += 1
        sleep(1)
        if clicks > 10:
            current_state += 1
            clicks = 0    
    label["text"] = f"Clicks {clicks}"
    labelstate["text"] = f"State {current_state}"

    after_id = root.after(1500,eloop)        

 
def event_page():
    global current_state,loop,clicks
    if not loop:
        return
    location = pyautogui.locateOnScreen('event_fight.png', confidence=0.9)
    if location != None:
        pyautogui.click(location)
        current_state = 2
        labelstate["text"] = current_state
        clicks = 0
        after_id = root.after(1000,start_fight)    
    else:
#        pyautogui.moveTo(1, 1)
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
            labelstate["text"] = current_state
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
            labelstate["text"] = current_state
    after_id = root.after(1000,event_page)

def check_keys(key):
    global loop
    if not loop:
        return
    if key == Key.esc:
        click_button()

listener = Listener(on_press = check_keys)   
listener.start()



    
#     global clicks,loop,after_id
#     if not loop:
#         return
#     after_id = root.after(1000,tick)
#     clicks += 1
#     label["text"] = clicks
#     location = pyautogui.locateOnScreen('test_5.png', confidence=0.8)
#     if location != None:
# ##    if pyautogui.locateOnScreen("test_5.png", confidence=0.5) != None:
#         pyautogui.click(location)

def click_button():
    global loop,current_state
    loop = not loop
    if loop:
        btn["text"] = f"Stop"
        eloop()
    else:
        btn["text"] = f"Start"
        current_state = -2

root = Tk()
root.title("title")
root.geometry("300x250+600+500")    # устанавливаем размеры окна
label = Label(text="0")
label.pack()
labelstate = Label(text="0")
labelstate.pack()
btn = ttk.Button(text="Start", command=click_button)
btn.pack()

#with keyboard.pressed(Key.alt):
#    click_button()
    
root.mainloop()

