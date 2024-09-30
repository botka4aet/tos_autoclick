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

def search_location():
    location = pyautogui.locateOnScreen('img/event_map.png', grayscale=False)   
    if location != None:
        return 2,0
    location = pyautogui.locateOnScreen('img/main_arena.png', grayscale=False)   
    if location != None:
        return -1,0
    location = pyautogui.locateOnScreen('img/story_map.png', grayscale=False)   
    if location != None:
        return 22,0
    location = pyautogui.locateOnScreen('img/arena_fight.png', grayscale=False)   
    if location != None:
        return 12,0
    location = pyautogui.locateOnScreen('img/win_button.png', confidence=0.9)    
    if location != None:
        pyautogui.click(location)
    location = pyautogui.locateOnScreen('img/event_close.png', confidence=0.9)    
    if location != None:
        pyautogui.click(location)
    location = pyautogui.locateOnScreen('img/event_reward.png', confidence=0.9)    
    if location != None:
        pyautogui.click(location)
    location = pyautogui.locateOnScreen('img/arena_close.png', confidence=0.9)    
    if location != None:
        pyautogui.click(location)
    location = pyautogui.locateOnScreen('img/sale_banner.png', confidence=0.9)    
    if location != None:
        pyautogui.click(location)
    return -2,20

def eloop():
    global current_state,loop,clicks,target_state,time_crusade_pause,time_crusade_resume

    if not loop:
        return
    
    location = pyautogui.locateOnScreen('img/win_button.png', confidence=0.9)    
    if location != None:
        pyautogui.click(location)
        current_state += 1
        sleep(5)

    if current_state == -2 or clicks > 15:
        current_state,clicks = search_location()

    if time_crusade_pause <= datetime.datetime.now().time() <= time_crusade_resume and current_state % 10 == 2:
        sleep(5*60)
        location = pyautogui.locateOnScreen('img/event_close.png', grayscale=False)
        if location != None:
            pyautogui.click(location)
        location = pyautogui.locateOnScreen('img/arena_close.png', grayscale=False)
        if location != None:
            pyautogui.click(location)
        sleep(5)
        location = pyautogui.locateOnScreen('img/event_close.png', grayscale=False)
        if location != None:
            pyautogui.click(location)
        location = pyautogui.locateOnScreen('img/arena_close.png', grayscale=False)
        if location != None:
            pyautogui.click(location)
        current_state = -2

### Выбор карты
    if current_state == -1:
        current_state = -2
        if target_state == 0:
            location = pyautogui.locateOnScreen('img/main_event.png', grayscale=False)   
            if location != None:
                pyautogui.click(location)
        elif target_state == 1:
            location = pyautogui.locateOnScreen('img/main_arena.png', grayscale=False)   
            if location != None:
                pyautogui.click(location)
        elif target_state == 2:
            location = pyautogui.locateOnScreen('img/main_story.png', grayscale=False)   
            if location != None:
                pyautogui.click(location)
        elif target_state == 3:
            location = pyautogui.locateOnScreen('img/main_crusade.png', grayscale=False)   
            if location != None:
                pyautogui.click(location)
### Битва                
    elif current_state % 10 == 0:
        location = pyautogui.locateOnScreen('img/fight_skip.png', grayscale=False)   
        if location != None:
            pyautogui.click(location)
            current_state += 1
            clicks = -1
### Меню эвента               
    elif current_state == 2:
        location = pyautogui.locateOnScreen('img/event_fight.png', confidence=0.9)    
        if location != None:
            pyautogui.click(location)
            current_state = 0
            clicks = -1
        else:
            if clicks < 15:
                location = pyautogui.locateOnScreen('img/move_left.png', confidence=0.9)
                if location != None:
                    pyautogui.click(location)
            else:
                target_state = 1
                location = pyautogui.locateOnScreen('img/event_close.png', grayscale=False)
                if location != None:
                    pyautogui.click(location)
                    current_state = -2
                    clicks = -1
### Меню арены               
    elif current_state == 12:
        location = pyautogui.locateOnScreen('img/arena_open.png', confidence=0.9)    
        if location != None:
            pyautogui.click(location)
            current_state -= 1
        else:
            current_state = 13 
    elif current_state == 13:
        location = pyautogui.locateOnScreen('img/arena_empty.png', confidence=0.9)    
        if location == None:
            target_state = 0
            location = pyautogui.locateOnScreen('img/arena_close.png', confidence=0.9)    
            if location != None:
                current_state = -2
                pyautogui.click(location)
        else:
            location = pyautogui.locateOnScreen('img/arena_fight.png', confidence=0.9)    
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

