from Tkinter import *
from basicAnimation import BasicAnimationRunner
def myBasicAnim(app, canvas):
    (x,y,r) = (app.width/2, app.height/2, 25)
    while app.isRunning():
        (eventType, event) = app.getEvent()
        if (eventType == "mousePressed"):
            (x,y) = (event.x, event.y)
        elif (eventType == "keyPressed"):
            if (event.keysym == "Up"): y -= 10
            elif (event.keysym == "Down"): y += 10
            elif (event.keysym == "Left"): x -= 10
            elif (event.keysym == "Right"): x += 10
        canvas.delete(ALL)
        canvas.create_rectangle(x-r, y-r, x+r, y+r, fill="green")
        canvas.create_text(app.width/2, app.height/2,
                           text="Click mouse or press Arrow keys.")
    print "Done!"
BasicAnimationRunner(myBasicAnim, width=300, height=300)
