from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import os
import threading
from flask import * 



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

threading.Thread(target=startServer).start()
threading.Thread(target=startClient).start()