# basicAnimationDemo1.py
# version 0.2

# Barebones mouse and keyboard events (no timer events until next week...)
# without (much) event-based programming or (much) object-oriented programming

# To run this, first save basicAnimation.py in the same folder as this file.

from Tkinter import *
from basicAnimation import BasicAnimationRunner

def myBasicAnimation(app, canvas):
    (x,y,r) = (app.width/2, app.height/2, 25)
    while app.isRunning():
        (eventType, event) = app.getEvent()
        if (eventType == "mousePressed"):
            (x,y) = (event.x, event.y)
        canvas.delete(ALL)
        canvas.create_text(app.width/2, app.height/2,
                           text="Click mouse or press Arrow keys.")
    print "Done!"

BasicAnimationRunner(myBasicAnimation, width=300, height=300)