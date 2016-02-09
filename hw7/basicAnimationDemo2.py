# basicAnimationDemo2.py
# version 0.5

# Barebones timer, mouse, and keyboard events
# without (much) event-based programming or (much) object-oriented programming

# To run this, you need to download basicAnimation.py
# and save that file in the same folder as this one.

from Tkinter import *
from basicAnimation import BasicAnimationRunner

def onMousePressed(canvas, event):
    (canvas.data.x, canvas.data.y) = (event.x, event.y)

def onKeyPressed(canvas, event):
    if (event.keysym == "Up"): canvas.data.y -= 5
    elif (event.keysym == "Down"): canvas.data.y += 5

def onTimerFired(canvas):
    canvas.data.x = (canvas.data.x + 10) % (canvas.app.width)

def init(canvas):
    canvas.app.setTimerDelay(100)
    canvas.data.x = 50
    canvas.data.y = 50
    canvas.data.r = 25

def redrawAll(canvas):
    (x, y, r) = (canvas.data.x, canvas.data.y, canvas.data.r)
    canvas.delete(ALL)
    canvas.create_oval(x-r, y-r, x+r, y+r, fill="green")
    canvas.create_text(canvas.app.width/2, 20, text="Click to move circle")
    canvas.create_text(canvas.app.width/2, 40, text="Up/Down arrows also work")

def myBasicAnimation(app, canvas, extraArg):
    print "Running animation, extraArg =", extraArg
    init(canvas)
    while app.isRunning():
        (eventType, event) = app.getEvent()
        if (eventType == "mousePressed"): onMousePressed(canvas, event)
        elif (eventType == "keyPressed"): onKeyPressed(canvas, event)
        elif (eventType == "timerFired"): onTimerFired(canvas)
        redrawAll(canvas)
    print "Done!"

BasicAnimationRunner(myBasicAnimation, width=300, height=300, extraArg="wow!")
