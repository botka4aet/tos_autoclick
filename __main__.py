from typing import List

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
# 30 - битва крусейд
# 31 - битва крусейд, ожидание победы
# 32 - карта крусейд 
current_state = -2

#-1 - главное меню
# 0 - событие
# 1 - арена
# 2 - сюжет
# 3 - крусейд
target_state = 0

time_crusade_pause = datetime.time(2, 55, 0, 0)
time_crusade_resume = datetime.time(3, 0, 0, 0)

clicks = 0
loop = False
after_id = ''

arr_img = ['event_map.png','main_arena.png','story_map.png','arena_fight.png','win_button.png','event_close.png','event_reward.png','arena_close.png','arena_close.png'] 
arr_state: List[int] = [2,-1,22,12,-2,-2,-2,-2,-2] 

# arr_img.append('event_map.png')
# arr_img.append('main_arena.png')
# arr_img.append('story_map.png')
# arr_img.append('arena_fight.png')
# arr_img.append('win_button.png')
# arr_img.append('event_close.png')
# arr_img.append('event_reward.png')
# arr_img.append('arena_close.png')
# arr_img.append('arena_close.png')


def search_location():
    for idx, img in enumerate(arr_img):
        state = arr_state[idx]
        location = pyautogui.locateOnScreen(img, grayscale=False)
        if location != None:
            if state != -2:
                return state,0
            pyautogui.click(location)
            break
    return -2,20

def search_location1():
    location = pyautogui.locateOnScreen('event_map.png', grayscale=False)   
    if location != None:
        return 2,0
    location = pyautogui.locateOnScreen('main_arena.png', grayscale=False)   
    if location != None:
        return -1,0
    location = pyautogui.locateOnScreen('story_map.png', grayscale=False)   
    if location != None:
        return 22,0
    location = pyautogui.locateOnScreen('arena_fight.png', grayscale=False)   
    if location != None:
        return 12,0
    location = pyautogui.locateOnScreen('win_button.png', confidence=0.9)    
    if location != None:
        pyautogui.click(location)
    location = pyautogui.locateOnScreen('event_close.png', confidence=0.9)    
    if location != None:
        pyautogui.click(location)
    location = pyautogui.locateOnScreen('event_reward.png', confidence=0.9)    
    if location != None:
        pyautogui.click(location)
    location = pyautogui.locateOnScreen('arena_close.png', confidence=0.9)    
    if location != None:
        pyautogui.click(location)
    location = pyautogui.locateOnScreen('sale_banner.png', confidence=0.9)    
    if location != None:
        pyautogui.click(location)
    return -2,20

def eloop():
    global current_state,loop,clicks,target_state,time_crusade_pause,time_crusade_resume
    if not loop:
        return
    location = pyautogui.locateOnScreen('win_button.png', confidence=0.9)    
    if location != None:
        pyautogui.click(location)
        current_state += 1
        sleep(5)
    if current_state == -2 or clicks > 15:
       current_state,clicks = search_location()

    if time_crusade_pause <= datetime.datetime.now().time() <= time_crusade_resume and current_state % 10 == 2:
        sleep(5*60)
        # location = pyautogui.locateOnScreen('event_close.png', grayscale=False)
        # if location != None:
        #     pyautogui.click(location)
        # location = pyautogui.locateOnScreen('arena_close.png', grayscale=False)
        # if location != None:
        #     pyautogui.click(location)
        # sleep(5)
        # location = pyautogui.locateOnScreen('event_close.png', grayscale=False)
        # if location != None:
        #     pyautogui.click(location)
        # location = pyautogui.locateOnScreen('arena_close.png', grayscale=False)
        # if location != None:
        #     pyautogui.click(location)
        # current_state = -2

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
        sleep(5)
### Битва                
    elif current_state % 10 == 0:
        location = pyautogui.locateOnScreen('fight_skip.png', grayscale=False)   
        if location != None:
            pyautogui.click(location)
            current_state += 1
            clicks = -1
### Меню эвента               
    elif current_state == 2:
        location = pyautogui.locateOnScreen('event_fight.png', confidence=0.9)    
        if location != None:
            pyautogui.click(location)
            current_state = 0
            clicks = -1
        else:
            if clicks < 14:
                location = pyautogui.locateOnScreen('move_left.png', confidence=0.9)
                if location != None:
                    pyautogui.click(location)
            else:
                target_state = 1
                location = pyautogui.locateOnScreen('event_close.png', grayscale=False)
                if location != None:
                    pyautogui.click(location)
                    current_state = -2
                    clicks = -1
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
        sleep(1)
        if clicks > 10:
            current_state += 1
            clicks = -1    
    clicks += 1
    
    label["text"] = f"Clicks {clicks}"
    labelstate["text"] = f"State {current_state}"

    after_id = root.after(1500,eloop)        

def check_keys(key):
    global loop
    if not loop:
        return
    if key == Key.esc:
        click_button()

listener = Listener(on_press = check_keys)   
listener.start()

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
root.mainloop()

