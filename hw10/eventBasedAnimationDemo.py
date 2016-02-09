# eventBasedAnimationDemo.py

from Tkinter import *
from eventBasedAnimationClass import EventBasedAnimationClass

class EventBasedAnimationDemo(EventBasedAnimationClass):
    def onMousePressed(self, event):
        self.mouseText = "last mousePressed: " + str((event.x, event.y))

    def onKeyPressed(self, event):
        self.keyText = "last keyPressed: char=" + event.char + ", keysym=" + event.keysym

    def onTimerFired(self):
        self.timerCounter += 1
        self.timerText = "timerCounter = " + str(self.timerCounter)

    def redrawAll(self):
        self.canvas.delete(ALL)
        # draw the text
        self.canvas.create_text(150,20,text="events-example1.py")
        self.canvas.create_text(150,40,text=self.mouseText)
        self.canvas.create_text(150,60,text=self.keyText)
        self.canvas.create_text(150,80,text=self.timerText)

    def initAnimation(self):
        self.mouseText = "No mousePresses yet"
        self.keyText = "No keyPresses yet"
        self.timerText = "No timerFired calls yet"
        self.timerCounter = 0

EventBasedAnimationDemo(300,300).run()
