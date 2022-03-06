import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons, TextBox
import random
import serial
import keyboard
import csv

#############################################################
##################### MATPLOTLIB GUI ########################
#############################################################
t = np.arange(0.0, 3.0, 0.001)
s = t*0
s[0]=1024


plt.ion()
fig, ax = plt.subplots()
ax.margins(x=0)
plt.subplots_adjust(left=0.1, bottom=0.25, top=0.88, right=0.9)
l, = plt.plot(t, s, lw=2)



axcolor = 'lightgoldenrodyellow'

## Connection GUI
axConnBox = plt.axes([0.1, 0.90, 0.7, 0.05], facecolor=axcolor)
wConnBox = TextBox(axConnBox, 'Port: ', initial="COM7")
running=False
arduino =0
print(arduino)
def arduinoConnect(event):
    global arduino
    arduino = serial.Serial(wConnBox.text, 9600, timeout=1)
    wConnButt.color = "green"
axConnButt = plt.axes([0.8, 0.90, 0.1, 0.05])
wConnButt = Button(axConnButt, 'Connect', color=axcolor, hovercolor='0.975')
wConnButt.on_clicked(arduinoConnect)


## Threshold GUI
threshold = 379
thresholdLine, = ax.plot([0,t[-1]], [threshold,threshold])
def threshold_update(val):
    thresholdLine.set_ydata([val,val])
    global threshold
    threshold=val
    fig.canvas.flush_events()
axThreshold = plt.axes([0.95, 0.25, 0.03, 0.88-0.25], facecolor=axcolor)
wThreshold = Slider(axThreshold, 'Trig', 0, 1024, valinit=threshold, valstep=1, orientation= 'vertical')
wThreshold.on_changed(threshold_update)

## Saving GUI
axSaveBox = plt.axes([0.52, 0.075, 0.36, 0.05], facecolor=axcolor)
wSaveBox = TextBox(axSaveBox, 'Path: ', initial="file01.csv")
axSaveButt = plt.axes([0.88, 0.075, 0.1, 0.05])
wSaveButton = Button(axSaveButt, 'Save', color=axcolor, hovercolor='0.975')
record = []
def saveFunction(event):
    global record
    print("hey")
    with open(wSaveBox.text, 'w') as f:
        for r in record:
            f.write(str(int(r[0]))+","+str(r[1])+"\n")
        print("hey")

wSaveButton.on_clicked(saveFunction)

## Input char GUI 
axOutCharBox = plt.axes([0.1, 0.1, 0, 0.], facecolor=axcolor)
wOutCharBox = TextBox(axOutCharBox, 'Output\nKey:  ')
outputChar=("a", "b", "c")
axOutCharRadio = plt.axes([0.12, 0.03, 0.1, 0.15], facecolor=axcolor)
wOutCharRadio = RadioButtons(axOutCharRadio, outputChar, active=0)
selectedOutputChar = outputChar[0]
def inputfuction(label):
    global selectedOutputChar
    selectedOutputChar = label
wOutCharRadio.on_clicked(inputfuction)

## Stiffness GUI 
axStiffBox = plt.axes([0.35, 0.1, 0, 0.], facecolor=axcolor)
wStiffBox = TextBox(axStiffBox, 'Stiffness:  ')
axStiffRadio = plt.axes([0.34, 0.03, 0.1, 0.15], facecolor=axcolor)
WStiffRadio = RadioButtons(axStiffRadio, ("Low", "High"), active=0)
curr_stiffness=0
def stifffuction(label):
    global curr_stiffness
    if(label=="Low"):
        arduino.write(b'#')
        curr_stiffness=0
    else:
        arduino.write(b'a')
        curr_stiffness=1
WStiffRadio.on_clicked(stifffuction)
#############################################################
#############################################################

print(arduino)


i=0
clicked = False
unclickedTick=0
while True:
    if(arduino!=0):
        safedata=False
        while(safedata==False):
            d = arduino.read(1)
            if(int.from_bytes(d,"little")==255):
                d = arduino.read(1)
                if(int.from_bytes(d,"little")==255):
                    safedata=True
        d = arduino.read(2)
        print('\rPos: ', end="")
        print(int.from_bytes(d,"little"),end="   ")
        s[i]=int.from_bytes(d,"little")
        record.append([s[i], curr_stiffness])
        if(i%50==0):
            l.set_ydata(s)
            fig.canvas.draw()
            fig.canvas.flush_events()

        if(s[i]<threshold and clicked==False and unclickedTick>10):
            print("\rclicked   ")
            keyboard.press_and_release(selectedOutputChar)
            clicked = True
            unclickedTick=0
        elif(s[i]>=threshold):
            unclickedTick = unclickedTick+1
            clicked = False
        
        i = i + 1
        if(i>=len(t)):
            i=0
    else:
        fig.canvas.draw()
        fig.canvas.flush_events()
