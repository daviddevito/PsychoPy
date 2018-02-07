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
import datetime
from psychopy.visual import ShapeStim

now=datetime.datetime.now()

random.seed() #initialize random number generator

#global variables
ISI = 1.0 #duration of time separating trials
TEXT_HEIGHT = 0.75
TEXT_WRAPPING = 30
LargeTextSize = 1.25
SmallTextSize = 1


FIXATION_TIME = 0.5
CUEARROW_TIME = 1.0
FACE_ON_SCREEN = .25
FACE_OFF_SCREEN = 1.6
FEEDBACK_TIME = 0.15

#creating array 
BLANKBETWEENCUEANDFACE = [0]*204 + [0.01667]*159 + [0.03334]*119 + [0.05001]*95 + [0.06668]*76 + [0.08335]*60 + [0.10002]*48 + [0.11669]*36 + [0.13336]*30 + [0.15003]*21 + [0.16667]*20 + [0.18337]*16 + [0.20004]*10 + [0.21671]*9 + [0.23338]*7 + [0.25005]*7 + [0.26672]*4 + [0.28339]*3 + [0.30006]*3 + [0.31673]*2 + [0.3334]*1 + [0.35007]*1 + [0.36674]*1 + [0.40008]*1 + [0.41675]*1 + [0.45009]*1 + [0.5001]*1
random.shuffle(BLANKBETWEENCUEANDFACE)

#Array of Positions for picture stimuli. Can either be left of fixation or right of fixation
POSARRAY = [[-10,0],[10,0]]
ARROWPOS = [0,0]
ARROWSIZE = 3
FACEWIDTH = 12
FACEHEIGHT = 8.5

SIZE = 4
NUM_REPS = 1
NUM_REPS_CATCHTRIALS = 2
NUM_STIMULI = 56


runTime = now.strftime("%Y-%m-%d %Hhr%Mmin")

# Get subject number
expName = 'Cued2Emotion_SEP2016'
fileName = ''
while True:
    expInfo = {'subjNum':''}
    dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
    if dlg.OK == False: core.quit()  # user pressed cancel so exit experiment
    if expInfo['subjNum'].isdigit(): #make sure subject number is a number
        fileName = expName + '_' + expInfo['subjNum'] + '_' + str(runTime) + '.txt'
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
while True:
    expInfo2 = {'age':''}
    dlg = gui.DlgFromDict(dictionary=expInfo2, title=expName)
    if dlg.OK == False: core.quit()  # user pressed cancel so exit experiment
    else:
        break
while True:
    expInfo3 = {'gender':''}
    dlg = gui.DlgFromDict(dictionary=expInfo3, title=expName)
    if dlg.OK == False: core.quit()  # user pressed cancel so exit experiment
    else:
        break
while True:
    expInfo4 = {'handedness':''}
    dlg = gui.DlgFromDict(dictionary=expInfo4, title=expName)
    if dlg.OK == False: core.quit()  # user pressed cancel so exit experiment
    else:
        break
while True:
    expInfo5 = {'race':''}
    dlg = gui.DlgFromDict(dictionary=expInfo5, title=expName)
    if dlg.OK == False: core.quit()  # user pressed cancel so exit experiment
    else:
        break
while True:
    expInfo6 = {'glasses/contacts?':''}
    dlg = gui.DlgFromDict(dictionary=expInfo6, title=expName)
    if dlg.OK == False: core.quit()  # user pressed cancel so exit experiment
    else:
        break
        
        
outputFile = open(fileName, 'w')

subjectNumber = expInfo['subjNum']
buttonCounterbalance = int(subjectNumber)%(4)
#0=sl(happy),dk(angry),happyCyan,AngryPurple
#1=sl(happy),dk(angry),happyPurple,AngryCyan
#2=sl(angry),dk(happy),happyCyan,AngryPurple
#3=sl(angry),dk(happy),happyPurple,AngryCyan


#Column headers for output file
outStr = "SubjectNumber\tAge\tGender\tHandedness\tRace\tGlassesOrContacts\tTime\tTrialType\tTrial#\tCuedType(0=Both,1=CuedSide,2=CuedEmotion,3=UncuedTrial)\tCuedSide(0=Left,1=Right)\tEmotion(0=Happy,1=Angry)\tArrowColor\tFaceStim\tFacePosition\tCorrectKey\tKeyResponse\tKeyResponseRT\tErrorCode\tErrorName\tRegularOrCatch(0=Regular Trial,1=Opposite Emotion Catch Trial,2=Same Emotion Catch Trial)\tDelayBetweenCueAndFace\t"
outputFile.write(outStr + "eol\n")

# Setup the Psycho variables (screen, stimuli, sounds, etc)
win = visual.Window(fullscr=True, screen=0, allowGUI=False, allowStencil=False, monitor='DavesLaptop', color = 'gray', colorSpace='rgb', units='deg')
mon = monitors.Monitor('DavesLaptop')
trialClock = core.Clock()
eventClock = core.Clock()
evalClock = core.Clock()
isiClock = core.Clock()
keyResp = event.BuilderKeyResponse()  # create an object of type KeyResponse

#creating the fixation cross
fixationVertical = visual.Line(win,start=(0,-0.3), end=(0,0.3), lineColor = u'black',lineWidth=3.0)
fixationHorizontal = visual.Line(win,start=(-0.3,0), end=(0.3,0), lineColor = u'black',lineWidth=3.0)

#creating the array of trials
trialsArray=[]
trial=0
for rep in range(0, NUM_REPS):
    for cuedOrUncued in range (0,4):#0=CuedBoth, 1=CuedSide, 2=CuedEmotion, 3=UncuedTrial
        for emotion in range (0,2):#0=Happy, 1=Angry
            for leftOrRight in range (0,2):#0=Left, 1=Right
                for imageStim in range (0,56):#0=Image Happy0 or Angry0,#1=Image Happy1 or Angry1, etc.
                    trialsArray.append([trial,cuedOrUncued,emotion,leftOrRight,imageStim,0])
                    trial = trial+1

#opposite emotion catch trials - so if expecting happy on the left, angry shows on the right - no uncued here cause can't have uncued catch trials
for rep in range(0, NUM_REPS_CATCHTRIALS):
    for cuedOrUncued in range (0,3):#0=CuedBoth, 1=CuedSide, 2=CuedEmotion
        for emotion in range (0,2):#0=Happy, 1=Angry
            for leftOrRight in range (0,2):#0=Left, 1=Right
                trialsArray.append([trial,cuedOrUncued,emotion,leftOrRight,3,1])
                trial = trial+1

#same emotion catch trials - so if expecting happy on the left, happy shows on the right - no uncued here cause can't have uncued catch trials
for rep in range(0, NUM_REPS_CATCHTRIALS):
    for cuedOrUncued in range (0,2):#0=CuedBoth, 1=CuedSide
        for emotion in range (0,2):#0=Happy, 1=Angry
            for leftOrRight in range (0,2):#0=Left, 1=Right
                trialsArray.append([trial,cuedOrUncued,emotion,leftOrRight,3,2])
                trial = trial+1

#create arbitrary column that is shuffled to randomize trialsArray
idxTrialsArray = range(0, len(trialsArray)); random.shuffle(idxTrialsArray)

blocktrial = 0
totalTrials = 0
pracTrialCount = 0


blackArrowArray = ['Arrows/LeftBlack.png','Arrows/RightBlack.png','Arrows/UpBlack.png']

if buttonCounterbalance == 0 or buttonCounterbalance == 2:
    happyArrowArray = ['Arrows/LeftCyan.png','Arrows/RightCyan.png','Arrows/UpCyan.png']
    angryArrowArray = ['Arrows/LeftPurple.png','Arrows/RightPurple.png','Arrows/UpPurple.png']
    happyArrowCol = 'Cyan'
    angryArrowCol = 'Purple'
    happyTextCol = 'Cyan'
    angryTextCol = 'Purple'
if buttonCounterbalance == 1 or buttonCounterbalance == 3:
    angryArrowArray = ['Arrows/LeftCyan.png','Arrows/RightCyan.png','Arrows/UpCyan.png']
    happyArrowArray = ['Arrows/LeftPurple.png','Arrows/RightPurple.png','Arrows/UpPurple.png']
    angryArrowCol = 'Cyan'
    happyArrowCol = 'Purple'
    happyTextCol = 'Purple'
    angryTextCol = 'Cyan'



#INSTRUCTIONS
Instruct1 = visual.TextStim(win=win, ori=0, name='Instruct1', text='Welcome to the Experiment.',    font=u'Arial', pos=[0, 6], height=LargeTextSize, wrapWidth=30, color='black', colorSpace=u'rgb', opacity=1, depth=-1.0)
Instruct2 = visual.TextStim(win=win, ori=0, name='Instruct2', text='This experiment will test your ability to judge the emotion displayed by various faces.',    font=u'Arial', pos=[0, 2], height=LargeTextSize, wrapWidth=30, color='black', colorSpace=u'rgb', opacity=1, depth=-1.0)
Instruct3 = visual.TextStim(win=win, ori=0, name='Instruct3', text='Begin by placing your hands on the keyboard in the following positions:',    font=u'Arial', pos=[0, -2], height=LargeTextSize, wrapWidth=28, color='black', colorSpace=u'rgb', opacity=1, depth=-1.0)
Instruct4 = visual.TextStim(win=win, ori=0, name='Instruct4', text='S key\t\t\t\tD key\t\t\t\t\tK key\t\t\t\tL key',    font=u'Arial', pos=[0, -6], height=LargeTextSize, wrapWidth=35, color='black', colorSpace=u'rgb', opacity=1, depth=-1.0)
Instruct5 = visual.TextStim(win=win, ori=0, name='Instruct5', text='   Left middle finger\t\tLeft index finger\t\t   Right index finger\t\tRight middle finger',    font=u'Arial', pos=[0, -7.5], height=SmallTextSize, wrapWidth=40, color='black', colorSpace=u'rgb', opacity=1, depth=-1.0)

Instruct13 = visual.TextStim(win=win, ori=0, name='Instruct13', text='Press any key to continue with the instructions.',    font=u'Arial', pos=[0, -11.5], height=LargeTextSize, wrapWidth=30, color='black', colorSpace=u'rgb', opacity=1, depth=-1.0)

Instruct1.setAutoDraw(True);Instruct2.setAutoDraw(True);Instruct3.setAutoDraw(True);Instruct4.setAutoDraw(True);Instruct5.setAutoDraw(True);Instruct13.setAutoDraw(True);win.flip();event.waitKeys();

Instruct1.setAutoDraw(False);Instruct2.setAutoDraw(False);Instruct3.setAutoDraw(False);Instruct4.setAutoDraw(False);Instruct5.setAutoDraw(False);
Instruct6 = visual.TextStim(win=win, ori=0, name='Instruct6', text='On each trial you will first be presented with an arrow in the center of the screen indicating the side of the screen where the face image will appear. \nMaintain focus on the arrow until it disappears.\n\nAn arrow pointing left indicates the face image will appear on the left side of the screen. \n',    font=u'Arial', pos=[0, 5.5], height=SmallTextSize, wrapWidth=30, color='black', colorSpace=u'rgb', opacity=1, depth=-1.0)
ArrowImage = visual.ImageStim(win=win,image= happyArrowArray[0], pos= ARROWPOS, size=(ARROWSIZE,ARROWSIZE))
Instruct6.setAutoDraw(True);ArrowImage.setAutoDraw(True);win.flip();event.waitKeys();

Instruct6.setAutoDraw(False);ArrowImage.setAutoDraw(False);
Instruct6 = visual.TextStim(win=win, ori=0, name='Instruct6', text='An arrow pointing right indicates the face image will appear on the right side of the screen. \n',    font=u'Arial', pos=[0, 3], height=SmallTextSize, wrapWidth=30, color='black', colorSpace=u'rgb', opacity=1, depth=-1.0)
ArrowImage = visual.ImageStim(win=win,image= angryArrowArray[1], pos= ARROWPOS, size=(ARROWSIZE,ARROWSIZE))
Instruct6.setAutoDraw(True);ArrowImage.setAutoDraw(True);win.flip();event.waitKeys();

Instruct6.setAutoDraw(False);ArrowImage.setAutoDraw(False);
Instruct6 = visual.TextStim(win=win, ori=0, name='Instruct6', text='If the arrow points up then the face image can appear on either the left or right side of the screen.\n',    font=u'Arial', pos=[0, 3], height=SmallTextSize, wrapWidth=30, color='black', colorSpace=u'rgb', opacity=1, depth=-1.0)
ArrowImage = visual.ImageStim(win=win,image= blackArrowArray[2], pos= ARROWPOS, size=(ARROWSIZE,ARROWSIZE))
Instruct6.setAutoDraw(True);ArrowImage.setAutoDraw(True);win.flip();event.waitKeys();

Instruct6.setAutoDraw(False);ArrowImage.setAutoDraw(False);
Instruct6 = visual.TextStim(win=win, ori=0, name='Instruct6', text='The arrow also indicates the emotion of the face image that will appear. \nA ' + happyArrowCol + ' arrow indicates that the face will be happy.',    font=u'Arial', pos=[0, 4], height=SmallTextSize, wrapWidth=30, color='black', colorSpace=u'rgb', opacity=1, depth=-1.0)
ArrowImage = visual.ImageStim(win=win,image= happyArrowArray[0], pos= ARROWPOS, size=(ARROWSIZE,ARROWSIZE))
Instruct6.setAutoDraw(True);ArrowImage.setAutoDraw(True);win.flip();event.waitKeys();

Instruct6.setAutoDraw(False);ArrowImage.setAutoDraw(False);
Instruct6 = visual.TextStim(win=win, ori=0, name='Instruct6', text='A ' + angryArrowCol + ' arrow indicates that the face will be angry.',    font=u'Arial', pos=[0, 3], height=SmallTextSize, wrapWidth=30, color='black', colorSpace=u'rgb', opacity=1, depth=-1.0)
ArrowImage = visual.ImageStim(win=win,image= angryArrowArray[1], pos= ARROWPOS, size=(ARROWSIZE,ARROWSIZE))
Instruct6.setAutoDraw(True);ArrowImage.setAutoDraw(True);win.flip();event.waitKeys();

Instruct6.setAutoDraw(False);ArrowImage.setAutoDraw(False);
Instruct6 = visual.TextStim(win=win, ori=0, name='Instruct6', text='A Black arrow indicates that the face will be either happy or angry.',    font=u'Arial', pos=[0, 3], height=SmallTextSize, wrapWidth=30, color='black', colorSpace=u'rgb', opacity=1, depth=-1.0)
ArrowImage = visual.ImageStim(win=win,image= blackArrowArray[2], pos= ARROWPOS, size=(ARROWSIZE,ARROWSIZE))
Instruct7 = visual.TextStim(win=win, ori=0, name='Instruct7', text='Each time an arrow appears words will also be presented to instruct you if the image will be happy or angry, and if it will be presented on the left or right side of the screen.',    font=u'Arial', pos=[0, -4], height=SmallTextSize, wrapWidth=40, color='black', colorSpace=u'rgb', opacity=1, depth=-1.0)
Instruct6.setAutoDraw(True);Instruct7.setAutoDraw(True);ArrowImage.setAutoDraw(True);win.flip();event.waitKeys();

Instruct6.setAutoDraw(False);Instruct7.setAutoDraw(False);ArrowImage.setAutoDraw(False);
Instruct7 = visual.TextStim(win=win, ori=0, name='Instruct7', text='Following the arrow a face image will then be presented on the screen.\n',    font=u'Arial', pos=[0, 5.5], height=SmallTextSize, wrapWidth=33, color='black', colorSpace=u'rgb', opacity=1, depth=-1.0)
FaceImage = visual.ImageStim(win=win,image= u'Faces/Happy100.jpg', pos= POSARRAY[0], size=(FACEWIDTH,FACEHEIGHT))
if buttonCounterbalance == 0 or buttonCounterbalance == 1:
    Instruct8 = visual.TextStim(win=win, ori=0, name='Instruct8', text='If a happy face is presented on the left side of the screen, respond as quickly and accurately as possible with the middle finger of your left hand.\n',    font=u'Arial', pos=[-10, -7.75], height=SmallTextSize, wrapWidth=15, color='black', colorSpace=u'rgb', opacity=1, depth=-1.0)
if buttonCounterbalance == 2 or buttonCounterbalance == 3:
    Instruct8 = visual.TextStim(win=win, ori=0, name='Instruct8', text='If a happy face is presented on the left side of the screen, respond as quickly and accurately as possible with the index finger of your left hand.\n',    font=u'Arial', pos=[-10, -7.75], height=SmallTextSize, wrapWidth=15, color='black', colorSpace=u'rgb', opacity=1, depth=-1.0)
Instruct7.setAutoDraw(True);Instruct8.setAutoDraw(True);FaceImage.setAutoDraw(True);win.flip();event.waitKeys();

Instruct8.setAutoDraw(False);FaceImage.setAutoDraw(False);
FaceImage = visual.ImageStim(win=win,image= u'Faces/Angry100.jpg', pos= POSARRAY[0], size=(FACEWIDTH,FACEHEIGHT))
if buttonCounterbalance == 0 or buttonCounterbalance == 1:
    Instruct9 = visual.TextStim(win=win, ori=0, name='Instruct9', text='If an angry face is presented on the left side of the screen, respond as quickly and accurately as possible with the index finger of your left hand.\n',    font=u'Arial', pos=[-10, -7.75], height=SmallTextSize, wrapWidth=15, color='black', colorSpace=u'rgb', opacity=1, depth=-1.0)
if buttonCounterbalance == 2 or buttonCounterbalance == 3:
    Instruct9 = visual.TextStim(win=win, ori=0, name='Instruct9', text='If an angry face is presented on the left side of the screen, respond as quickly and accurately as possible with the middle finger of your left hand.\n',    font=u'Arial', pos=[-10, -7.75], height=SmallTextSize, wrapWidth=15, color='black', colorSpace=u'rgb', opacity=1, depth=-1.0)
Instruct9.setAutoDraw(True);FaceImage.setAutoDraw(True);win.flip();event.waitKeys();

Instruct9.setAutoDraw(False);FaceImage.setAutoDraw(False);
FaceImage = visual.ImageStim(win=win,image= u'Faces/Happy100.jpg', pos= POSARRAY[1], size=(FACEWIDTH,FACEHEIGHT))
if buttonCounterbalance == 0 or buttonCounterbalance == 1:
    Instruct10 = visual.TextStim(win=win, ori=0, name='Instruct10', text='If a happy face is presented on the right side of the screen, respond as quickly and accurately as possible with the middle finger of your right hand.\n',    font=u'Arial', pos=[10, -7.75], height=SmallTextSize, wrapWidth=15, color='black', colorSpace=u'rgb', opacity=1, depth=-1.0)
if buttonCounterbalance == 2 or buttonCounterbalance == 3:
    Instruct10 = visual.TextStim(win=win, ori=0, name='Instruct10', text='If a happy face is presented on the right side of the screen, respond as quickly and accurately as possible with the index finger of your right hand.\n',    font=u'Arial', pos=[10, -7.75], height=SmallTextSize, wrapWidth=15, color='black', colorSpace=u'rgb', opacity=1, depth=-1.0)
Instruct10.setAutoDraw(True);FaceImage.setAutoDraw(True);win.flip();event.waitKeys();

Instruct10.setAutoDraw(False);FaceImage.setAutoDraw(False);
FaceImage = visual.ImageStim(win=win,image= u'Faces/Angry100.jpg', pos= POSARRAY[1], size=(FACEWIDTH,FACEHEIGHT))
if buttonCounterbalance == 0 or buttonCounterbalance == 1:
    Instruct11 = visual.TextStim(win=win, ori=0, name='Instruct11', text='If an angry face is presented on the right side of the screen, respond as quickly and accurately as possible with the index finger of your right hand.\n',    font=u'Arial', pos=[10, -7.75], height=SmallTextSize, wrapWidth=15, color='black', colorSpace=u'rgb', opacity=1, depth=-1.0)
if buttonCounterbalance == 2 or buttonCounterbalance == 3:
    Instruct11 = visual.TextStim(win=win, ori=0, name='Instruct11', text='If an angry face is presented on the right side of the screen, respond as quickly and accurately as possible with the middle finger of your right hand.\n',    font=u'Arial', pos=[10, -7.75], height=SmallTextSize, wrapWidth=15, color='black', colorSpace=u'rgb', opacity=1, depth=-1.0)
Instruct11.setAutoDraw(True);FaceImage.setAutoDraw(True);win.flip();event.waitKeys();

Instruct11.setAutoDraw(False);Instruct7.setAutoDraw(False);FaceImage.setAutoDraw(False);Instruct13.setAutoDraw(False);
Instruct12 = visual.TextStim(win=win, ori=0, name='Instruct12', text='You are now ready to begin the practice trials.\n\nRemember to maintain focus on the arrow when it is on the screen.\n\nPress any key when you would like to start. ',    font=u'Arial', pos=[0, 2], height=SmallTextSize, wrapWidth=30, color='black', colorSpace=u'rgb', opacity=1, depth=-1.0)
Instruct12.setAutoDraw(True);win.flip();event.waitKeys();

Instruct12.setAutoDraw(False);


fixationVertical.setAutoDraw(True)
fixationHorizontal.setAutoDraw(True)

#Practice Trials
TrialType = "Practice"
pracAccuracyArray = [0,0,0,0,0,0,0,0,0,0]
pracTrialNum = 0

for ptrial in range(0, 300):
    
    INTER_TRIAL_INTERVAL = (random.random()/5) + 0.2
    
    
    if pracTrialNum<12:
        CUEARROW_TIME = 2.0;FACE_ON_SCREEN = .5;FACE_OFF_SCREEN = 1.6
    if pracTrialNum>11:
        CUEARROW_TIME = 1.0;FACE_ON_SCREEN = .25;FACE_OFF_SCREEN = 1.6
    
    pracTrialACC = 0
    
    #deciding which stimulus
    randStim = random.randint(100,103)
    
    
    #generating practice trial condition randomly
    emotionRand = random.randint(0,1)#0=happy,1=angry
    leftRightRand = random.randint(0,1)#0=left,1=right
    cuedTypeRand = random.randint(0,3)#0=CuedBoth, 1=CuedSide, 2=CuedEmotion, 3=UncuedTrial
    
    
    runTime = time.strftime("%c")
    
    #Fixation Cross Presented
    win.flip()
    trialClock.reset()
    while trialClock.getTime() < INTER_TRIAL_INTERVAL: pass
    
    
    #Presenting Arrow on the Screen
    
    #UnCued
    if cuedTypeRand == 3:
        ArrowImage = visual.ImageStim(win=win,image= blackArrowArray[2], pos= ARROWPOS, size=(ARROWSIZE,ARROWSIZE))
        arrowCol='Black'
        EmotionCueText = visual.TextStim(win=win, ori=0, name='CueText', text='Either Emotion',    font=u'Arial', pos=[0, 3], height=LargeTextSize, wrapWidth=30, color='black', colorSpace=u'rgb', opacity=1, depth=-1.0)
        SideCueText = visual.TextStim(win=win, ori=0, name='CueText', text='Either Side',    font=u'Arial', pos=[0, -3], height=LargeTextSize, wrapWidth=30, color='black', colorSpace=u'rgb', opacity=1, depth=-1.0)
    #Both Emotion and Side Cued
    if cuedTypeRand == 0:
        #left side
        if leftRightRand == 0:
            #Happy
            if emotionRand == 0:
                ArrowImage = visual.ImageStim(win=win,image= happyArrowArray[0], pos= ARROWPOS, size=(ARROWSIZE,ARROWSIZE))
                arrowCol=happyArrowCol
                EmotionCueText = visual.TextStim(win=win, ori=0, name='CueText', text='Happy Emotion',    font=u'Arial', pos=[0, 3], height=LargeTextSize, wrapWidth=30, color=happyTextCol, colorSpace=u'rgb', opacity=1, depth=-1.0)
                SideCueText = visual.TextStim(win=win, ori=0, name='CueText', text='Left Side',    font=u'Arial', pos=[0, -3], height=LargeTextSize, wrapWidth=30, color=happyTextCol, colorSpace=u'rgb', opacity=1, depth=-1.0)
            #Angry
            if emotionRand == 1:
                ArrowImage = visual.ImageStim(win=win,image= angryArrowArray[0], pos= ARROWPOS, size=(ARROWSIZE,ARROWSIZE))
                arrowCol=angryArrowCol
                EmotionCueText = visual.TextStim(win=win, ori=0, name='CueText', text='Angry Emotion',    font=u'Arial', pos=[0, 3], height=LargeTextSize, wrapWidth=30, color=angryTextCol, colorSpace=u'rgb', opacity=1, depth=-1.0)
                SideCueText = visual.TextStim(win=win, ori=0, name='CueText', text='Left Side',    font=u'Arial', pos=[0, -3], height=LargeTextSize, wrapWidth=30, color=angryTextCol, colorSpace=u'rgb', opacity=1, depth=-1.0)
        #right side
        if leftRightRand == 1:
            #Happy
            if emotionRand == 0:
                ArrowImage = visual.ImageStim(win=win,image= happyArrowArray[1], pos= ARROWPOS, size=(ARROWSIZE,ARROWSIZE))
                arrowCol=happyArrowCol
                EmotionCueText = visual.TextStim(win=win, ori=0, name='CueText', text='Happy Emotion',    font=u'Arial', pos=[0, 3], height=LargeTextSize, wrapWidth=30, color=happyTextCol, colorSpace=u'rgb', opacity=1, depth=-1.0)
                SideCueText = visual.TextStim(win=win, ori=0, name='CueText', text='Right Side',    font=u'Arial', pos=[0, -3], height=LargeTextSize, wrapWidth=30, color=happyTextCol, colorSpace=u'rgb', opacity=1, depth=-1.0)
            #Angry
            if emotionRand == 1:
                ArrowImage = visual.ImageStim(win=win,image= angryArrowArray[1], pos= ARROWPOS, size=(ARROWSIZE,ARROWSIZE))
                arrowCol=angryArrowCol
                EmotionCueText = visual.TextStim(win=win, ori=0, name='CueText', text='Angry Emotion',    font=u'Arial', pos=[0, 3], height=LargeTextSize, wrapWidth=30, color=angryTextCol, colorSpace=u'rgb', opacity=1, depth=-1.0)
                SideCueText = visual.TextStim(win=win, ori=0, name='CueText', text='Right Side',    font=u'Arial', pos=[0, -3], height=LargeTextSize, wrapWidth=30, color=angryTextCol, colorSpace=u'rgb', opacity=1, depth=-1.0)

    #Only Side is Cued
    if cuedTypeRand == 1:
        arrowCol='Black'
        #left side
        if leftRightRand == 0:
            ArrowImage = visual.ImageStim(win=win,image= blackArrowArray[0], pos= ARROWPOS, size=(ARROWSIZE,ARROWSIZE))
            EmotionCueText = visual.TextStim(win=win, ori=0, name='CueText', text='Either Emotion',    font=u'Arial', pos=[0, 3], height=LargeTextSize, wrapWidth=30, color='black', colorSpace=u'rgb', opacity=1, depth=-1.0)
            SideCueText = visual.TextStim(win=win, ori=0, name='CueText', text='Left Side',    font=u'Arial', pos=[0, -3], height=LargeTextSize, wrapWidth=30, color='black', colorSpace=u'rgb', opacity=1, depth=-1.0)
        #right side
        if leftRightRand == 1:
            ArrowImage = visual.ImageStim(win=win,image= blackArrowArray[1], pos= ARROWPOS, size=(ARROWSIZE,ARROWSIZE))
            EmotionCueText = visual.TextStim(win=win, ori=0, name='CueText', text='Either Emotion',    font=u'Arial', pos=[0, 3], height=LargeTextSize, wrapWidth=30, color='black', colorSpace=u'rgb', opacity=1, depth=-1.0)
            SideCueText = visual.TextStim(win=win, ori=0, name='CueText', text='Right Side',    font=u'Arial', pos=[0, -3], height=LargeTextSize, wrapWidth=30, color='black', colorSpace=u'rgb', opacity=1, depth=-1.0)
            
    #Only Emotion is Cued
    if cuedTypeRand == 2:
        #Happy
        if emotionRand == 0:
            ArrowImage = visual.ImageStim(win=win,image= happyArrowArray[2], pos= ARROWPOS, size=(ARROWSIZE,ARROWSIZE))
            arrowCol=happyArrowCol
            EmotionCueText = visual.TextStim(win=win, ori=0, name='CueText', text='Happy Emotion',    font=u'Arial', pos=[0, 3], height=LargeTextSize, wrapWidth=30, color=happyTextCol, colorSpace=u'rgb', opacity=1, depth=-1.0)
            SideCueText = visual.TextStim(win=win, ori=0, name='CueText', text='Either Side',    font=u'Arial', pos=[0, -3], height=LargeTextSize, wrapWidth=30, color=happyTextCol, colorSpace=u'rgb', opacity=1, depth=-1.0)
        #Angry
        if emotionRand == 1:
            ArrowImage = visual.ImageStim(win=win,image= angryArrowArray[2], pos= ARROWPOS, size=(ARROWSIZE,ARROWSIZE))
            arrowCol=angryArrowCol
            EmotionCueText = visual.TextStim(win=win, ori=0, name='CueText', text='Angry Emotion',    font=u'Arial', pos=[0, 3], height=LargeTextSize, wrapWidth=30, color=angryTextCol, colorSpace=u'rgb', opacity=1, depth=-1.0)
            SideCueText = visual.TextStim(win=win, ori=0, name='CueText', text='Either Side',    font=u'Arial', pos=[0, -3], height=LargeTextSize, wrapWidth=30, color=angryTextCol, colorSpace=u'rgb', opacity=1, depth=-1.0)

            
    fixationVertical.setAutoDraw(False)
    fixationHorizontal.setAutoDraw(False)
    EmotionCueText.setAutoDraw(True)
    SideCueText.setAutoDraw(True)
    ArrowImage.setAutoDraw(True)
    win.flip()
    
    while trialClock.getTime() < INTER_TRIAL_INTERVAL + CUEARROW_TIME: pass
    
    
    #Present Face Image
    #left side
    if leftRightRand == 0:
        FACEPOS = POSARRAY[0]
    #right side
    if leftRightRand == 1:
        FACEPOS = POSARRAY[1]

    
    #Happy
    if emotionRand == 0:
        FaceImage = visual.ImageStim(win=win,image= u'Faces/Happy' + str(randStim) + '.jpg', pos= FACEPOS, size=(FACEWIDTH,FACEHEIGHT))
        FaceStim = 'Happy' + str(randStim) + '.jpg'
    #Angry
    if emotionRand == 1:
        FaceImage = visual.ImageStim(win=win,image= u'Faces/Angry' + str(randStim) + '.jpg', pos= FACEPOS, size=(FACEWIDTH,FACEHEIGHT))
        FaceStim = 'Angry' + str(randStim) + '.jpg'



    #CORRECT RESPONSE FOR THIS TRIAL
    #Left Happy
    if emotionRand == 0 and leftRightRand == 0:
        if buttonCounterbalance == 0 or buttonCounterbalance == 1:correctKey = 's'
        if buttonCounterbalance == 2 or buttonCounterbalance == 3:correctKey = 'd'
    #Left Angry
    if emotionRand == 1 and leftRightRand == 0:
        if buttonCounterbalance == 0 or buttonCounterbalance == 1:correctKey = 'd'
        if buttonCounterbalance == 2 or buttonCounterbalance == 3:correctKey = 's'
    #Right Happy
    if emotionRand == 0 and leftRightRand == 1:
        if buttonCounterbalance == 0 or buttonCounterbalance == 1:correctKey = 'l'
        if buttonCounterbalance == 2 or buttonCounterbalance == 3:correctKey = 'k'
    #Right Angry
    if emotionRand == 1 and leftRightRand == 1:
        if buttonCounterbalance == 0 or buttonCounterbalance == 1:correctKey = 'k'
        if buttonCounterbalance == 2 or buttonCounterbalance == 3:correctKey = 'l'


    EmotionCueText.setAutoDraw(False)
    SideCueText.setAutoDraw(False)
    ArrowImage.setAutoDraw(False)
    win.flip()
    
    #jitter fixation cross presentation between cue and face presentation. 0-200ms
    TIME_BETWEEN_CUE_AND_FACE_PRAC = (random.random()/5)
    while trialClock.getTime() < INTER_TRIAL_INTERVAL + CUEARROW_TIME + TIME_BETWEEN_CUE_AND_FACE_PRAC: pass
    
    FaceImage.setAutoDraw(True)
    win.flip()
    eventClock.reset()
    stimOnScreen = True
    keyResp.status = NOT_STARTED
    respErrorCode = -1
    respErrorName = ''
    noResponseYet = True
    keyResp.keys = []
    keyResp.rt = -1
    while trialClock.getTime() < INTER_TRIAL_INTERVAL + CUEARROW_TIME + TIME_BETWEEN_CUE_AND_FACE_PRAC + FACE_ON_SCREEN + FACE_OFF_SCREEN:
        t = eventClock.getTime()
        #initialize key checker
        if keyResp.status == NOT_STARTED:
            keyResp.tStart = t
            keyResp.status = STARTED
            keyResp.clock.reset()
            #event.getKeys()
            event.clearEvents()
            
        
        
        #check for a keyboard response
        theseKeys = event.getKeys(keyList=['s','d','k','l'])
        if len(theseKeys) > 0: #test if atleast one key pressed
            keyResp.keys = theseKeys[-1] #just the last key pressed
            keyResp.rt = keyResp.clock.getTime()
            faceResponse = keyResp.keys
            faceResponseRT = keyResp.rt
            if noResponseYet:
                if correctKey == 's':
                    if keyResp.keys == 'd' or keyResp.keys == 'k' or keyResp.keys == 'l':
                        respErrorCode = 2;respErrorName = 'incorrect response'
                if correctKey == 'd':
                    if keyResp.keys == 's' or keyResp.keys == 'k' or keyResp.keys == 'l':
                        respErrorCode = 2;respErrorName = 'incorrect response'
                if correctKey == 'k':
                    if keyResp.keys == 's' or keyResp.keys == 'd' or keyResp.keys == 'l':
                        respErrorCode = 2;respErrorName = 'incorrect response'
                if correctKey == 'l':
                    if keyResp.keys == 's' or keyResp.keys == 'd' or keyResp.keys == 'k':
                        respErrorCode = 2;respErrorName = 'incorrect response'
                noResponseYet = False
            else:
                if correctKey == 's':
                    if keyResp.keys == 'd' or keyResp.keys == 'k' or keyResp.keys == 'l':
                        respErrorCode = 2;respErrorName = 'incorrect response'
                if correctKey == 'd':
                    if keyResp.keys == 's' or keyResp.keys == 'k' or keyResp.keys == 'l':
                        respErrorCode = 2;respErrorName = 'incorrect response'
                if correctKey == 'k':
                    if keyResp.keys == 's' or keyResp.keys == 'd' or keyResp.keys == 'l':
                        respErrorCode = 2;respErrorName = 'incorrect response'
                if correctKey == 'l':
                    if keyResp.keys == 's' or keyResp.keys == 'd' or keyResp.keys == 'k':
                        respErrorCode = 2;respErrorName = 'incorrect response'
                if respErrorCode != -1:
                    respErrorCode = 1
                    respErrorName = 'multi-response'
        
        
        
        if stimOnScreen and t > FACE_ON_SCREEN:
            FaceImage.setAutoDraw(False)
            win.flip()
            stimOnScreen = False
        
        
        # check for quit (the [Esc] key)
        if event.getKeys(["escape"]):
            core.quit()
            

    
    if noResponseYet:
       faceResponse = 'no response'
       faceResponseRT = 'no response'
       respErrorCode = 5
       respErrorName = 'no response'
       noResponseYet = False
        

    #Feedback Screen
    if respErrorCode == -1:
        feedbackText = visual.TextStim(win=win, ori=0, name='feedbackText', text='Correct',    font=u'Arial', pos=[0, 2], height=LargeTextSize, wrapWidth=15, color='lightgreen', colorSpace=u'rgb', opacity=1, depth=-1.0)
    elif respErrorCode == 2:
        feedbackText = visual.TextStim(win=win, ori=0, name='feedbackText', text='Incorrect',    font=u'Arial', pos=[0, 2], height=LargeTextSize, wrapWidth=15, color='darkred', colorSpace=u'rgb', opacity=1, depth=-1.0)
    elif respErrorCode == 5:
        feedbackText = visual.TextStim(win=win, ori=0, name='feedbackText', text='No Response',    font=u'Arial', pos=[0, 2], height=LargeTextSize, wrapWidth=15, color='darkred', colorSpace=u'rgb', opacity=1, depth=-1.0)
    elif respErrorCode == 1:
        feedbackText = visual.TextStim(win=win, ori=0, name='feedbackText', text='Multiple Responses',    font=u'Arial', pos=[0, 2], height=LargeTextSize, wrapWidth=15, color='darkred', colorSpace=u'rgb', opacity=1, depth=-1.0)
    if keyResp.rt > 1:
        feedbackText = visual.TextStim(win=win, ori=0, name='feedbackText', text='Late Response',    font=u'Arial', pos=[0, 2], height=LargeTextSize, wrapWidth=15, color='darkred', colorSpace=u'rgb', opacity=1, depth=-1.0)
    feedbackText.setAutoDraw(True);
    fixationVertical.setAutoDraw(True)
    fixationHorizontal.setAutoDraw(True)
    win.flip();
    while trialClock.getTime() < INTER_TRIAL_INTERVAL + CUEARROW_TIME + TIME_BETWEEN_CUE_AND_FACE_PRAC + FACE_ON_SCREEN + FACE_OFF_SCREEN + FEEDBACK_TIME:pass
    feedbackText.setAutoDraw(False)

    if respErrorCode == -1:
        pracTrialACC = 1
        

    
    pracTrialNum = pracTrialNum + 1
    
    
    outStr = str(subjectNumber)+ '\t'
    outStr = outStr + str(expInfo2['age']) + '\t'
    outStr = outStr + str(expInfo3['gender']) + '\t'
    outStr = outStr + str(expInfo4['handedness']) + '\t'
    outStr = outStr + str(expInfo5['race']) + '\t'
    outStr = outStr + str(expInfo6['glasses/contacts?']) + '\t'
    outStr = outStr + str(runTime) + '\t'
    outStr = outStr + str(TrialType) + '\t'
    outStr = outStr + str(pracTrialNum) + '\t'
    outStr = outStr + str(cuedTypeRand) + '\t'
    outStr = outStr + str(leftRightRand) + '\t'
    outStr = outStr + str(emotionRand) + '\t'
    outStr = outStr + str(arrowCol) + '\t'
    outStr = outStr + str(FaceStim) + '\t'
    outStr = outStr + str(FACEPOS) + '\t'
    outStr = outStr + correctKey + '\t'
    outStr = outStr + str(faceResponse) + '\t'
    outStr = outStr + str(faceResponseRT) + '\t'
    outStr = outStr + str(respErrorCode) + '\t'
    outStr = outStr + respErrorName + '\t'
    outStr = outStr + '0' + '\t'
    outStr = outStr + str(TIME_BETWEEN_CUE_AND_FACE_PRAC) + '\t'
    outputFile.write(outStr + 'eol\n')
    
    if pracTrialNum>30:
        pracAccuracyArrayNew = [pracTrialACC,pracAccuracyArray[0],pracAccuracyArray[1],pracAccuracyArray[2],pracAccuracyArray[3],pracAccuracyArray[4],pracAccuracyArray[5],pracAccuracyArray[6],pracAccuracyArray[7],pracAccuracyArray[8]]
        pracAccuracyArray = pracAccuracyArrayNew
        pracAccuracyValue = sum(pracAccuracyArray)
        if pracAccuracyValue>8:
            break





Instruct7 = visual.TextStim(win=win, ori=0, name='Instruct7', text='Remember...\n',    font=u'Arial', pos=[0, 5.5], height=SmallTextSize, wrapWidth=20, color='black', colorSpace=u'rgb', opacity=1, depth=-1.0)
Instruct7.setAutoDraw(True);win.flip();event.waitKeys();
FaceImage = visual.ImageStim(win=win,image= u'Faces/Happy100.jpg', pos= POSARRAY[0], size=(FACEWIDTH,FACEHEIGHT))
if buttonCounterbalance == 0 or buttonCounterbalance == 1:
    Instruct8 = visual.TextStim(win=win, ori=0, name='Instruct8', text='If a happy face is presented on the left side of the screen, respond as quickly and accurately as possible with the middle finger of your left hand.\n',    font=u'Arial', pos=[-10, -7.75], height=SmallTextSize, wrapWidth=15, color='black', colorSpace=u'rgb', opacity=1, depth=-1.0)
if buttonCounterbalance == 2 or buttonCounterbalance == 3:
    Instruct8 = visual.TextStim(win=win, ori=0, name='Instruct8', text='If a happy face is presented on the left side of the screen, respond as quickly and accurately as possible with the index finger of your left hand.\n',    font=u'Arial', pos=[-10, -7.75], height=SmallTextSize, wrapWidth=15, color='black', colorSpace=u'rgb', opacity=1, depth=-1.0)
Instruct8.setAutoDraw(True);FaceImage.setAutoDraw(True);win.flip();event.waitKeys();

Instruct8.setAutoDraw(False);FaceImage.setAutoDraw(False);
FaceImage = visual.ImageStim(win=win,image= u'Faces/Angry100.jpg', pos= POSARRAY[0], size=(FACEWIDTH,FACEHEIGHT))
if buttonCounterbalance == 0 or buttonCounterbalance == 1:
    Instruct9 = visual.TextStim(win=win, ori=0, name='Instruct9', text='If an angry face is presented on the left side of the screen, respond as quickly and accurately as possible with the index finger of your left hand.\n',    font=u'Arial', pos=[-10, -7.75], height=SmallTextSize, wrapWidth=15, color='black', colorSpace=u'rgb', opacity=1, depth=-1.0)
if buttonCounterbalance == 2 or buttonCounterbalance == 3:
    Instruct9 = visual.TextStim(win=win, ori=0, name='Instruct9', text='If an angry face is presented on the left side of the screen, respond as quickly and accurately as possible with the middle finger of your left hand.\n',    font=u'Arial', pos=[-10, -7.75], height=SmallTextSize, wrapWidth=15, color='black', colorSpace=u'rgb', opacity=1, depth=-1.0)
Instruct9.setAutoDraw(True);FaceImage.setAutoDraw(True);win.flip();event.waitKeys();

Instruct9.setAutoDraw(False);FaceImage.setAutoDraw(False);
FaceImage = visual.ImageStim(win=win,image= u'Faces/Happy100.jpg', pos= POSARRAY[1], size=(FACEWIDTH,FACEHEIGHT))
if buttonCounterbalance == 0 or buttonCounterbalance == 1:
    Instruct10 = visual.TextStim(win=win, ori=0, name='Instruct10', text='If a happy face is presented on the right side of the screen, respond as quickly and accurately as possible with the middle finger of your right hand.\n',    font=u'Arial', pos=[10, -7.75], height=SmallTextSize, wrapWidth=15, color='black', colorSpace=u'rgb', opacity=1, depth=-1.0)
if buttonCounterbalance == 2 or buttonCounterbalance == 3:
    Instruct10 = visual.TextStim(win=win, ori=0, name='Instruct10', text='If a happy face is presented on the right side of the screen, respond as quickly and accurately as possible with the index finger of your right hand.\n',    font=u'Arial', pos=[10, -7.75], height=SmallTextSize, wrapWidth=15, color='black', colorSpace=u'rgb', opacity=1, depth=-1.0)
Instruct10.setAutoDraw(True);FaceImage.setAutoDraw(True);win.flip();event.waitKeys();

Instruct10.setAutoDraw(False);FaceImage.setAutoDraw(False);
FaceImage = visual.ImageStim(win=win,image= u'Faces/Angry100.jpg', pos= POSARRAY[1], size=(FACEWIDTH,FACEHEIGHT))
if buttonCounterbalance == 0 or buttonCounterbalance == 1:
    Instruct11 = visual.TextStim(win=win, ori=0, name='Instruct11', text='If an angry face is presented on the right side of the screen, respond as quickly and accurately as possible with the index finger of your right hand.\n',    font=u'Arial', pos=[10, -7.75], height=SmallTextSize, wrapWidth=15, color='black', colorSpace=u'rgb', opacity=1, depth=-1.0)
if buttonCounterbalance == 2 or buttonCounterbalance == 3:
    Instruct11 = visual.TextStim(win=win, ori=0, name='Instruct11', text='If an angry face is presented on the right side of the screen, respond as quickly and accurately as possible with the middle finger of your right hand.\n',    font=u'Arial', pos=[10, -7.75], height=SmallTextSize, wrapWidth=15, color='black', colorSpace=u'rgb', opacity=1, depth=-1.0)
Instruct11.setAutoDraw(True);FaceImage.setAutoDraw(True);win.flip();event.waitKeys();

Instruct11.setAutoDraw(False);FaceImage.setAutoDraw(False);
Instruct11 = visual.TextStim(win=win, ori=0, name='Instruct11', text='Please note: On 5% of trials the face image that is displayed will not correspond with the side and colour of the cue arrow. In those cases please respond to the actual emotion and location of the face image, and not with the emotion and location predicted by the arrow.',    font=u'Arial', pos=[0, -4.5], height=SmallTextSize, wrapWidth=25, color='black', colorSpace=u'rgb', opacity=1, depth=-1.0)
Instruct11.setAutoDraw(True);win.flip();event.waitKeys();

Instruct11.setAutoDraw(False);Instruct7.setAutoDraw(False);FaceImage.setAutoDraw(False);Instruct13.setAutoDraw(False);
Instruct12 = visual.TextStim(win=win, ori=0, name='Instruct12', text='You are now ready to begin the experimental trials.\nRemember to maintain focus on the arrow when it is on the screen.\nPress any key when you would like to start. ',    font=u'Arial', pos=[0, 5], height=SmallTextSize, wrapWidth=30, color='black', colorSpace=u'rgb', opacity=1, depth=-1.0)
Instruct12.setAutoDraw(True);win.flip();event.waitKeys();

Instruct12.setAutoDraw(False);

trialNum=0
blocktrial=0
trialCount=0
percDone=0
blockACC=0
blockRT=0
correctTrialCount = 0
lateTrialCount = 0

fixationVertical.setAutoDraw(True)
fixationHorizontal.setAutoDraw(True)

#Actual Trials
TrialType = "Attention"
CUEARROW_TIME = 1.0;FACE_ON_SCREEN = .25;FACE_OFF_SCREEN = 1.6
for trial in range(0, 936):
    
    
    INTER_TRIAL_INTERVAL = (random.random()/5) + 0.2
    
    runTime = time.strftime("%c")
    
    curRow = idxTrialsArray[trial]
    
    #Fixation Cross Presented
    win.flip()
    trialClock.reset()
    while trialClock.getTime() < INTER_TRIAL_INTERVAL: pass
    
    
    #Presenting Arrow on the Screen
    
    #UnCued
    if trialsArray[curRow][1] == 3:
        ArrowImage = visual.ImageStim(win=win,image= blackArrowArray[2], pos= ARROWPOS, size=(ARROWSIZE,ARROWSIZE))
        arrowCol='Black'
        EmotionCueText = visual.TextStim(win=win, ori=0, name='CueText', text='Either Emotion',    font=u'Arial', pos=[0, 3], height=LargeTextSize, wrapWidth=30, color='black', colorSpace=u'rgb', opacity=1, depth=-1.0)
        SideCueText = visual.TextStim(win=win, ori=0, name='CueText', text='Either Side',    font=u'Arial', pos=[0, -3], height=LargeTextSize, wrapWidth=30, color='black', colorSpace=u'rgb', opacity=1, depth=-1.0)
    #Both Emotion and Side Cued
    if trialsArray[curRow][1] == 0:
        #left side
        if trialsArray[curRow][3] == 0:
            #Happy
            if trialsArray[curRow][2] == 0:
                ArrowImage = visual.ImageStim(win=win,image= happyArrowArray[0], pos= ARROWPOS, size=(ARROWSIZE,ARROWSIZE))
                arrowCol=happyArrowCol
                EmotionCueText = visual.TextStim(win=win, ori=0, name='CueText', text='Happy Emotion',    font=u'Arial', pos=[0, 3], height=LargeTextSize, wrapWidth=30, color=happyTextCol, colorSpace=u'rgb', opacity=1, depth=-1.0)
                SideCueText = visual.TextStim(win=win, ori=0, name='CueText', text='Left Side',    font=u'Arial', pos=[0, -3], height=LargeTextSize, wrapWidth=30, color=happyTextCol, colorSpace=u'rgb', opacity=1, depth=-1.0)
            #Angry
            if trialsArray[curRow][2] == 1:
                ArrowImage = visual.ImageStim(win=win,image= angryArrowArray[0], pos= ARROWPOS, size=(ARROWSIZE,ARROWSIZE))
                arrowCol=angryArrowCol
                EmotionCueText = visual.TextStim(win=win, ori=0, name='CueText', text='Angry Emotion',    font=u'Arial', pos=[0, 3], height=LargeTextSize, wrapWidth=30, color=angryTextCol, colorSpace=u'rgb', opacity=1, depth=-1.0)
                SideCueText = visual.TextStim(win=win, ori=0, name='CueText', text='Left Side',    font=u'Arial', pos=[0, -3], height=LargeTextSize, wrapWidth=30, color=angryTextCol, colorSpace=u'rgb', opacity=1, depth=-1.0)
        #right side
        if trialsArray[curRow][3] == 1:
            #Happy
            if trialsArray[curRow][2] == 0:
                ArrowImage = visual.ImageStim(win=win,image= happyArrowArray[1], pos= ARROWPOS, size=(ARROWSIZE,ARROWSIZE))
                arrowCol=happyArrowCol
                EmotionCueText = visual.TextStim(win=win, ori=0, name='CueText', text='Happy Emotion',    font=u'Arial', pos=[0, 3], height=LargeTextSize, wrapWidth=30, color=happyTextCol, colorSpace=u'rgb', opacity=1, depth=-1.0)
                SideCueText = visual.TextStim(win=win, ori=0, name='CueText', text='Right Side',    font=u'Arial', pos=[0, -3], height=LargeTextSize, wrapWidth=30, color=happyTextCol, colorSpace=u'rgb', opacity=1, depth=-1.0)
            #Angry
            if trialsArray[curRow][2] == 1:
                ArrowImage = visual.ImageStim(win=win,image= angryArrowArray[1], pos= ARROWPOS, size=(ARROWSIZE,ARROWSIZE))
                arrowCol=angryArrowCol
                EmotionCueText = visual.TextStim(win=win, ori=0, name='CueText', text='Angry Emotion',    font=u'Arial', pos=[0, 3], height=LargeTextSize, wrapWidth=30, color=angryTextCol, colorSpace=u'rgb', opacity=1, depth=-1.0)
                SideCueText = visual.TextStim(win=win, ori=0, name='CueText', text='Right Side',    font=u'Arial', pos=[0, -3], height=LargeTextSize, wrapWidth=30, color=angryTextCol, colorSpace=u'rgb', opacity=1, depth=-1.0)
                
    #Only Side is Cued
    if trialsArray[curRow][1] == 1:
        arrowCol='Black'
        #left side
        if trialsArray[curRow][3] == 0:
            ArrowImage = visual.ImageStim(win=win,image= blackArrowArray[0], pos= ARROWPOS, size=(ARROWSIZE,ARROWSIZE))
            EmotionCueText = visual.TextStim(win=win, ori=0, name='CueText', text='Either Emotion',    font=u'Arial', pos=[0, 3], height=LargeTextSize, wrapWidth=30, color='black', colorSpace=u'rgb', opacity=1, depth=-1.0)
            SideCueText = visual.TextStim(win=win, ori=0, name='CueText', text='Left Side',    font=u'Arial', pos=[0, -3], height=LargeTextSize, wrapWidth=30, color='black', colorSpace=u'rgb', opacity=1, depth=-1.0)
        #right side
        if trialsArray[curRow][3] == 1:
            ArrowImage = visual.ImageStim(win=win,image= blackArrowArray[1], pos= ARROWPOS, size=(ARROWSIZE,ARROWSIZE))
            EmotionCueText = visual.TextStim(win=win, ori=0, name='CueText', text='Either Emotion',    font=u'Arial', pos=[0, 3], height=LargeTextSize, wrapWidth=30, color='black', colorSpace=u'rgb', opacity=1, depth=-1.0)
            SideCueText = visual.TextStim(win=win, ori=0, name='CueText', text='Right Side',    font=u'Arial', pos=[0, -3], height=LargeTextSize, wrapWidth=30, color='black', colorSpace=u'rgb', opacity=1, depth=-1.0)
            
    #Only Emotion is Cued
    if trialsArray[curRow][1] == 2:
        #Happy
        if trialsArray[curRow][2] == 0:
            ArrowImage = visual.ImageStim(win=win,image= happyArrowArray[2], pos= ARROWPOS, size=(ARROWSIZE,ARROWSIZE))
            arrowCol=happyArrowCol
            EmotionCueText = visual.TextStim(win=win, ori=0, name='CueText', text='Happy Emotion',    font=u'Arial', pos=[0, 3], height=LargeTextSize, wrapWidth=30, color=happyTextCol, colorSpace=u'rgb', opacity=1, depth=-1.0)
            SideCueText = visual.TextStim(win=win, ori=0, name='CueText', text='Either Side',    font=u'Arial', pos=[0, -3], height=LargeTextSize, wrapWidth=30, color=happyTextCol, colorSpace=u'rgb', opacity=1, depth=-1.0)
        #Angry
        if trialsArray[curRow][2] == 1:
            ArrowImage = visual.ImageStim(win=win,image= angryArrowArray[2], pos= ARROWPOS, size=(ARROWSIZE,ARROWSIZE))
            arrowCol=angryArrowCol
            EmotionCueText = visual.TextStim(win=win, ori=0, name='CueText', text='Angry Emotion',    font=u'Arial', pos=[0, 3], height=LargeTextSize, wrapWidth=30, color=angryTextCol, colorSpace=u'rgb', opacity=1, depth=-1.0)
            SideCueText = visual.TextStim(win=win, ori=0, name='CueText', text='Either Side',    font=u'Arial', pos=[0, -3], height=LargeTextSize, wrapWidth=30, color=angryTextCol, colorSpace=u'rgb', opacity=1, depth=-1.0)

    fixationVertical.setAutoDraw(False)
    fixationHorizontal.setAutoDraw(False)
    EmotionCueText.setAutoDraw(True)
    SideCueText.setAutoDraw(True)
    ArrowImage.setAutoDraw(True)
    win.flip()
    
    while trialClock.getTime() < INTER_TRIAL_INTERVAL + CUEARROW_TIME: pass
    
    
    #Present Face Image
    #left side
    if trialsArray[curRow][3] == 0:
        #regular trial
        if trialsArray[curRow][5] == 0:
            FACEPOS = POSARRAY[0]
        #catch trial
        if trialsArray[curRow][5] == 1 or trialsArray[curRow][5] == 2:
            FACEPOS = POSARRAY[1]
    #right side
    if trialsArray[curRow][3] == 1:
        #regular trial
        if trialsArray[curRow][5] == 0:
            FACEPOS = POSARRAY[1]
        #catch trial
        if trialsArray[curRow][5] == 1 or trialsArray[curRow][5] == 2:
            FACEPOS = POSARRAY[0]
    
    
    #for both types of catch trials, picking a random number between 110 or 113 for the image that will be used.
    if trialsArray[curRow][5] == 1 or trialsArray[curRow][5] == 2:#then it is a catch trial
        trialsArray[curRow][4] = random.randint(110,113)
    
    #Happy
    if trialsArray[curRow][2] == 0:
        if trialsArray[curRow][5] == 0 or trialsArray[curRow][5] == 2:#regular trials or same emotion catch trials
            FaceImage = visual.ImageStim(win=win,image= u'Faces/Happy' + str(trialsArray[curRow][4]) + '.jpg', pos= FACEPOS, size=(FACEWIDTH,FACEHEIGHT))
            FaceStim = 'Happy' + str(trialsArray[curRow][4]) + '.jpg'
        if trialsArray[curRow][5] == 1:#opposite emotion catch trials
            FaceImage = visual.ImageStim(win=win,image= u'Faces/Angry' + str(trialsArray[curRow][4]) + '.jpg', pos= FACEPOS, size=(FACEWIDTH,FACEHEIGHT))
            FaceStim = 'Angry' + str(trialsArray[curRow][4]) + '.jpg'
    #Angry
    if trialsArray[curRow][2] == 1:
        if trialsArray[curRow][5] == 0 or trialsArray[curRow][5] == 2:#regular trials or same emotion catch trials
            FaceImage = visual.ImageStim(win=win,image= u'Faces/Angry' + str(trialsArray[curRow][4]) + '.jpg', pos= FACEPOS, size=(FACEWIDTH,FACEHEIGHT))
            FaceStim = 'Angry' + str(trialsArray[curRow][4]) + '.jpg'
        if trialsArray[curRow][5] == 1:#opposite emotion catch trials
            FaceImage = visual.ImageStim(win=win,image= u'Faces/Happy' + str(trialsArray[curRow][4]) + '.jpg', pos= FACEPOS, size=(FACEWIDTH,FACEHEIGHT))
            FaceStim = 'Happy' + str(trialsArray[curRow][4]) + '.jpg'



    #CORRECT RESPONSE FOR THIS TRIAL
    #Left Happy
    if trialsArray[curRow][2] == 0 and trialsArray[curRow][3] == 0:
        if buttonCounterbalance == 0 or buttonCounterbalance == 1:
            if trialsArray[curRow][5] == 0:correctKey = 's'
            if trialsArray[curRow][5] == 1:correctKey = 'k'#Right Angry
            if trialsArray[curRow][5] == 2:correctKey = 'l'#Right Happy
        if buttonCounterbalance == 2 or buttonCounterbalance == 3:
            if trialsArray[curRow][5] == 0:correctKey = 'd'
            if trialsArray[curRow][5] == 1:correctKey = 'l'#Right Angry
            if trialsArray[curRow][5] == 2:correctKey = 'k'#Right Happy
    #Left Angry
    if trialsArray[curRow][2] == 1 and trialsArray[curRow][3] == 0:
        if buttonCounterbalance == 0 or buttonCounterbalance == 1:
            if trialsArray[curRow][5] == 0:correctKey = 'd'
            if trialsArray[curRow][5] == 1:correctKey = 'l'#Right Happy
            if trialsArray[curRow][5] == 2:correctKey = 'k'#Right Angry
        if buttonCounterbalance == 2 or buttonCounterbalance == 3:
            if trialsArray[curRow][5] == 0:correctKey = 's'
            if trialsArray[curRow][5] == 1:correctKey = 'k'#Right Happy
            if trialsArray[curRow][5] == 2:correctKey = 'l'#Right Angry
    #Right Happy
    if trialsArray[curRow][2] == 0 and trialsArray[curRow][3] == 1:
        if buttonCounterbalance == 0 or buttonCounterbalance == 1:
            if trialsArray[curRow][5] == 0:correctKey = 'l'
            if trialsArray[curRow][5] == 1:correctKey = 'd'#Left Angry
            if trialsArray[curRow][5] == 2:correctKey = 's'#Left Happy
        if buttonCounterbalance == 2 or buttonCounterbalance == 3:
            if trialsArray[curRow][5] == 0:correctKey = 'k'
            if trialsArray[curRow][5] == 1:correctKey = 's'#Left Angry
            if trialsArray[curRow][5] == 2:correctKey = 'd'#Left Happy
    #Right Angry
    if trialsArray[curRow][2] == 1 and trialsArray[curRow][3] == 1:
        if buttonCounterbalance == 0 or buttonCounterbalance == 1:
            if trialsArray[curRow][5] == 0:correctKey = 'k'
            if trialsArray[curRow][5] == 1:correctKey = 's'#Left Happy
            if trialsArray[curRow][5] == 2:correctKey = 'd'#Left Angry
        if buttonCounterbalance == 2 or buttonCounterbalance == 3:
            if trialsArray[curRow][5] == 0:correctKey = 'l'
            if trialsArray[curRow][5] == 1:correctKey = 'd'#Left Happy
            if trialsArray[curRow][5] == 2:correctKey = 's'#Left Angry


    EmotionCueText.setAutoDraw(False)
    SideCueText.setAutoDraw(False)
    ArrowImage.setAutoDraw(False)
    win.flip()
    
    TIME_BETWEEN_CUE_AND_FACE_TASK = BLANKBETWEENCUEANDFACE[curRow]
    while trialClock.getTime() < INTER_TRIAL_INTERVAL + CUEARROW_TIME + TIME_BETWEEN_CUE_AND_FACE_TASK: pass
    
    FaceImage.setAutoDraw(True)
    win.flip()
    eventClock.reset()
    stimOnScreen = True
    keyResp.status = NOT_STARTED
    respErrorCode = -1
    respErrorName = ''
    noResponseYet = True
    keyResp.keys = []
    keyResp.rt = -1
    while trialClock.getTime() < INTER_TRIAL_INTERVAL + CUEARROW_TIME + TIME_BETWEEN_CUE_AND_FACE_TASK + FACE_ON_SCREEN + FACE_OFF_SCREEN:
        t = eventClock.getTime()
        #initialize key checker
        if keyResp.status == NOT_STARTED:
            keyResp.tStart = t
            keyResp.status = STARTED
            keyResp.clock.reset()
            #event.getKeys()
            event.clearEvents()
            
        #check for a keyboard response
        theseKeys = event.getKeys(keyList=['s','d','k','l'])
        if len(theseKeys) > 0: #test if atleast one key pressed
            keyResp.keys = theseKeys[-1] #just the last key pressed
            keyResp.rt = keyResp.clock.getTime()
            faceResponse = keyResp.keys
            faceResponseRT = keyResp.rt
            if noResponseYet:
                if correctKey == 's':
                    if keyResp.keys == 'd' or keyResp.keys == 'k' or keyResp.keys == 'l':
                        respErrorCode = 2;respErrorName = 'incorrect response'
                if correctKey == 'd':
                    if keyResp.keys == 's' or keyResp.keys == 'k' or keyResp.keys == 'l':
                        respErrorCode = 2;respErrorName = 'incorrect response'
                if correctKey == 'k':
                    if keyResp.keys == 's' or keyResp.keys == 'd' or keyResp.keys == 'l':
                        respErrorCode = 2;respErrorName = 'incorrect response'
                if correctKey == 'l':
                    if keyResp.keys == 's' or keyResp.keys == 'd' or keyResp.keys == 'k':
                        respErrorCode = 2;respErrorName = 'incorrect response'
                noResponseYet = False
            else:
                if correctKey == 's':
                    if keyResp.keys == 'd' or keyResp.keys == 'k' or keyResp.keys == 'l':
                        respErrorCode = 2;respErrorName = 'incorrect response'
                if correctKey == 'd':
                    if keyResp.keys == 's' or keyResp.keys == 'k' or keyResp.keys == 'l':
                        respErrorCode = 2;respErrorName = 'incorrect response'
                if correctKey == 'k':
                    if keyResp.keys == 's' or keyResp.keys == 'd' or keyResp.keys == 'l':
                        respErrorCode = 2;respErrorName = 'incorrect response'
                if correctKey == 'l':
                    if keyResp.keys == 's' or keyResp.keys == 'd' or keyResp.keys == 'k':
                        respErrorCode = 2;respErrorName = 'incorrect response'
                if respErrorCode != -1:
                    respErrorCode = 1
                    respErrorName = 'multi-response'
        
        
        
        if stimOnScreen and t > FACE_ON_SCREEN:
            FaceImage.setAutoDraw(False)
            win.flip()
            stimOnScreen = False
        
        
        # check for quit (the [Esc] key)
        if event.getKeys(["escape"]):
            core.quit()
            

    
    if noResponseYet:
       faceResponse = 'no response'
       faceResponseRT = 'no response'
       respErrorCode = 5
       respErrorName = 'no response'
       noResponseYet = False
        

    #Feedback Screen
    if respErrorCode == -1:
        feedbackText = visual.TextStim(win=win, ori=0, name='feedbackText', text='Correct',    font=u'Arial', pos=[0, 2], height=LargeTextSize, wrapWidth=15, color='lightgreen', colorSpace=u'rgb', opacity=1, depth=-1.0)
    elif respErrorCode == 2:
        feedbackText = visual.TextStim(win=win, ori=0, name='feedbackText', text='Incorrect',    font=u'Arial', pos=[0, 2], height=LargeTextSize, wrapWidth=15, color='darkred', colorSpace=u'rgb', opacity=1, depth=-1.0)
    elif respErrorCode == 5:
        feedbackText = visual.TextStim(win=win, ori=0, name='feedbackText', text='No Response',    font=u'Arial', pos=[0, 2], height=LargeTextSize, wrapWidth=15, color='darkred', colorSpace=u'rgb', opacity=1, depth=-1.0)
    elif respErrorCode == 1:
        feedbackText = visual.TextStim(win=win, ori=0, name='feedbackText', text='Multiple Responses',    font=u'Arial', pos=[0, 2], height=LargeTextSize, wrapWidth=15, color='darkred', colorSpace=u'rgb', opacity=1, depth=-1.0)
    if keyResp.rt > 1:
        feedbackText = visual.TextStim(win=win, ori=0, name='feedbackText', text='Late Response',    font=u'Arial', pos=[0, 2], height=LargeTextSize, wrapWidth=15, color='darkred', colorSpace=u'rgb', opacity=1, depth=-1.0)
        lateTrialCount = lateTrialCount + 1
    feedbackText.setAutoDraw(True);
    fixationVertical.setAutoDraw(True)
    fixationHorizontal.setAutoDraw(True)
    win.flip();

    while trialClock.getTime() < INTER_TRIAL_INTERVAL + CUEARROW_TIME + TIME_BETWEEN_CUE_AND_FACE_TASK + FACE_ON_SCREEN + FACE_OFF_SCREEN + FEEDBACK_TIME:pass
    feedbackText.setAutoDraw(False)
    
    
    trialNum = trialNum + 1
    blocktrial = blocktrial + 1
    trialCount = trialCount + 1
    
    
    outStr = str(subjectNumber)+ '\t'
    outStr = outStr + str(expInfo2['age']) + '\t'
    outStr = outStr + str(expInfo3['gender']) + '\t'
    outStr = outStr + str(expInfo4['handedness']) + '\t'
    outStr = outStr + str(expInfo5['race']) + '\t'
    outStr = outStr + str(expInfo6['glasses/contacts?']) + '\t'
    outStr = outStr + str(runTime) + '\t'
    outStr = outStr + str(TrialType) + '\t'
    outStr = outStr + str(trialNum) + '\t'
    outStr = outStr + str(trialsArray[curRow][1]) + '\t'
    outStr = outStr + str(trialsArray[curRow][3]) + '\t'
    outStr = outStr + str(trialsArray[curRow][2]) + '\t'
    outStr = outStr + str(arrowCol) + '\t'
    outStr = outStr + str(FaceStim) + '\t'
    outStr = outStr + str(FACEPOS) + '\t'
    outStr = outStr + correctKey + '\t'
    outStr = outStr + str(faceResponse) + '\t'
    outStr = outStr + str(faceResponseRT) + '\t'
    outStr = outStr + str(respErrorCode) + '\t'
    outStr = outStr + respErrorName + '\t'
    outStr = outStr + str(trialsArray[curRow][5]) + '\t'
    outStr = outStr + str(TIME_BETWEEN_CUE_AND_FACE_TASK) + '\t'
    outputFile.write(outStr + 'eol\n')
                
    
    if respErrorCode == -1:
        correctTrialCount = correctTrialCount + 1
        blockACC=blockACC + 1
        blockRT=blockRT + faceResponseRT
                
    
    #BREAK SCRIPT
    if trialNum<900:
        if blocktrial == 117:
            blockACCValue=blockACC*100
            blockACCValue=blockACCValue/blocktrial

            breakTextOnScreen = visual.TextStim(win=win, ori=0, name='breakTextOnScreen', text='Take a Break\n\nRemember to maintain focus on the arrow while it is on the screen.\n\nPress the space bar to start the next block...',    font=u'Arial', pos=[0, 5], height=SmallTextSize, wrapWidth=None, color='black', colorSpace=u'rgb', opacity=1, depth=-1.0)
            if blockACCValue < 80:
                TooInaccurateTextOnScreen = visual.TextStim(win=win, ori=0, name='TooInaccurateTextOnScreen', text='Respond more accurately.',    font=u'Arial', pos=[0, -3], height=SmallTextSize, wrapWidth=30, color='darkred', colorSpace=u'rgb', opacity=1, depth=-1.0)
            if lateTrialCount > 11:
                TooSlowTextOnScreen = visual.TextStim(win=win, ori=0, name='TooSlowTextOnScreen', text='Respond more quickly.',    font=u'Arial', pos=[0, -4.5], height=SmallTextSize, wrapWidth=30, color='darkred', colorSpace=u'rgb', opacity=1, depth=-1.0)

            if trialNum == 234 or trialNum == 468 or trialNum == 702:
                if trialNum == 234:
                    percDone = 25
                if trialNum == 468:
                    percDone = 50
                if trialNum == 702:
                    percDone = 75
                percentDone = visual.TextStim(win=win, ori=0, name='percentDone', text='You have completed ' + str(percDone) + '% of the experiment.',    font=u'Arial', pos=[0, -8], height=SmallTextSize, wrapWidth=None, color='black', colorSpace=u'rgb', opacity=1, depth=-1.0)
                percentDone.setAutoDraw(True)
            breakTextOnScreen.setAutoDraw(True)
            if blockACCValue < 80:
                TooInaccurateTextOnScreen.setAutoDraw(True)
            if lateTrialCount > 11:
                TooSlowTextOnScreen.setAutoDraw(True)
            win.flip()
            event.waitKeys()

            if trialNum == 234 or trialNum == 468 or trialNum == 702:
                percentDone.setAutoDraw(False)
            breakTextOnScreen.setAutoDraw(False)
            if blockACCValue < 80:
                TooInaccurateTextOnScreen.setAutoDraw(False)
            if lateTrialCount > 11:
                TooSlowTextOnScreen.setAutoDraw(False)
            blocktrial = 0
            blockRT = 0
            blockACC = 0
            lateTrialCount = 0
            win.flip()


