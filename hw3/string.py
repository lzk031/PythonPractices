import string
import math
from Tkinter import *
def move(canvas,n,angle,color,cx,cy,drawWidth):
	angle = math.radians(angle)

	#calculate the x and y in the end of this step
	newx = cx + n*math.cos(angle)
	newy = cy - n*math.sin(angle)
	if color == "none":
		pass
	else:	
	#calculate the axes of two tops for the rectangle
		r=drawWidth/2.0
		(x0,y0) = (cx+r*math.cos(1.5*math.pi+angle),(cy-r*math.sin(1.5*math.pi+angle)))
		(x1,y1) = (cx+r*math.cos(0.5*math.pi+angle),(cy-r*math.sin(0.5*math.pi+angle)))
		(x2,y2) = (newx+r*math.cos(0.5*math.pi+angle),(newy-r*math.sin(0.5*math.pi+angle)))
		(x3,y3) = (newx+r*math.cos(1.5*math.pi+angle),(newy-r*math.sin(1.5*math.pi+angle)))
		canvas.create_polygon(x0,y0,x1,y1,x2,y2,x3,y3,fill=color)
	return (newx,newy)


def turnLeft(change,angle):
	print "angle change", angle+change
	return angle + change

def turnRight(change,angle):
	print "angle change", angle-change
	return angle - change

def runSimpleTortoiseProgram(program,winWidth=500,winHeight=500):
	root = Tk()
	canvas = Canvas(root, width=winWidth, height=winHeight)
	canvas.pack()
	color = None
	angle = 0
	currentX = winWidth/2.0
	currentY = winHeight/2.0
	drawWidth = 4
	for line in program.splitlines():
		canvas.create_text(x,y)
		line = line.strip() #delete white space in the begin and the end of this line
		if line.startswith("#"):
			continue
		elif line.startswith("color"):
			color = line.split(" ")[1]
		elif line.startswith("move"):
			(currentX,currentY) = move(canvas,int(line.split(" ")[1]),angle,color,currentX,currentY,drawWidth)
		elif line.startswith("left"):
			angle = turnLeft(int(line.split(" ")[1]), angle)
		elif line.startswith("right"):
			angle = turnRight(int(line.split(" ")[1]), angle)
	root.mainloop()

runSimpleTortoiseProgram("""
# This is a simple tortoise program
color blue
move 50

left 90

color red
move 100

color none # turns off drawing
move 50

right 45

color green # drawing is on again
move 50

right 45

color orange
move 50

right 90

color purple
move 100
""", 300, 400)
