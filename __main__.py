from tkinter import *
from tkinter import ttk
import time
 
clicks = 0
loop = False
after_id = ''
 
def tick():
    global clicks,loop,after_id
    if not loop:
        return
    after_id = root.after(1000,tick)
    clicks += 1
    label["text"] = clicks

def click_button():
    global loop
    loop = not loop
    if loop:
        btn["text"] = f"Stop"
        tick()
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