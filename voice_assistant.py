import speech_recognition as sr
import os
import sys
import pyttsx3
import pyaudio

#import multiprocessing
import time
from playsound import playsound

from PyQt5.QtCore import QTimer

class VoiceAssistant:
    def __init__(self):
        self.eng = pyttsx3.init() #initialize an instance
        self.voice = self.eng.getProperty('voices') #get the available voices
        self.eng.setProperty('voice', self.voice[33].id) #0 basic male #7 reddit male #10 female #17 aussie
        # 26 female (good) 33 female (siri) 
        self.defaultResponse = ['goodnight', 'good morning', 'yes']

        self.eng.say("Welcome to Sleep Apnea Guardian. My name is Apnea!")
        self.eng.runAndWait()
        
        self.usrname = self.username()
        self.eng.say("It's time for bed "+self.usrname)
        self.eng.runAndWait()
        query = ''
        while self.defaultResponse[0] not in query:
            query = self.takeCommand().lower()
        if 'goodnight' in query:
            self.eng.say("Sweet Dreams.")
            self.eng.runAndWait()
            self.eng.say("Sleep monitoring activated")
            self.eng.runAndWait()



    def takeCommand(self):
        
        r = sr.Recognizer()
        r.energy_threshold = 3000

        with sr.Microphone() as source:
            print("Listening...")
            playsound('beep.m4a')
            r.pause_threshold = 1
            audio = r.listen(source)
    
        try:
            print("Recognizing...")   
            query = r.recognize_google(audio, language ='en-in')
            print(f"{query}\n")
    
        except Exception as e:
            print(e)   
            print("Unable to Recognize your voice.") 
            return ''
        return query

    def username(self):
        self.eng.say("What's your name?")

        usrname = self.takeCommand()
        return usrname

    
    
    def listen_for_morning(self):
        query = ''
        while self.defaultResponse[1] not in query:
            query = self.takeCommand().lower()
        if 'good morning' in query:
            self.eng.say("Good Morning "+self.usrname + "!")
            self.eng.runAndWait()


        self.eng.say("I made a graph of your sleep last night, would you like to see it?")
        self.eng.runAndWait()
        query = self.takeCommand().lower()
        if 'yes' in query:
            self.eng.say('Here you go!')
            self.eng.runAndWait()

        return True

    def username(self):
        self.eng.say("What's your name?")
        self.eng.runAndWait()
        usrname = self.takeCommand()
        return usrname

if __name__ == "__main__":
    for i in range(48):
        print(i)
        eng = pyttsx3.init()
        voice = eng.getProperty('voices') #get the available voices
        eng.setProperty('voice', voice[i].id) #0 basic male #7 reddit male #10 female #17 aussie 
        eng.say("Welcome to Sleep Apnea Detector. My name is Apnea!")
        eng.runAndWait()
