import random

import pyautogui
import os
import time
import board
import re
import win32api, win32con
from random import randrange
import cv2
import pytesseract
import math
x_pad = 1152
y_pad = 176
from PIL import ImageOps, ImageGrab
import numpy as np
mover=92
p_00=(75,705)
x_0 = 75
y_0= 715
number_of_rows=8
letters=[]

word_list = open('words.txt','r', encoding="utf8")


def play_word(word):
    pyautogui.write(word, interval=0.01)




def screen_grab():
    number=0
    while(number<number_of_rows):
        box = (x_pad + 10, y_pad + 650-number*mover, x_pad + 570, y_pad + 750-number*mover) #Y är 0
        im = ImageGrab.grab(box)
        im.save(os.getcwd() + '\\snap'+str(int(number)) +'.png', 'PNG')
        number+=1

def add_letters(vals):
    for x in vals:
        letters.append(x)

def check_letters():
    number = 0
    while (number < number_of_rows):
        img = cv2.imread('snap'+str(int(number)) +'.png')

        kernel = np.ones((3, 3), np.uint8)
        img =cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        erosion = cv2.erode(img, kernel, iterations=2)
        custom_config = r'-l eng --oem 3 --psm 7 -c tessedit_char_whitelist="ABCDEFGHIJKLMNOPQRSTUVWXYZ"'
        y=pytesseract.image_to_string(erosion, config=custom_config)
        vals= list([val for val in y if val.isalpha()])
        add_letters(vals)
        number+=1

def mouse_pos(cord):
    win32api.SetCursorPos((x_pad + cord[0], y_pad + cord[1]))


def left_click():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
    print ("Click.")


def start_game():
    #location of first menu
    mouse_pos((274, 344))
    left_click()
    time.sleep(.1)

def word_to_chars(word):
    letters_in_word={}
    for i in word:
        if i.isalpha():
            i=i.upper()
            letters_in_word[i]=letters_in_word.get(i,0)+1
    return letters_in_word

def search_word():
    listan=[]
    letters_amount = word_to_chars(letters)
    #print(letters_amount)
    word_list2 = open('words2.txt', 'r', encoding="utf8")
    for word in word_list2:
        x = True
        word_letters=word_to_chars(word)
        print(x)
        for char in word_letters:
            if char not in letters:
                x = False
            else:
                if letters_amount[char]!= word_letters[char]:
                    x=False

        if x==True:
            print(word)
            i = word.strip()
            if len(i)>=5 and i.isalpha()==True:
                return word
    if not listan:
        return False
    else:
        return random.choice((listan))



def send_word():
    print("sending word")
    pyautogui.press('enter')
    #mouse_pos((553, 802))
    #left_click()



def play_game():
    while True:
        screen_grab()
        check_letters()
        print(letters)
        word= search_word()
        print("this is word ")
        print(word)
        if word is not False:
            print(word)
            play_word(word)
            send_word()
        letters.clear()

if __name__ == "__main__":
    start_game()
    play_game()