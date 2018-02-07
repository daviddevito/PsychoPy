#Match image size on screen with image size used for go/no-go

from psychopy import visual, core, data, event, logging, sound, gui, misc, monitors
import numpy as np  # whole numpy lib is available, prepend 'np.'
import os  # handy system and path functions
from psychopy.constants import *  # things like STARTED, FINISHED
import random
import math
#import win32api
import Image
import ctypes
import time

random.seed() #initialize random number generator

#global variables
SIZE = 4


# Get subject number
expName = 'Mug_EndowmentEffect_MAR2015'
fileName = ''
while True:
    expInfo = {'subjNum':''}
    dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
    if dlg.OK == False: core.quit()  # user pressed cancel so exit experiment
    if expInfo['subjNum'].isdigit(): #make sure subject number is a number
        fileName = expName + '_' + expInfo['subjNum'] + '.txt'
        if int(expInfo['subjNum']) == 999: break #always accept in testing
        if not os.path.isfile(fileName): break #check if data file already exists
        else: #if data file already exists, ask experimenter if should overwrite
#            if ctypes.windll.user32.MessageBoxA(0,'File already exists. Press OK to overwrite.','File already exists',1) == 1:
#                if ctypes.windll.user32.MessageBoxA(0,'Not that I don\'t trust you, but are you sure you want to overwrite? \n\nPress OK to overwrite.','File already exists',1) == 1:
#                    break
            break
    else:
        #ctypes.windll.user32.MessageBoxA(0,'Please specify a number','Invalid participant number',0)      
        break
outputFile = open(fileName, 'w')

subjectNumber = expInfo['subjNum']


#Column headers for output file
outStr = "Time\tValueDisplayed\tButtonPressed(z=yes,m=no)\tResponseTime\t"
outputFile.write(outStr + "eol\n")

# Setup the Psycho variables (screen, stimuli, sounds, ect)
win = visual.Window(fullscr=True, screen=0, allowGUI=False, allowStencil=False, monitor='FenskeLabTestingComps', color=[0,0,0], colorSpace='rgb', units='deg')
mon = monitors.Monitor('FenskeLabTestingComps')
trialClock = core.Clock()
eventClock = core.Clock()
evalClock = core.Clock()
keyResp = event.BuilderKeyResponse()  # create an object of type KeyResponse

#Base trial value, will change when task starts
trialValue = 10.00

instructionsOne = visual.ImageStim(win=win,image = 'Slide16.jpg', pos=[0,0], size=(20,15))
instructionsOne.setAutoDraw(True)
win.flip()
event.waitKeys()
instructionsOne.setAutoDraw(False)

instructionsTwo = visual.ImageStim(win=win,image = 'Slide17.jpg', pos=[0,0], size=(20,15))
instructionsTwo.setAutoDraw(True)
win.flip()
event.waitKeys()
instructionsTwo.setAutoDraw(False)
win.flip()

valueArray = [0.50,1.00,1.50,2.00,2.50,3.00,3.50,4.00,4.50,5.00,5.50,6.00,6.50,7.00,7.50,8.00,8.50,9.00,9.50,10.00]
random.shuffle(valueArray)

questionText = visual.TextStim(win=win, ori=0, name='questionText', text='Would you be willing to give back your mug for this amount?',    font=u'Arial', pos=[0, 3], height=1, wrapWidth=None, color='black', colorSpace=u'rgb', opacity=1, depth=-1.0)
yesNoText = visual.TextStim(win=win, ori=0, name='yesNoText', text='Yes    or    No',    font=u'Arial', pos=[0, -3], height=1, wrapWidth=None, color='black', colorSpace=u'rgb', opacity=1, depth=-1.0)



for valueTrial in range (0,20):
    
    runTime = time.strftime("%c")

    #Creating MugImage and ValueText
    displayedValue3 = ("%.2f" % valueArray[valueTrial])
    displayedValue = '$' + str(displayedValue3)
    valueText = visual.TextStim(win=win, ori=0, name='valueText', text=displayedValue,    font=u'Arial', pos=[0, 0], height=1, wrapWidth=None, color='black', colorSpace=u'rgb', opacity=1, depth=-1.0)


    #Presenting MugImage and ValueText on the screen
    valueText.setAutoDraw(True)
    questionText.setAutoDraw(True)
    yesNoText.setAutoDraw(True)
    win.flip()
    eventClock.reset()
    stimOnScreen = True
    keyResp.status = NOT_STARTED
    errorCode = -1
    errorName = ''
    noResponseYet = True
    keyResp.keys = [] #just the last key pressed
    keyResp.rt = -1
    while noResponseYet: 
        t = eventClock.getTime()
        #initialize key checker
        if keyResp.status == NOT_STARTED:
            keyResp.tStart = t
            keyResp.status = STARTED
            keyResp.clock.reset()
            #event.getKeys()
            event.clearEvents()
            
        #check for a keyboard response, down=money, up=mug
        theseKeys = event.getKeys(keyList=['z','m'])
        if len(theseKeys) > 0: #test if atleast one key pressed
            keyResp.keys = theseKeys[-1] #just the last key pressed
            keyResp.rt = keyResp.clock.getTime()
            noResponseYet = False

        # check for quit (the [Esc] key)
        if event.getKeys(["escape"]):
            core.quit()

    valueText.setAutoDraw(False)
#    questionText.setAutoDraw(False)
#    yesNoText.setAutoDraw(False)
    win.flip()
    core.wait(0.5)
    

    outStr = str(runTime)+ '\t'
    outStr = outStr + str(displayedValue)+ '\t'
    outStr = outStr + str(keyResp.keys) + '\t'
    keyRT = ("%.2f" % keyResp.rt)
    outStr = outStr + str(keyRT) + '\t'
    outputFile.write(outStr + 'eol\n')


questionText.setAutoDraw(False)
yesNoText.setAutoDraw(False)
instructionsThree = visual.ImageStim(win=win,image = 'Slide18.jpg', pos=[0,0], size=(20,15))
instructionsThree.setAutoDraw(True)
win.flip()
event.waitKeys()
core.quit()

