# basicAnimation.py (for CMU 15-112)
# version 0.3

# @TODO:
# immediate rather than deferred errors, say: create_line(range(100))

# Change log:
# 0.3: better error message on canvas.fn error

################################################
#
# See basicAnimationDemo.py for user documentation
#
# The code in this file is not intended for 112 students to
# even look at, let alone understand!
#
# For those who care, this code coerces Tkinter to let
# us use it from an external thread.  Then, we pretend
# this didn't happen, so that a programmer can use
# Tkinter graphics along with mouse, keyboard, and
# timer-based interactivity in what feels like a traditional,
# single-threaded, non-event-based, non-object-based way.
#
# We do this to get some simple interactive graphics into
# the early part of the course.  We absolutely double back
# later and do interactive graphics the "right" way,
# event-based and object-oriented.  And then, for the highly
# motivated, we may even explore all the yuck that went
# into this file to make their "simple" projects work at all.  :-)
#
# Bottom line: really nobody should ever use this code for
# anything beyond some really simple examples early on in a
# first programming course.
################################################

from Tkinter import *
from Queue import Queue
from threading import Thread
import sys, os, signal

class BasicAnimationRunner(object):
    class WrappedCanvas(object):
        def __init__(self, drawingQueue):
            self.drawingQueue = drawingQueue
            self.attrMap = { }
        def __getattr__(self, name):
            fn = self.attrMap.get(name)
            if (fn == None):
                fn = lambda *args, **kwargs: self.drawingQueue.put((name, args, kwargs))
                self.attrMap[name] = fn
            return fn

    def __init__(self, appFn, width=300, height=300):
        self.width = width
        self.height = height
        self.drawingQueue = Queue()
        self.eventQueue = Queue()
        self.eventQueue.put(("appLaunched", None))
        self._isRunning = True
        self.root = Tk()
        self.timerDelay = None # no timer by default
        def onDeleteWindow():
            if (self._isRunning):
                self.eventQueue.put(("windowClosed", None))
            self._isRunning = False
            self.root.destroy()
            #sys.exit(0)
            self.thread.join()
        self.root.protocol("WM_DELETE_WINDOW", onDeleteWindow)
        def onButtonPressed(event):
            if (not self._isRunning): return
            self.eventQueue.put(("mousePressed", event))
        self.root.bind("<Button-1>", onButtonPressed)
        def onKeyPressed(event):
            if (not self._isRunning): return
            self.eventQueue.put(("keyPressed", event))
        self.root.bind("<Key>", onKeyPressed)
        self.wrappedCanvas = self.WrappedCanvas(self.drawingQueue)
        self.canvas = Canvas(self.root, width=width, height=height)
        self.canvas.pack()
        self.canvas.after(100, lambda: self.drawingQueueTimerFired())
        # get the app runner going in a new thread
        self.thread = Thread(target=lambda : appFn(self, self.wrappedCanvas))
        self.thread.daemon = False
        self.thread.start()
        # and then run the mainloop in this thread
        self.root.mainloop()

    def drawingQueueTimerFired(self):
        # clear drawing queue
        while (not self.drawingQueue.empty()):
            (fnName, args, kwargs) = self.drawingQueue.get()
            if (not self._isRunning): return
            try:
                fn = getattr(self.canvas, fnName)
                fn(*args, **kwargs)
            except Exception as e:
                print "Error %s in canvas.%s" % (str(e), fn.__name__)
                #raise e
        if (not self._isRunning): return
        self.canvas.update()
        self.canvas.after(100, lambda: self.drawingQueueTimerFired())

    def setTimerDelay(self, timerDelay): self.timerDelay = timerDelay
    def isRunning(self): return self._isRunning

    def getEvent(self, timeout=None):
        if (not self._isRunning): return ("timerFired", None)
        #self.clearDrawingQueue()
        if (timeout == None): timeout = self.timerDelay
        try:
            if ((timeout == None) or (timeout < 0)):
                return self.eventQueue.get()
            else:
                return self.eventQueue.get(True, timeout/1000.0)
        except:
            return ("timerFired", None)

# BasicAnimationRunner(myBasicAnimation, width=300, height=300)