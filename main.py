from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import os
import threading
from flask import * 
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk


channelName = input("Channel name: ")


def startServer():
    os.system("python server.py")
    


def startClient():
    options = Options()
    options.headless = True
    options.add_argument("--mute-audio")
    options.add_experimental_option("detach", True)
    browser = webdriver.Chrome(executable_path='chromedriver.exe', options=options)
    browser.get('http://127.0.0.1:5000/')

    browser.find_element(By.ID, "click").click()


    browser.execute_script('createChannel("'+ channelName + '");')

    window = Tk()
    window.title("PowerUI Broadcast Studio: " + channelName)
    window.configure(background="black")
    window.state("zoomed")
    window.lift()
    window.attributes('-topmost',True)
    window.after_idle(window.attributes,'-topmost',False)

    curLabel = Label(window, text = "Currently broadcasting to: " + channelName, font=('Segoe UI Semibold', '18'), fg="white", anchor="w")
    curLabel.configure(background="black")

    streamPreview = Label(window)

    def updatePreview(): 
        browser.find_element(By.ID, "broadcast").screenshot("preview.png")
        rawPreview = PhotoImage(file= "preview.png")
        preview = rawPreview.subsample(2, 2)
        streamPreview.configure(image=preview, background="black")
        streamPreview.image = preview
        window.after(1, lambda: updatePreview())


    curLabel.pack(side = TOP, padx = 10, pady = 10, fill="both")
    streamPreview.pack(side = TOP, padx = 20, pady = 20, fill="both")
    updatePreview()
    window.mainloop()

threading.Thread(target=startServer).start()
threading.Thread(target=startClient).start()