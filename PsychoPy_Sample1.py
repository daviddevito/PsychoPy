from psychopy import visual, core, data, event, logging, gui, misc, monitors
import numpy as np  # whole numpy lib is available, prepend 'np.'
import os  # handy system and path functions
from psychopy.constants import *  # things like STARTED, FINISHED
import random
import math
#import win32api
#import Image
import ctypes
import time
import pylab

random.seed() #initialize random number generator

#global variables
NUM_SEARCH_POS = 8
NUM_TARGET_POS = 8
NUM_STIMULUS_POS = 4
ISI = 1.0 #duration of time separating trials
ISA = 0.2 #time between search arrays
TEXT_HEIGHT = 0.75
TEXT_WRAPPING = 30

tCol = [.0,.0,.0] #text and cue colour

STIM_TIME = 0.5
FIXATION_TIME = 0.15
FIRST_CUE_TIME = 0.2
SECOND_CUE_TIME = 0.2
FIRST_RETENTION_INTERVAL = 0.8
SECOND_RETENTION_INTERVAL = 0.8
THIRD_RETENTION_INTERVAL = 0.8
FOURTH_RETENTION_INTERVAL = 0.8
FIFTH_RETENTION_INTERVAL = 0.8
FIRST_PROBE_ON_SCREEN = 1.0
FIRST_PROBE_OFF_SCREEN = 1.0
SECOND_PROBE_ON_SCREEN = 1.0
SECOND_PROBE_OFF_SCREEN = 1.0
EVAL_FIXATION_TIME = 0.15
MEMORY_TEXT_TIME = 0.4
REMEMBER_TEXT_TIME = 0.4
EVAL_TEXT_TIME = 0.4
EVAL_STIM_ON_SCREEN = 1.0
EVAL_STIM_OFF_SCREEN = 1.0
INTER_TRIAL_INTERVAL = 0.5
FEEDBACK_TIME = 0.15
SEARCH_ARRAY_TIME = 6.0
EVAL_BEFORE_RETRO_BLANK = FIRST_CUE_TIME + SECOND_RETENTION_INTERVAL
EVAL_AFTER_RETRO_BLANK = SECOND_RETENTION_INTERVAL + FIRST_CUE_TIME + FIXATION_TIME

bCol = [1,1,1] #background colour
sCol=[0.35,0.35,0.35] #search stim colour
tCol = [.0,.0,.0] #text and cue colour
TOTAL_DEGREES = 360
SEARCH_ECCEN = 3.66 #width of search array
idxSearchPos = range(0, NUM_SEARCH_POS)

#DEBUGGING/TESTING TIMING
#STIM_TIME = 0.05
#RETENTION_INTERVAL = 0.05
#FIXATION_TIME = 0.05
#FIRST_CUE_TIME = 0.05
#SECOND_CUE_TIME = 0.05
#FIRST_RETENTION_INTERVAL = 0.05
#SECOND_RETENTION_INTERVAL = 0.05
#THIRD_RETENTION_INTERVAL = 0.05
#FOURTH_RETENTION_INTERVAL = 0.05
#FIFTH_RETENTION_INTERVAL = 0.05
#FIRST_PROBE_ON_SCREEN = 0.05
#FIRST_PROBE_OFF_SCREEN = 0.05
#SECOND_PROBE_ON_SCREEN = 0.05
#SECOND_PROBE_OFF_SCREEN = 0.05
#EVAL_FIXATION_TIME = 0.05
#MEMORY_TEXT_TIME = 0.05
#EVAL_TEXT_TIME = 0.05
#EVAL_STIM_ON_SCREEN = 0.05
#EVAL_STIM_OFF_SCREEN = 0.05
#INTER_TRIAL_INTERVAL = 0.05


#Array of Positions of stimuli in each array, randomized before each array is presented
POSARRAY = [[-3,-3],[-3,3],[3,3],[3,-3]]

SIZE = 2
NUM_REPS = 2
NUM_SEARCH_REPS = 6
NUM_STIMULI = 480


#Get subject number
expName = 'ActAccess_Halves_SearchTask_Mar2017'
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
    expInfo5 = {'glasses/contacts?':''}
    dlg = gui.DlgFromDict(dictionary=expInfo5, title=expName)
    if dlg.OK == False: core.quit()  # user pressed cancel so exit experiment
    else:
        break
        
        
        
outputFile = open(fileName, 'w')

subjectNumber = expInfo['subjNum']
buttonCounterbalance = int(subjectNumber)%(2)

if buttonCounterbalance == 0:
    butVar1 = 'Circle'
    butVar2 = 'Square'
if buttonCounterbalance == 1:
    butVar1 = 'Square'
    butVar2 = 'Circle'

#buttonCounterbalance = 0: up same, down different, buttonCounterbalance = 1: up different, down same
#up circle button
#down square button


#Column headers for output file
outStr = "Time\tTrialNum\tTrialType\tBlueStim\tBluePos\tGreenStim\tGreenPos\tPurpleStim\tPurplePos\tPinkStim\tPinkPos\tOrangeStim\tOrangePos\tFirstCuedSide(0=Left,1=Right)\tFirstCuedPos\tSecondCuedPos\tFirstProbeStim\tFirstProbeSameorDifferent(0=Same,1=Different)\tFirstProbeResp\tFirstProbeACC\tFirstProbeRT\tFirstProbeErrorCode\tFirstProbeErrorName\tSecondProbeStim\tSecondProbeSameorDifferent(0=Same,1=Different)\tSecondProbeResp\tSecondProbeACC\tSecondProbeRT\tSecondProbeErrorCode\tSecondProbeErrorName\tEvaluatedStim\tEvalStimType(0=NeverCuedSecondCuedSide,1=FirstCuedStim)\tEvalResp\tEvalRT\tEvalErrorCode\tEvalErrorName\tArrayPresTime\tWhenEvalHappens(0=BeforeRetroCue,1=AfterRetroCue,2=SearchTask)\tSingletonType(0=FirstCuedStimColour,1=NeverCuedSecondCuedSideColour,2=NovelColour)\tSingletonColour\tSingletonPosition\tSingletonOrientation\tTargetOrientation\tTargetPosition\tSearchResp\tSearchRT\tSearchErrorCode\tSearchErrorName\tPart(0=Practice,1=NoSearch,2=Search)\tAge\tGender\tHandedness\tGlassesOrContacts\t"
outputFile.write(outStr + "eol\n")

# Setup the Psycho variables (screen, stimuli, sounds, ect)
win = visual.Window(fullscr=True, screen=0, allowGUI=False, allowStencil=False, monitor='FenskeLabTestingComps', color='white', colorSpace='rgb', units='deg')
mon = monitors.Monitor('FenskeLabTestingComps')
trialClock = core.Clock()
eventClock = core.Clock()
evalClock = core.Clock()
isiClock = core.Clock()
keyResp = event.BuilderKeyResponse()  # create an object of type KeyResponse

#creating the fixation cross
fixationVertical = visual.Line(win,start=(0,-0.3), end=(0,0.3), lineColor = u'black',lineWidth=3.0)
fixationHorizontal = visual.Line(win,start=(-0.3,0), end=(0.3,0), lineColor = u'black',lineWidth=3.0)

#create search stim (landolt c's) #literally drawing a landolt c
def GetVertices():
    #vertices = [[-1,.5],[-1,1],[0,1],[1,1],[1,0],[1,-1],[0,-1],[-1,-1][-1,-.5]]
    SEARCH_TARG_SIZE = 0.44 #size of landolt c's
    vertices = [[-SEARCH_TARG_SIZE,SEARCH_TARG_SIZE/2.0],[-SEARCH_TARG_SIZE,SEARCH_TARG_SIZE],[SEARCH_TARG_SIZE,SEARCH_TARG_SIZE],[SEARCH_TARG_SIZE,-SEARCH_TARG_SIZE],[-SEARCH_TARG_SIZE,-SEARCH_TARG_SIZE],[-SEARCH_TARG_SIZE,-SEARCH_TARG_SIZE/2.0]]
    return vertices

trialsArray=[]
trial=0
for rep in range(0, NUM_REPS):
    for firstCuedSide in range (0,2):#0=Left, 1=Right
        for firstCuedStim in range (0,2):#0=Top, 1=Bottom
            for secondCuedStim in range (0,2):#0=Diagonal from FirstCued, 1=Horizontal from FirstCued
                for whichEvaluated in range (0,2):#0=NeverCuedStimSecondCuedSide, 1=FirstCuedStim
                    for whenEvaluate in range (0,2):#0=BeforeRetroCue, 1=AfterRetroCue
                        trialsArray.append([trial,firstCuedSide,firstCuedStim,secondCuedStim,whichEvaluated,whenEvaluate,5])
                        trial = trial+1

trialsArray2=[]
trial=0
for rep in range(0, NUM_REPS):
    for firstCuedSide in range (0,2):#0=Left, 1=Right
        for firstCuedStim in range (0,2):#0=Top, 1=Bottom
            for secondCuedStim in range (0,2):#0=Diagonal from FirstCued, 1=Horizontal from FirstCued
                for whichEvaluated in range (0,2):#0=NeverCuedStimSecondCuedSide, 1=FirstCuedStim
                    for whenEvaluate in range (0,2):#0=BeforeRetroCue, 1=AfterRetroCue
                        trialsArray2.append([trial,firstCuedSide,firstCuedStim,secondCuedStim,whichEvaluated,whenEvaluate,5])
                        trial = trial+1
                        

for rep in range(0, NUM_SEARCH_REPS):
    for firstCuedSide in range (0,2):#0=Left, 1=Right
        for firstCuedStim in range (0,2):#0=Top, 1=Bottom
            for singletonType in range (0,3):#0=activematching,1=accessorymatching,2=novelcolour
                trialsArray2.append([trial,firstCuedSide,firstCuedStim,5,5,2,singletonType])
                trial = trial+1


#create arbitrary column that is shuffled to randomize trialsArray
idxTrialsArray = range(0, len(trialsArray)); random.shuffle(idxTrialsArray)
idxTrialsArray2 = range(0, len(trialsArray2)); random.shuffle(idxTrialsArray2)

idxBlueStim = range(0,NUM_STIMULI); random.shuffle(idxBlueStim)
idxGreenStim = range(0,NUM_STIMULI); random.shuffle(idxGreenStim)
idxPurpleStim = range(0,NUM_STIMULI); random.shuffle(idxPurpleStim)
idxPinkStim = range(0,NUM_STIMULI); random.shuffle(idxPinkStim)
idxOrangeStim = range(0,NUM_STIMULI); random.shuffle(idxOrangeStim)

BlueStimCount = -1
GreenStimCount = -1
PurpleStimCount = -1
PinkStimCount = -1
OrangeStimCount = -1
blocktrial = 0
totalTrials = 0
pracTrialCount = 0
TrialType = "Practice"

colourArray = ['Blue','Green','Purple','Pink','Orange']
arrowArray = ['Arrows/BottomLeft.png','Arrows/TopLeft.png','Arrows/TopRight.png','Arrows/BottomRight.png']

#INSTRUCTIONS

Instruct1 = visual.ImageStim(win=win,image= 'Slide01.jpg', pos= [0,0], size=(36,23))
Instruct1.setAutoDraw(True)
win.flip()
event.waitKeys()
Instruct1.setAutoDraw(False)
Instruct1 = visual.ImageStim(win=win,image= 'Slide02.jpg', pos= [0,0], size=(36,23))
Instruct1.setAutoDraw(True)
win.flip()
event.waitKeys()
Instruct1.setAutoDraw(False)
Instruct1 = visual.ImageStim(win=win,image= 'Slide03.jpg', pos= [0,0], size=(36,23))
Instruct1.setAutoDraw(True)
win.flip()
event.waitKeys()
Instruct1.setAutoDraw(False)
Instruct1 = visual.ImageStim(win=win,image= 'Slide04.jpg', pos= [0,0], size=(36,23))
Instruct1.setAutoDraw(True)
win.flip()
event.waitKeys()
Instruct1.setAutoDraw(False)
if buttonCounterbalance == 0:
    Instruct1 = visual.ImageStim(win=win,image= 'Slide05.jpg', pos= [0,0], size=(36,23))
if buttonCounterbalance == 1:
    Instruct1 = visual.ImageStim(win=win,image= 'Slide06.jpg', pos= [0,0], size=(36,23))
Instruct1.setAutoDraw(True)
win.flip()
event.waitKeys()
Instruct1.setAutoDraw(False)
if buttonCounterbalance == 0:
    Instruct1 = visual.ImageStim(win=win,image= 'Slide07.jpg', pos= [0,0], size=(36,23))
if buttonCounterbalance == 1:
    Instruct1 = visual.ImageStim(win=win,image= 'Slide08.jpg', pos= [0,0], size=(36,23))
Instruct1.setAutoDraw(True)
win.flip()
event.waitKeys()
Instruct1.setAutoDraw(False)
Instruct1 = visual.ImageStim(win=win,image= 'Slide09.jpg', pos= [0,0], size=(36,23))
Instruct1.setAutoDraw(True)
win.flip()
event.waitKeys()
Instruct1.setAutoDraw(False)
Instruct1 = visual.ImageStim(win=win,image= 'Slide10.jpg', pos= [0,0], size=(36,23))
Instruct1.setAutoDraw(True)
win.flip()
event.waitKeys()
Instruct1.setAutoDraw(False)
if buttonCounterbalance == 0:
    Instruct1 = visual.ImageStim(win=win,image= 'Slide11.jpg', pos= [0,0], size=(36,23))
if buttonCounterbalance == 1:
    Instruct1 = visual.ImageStim(win=win,image= 'Slide12.jpg', pos= [0,0], size=(36,23))
Instruct1.setAutoDraw(True)
win.flip()
event.waitKeys()
Instruct1.setAutoDraw(False)
win.flip()
if buttonCounterbalance == 0:
    Instruct1 = visual.ImageStim(win=win,image= 'Slide20.jpg', pos= [0,0], size=(36,23))
if buttonCounterbalance == 1:
    Instruct1 = visual.ImageStim(win=win,image= 'Slide21.jpg', pos= [0,0], size=(36,23))
Instruct1.setAutoDraw(True)
win.flip()
event.waitKeys()
Instruct1.setAutoDraw(False)
win.flip()


core.wait(2.0)


lastFourTrialsArray = [0,0,0,0]
previousTrial = 0
twoTrialsAgo = 0
threeTrialsAgo = 0
fourTrialsAgo = 0

ratingScaleText = visual.TextStim(win=win, ori=0, name='ratingScaleText', text='1  -  2  -  3  -  4',    font=u'Arial', pos=[0, -5], height=0.75, wrapWidth=None, color='black', colorSpace=u'rgb', opacity=1, depth=-1.0)


#Practice Trials
for ptrial in range(0, 20):
    pracTrialCount = pracTrialCount + 1

    random.shuffle(colourArray)
    
    runTime = time.strftime("%c")
    
    
    #put memory task text on screen
    memTextOnScreen = visual.TextStim(win=win, ori=0, name='memTextOnScreen', text='Memorize',    font=u'Arial', pos=[0, 0], height=0.75, wrapWidth=None, color='black', colorSpace=u'rgb', opacity=1, depth=-1.0)
    memTextOnScreen.setAutoDraw(True)
    win.flip()
    trialClock.reset()
    while trialClock.getTime() < MEMORY_TEXT_TIME:pass
    
    #Fixation Cross
    memTextOnScreen.setAutoDraw(False)
    fixationVertical.setAutoDraw(True);fixationHorizontal.setAutoDraw(True)
    win.flip()
    while trialClock.getTime() < FIXATION_TIME + MEMORY_TEXT_TIME: pass
    
    #Decide Positions of Each Color
    FirstColour = colourArray[0]
    SecondColour = colourArray[1]
    ThirdColour = colourArray[2]
    FourthColour = colourArray[3]
    FirstPos = POSARRAY[0]
    SecondPos = POSARRAY[1]
    ThirdPos = POSARRAY[2]
    FourthPos = POSARRAY[3]
    
    #Create Stimuli
    FirstItem = visual.ImageStim(win=win,image= 'Images/' + colourArray[0] + '/' + colourArray[0] + '498.bmp', pos= FirstPos, size=(SIZE,SIZE))
    SecondItem = visual.ImageStim(win=win,image= 'Images/' + colourArray[1] + '/' + colourArray[1] + '498.bmp', pos= SecondPos, size=(SIZE,SIZE))
    ThirdItem = visual.ImageStim(win=win,image= 'Images/' + colourArray[2] + '/' + colourArray[2] + '498.bmp', pos= ThirdPos, size=(SIZE,SIZE))
    FourthItem = visual.ImageStim(win=win,image= 'Images/' + colourArray[3] + '/' + colourArray[3] + '498.bmp', pos= FourthPos, size=(SIZE,SIZE))
    
    #Put Stimulus Array on Screen
    FirstItem.setAutoDraw(True);SecondItem.setAutoDraw(True);ThirdItem.setAutoDraw(True);FourthItem.setAutoDraw(True)
    win.flip()
    while trialClock.getTime() < STIM_TIME + FIXATION_TIME + MEMORY_TEXT_TIME: pass
    
    #Take Stimulus Array off Screen
    FirstItem.setAutoDraw(False);SecondItem.setAutoDraw(False);ThirdItem.setAutoDraw(False);FourthItem.setAutoDraw(False)
    win.flip()
    while trialClock.getTime() < FIRST_RETENTION_INTERVAL + STIM_TIME + FIXATION_TIME + MEMORY_TEXT_TIME: pass

    #decide where first cue points and create first cue
    firstPracCuePos = random.randint(0,3)
    firstCueArrow = visual.ImageStim(win=win,image= arrowArray[firstPracCuePos], pos= [0,0], size=(1,1))
        
    #decide where second cue points and create second cue
    secondPracCuePos = random.randint(0,1)
    if firstPracCuePos == 0 or firstPracCuePos == 1:#First cue pointed to left side of screen
        secondPracCuePos = secondPracCuePos + 2
        secondCueArrow = visual.ImageStim(win=win,image= arrowArray[secondPracCuePos], pos= [0,0], size=(1,1))
    if firstPracCuePos == 2 or firstPracCuePos == 3:#First cue point to right side of screen
        secondCueArrow = visual.ImageStim(win=win,image= arrowArray[secondPracCuePos], pos= [0,0], size=(1,1))
        
    #Find out position of evaluated stimulus
    pracWhichEval = random.randint(0,1)#0=NeverCuedStimSecondCuedSide, 1=FirstCuedStim
    if pracWhichEval == 0:#NeverCuedStimSeconCuedSide
        if secondPracCuePos == 0:pracEvalPos = POSARRAY[1]
        if secondPracCuePos == 1:pracEvalPos = POSARRAY[0]
        if secondPracCuePos == 2:pracEvalPos = POSARRAY[3]
        if secondPracCuePos == 3:pracEvalPos = POSARRAY[2]
    if pracWhichEval == 1: #FirstCuedStim
        pracEvalPos = POSARRAY[firstPracCuePos]
        

    #Determine which actual stimulus will be evaluated
    if pracEvalPos == FirstPos:pracEvalImgName = 'Images/' + colourArray[0] + '/' + colourArray[0] + '498.bmp'
    if pracEvalPos == SecondPos:pracEvalImgName = 'Images/' + colourArray[1] + '/' + colourArray[1] + '498.bmp'
    if pracEvalPos == ThirdPos:pracEvalImgName = 'Images/' + colourArray[2] + '/' + colourArray[2] + '498.bmp'
    if pracEvalPos == FourthPos:pracEvalImgName = 'Images/' + colourArray[3] + '/' + colourArray[3] + '498.bmp'


    whenEvalHappens = random.randint(0,1)#0=BeforeRetroCue,1=AfterRetroCue, - No search task practice 2=SearchTask
    if whenEvalHappens == 0:#Evaluate before RetroCue
        while trialClock.getTime() < EVAL_BEFORE_RETRO_BLANK + FIRST_RETENTION_INTERVAL + STIM_TIME + FIXATION_TIME + MEMORY_TEXT_TIME: pass
    if whenEvalHappens == 1 or whenEvalHappens == 2:#Evaluate After RetroCue or SearchTask
        #First cue arrow on screen
        firstCueArrow.setAutoDraw(True)
        #Take fixation cross off screen
        fixationVertical.setAutoDraw(False);fixationHorizontal.setAutoDraw(False)
        win.flip()
        while trialClock.getTime() < FIRST_CUE_TIME + FIRST_RETENTION_INTERVAL + STIM_TIME + FIXATION_TIME + MEMORY_TEXT_TIME: pass
    
        #Fixation on Screen
        fixationVertical.setAutoDraw(True);fixationHorizontal.setAutoDraw(True)
        #Take off first cue arrow
        firstCueArrow.setAutoDraw(False)
        win.flip()
        while trialClock.getTime() < SECOND_RETENTION_INTERVAL + FIRST_CUE_TIME + FIRST_RETENTION_INTERVAL + STIM_TIME + FIXATION_TIME + MEMORY_TEXT_TIME: pass
    if whenEvalHappens == 2:#Search Task
        #determine singleton type
        singType = random.randint(0,2)#0=activematching,1=accessorymatching,2=novelcolour
        #setup target locations in a circle around fixation
        targetPositions = []
        for pos in range(0, NUM_TARGET_POS):#8 target positions
            angle = math.radians(360 / NUM_TARGET_POS * pos)
            targetPositions.append([math.cos(angle)*SEARCH_ECCEN, math.sin(angle)*SEARCH_ECCEN])#setup target locations in a circle around fixation

        #set stimulus properties
        distractorOris = [0, 180] #orientations for the landolt c stimuli #gap pointing left or right for all distractors.
        idxDistractorOris = range(len(distractorOris))
        targetOris = [90,270]
        idxTargetOris = range(len(targetOris))

        #setup search stim
        searchStim = [] #create a list of 8 distractor stim to be used on each trial -- these stim are all leftOpen so later on we will randomly assign them an orientation (90 or 180) so they become top/bottom open
        for distractor in range (0, NUM_SEARCH_POS):
            distractor = visual.ShapeStim(win, lineColorSpace='rgb', fillColorSpace = 'rgb', fillColor=bCol, lineColor=sCol, vertices=GetVertices(), closeShape=False, lineWidth = 9)
            searchStim.append(distractor)

        #set colour of singleton based on condition
        if singType == 0:#activematching
            singCol = colourArray[firstPracCuePos]
        elif singType == 1:#accessorymatching
            if secondPracCuePos == 0:
                singCol = colourArray[1]
            if secondPracCuePos == 1:
                singCol = colourArray[0]
            if secondPracCuePos == 2:
                singCol = colourArray[3]
            if secondPracCuePos == 3:
                singCol = colourArray[2]
        else:#novelmatching
            singCol = colourArray[4]
            
        if singCol == 'Blue':
            singColName = 'Blue'
            singCol = [-.875,-.827,.639]
        if singCol == 'Green':
            singColName = 'Green'
            singCol = [-.671,.129,-.537]
        if singCol == 'Purple':
            singColName = 'Purple'
            singCol = [.545,-.576,.78]
        #if singCol == 'Yellow':
        #    singCol = [.843,.835,-.522]
        if singCol == 'Orange':
            singColName = 'Orange'
            singCol = [.435,-.255,-.741]
        if singCol == 'Pink':
            singColName = 'Pink'
            singCol = [.89,.231,.757]
        #if singCol == 'Red':
        #    singCol = [.075,-.757,-.725]
        
        random.shuffle(idxSearchPos) #randomly shuffle the list of positions in the search array

        #Search display #create 8 distractors
        for item in range (0, NUM_TARGET_POS):
            random.shuffle(idxDistractorOris)
            searchStim[item].ori=distractorOris[idxDistractorOris[0]]
            searchStim[item].pos = targetPositions[idxSearchPos[item]]
            searchStim[item].setAutoDraw(True)
            
        tarPos = searchStim[0].pos
        singPos = searchStim[1].pos

        #here you're changing one of the previously created distractors to be the target. So first item in SearchStim list is being changed to have targetOrientation.
        random.shuffle(idxTargetOris)
        targetPos = 0
        targetOri = targetOris[idxTargetOris[0]]
        searchStim[targetPos].ori=targetOri
        searchStim[targetPos].setAutoDraw(True)

        #here you're changing one of the previously created distractors to be the singleton. So second item in SearchStim list is being changed to singletoncolour.
        singletonPos = 1
#        if searchCond == 4:
        searchStim[singletonPos].setLineColor(singCol)
#        else:
#            searchStim[singletonPos].setLineColor('blue')
        searchStim[singletonPos].setAutoDraw(True)

        #put the whole search task on the screen including target, singleton, and 6 neutral distractors
        win.flip()
            
            
        #SEARCH TASK: wait for response
        #io.clearEvents('all')
        eventClock.reset()
        keyResp.status = NOT_STARTED
        searchErrorCode = -1
        searchErrorName = ''
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
                
                
            #check for a keyboard response
            theseKeys = event.getKeys(keyList=['up','down'])
            if len(theseKeys) > 0: #test if atleast one key pressed
                if keyResp.keys == []:
                    keyResp.keys = theseKeys[-1] #just the last key pressed
                    keyResp.rt = keyResp.clock.getTime()
                    searchResponse = keyResp.keys
                    searchRT = keyResp.rt
                    noResponseYet = False
                    if (targetOri != 90 and keyResp.keys=='up') or (targetOri != 270 and keyResp.keys=='down'):
                        searchErrorCode = 2
                        searchErrorName = "Incorrect response"
            
            
            
            # check for quit (the [Esc] key)
            if event.getKeys(["escape"]):
                core.quit()

        #Search delay
        for item in range (0, NUM_TARGET_POS):
            searchStim[item].setAutoDraw(False)
        win.flip()


    else:
        
        #Evaluation Task
        fixationVertical.setAutoDraw(False); fixationHorizontal.setAutoDraw(False)
        evalTextOnScreen = visual.TextStim(win=win, ori=0, name='evalTextOnScreen', text='Evaluate',    font=u'Arial', pos=[0, 0], height=0.75, wrapWidth=None, color='black', colorSpace=u'rgb', opacity=1, depth=-1.0)
        evalTextOnScreen.setAutoDraw(True)
        win.flip()
        if whenEvalHappens == 0:
            while trialClock.getTime() < EVAL_TEXT_TIME + EVAL_BEFORE_RETRO_BLANK + FIRST_RETENTION_INTERVAL + STIM_TIME + FIXATION_TIME + MEMORY_TEXT_TIME: pass
        if whenEvalHappens == 1:
            while trialClock.getTime() < EVAL_TEXT_TIME + SECOND_RETENTION_INTERVAL + FIRST_CUE_TIME + FIRST_RETENTION_INTERVAL + STIM_TIME + FIXATION_TIME + MEMORY_TEXT_TIME:pass
        evalTextOnScreen.setAutoDraw(False)
        
        

        ratingScaleText.setAutoDraw(True)

        win.flip()
        if whenEvalHappens == 0:
            while trialClock.getTime() < EVAL_FIXATION_TIME + EVAL_TEXT_TIME + EVAL_BEFORE_RETRO_BLANK + FIRST_RETENTION_INTERVAL + STIM_TIME + FIXATION_TIME + MEMORY_TEXT_TIME: pass
        if whenEvalHappens == 1:
            while trialClock.getTime() < EVAL_FIXATION_TIME + EVAL_TEXT_TIME + SECOND_RETENTION_INTERVAL + FIRST_CUE_TIME + FIRST_RETENTION_INTERVAL + STIM_TIME + FIXATION_TIME + MEMORY_TEXT_TIME:pass
        #Create evaluated stimulus
        evaluatedstimulus = visual.ImageStim(win=win,image = pracEvalImgName, pos=[0,0], size=(SIZE,SIZE))
        evaluatedstimulus.setAutoDraw(True)
        win.flip()
        

        eventClock.reset()
        stimOnScreen = True
        keyResp.status = NOT_STARTED
        evalErrorCode = -1
        evalErrorName = ''
        noResponseYet = True
        probeOnScreen = True
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
                
                
            #check for a keyboard response
            theseKeys = event.getKeys(keyList=['1','2','3','4'])
            if len(theseKeys) > 0: #test if atleast one key pressed
                if keyResp.keys == []:
                    keyResp.keys = theseKeys[-1] #just the last key pressed
                    keyResp.rt = keyResp.clock.getTime()
                    evalResponse = keyResp.keys
                    evalRT = keyResp.rt
                    noResponseYet = False
            
            if stimOnScreen and t > EVAL_STIM_ON_SCREEN:
                evaluatedstimulus.setAutoDraw(False)
                win.flip()
                stimOnScreen = False
            
            
            # check for quit (the [Esc] key)
            if event.getKeys(["escape"]):
                core.quit()

        
        
        fixationVertical.setAutoDraw(True);fixationHorizontal.setAutoDraw(True)
        evaluatedstimulus.setAutoDraw(False)
        ratingScaleText.setAutoDraw(False)
        win.flip()
        if whenEvalHappens == 0:
            while trialClock.getTime() < FIXATION_TIME + evalRT + EVAL_FIXATION_TIME + EVAL_TEXT_TIME + EVAL_BEFORE_RETRO_BLANK + FIRST_RETENTION_INTERVAL + STIM_TIME + FIXATION_TIME + MEMORY_TEXT_TIME: pass
        if whenEvalHappens == 1:
            while trialClock.getTime() < FIXATION_TIME + evalRT + EVAL_FIXATION_TIME + EVAL_TEXT_TIME + SECOND_RETENTION_INTERVAL + FIRST_CUE_TIME + FIRST_RETENTION_INTERVAL + STIM_TIME + FIXATION_TIME + MEMORY_TEXT_TIME:pass


        if whenEvalHappens == 0:
            #Fixation on Screen
            fixationVertical.setAutoDraw(True);fixationHorizontal.setAutoDraw(True)
            win.flip()
            while trialClock.getTime() < FIXATION_TIME + FIXATION_TIME + evalRT + EVAL_FIXATION_TIME + EVAL_TEXT_TIME + EVAL_BEFORE_RETRO_BLANK + FIRST_RETENTION_INTERVAL + STIM_TIME + FIXATION_TIME + MEMORY_TEXT_TIME: pass
            
            #First cue arrow on screen
            firstCueArrow.setAutoDraw(True)
            #Take fixation cross off screen
            fixationVertical.setAutoDraw(False);fixationHorizontal.setAutoDraw(False)
            win.flip()
            while trialClock.getTime() < FIRST_CUE_TIME + FIXATION_TIME + FIXATION_TIME + evalRT + EVAL_FIXATION_TIME + EVAL_TEXT_TIME + EVAL_BEFORE_RETRO_BLANK + FIRST_RETENTION_INTERVAL + STIM_TIME + FIXATION_TIME + MEMORY_TEXT_TIME: pass
        
            #Fixation on Screen
            fixationVertical.setAutoDraw(True);fixationHorizontal.setAutoDraw(True)
            #Take off first cue arrow
            firstCueArrow.setAutoDraw(False)
            win.flip()
            while trialClock.getTime() < SECOND_RETENTION_INTERVAL + FIRST_CUE_TIME + FIXATION_TIME + FIXATION_TIME + evalRT + EVAL_FIXATION_TIME + EVAL_TEXT_TIME + EVAL_BEFORE_RETRO_BLANK + FIRST_RETENTION_INTERVAL + STIM_TIME + FIXATION_TIME + MEMORY_TEXT_TIME: pass
            fixationVertical.setAutoDraw(False);fixationHorizontal.setAutoDraw(False)
        if whenEvalHappens == 1:
            while trialClock.getTime() < EVAL_AFTER_RETRO_BLANK + FIXATION_TIME + evalRT + EVAL_FIXATION_TIME + EVAL_TEXT_TIME + SECOND_RETENTION_INTERVAL + FIRST_CUE_TIME + FIRST_RETENTION_INTERVAL + STIM_TIME + FIXATION_TIME + MEMORY_TEXT_TIME:pass


        #Back to Memory Task
        fixationVertical.setAutoDraw(False);fixationHorizontal.setAutoDraw(False)
        rememberTextOnScreen = visual.TextStim(win=win, ori=0, name='rememberTextOnScreen', text='Same?',    font=u'Arial', pos=[0, 0], height=0.75, wrapWidth=None, color='black', colorSpace=u'rgb', opacity=1, depth=-1.0)
        rememberTextOnScreen.setAutoDraw(True)
        win.flip()
        if whenEvalHappens == 0:
            while trialClock.getTime() < REMEMBER_TEXT_TIME + SECOND_RETENTION_INTERVAL + FIRST_CUE_TIME + FIXATION_TIME + FIXATION_TIME + evalRT + EVAL_FIXATION_TIME + EVAL_TEXT_TIME + EVAL_BEFORE_RETRO_BLANK + FIRST_RETENTION_INTERVAL + STIM_TIME + FIXATION_TIME + MEMORY_TEXT_TIME: pass
        if whenEvalHappens == 1:
            while trialClock.getTime() < REMEMBER_TEXT_TIME + EVAL_AFTER_RETRO_BLANK + FIXATION_TIME + evalRT + EVAL_FIXATION_TIME + EVAL_TEXT_TIME + SECOND_RETENTION_INTERVAL + FIRST_CUE_TIME + FIRST_RETENTION_INTERVAL + STIM_TIME + FIXATION_TIME + MEMORY_TEXT_TIME:pass
        rememberTextOnScreen.setAutoDraw(False)
        
        
        
        
        fixationVertical.setAutoDraw(True);fixationHorizontal.setAutoDraw(True)
        win.flip()
        if whenEvalHappens == 0:
            while trialClock.getTime() < FIXATION_TIME + REMEMBER_TEXT_TIME + SECOND_RETENTION_INTERVAL + FIRST_CUE_TIME + FIXATION_TIME + FIXATION_TIME + evalRT + EVAL_FIXATION_TIME + EVAL_TEXT_TIME + EVAL_BEFORE_RETRO_BLANK + FIRST_RETENTION_INTERVAL + STIM_TIME + FIXATION_TIME + MEMORY_TEXT_TIME: pass
        if whenEvalHappens == 1:
            while trialClock.getTime() < FIXATION_TIME + REMEMBER_TEXT_TIME + EVAL_AFTER_RETRO_BLANK + FIXATION_TIME + evalRT + EVAL_FIXATION_TIME + EVAL_TEXT_TIME + SECOND_RETENTION_INTERVAL + FIRST_CUE_TIME + FIRST_RETENTION_INTERVAL + STIM_TIME + FIXATION_TIME + MEMORY_TEXT_TIME:pass
        fixationVertical.setAutoDraw(False);fixationHorizontal.setAutoDraw(False)
        
        
        
    #First Probe
        firstPracProbeCuedUncued = random.randint(0,1)#0=Cued,1=Uncued
        firstPracProbeRand = random.randint(0,2)#Random number for if it's an uncued stimulus being probed
        firstPosition = POSARRAY[firstPracCuePos]#position of first cued stimulus
        if firstPracProbeCuedUncued == 0:#Cued Stim is Probed
            if firstPosition == FirstPos:FirstProbe = visual.ImageStim(win=win,image= 'Images/' + colourArray[0] + '/' + colourArray[0] + '498.bmp', pos= [0,0], size=(SIZE,SIZE));firstProbeStim = colourArray[0] + '498'
            if firstPosition == SecondPos:FirstProbe = visual.ImageStim(win=win,image= 'Images/' + colourArray[1] + '/' + colourArray[1] + '498.bmp', pos= [0,0], size=(SIZE,SIZE));firstProbeStim = colourArray[1] + '498'
            if firstPosition == ThirdPos:FirstProbe = visual.ImageStim(win=win,image= 'Images/' + colourArray[2] + '/' + colourArray[2] + '498.bmp', pos= [0,0], size=(SIZE,SIZE));firstProbeStim = colourArray[2] + '498'
            if firstPosition == FourthPos:FirstProbe = visual.ImageStim(win=win,image= 'Images/' + colourArray[3] + '/' + colourArray[3] + '498.bmp', pos= [0,0], size=(SIZE,SIZE));firstProbeStim = colourArray[3] + '498'
        if firstPracProbeCuedUncued == 1:#Uncued Stim is Probed
            UncuedProbedStim = POSARRAY.index(firstPosition)
            if UncuedProbedStim == 0:
                if firstPracProbeRand == 0:FirstProbePos = POSARRAY[1]
                if firstPracProbeRand == 1:FirstProbePos = POSARRAY[2]
                if firstPracProbeRand == 2:FirstProbePos = POSARRAY[3]
            if UncuedProbedStim == 1:
                if firstPracProbeRand == 0:FirstProbePos = POSARRAY[0]
                if firstPracProbeRand == 1:FirstProbePos = POSARRAY[2]
                if firstPracProbeRand == 2:FirstProbePos = POSARRAY[3]
            if UncuedProbedStim == 2:
                if firstPracProbeRand == 0:FirstProbePos = POSARRAY[0]
                if firstPracProbeRand == 1:FirstProbePos = POSARRAY[1]
                if firstPracProbeRand == 2:FirstProbePos = POSARRAY[3]
            if UncuedProbedStim == 3:
                if firstPracProbeRand == 0:FirstProbePos = POSARRAY[0]
                if firstPracProbeRand == 1:FirstProbePos = POSARRAY[1]
                if firstPracProbeRand == 2:FirstProbePos = POSARRAY[2]
            
            if FirstProbePos == FirstPos:FirstProbe = visual.ImageStim(win=win,image= 'Images/' + colourArray[0] + '/' + colourArray[0] + '498.bmp', pos= [0,0], size=(SIZE,SIZE));firstProbeStim = colourArray[0] + '498'
            if FirstProbePos == SecondPos:FirstProbe = visual.ImageStim(win=win,image= 'Images/' + colourArray[1] + '/' + colourArray[1] + '498.bmp', pos= [0,0], size=(SIZE,SIZE));firstProbeStim = colourArray[1] + '498'
            if FirstProbePos == ThirdPos:FirstProbe = visual.ImageStim(win=win,image= 'Images/' + colourArray[2] + '/' + colourArray[2] + '498.bmp', pos= [0,0], size=(SIZE,SIZE));firstProbeStim = colourArray[2] + '498'
            if FirstProbePos == FourthPos:FirstProbe = visual.ImageStim(win=win,image= 'Images/' + colourArray[3] + '/' + colourArray[3] + '498.bmp', pos= [0,0], size=(SIZE,SIZE));firstProbeStim = colourArray[3] + '498'
                
                
        FirstProbe.setAutoDraw(True)
        win.flip()
        
        
        
        eventClock.reset()
        stimOnScreen = True
        keyResp.status = NOT_STARTED
        firstProbeErrorCode = -1
        firstProbeErrorName = ''
        noResponseYet = True
        probeOnScreen = True
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
                
                
            #check for a keyboard response
            theseKeys = event.getKeys(keyList=['up','down'])
            if noResponseYet == True:
                if len(theseKeys) > 0: #test if atleast one key pressed
                    if keyResp.keys == []:
                        FirstProbe.setAutoDraw(False)
                        keyResp.keys = theseKeys[-1] #just the last key pressed
                        keyResp.rt = keyResp.clock.getTime()
                        FirstProbeResponse = keyResp.keys
                        FirstProbeRT = keyResp.rt
                        if buttonCounterbalance == 0:
                            if keyResp.keys == 'up' and firstPracProbeCuedUncued == 1:
                               firstProbeErrorCode = 2
                               firstProbeErrorName = 'incorrect response'
                            if keyResp.keys == 'down' and firstPracProbeCuedUncued == 0:
                               firstProbeErrorCode = 2
                               firstProbeErrorName = 'incorrect response'
                        if buttonCounterbalance == 1:
                            if keyResp.keys == 'down' and firstPracProbeCuedUncued == 1:
                               firstProbeErrorCode = 2
                               firstProbeErrorName = 'incorrect response'
                            if keyResp.keys == 'up' and firstPracProbeCuedUncued == 0:
                               firstProbeErrorCode = 2
                               firstProbeErrorName = 'incorrect response'
                        noResponseYet = False
            
            if stimOnScreen and t > FIRST_PROBE_ON_SCREEN:
                FirstProbe.setAutoDraw(False)
                win.flip()
                stimOnScreen = False
            
            
            # check for quit (the [Esc] key)
            if event.getKeys(["escape"]):
                core.quit()

        FirstProbe.setAutoDraw(False)
        
        fixationVertical.setAutoDraw(True);fixationHorizontal.setAutoDraw(True)
        if firstProbeErrorCode == -1:
            feedbackTextOnScreen = visual.TextStim(win=win, ori=0, name='feedbackTextOnScreen', text='Correct',    font=u'Arial', pos=[0, 2], height=0.75, wrapWidth=None, color='green', colorSpace=u'rgb', opacity=1, depth=-1.0)
        if firstProbeErrorCode == 2:
            feedbackTextOnScreen = visual.TextStim(win=win, ori=0, name='feedbackTextOnScreen', text='Incorrect',    font=u'Arial', pos=[0, 2], height=0.75, wrapWidth=None, color='red', colorSpace=u'rgb', opacity=1, depth=-1.0)
        feedbackTextOnScreen.setAutoDraw(True)
        win.flip()
        
        if whenEvalHappens == 0:
            while trialClock.getTime() < FEEDBACK_TIME + FirstProbeRT + FIXATION_TIME + REMEMBER_TEXT_TIME + SECOND_RETENTION_INTERVAL + FIRST_CUE_TIME + FIXATION_TIME + FIXATION_TIME + evalRT + EVAL_FIXATION_TIME + EVAL_TEXT_TIME + EVAL_BEFORE_RETRO_BLANK + FIRST_RETENTION_INTERVAL + STIM_TIME + FIXATION_TIME + MEMORY_TEXT_TIME: pass
        if whenEvalHappens == 1:
            while trialClock.getTime() < FEEDBACK_TIME + FirstProbeRT + FIXATION_TIME + REMEMBER_TEXT_TIME + EVAL_AFTER_RETRO_BLANK + FIXATION_TIME + evalRT + EVAL_FIXATION_TIME + EVAL_TEXT_TIME + SECOND_RETENTION_INTERVAL + FIRST_CUE_TIME + FIRST_RETENTION_INTERVAL + STIM_TIME + FIXATION_TIME + MEMORY_TEXT_TIME:pass
        feedbackTextOnScreen.setAutoDraw(False)
        win.flip()
        
        if whenEvalHappens == 0:
            while trialClock.getTime() < THIRD_RETENTION_INTERVAL + FEEDBACK_TIME + FirstProbeRT + FIXATION_TIME + REMEMBER_TEXT_TIME + SECOND_RETENTION_INTERVAL + FIRST_CUE_TIME + FIXATION_TIME + FIXATION_TIME + evalRT + EVAL_FIXATION_TIME + EVAL_TEXT_TIME + EVAL_BEFORE_RETRO_BLANK + FIRST_RETENTION_INTERVAL + STIM_TIME + FIXATION_TIME + MEMORY_TEXT_TIME: pass
        if whenEvalHappens == 1:
            while trialClock.getTime() < THIRD_RETENTION_INTERVAL + FEEDBACK_TIME + FirstProbeRT + FIXATION_TIME + REMEMBER_TEXT_TIME + EVAL_AFTER_RETRO_BLANK + FIXATION_TIME + evalRT + EVAL_FIXATION_TIME + EVAL_TEXT_TIME + SECOND_RETENTION_INTERVAL + FIRST_CUE_TIME + FIRST_RETENTION_INTERVAL + STIM_TIME + FIXATION_TIME + MEMORY_TEXT_TIME:pass
        
        
        fixationVertical.setAutoDraw(False)
        fixationHorizontal.setAutoDraw(False)
        secondCueArrow.setAutoDraw(True)
        win.flip()
        if whenEvalHappens == 0:
            while trialClock.getTime() < SECOND_CUE_TIME + THIRD_RETENTION_INTERVAL + FEEDBACK_TIME + FirstProbeRT + FIXATION_TIME + REMEMBER_TEXT_TIME + SECOND_RETENTION_INTERVAL + FIRST_CUE_TIME + FIXATION_TIME + FIXATION_TIME + evalRT + EVAL_FIXATION_TIME + EVAL_TEXT_TIME + EVAL_BEFORE_RETRO_BLANK + FIRST_RETENTION_INTERVAL + STIM_TIME + FIXATION_TIME + MEMORY_TEXT_TIME: pass
        if whenEvalHappens == 1:
            while trialClock.getTime() < SECOND_CUE_TIME + THIRD_RETENTION_INTERVAL + FEEDBACK_TIME + FirstProbeRT + FIXATION_TIME + REMEMBER_TEXT_TIME + EVAL_AFTER_RETRO_BLANK + FIXATION_TIME + evalRT + EVAL_FIXATION_TIME + EVAL_TEXT_TIME + SECOND_RETENTION_INTERVAL + FIRST_CUE_TIME + FIRST_RETENTION_INTERVAL + STIM_TIME + FIXATION_TIME + MEMORY_TEXT_TIME:pass

        fixationVertical.setAutoDraw(True)
        fixationHorizontal.setAutoDraw(True)
        secondCueArrow.setAutoDraw(False)
        win.flip()
        if whenEvalHappens == 0:
            while trialClock.getTime() < FOURTH_RETENTION_INTERVAL + SECOND_CUE_TIME + THIRD_RETENTION_INTERVAL + FEEDBACK_TIME + FirstProbeRT + FIXATION_TIME + REMEMBER_TEXT_TIME + SECOND_RETENTION_INTERVAL + FIRST_CUE_TIME + FIXATION_TIME + FIXATION_TIME + evalRT + EVAL_FIXATION_TIME + EVAL_TEXT_TIME + EVAL_BEFORE_RETRO_BLANK + FIRST_RETENTION_INTERVAL + STIM_TIME + FIXATION_TIME + MEMORY_TEXT_TIME: pass
        if whenEvalHappens == 1:
            while trialClock.getTime() < FOURTH_RETENTION_INTERVAL + SECOND_CUE_TIME + THIRD_RETENTION_INTERVAL + FEEDBACK_TIME + FirstProbeRT + FIXATION_TIME + REMEMBER_TEXT_TIME + EVAL_AFTER_RETRO_BLANK + FIXATION_TIME + evalRT + EVAL_FIXATION_TIME + EVAL_TEXT_TIME + SECOND_RETENTION_INTERVAL + FIRST_CUE_TIME + FIRST_RETENTION_INTERVAL + STIM_TIME + FIXATION_TIME + MEMORY_TEXT_TIME:pass


    #Second Probe
        
        secondPracProbeCuedUncued = random.randint(0,1)#0=Cued,1=Uncued
        secondPracProbeRand = random.randint(0,2)#Random number for if it's an uncued stimulus being probed
        secondPosition = POSARRAY[secondPracCuePos]#position of second cued stimulus
        if secondPracProbeCuedUncued == 0:#Cued Stim is Probed
            if secondPosition == FirstPos:SecondProbe = visual.ImageStim(win=win,image= 'Images/' + colourArray[0] + '/' + colourArray[0] + '498.bmp', pos= [0,0], size=(SIZE,SIZE));secondProbeStim = colourArray[0] + '498'
            if secondPosition == SecondPos:SecondProbe = visual.ImageStim(win=win,image= 'Images/' + colourArray[1] + '/' + colourArray[1] + '498.bmp', pos= [0,0], size=(SIZE,SIZE));secondProbeStim = colourArray[1] + '498'
            if secondPosition == ThirdPos:SecondProbe = visual.ImageStim(win=win,image= 'Images/' + colourArray[2] + '/' + colourArray[2] + '498.bmp', pos= [0,0], size=(SIZE,SIZE));secondProbeStim = colourArray[2] + '498'
            if secondPosition == FourthPos:SecondProbe = visual.ImageStim(win=win,image= 'Images/' + colourArray[3] + '/' + colourArray[3] + '498.bmp', pos= [0,0], size=(SIZE,SIZE));secondProbeStim = colourArray[3] + '498'
        if secondPracProbeCuedUncued == 1:#Uncued Stim is Probed
            UncuedProbedStim = POSARRAY.index(secondPosition)
            if UncuedProbedStim == 0:
                if secondPracProbeRand == 0:SecondProbePos= POSARRAY[1]
                if secondPracProbeRand == 1:SecondProbePos = POSARRAY[2]
                if secondPracProbeRand == 2:SecondProbePos = POSARRAY[3]
            if UncuedProbedStim == 1:
                if secondPracProbeRand == 0:SecondProbePos = POSARRAY[0]
                if secondPracProbeRand == 1:SecondProbePos = POSARRAY[2]
                if secondPracProbeRand == 2:SecondProbePos = POSARRAY[3]
            if UncuedProbedStim == 2:
                if secondPracProbeRand == 0:SecondProbePos = POSARRAY[0]
                if secondPracProbeRand == 1:SecondProbePos = POSARRAY[1]
                if secondPracProbeRand == 2:SecondProbePos = POSARRAY[3]
            if UncuedProbedStim == 3:
                if secondPracProbeRand == 0:SecondProbePos = POSARRAY[0]
                if secondPracProbeRand == 1:SecondProbePos = POSARRAY[1]
                if secondPracProbeRand == 2:SecondProbePos = POSARRAY[2]
            
            if SecondProbePos == FirstPos:SecondProbe = visual.ImageStim(win=win,image= 'Images/' + colourArray[0] + '/' + colourArray[0] + '498.bmp', pos= [0,0], size=(SIZE,SIZE));secondProbeStim = colourArray[0] + '498'
            if SecondProbePos == SecondPos:SecondProbe = visual.ImageStim(win=win,image= 'Images/' + colourArray[1] + '/' + colourArray[1] + '498.bmp', pos= [0,0], size=(SIZE,SIZE));secondProbeStim = colourArray[1] + '498'
            if SecondProbePos == ThirdPos:SecondProbe = visual.ImageStim(win=win,image= 'Images/' + colourArray[2] + '/' + colourArray[2] + '498.bmp', pos= [0,0], size=(SIZE,SIZE));secondProbeStim = colourArray[2] + '498'
            if SecondProbePos == FourthPos:SecondProbe = visual.ImageStim(win=win,image= 'Images/' + colourArray[3] + '/' + colourArray[3] + '498.bmp', pos= [0,0], size=(SIZE,SIZE));secondProbeStim = colourArray[3] + '498'
                
                
        SecondProbe.setAutoDraw(True)
        win.flip()
        
        
        
        
        eventClock.reset()
        stimOnScreen = True
        keyResp.status = NOT_STARTED
        secondProbeErrorCode = -1
        secondProbeErrorName = ''
        noResponseYet = True
        probeOnScreen = True
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
                
                
            #check for a keyboard response
            theseKeys = event.getKeys(keyList=['up','down'])
            if noResponseYet == True:
                if len(theseKeys) > 0: #test if atleast one key pressed
                    if keyResp.keys == []:
                        SecondProbe.setAutoDraw(False)
                        keyResp.keys = theseKeys[-1] #just the last key pressed
                        keyResp.rt = keyResp.clock.getTime()
                        SecondProbeResponse = keyResp.keys
                        SecondProbeRT = keyResp.rt
                        if buttonCounterbalance == 0:
                            if keyResp.keys == 'up' and secondPracProbeCuedUncued == 1:
                               secondProbeErrorCode = 2
                               secondProbeErrorName = 'incorrect response'
                            if keyResp.keys == 'down' and secondPracProbeCuedUncued == 0:
                               secondProbeErrorCode = 2
                               secondProbeErrorName = 'incorrect response'
                        if buttonCounterbalance == 1:
                            if keyResp.keys == 'down' and secondPracProbeCuedUncued == 1:
                               secondProbeErrorCode = 2
                               secondProbeErrorName = 'incorrect response'
                            if keyResp.keys == 'up' and secondPracProbeCuedUncued == 0:
                               secondProbeErrorCode = 2
                               secondProbeErrorName = 'incorrect response'
                        noResponseYet = False
            
            if stimOnScreen and t > FIRST_PROBE_ON_SCREEN:
                SecondProbe.setAutoDraw(False)
                win.flip()
                stimOnScreen = False
            
            
            # check for quit (the [Esc] key)
            if event.getKeys(["escape"]):
                core.quit()

        SecondProbe.setAutoDraw(False)

        fixationVertical.setAutoDraw(True);fixationHorizontal.setAutoDraw(True)
        if secondProbeErrorCode == -1:
            feedbackTextOnScreen = visual.TextStim(win=win, ori=0, name='feedbackTextOnScreen', text='Correct',    font=u'Arial', pos=[0, 2], height=0.75, wrapWidth=None, color='green', colorSpace=u'rgb', opacity=1, depth=-1.0)
        if secondProbeErrorCode == 2:
            feedbackTextOnScreen = visual.TextStim(win=win, ori=0, name='feedbackTextOnScreen', text='Incorrect',    font=u'Arial', pos=[0, 2], height=0.75, wrapWidth=None, color='red', colorSpace=u'rgb', opacity=1, depth=-1.0)
        feedbackTextOnScreen.setAutoDraw(True)
        win.flip()
        
        if whenEvalHappens == 0:
            while trialClock.getTime() < FEEDBACK_TIME + SecondProbeRT + FOURTH_RETENTION_INTERVAL + SECOND_CUE_TIME + THIRD_RETENTION_INTERVAL + FEEDBACK_TIME + FirstProbeRT + FIXATION_TIME + REMEMBER_TEXT_TIME + SECOND_RETENTION_INTERVAL + FIRST_CUE_TIME + FIXATION_TIME + FIXATION_TIME + evalRT + EVAL_FIXATION_TIME + EVAL_TEXT_TIME + EVAL_BEFORE_RETRO_BLANK + FIRST_RETENTION_INTERVAL + STIM_TIME + FIXATION_TIME + MEMORY_TEXT_TIME: pass
        if whenEvalHappens == 1:
            while trialClock.getTime() < FEEDBACK_TIME + SecondProbeRT + FOURTH_RETENTION_INTERVAL + SECOND_CUE_TIME + THIRD_RETENTION_INTERVAL + FEEDBACK_TIME + FirstProbeRT + FIXATION_TIME + REMEMBER_TEXT_TIME + EVAL_AFTER_RETRO_BLANK + FIXATION_TIME + evalRT + EVAL_FIXATION_TIME + EVAL_TEXT_TIME + SECOND_RETENTION_INTERVAL + FIRST_CUE_TIME + FIRST_RETENTION_INTERVAL + STIM_TIME + FIXATION_TIME + MEMORY_TEXT_TIME:pass
        feedbackTextOnScreen.setAutoDraw(False)
        win.flip()
    
    
    #Inter-trial interval
    eventClock.reset()
    fixationHorizontal.setAutoDraw(False);fixationVertical.setAutoDraw(False)
    win.flip()
    while eventClock.getTime() < INTER_TRIAL_INTERVAL: pass



    outStr = str(runTime) + '\t'
    outStr = outStr + str(pracTrialCount) + '\t'
    outStr = outStr + str(TrialType) + '\t'
    outStr = outStr + 'Blue498' + '\t'
    if colourArray.index('Blue') < 4:
        outStr = outStr + str(POSARRAY[colourArray.index('Blue')]) + '\t'
    if colourArray.index('Blue') == 4:
        outStr = outStr + 'novelcolour' + '\t'
    outStr = outStr + 'Green498' + '\t'
    if colourArray.index('Green') < 4:
        outStr = outStr + str(POSARRAY[colourArray.index('Green')]) + '\t'
    if colourArray.index('Green') == 4:
        outStr = outStr + 'novelcolour' + '\t'
    outStr = outStr + 'Purple498' + '\t'
    if colourArray.index('Purple') < 4:
        outStr = outStr + str(POSARRAY[colourArray.index('Purple')]) + '\t'
    if colourArray.index('Purple') == 4:
        outStr = outStr + 'novelcolour' + '\t'
    outStr = outStr + 'Pink498' + '\t'
    if colourArray.index('Pink') < 4:
        outStr = outStr + str(POSARRAY[colourArray.index('Pink')]) + '\t'
    if colourArray.index('Pink') == 4:
        outStr = outStr + 'novelcolour' + '\t'
    outStr = outStr + 'Orange498' + '\t'
    if colourArray.index('Orange') < 4:
        outStr = outStr + str(POSARRAY[colourArray.index('Orange')]) + '\t'
    if colourArray.index('Orange') == 4:
        outStr = outStr + 'novelcolour' + '\t'
    if firstPracCuePos == 0 or firstPracCuePos == 1:
        outStr = outStr + '0' + '\t'
    if firstPracCuePos == 2 or firstPracCuePos == 3:
        outStr = outStr + '1' + '\t'
    outStr = outStr + str(POSARRAY[firstPracCuePos]) + '\t'
    if whenEvalHappens < 2:
        outStr = outStr + str(secondPosition) + '\t'
        outStr = outStr + str(firstProbeStim) + '\t'
        outStr = outStr + str(firstPracProbeCuedUncued) + '\t'
        outStr = outStr + str(FirstProbeResponse) + '\t'
        if firstProbeErrorCode == -1:
            outStr = outStr + '1' + '\t'
        if firstProbeErrorCode == 2:
            outStr = outStr + '0' + '\t'
        if firstProbeErrorCode == 5:
            outStr = outStr + '0' + '\t'
        if firstProbeErrorCode == 6:
            outStr = outStr + '0' + '\t'
        outStr = outStr + str(FirstProbeRT) + '\t'
        outStr = outStr + str(firstProbeErrorCode) + '\t'
        outStr = outStr + str(firstProbeErrorName) + '\t'
        outStr = outStr + str(secondProbeStim) + '\t'
        outStr = outStr + str(secondPracProbeCuedUncued) + '\t'
        outStr = outStr + str(SecondProbeResponse) + '\t'
        if secondProbeErrorCode == -1:
            outStr = outStr + '1' + '\t'
        if secondProbeErrorCode == 2:
            outStr = outStr + '0' + '\t'
        if secondProbeErrorCode == 5:
            outStr = outStr + '0' + '\t'
        if secondProbeErrorCode == 6:
            outStr = outStr + '0' + '\t'
        outStr = outStr + str(SecondProbeRT) + '\t'
        outStr = outStr + str(secondProbeErrorCode) + '\t'
        outStr = outStr + str(secondProbeErrorName) + '\t'
        pracEvalImgName2 = pracEvalImgName.rsplit("/")[-1]
        outStr = outStr + str(pracEvalImgName2) + '\t'
        outStr = outStr + str(pracWhichEval) + '\t'
        outStr = outStr + str(evalResponse) + '\t'
        outStr = outStr + str(evalRT) + '\t'
        outStr = outStr + str(evalErrorCode) + '\t'
        outStr = outStr + str(evalErrorName) + '\t'
    if whenEvalHappens == 2:
        outStr = outStr + 'searchtask\tsearchtask\tsearchtask\tsearchtask\tsearchtask\tsearchtask\tsearchtask\tsearchtask\tsearchtask\tsearchtask\tsearchtask\tsearchtask\tsearchtask\tsearchtask\tsearchtask\tsearchtask\tsearchtask\tsearchtask\tsearchtask\tsearchtask\tsearchtask\t'
    outStr = outStr + str(STIM_TIME) + '\t'
    outStr = outStr + str(whenEvalHappens) + '\t'
    if whenEvalHappens == 2:
        outStr = outStr + str(singType) + '\t'
        outStr = outStr + str(singColName) + '\t'
        outStr = outStr + str(singPos) + '\t'
        if searchStim[1].ori == 0:
            outStr = outStr + 'left' + '\t'
        if searchStim[1].ori == 180:
            outStr = outStr + 'right' + '\t'
        if targetOri == 90:
            outStr = outStr + 'up' + '\t'
        if targetOri == 270:
            outStr = outStr + 'down' + '\t'
        outStr = outStr + str(tarPos) + '\t'
        outStr = outStr + str(searchResponse) + '\t'
        outStr = outStr + str(searchRT) + '\t'
        outStr = outStr + str(searchErrorCode) + '\t'
        outStr = outStr + str(searchErrorName) + '\t'
    if whenEvalHappens < 2:
        outStr = outStr + 'nosearch\tnosearch\tnosearch\tnosearch\tnosearch\tnosearch\tnosearch\tnosearch\tnosearch\tnosearch\t'
    outStr = outStr + '0' + '\t'
    outStr = outStr + str(expInfo2['age']) + '\t'
    outStr = outStr + str(expInfo3['gender']) + '\t'
    outStr = outStr + str(expInfo4['handedness']) + '\t'
    outStr = outStr + str(expInfo5['glasses/contacts?']) + '\t'
    outputFile.write(outStr + 'eol\n')






Instruct1 = visual.ImageStim(win=win,image= 'Slide13.jpg', pos= [0,0], size=(36,23))
Instruct1.setAutoDraw(True)
win.flip()
event.waitKeys()
Instruct1.setAutoDraw(False)
if buttonCounterbalance == 0:
    Instruct1 = visual.ImageStim(win=win,image= 'Slide11.jpg', pos= [0,0], size=(36,23))
if buttonCounterbalance == 1:
    Instruct1 = visual.ImageStim(win=win,image= 'Slide12.jpg', pos= [0,0], size=(36,23))
Instruct1.setAutoDraw(True)
win.flip()
event.waitKeys()
Instruct1.setAutoDraw(False)
win.flip()
if buttonCounterbalance == 0:
    Instruct1 = visual.ImageStim(win=win,image= 'Slide20.jpg', pos= [0,0], size=(36,23))
if buttonCounterbalance == 1:
    Instruct1 = visual.ImageStim(win=win,image= 'Slide21.jpg', pos= [0,0], size=(36,23))
Instruct1.setAutoDraw(True)
win.flip()
event.waitKeys()
Instruct1.setAutoDraw(False)
win.flip()

core.wait(2.0)



#Actual Memory Trials
TrialType = "FirstHalf"

for trial in range(0, 64):
    random.shuffle(colourArray)
    
    runTime = time.strftime("%c")
    
    curRow = idxTrialsArray[trial]
    
    
    #put memory task text on screen
    memTextOnScreen = visual.TextStim(win=win, ori=0, name='memTextOnScreen', text='Memorize',    font=u'Arial', pos=[0, 0], height=0.75, wrapWidth=None, color='black', colorSpace=u'rgb', opacity=1, depth=-1.0)
    memTextOnScreen.setAutoDraw(True)
    win.flip()
    trialClock.reset()
    while trialClock.getTime() < MEMORY_TEXT_TIME:pass
    
    #Fixation Cross
    memTextOnScreen.setAutoDraw(False)
    fixationVertical.setAutoDraw(True);fixationHorizontal.setAutoDraw(True)
    win.flip()
    while trialClock.getTime() < FIXATION_TIME + MEMORY_TEXT_TIME: pass
    
    #Decide Positions of Each Color
    FirstColour = colourArray[0]
    SecondColour = colourArray[1]
    ThirdColour = colourArray[2]
    FourthColour = colourArray[3]
    FirstPos = POSARRAY[0]
    SecondPos = POSARRAY[1]
    ThirdPos = POSARRAY[2]
    FourthPos = POSARRAY[3]
    
    #Create Stimuli
    BlueStimCount = BlueStimCount + 1
    GreenStimCount = GreenStimCount + 1
    PurpleStimCount = PurpleStimCount + 1
    PinkStimCount = PinkStimCount + 1
    OrangeStimCount = OrangeStimCount + 1
    BlueCount = idxBlueStim[BlueStimCount]
    GreenCount = idxGreenStim[GreenStimCount]
    PurpleCount = idxPurpleStim[PurpleStimCount]
    PinkCount = idxPinkStim[PinkStimCount]
    OrangeCount = idxOrangeStim[OrangeStimCount]
    
    if colourArray.index('Blue') < 4:
        BluePos = POSARRAY[colourArray.index('Blue')]
        FirstItem = visual.ImageStim(win=win,image= 'Images/Blue/Blue' + str(BlueCount) + '.bmp', pos= BluePos, size=(SIZE,SIZE))
    if colourArray.index('Green') < 4:
        GreenPos = POSARRAY[colourArray.index('Green')]
        SecondItem = visual.ImageStim(win=win,image= 'Images/Green/Green' + str(GreenCount) + '.bmp', pos= GreenPos, size=(SIZE,SIZE))
    if colourArray.index('Purple') < 4:
        PurplePos = POSARRAY[colourArray.index('Purple')]
        ThirdItem = visual.ImageStim(win=win,image= 'Images/Purple/Purple' + str(PurpleCount) + '.bmp', pos= PurplePos, size=(SIZE,SIZE))
    if colourArray.index('Pink') < 4:
        PinkPos = POSARRAY[colourArray.index('Pink')]
        FourthItem = visual.ImageStim(win=win,image= 'Images/Pink/Pink' + str(PinkCount) + '.bmp', pos= PinkPos, size=(SIZE,SIZE))
    if colourArray.index('Orange') < 4:
        OrangePos = POSARRAY[colourArray.index('Orange')]
        if colourArray.index('Blue') == 4:
            FirstItem = visual.ImageStim(win=win,image= 'Images/Orange/Orange' + str(OrangeCount) + '.bmp', pos= OrangePos, size=(SIZE,SIZE))
        if colourArray.index('Green') == 4:
            SecondItem = visual.ImageStim(win=win,image= 'Images/Orange/Orange' + str(OrangeCount) + '.bmp', pos= OrangePos, size=(SIZE,SIZE))
        if colourArray.index('Purple') == 4:
            ThirdItem = visual.ImageStim(win=win,image= 'Images/Orange/Orange' + str(OrangeCount) + '.bmp', pos= OrangePos, size=(SIZE,SIZE))
        if colourArray.index('Pink') == 4:
            FourthItem = visual.ImageStim(win=win,image= 'Images/Orange/Orange' + str(OrangeCount) + '.bmp', pos= OrangePos, size=(SIZE,SIZE))
            
    
    #Put Stimulus Array on Screen
    FirstItem.setAutoDraw(True);SecondItem.setAutoDraw(True);ThirdItem.setAutoDraw(True);FourthItem.setAutoDraw(True)
    win.flip()
    while trialClock.getTime() < STIM_TIME + FIXATION_TIME + MEMORY_TEXT_TIME: pass
    
    #Take Stimulus Array off Screen
    FirstItem.setAutoDraw(False);SecondItem.setAutoDraw(False);ThirdItem.setAutoDraw(False);FourthItem.setAutoDraw(False)
    win.flip()
    while trialClock.getTime() < FIRST_RETENTION_INTERVAL + STIM_TIME + FIXATION_TIME + MEMORY_TEXT_TIME: pass

    #decide where first cue points
    if trialsArray[curRow][1] == 0 and trialsArray[curRow][2] == 0:firstCuePos=1#left top
    if trialsArray[curRow][1] == 0 and trialsArray[curRow][2] == 1:firstCuePos=0#left bottom
    if trialsArray[curRow][1] == 1 and trialsArray[curRow][2] == 0:firstCuePos=2#right top
    if trialsArray[curRow][1] == 1 and trialsArray[curRow][2] == 1:firstCuePos=3#right bottom
    firstCueArrow = visual.ImageStim(win=win,image= arrowArray[firstCuePos], pos= [0,0], size=(1,1))
        
    if trialsArray[curRow][5] == 0 or trialsArray[curRow][5] == 1:
        #where second cue points
        if firstCuePos == 0:#left bottom
            if trialsArray[curRow][3] == 0:secondCuePos=2#diagonal from left bottom is right top
            if trialsArray[curRow][3] == 1:secondCuePos=3#horizontal from left bottom is right bottom
        if firstCuePos == 1:#left top
            if trialsArray[curRow][3] == 0:secondCuePos=3#diagonal from left top is right bottom
            if trialsArray[curRow][3] == 1:secondCuePos=2#horizontal from left top is right top
        if firstCuePos == 2:#right top
            if trialsArray[curRow][3] == 0:secondCuePos=0#diagonal from right top is left bottom
            if trialsArray[curRow][3] == 1:secondCuePos=1#horizontal from right top is left top
        if firstCuePos == 3:#right bottom
            if trialsArray[curRow][3] == 0:secondCuePos=1#diagonal from right bottom is left top
            if trialsArray[curRow][3] == 1:secondCuePos=0#horizontal from right bottom is left bottom

        secondCueArrow = visual.ImageStim(win=win,image= arrowArray[secondCuePos], pos= [0,0], size=(1,1))

            
        #Find out position of evaluated stimulus
        if trialsArray[curRow][4] == 0:#NeverCuedStimSecondCuedSide
            if secondCuePos==0:EvalPos=POSARRAY[1]
            if secondCuePos==1:EvalPos=POSARRAY[0]
            if secondCuePos==2:EvalPos=POSARRAY[3]
            if secondCuePos==3:EvalPos=POSARRAY[2]
        if trialsArray[curRow][4] == 1:#FirstCuedStim
            EvalPos=POSARRAY[firstCuePos]
            

        #Determine which actual stimulus will be evaluated
        if colourArray.index('Blue') < 4:
            if EvalPos == BluePos:evalImgName = 'Images/Blue/Blue' + str(BlueCount) + '.bmp'
        if colourArray.index('Green') < 4:
            if EvalPos == GreenPos:evalImgName = 'Images/Green/Green' + str(GreenCount) + '.bmp'
        if colourArray.index('Purple') < 4:
            if EvalPos == PurplePos:evalImgName = 'Images/Purple/Purple' + str(PurpleCount) + '.bmp'
        if colourArray.index('Pink') < 4:
            if EvalPos == PinkPos:evalImgName = 'Images/Pink/Pink' + str(PinkCount) + '.bmp'
        if colourArray.index('Orange') < 4:
            if EvalPos == OrangePos:evalImgName = 'Images/Orange/Orange' + str(OrangeCount) + '.bmp'


    if trialsArray[curRow][5] == 0:#Evaluate before RetroCue
        while trialClock.getTime() < EVAL_BEFORE_RETRO_BLANK + FIRST_RETENTION_INTERVAL + STIM_TIME + FIXATION_TIME + MEMORY_TEXT_TIME: pass
    if trialsArray[curRow][5] == 1 or trialsArray[curRow][5] == 2:#Evaluate After RetroCue or SearchTask
        #First cue arrow on screen
        firstCueArrow.setAutoDraw(True)
        #Take fixation cross off screen
        fixationVertical.setAutoDraw(False);fixationHorizontal.setAutoDraw(False)
        win.flip()
        while trialClock.getTime() < FIRST_CUE_TIME + FIRST_RETENTION_INTERVAL + STIM_TIME + FIXATION_TIME + MEMORY_TEXT_TIME: pass
    
        #Fixation on Screen
        fixationVertical.setAutoDraw(True);fixationHorizontal.setAutoDraw(True)
        #Take off first cue arrow
        firstCueArrow.setAutoDraw(False)
        win.flip()
        while trialClock.getTime() < SECOND_RETENTION_INTERVAL + FIRST_CUE_TIME + FIRST_RETENTION_INTERVAL + STIM_TIME + FIXATION_TIME + MEMORY_TEXT_TIME: pass
    if trialsArray[curRow][5] == 2:#Search Task
        #determine singleton type
        singType = trialsArray[curRow][6]#0=activematching,1=accessorymatching,2=novelcolour
        #setup target locations in a circle around fixation
        targetPositions = []
        for pos in range(0, NUM_TARGET_POS):#8 target positions
            angle = math.radians(360 / NUM_TARGET_POS * pos)
            targetPositions.append([math.cos(angle)*SEARCH_ECCEN, math.sin(angle)*SEARCH_ECCEN])#setup target locations in a circle around fixation

        #set stimulus properties
        distractorOris = [0, 180] #orientations for the landolt c stimuli #gap pointing left or right for all distractors.
        idxDistractorOris = range(len(distractorOris))
        targetOris = [90,270]
        idxTargetOris = range(len(targetOris))

        #setup search stim 
        searchStim = [] #create a list of 8 distractor stim to be used on each trial -- these stim are all leftOpen so later on we will randomly assign them an orientation (90 or 180) so they become top/bottom open
        for distractor in range (0, NUM_SEARCH_POS):
            distractor = visual.ShapeStim(win, lineColorSpace='rgb', fillColorSpace = 'rgb', fillColor=bCol, lineColor=sCol, vertices=GetVertices(), closeShape=False, lineWidth = 9)
            searchStim.append(distractor)

        #set colour of singleton based on condition
        if singType == 0:#activematching
            singCol = colourArray[firstCuePos]
        elif singType == 1:#accessorymatching
            secondCuedRand = random.randint(0,1)#0=top,1=bottom
            if firstCuePos == 0 or firstCuePos == 1:
                if secondCuedRand == 0:
                    singCol = colourArray[2]
                if secondCuedRand == 1:
                    singCol = colourArray[3]
            if firstCuePos == 2 or firstCuePos == 3:
                if secondCuedRand == 0:
                    singCol = colourArray[1]
                if secondCuedRand == 1:
                    singCol = colourArray[0]
        else:#novelmatching
            singCol = colourArray[4]
            
        if singCol == 'Blue':
            singColName = 'Blue'
            singCol = [-.875,-.827,.639]
        if singCol == 'Green':
            singColName = 'Green'
            singCol = [-.671,.129,-.537]
        if singCol == 'Purple':
            singColName = 'Purple'
            singCol = [.545,-.576,.78]
        #if singCol == 'Yellow':
        #    singCol = [.843,.835,-.522]
        if singCol == 'Orange':
            singColName = 'Orange'
            singCol = [.435,-.255,-.741]
        if singCol == 'Pink':
            singColName = 'Pink'
            singCol = [.89,.231,.757]
        #if singCol == 'Red':
        #    singCol = [.075,-.757,-.725]
        
        random.shuffle(idxSearchPos) #randomly shuffle the list of positions in the search array

        #Search display #create 8 distractors
        for item in range (0, NUM_TARGET_POS):
            random.shuffle(idxDistractorOris)
            searchStim[item].ori=distractorOris[idxDistractorOris[0]]
            searchStim[item].pos = targetPositions[idxSearchPos[item]]
            searchStim[item].setAutoDraw(True)
            
        tarPos = searchStim[0].pos
        singPos = searchStim[1].pos

        #here you're changing one of the previously created distractors to be the target. So first item in SearchStim list is being changed to have targetOrientation.
        random.shuffle(idxTargetOris)
        targetPos = 0
        targetOri = targetOris[idxTargetOris[0]]
        searchStim[targetPos].ori=targetOri
        searchStim[targetPos].setAutoDraw(True)

        #here you're changing one of the previously created distractors to be the singleton. So second item in SearchStim list is being changed to singletoncolour.
        singletonPos = 1
#        if searchCond == 4:
        searchStim[singletonPos].setLineColor(singCol)
#        else:
#            searchStim[singletonPos].setLineColor('blue')
        searchStim[singletonPos].setAutoDraw(True)

        #put the whole search task on the screen including target, singleton, and 6 neutral distractors
        win.flip()
            
        #SEARCH TASK: wait for response
        #io.clearEvents('all')
        eventClock.reset()
        keyResp.status = NOT_STARTED
        searchErrorCode = -1
        searchErrorName = ''
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
                
                
            #check for a keyboard response
            theseKeys = event.getKeys(keyList=['up','down'])
            if len(theseKeys) > 0: #test if atleast one key pressed
                if keyResp.keys == []:
                    keyResp.keys = theseKeys[-1] #just the last key pressed
                    keyResp.rt = keyResp.clock.getTime()
                    searchResponse = keyResp.keys
                    searchRT = keyResp.rt
                    noResponseYet = False
                    if (targetOri != 90 and keyResp.keys=='up') or (targetOri != 270 and keyResp.keys=='down'):
                        searchErrorCode = 2
                        searchErrorName = "Incorrect response"
            
            
            
            # check for quit (the [Esc] key)
            if event.getKeys(["escape"]):
                core.quit()

        #Search delay
        for item in range (0, NUM_TARGET_POS):
            searchStim[item].setAutoDraw(False)
        win.flip()
        
    else:
        
        #Evaluation Task
        fixationVertical.setAutoDraw(False); fixationHorizontal.setAutoDraw(False)
        evalTextOnScreen = visual.TextStim(win=win, ori=0, name='evalTextOnScreen', text='Evaluate',    font=u'Arial', pos=[0, 0], height=0.75, wrapWidth=None, color='black', colorSpace=u'rgb', opacity=1, depth=-1.0)
        evalTextOnScreen.setAutoDraw(True)
        win.flip()
        if trialsArray[curRow][5] == 0:
            while trialClock.getTime() < EVAL_TEXT_TIME + EVAL_BEFORE_RETRO_BLANK + FIRST_RETENTION_INTERVAL + STIM_TIME + FIXATION_TIME + MEMORY_TEXT_TIME: pass
        if trialsArray[curRow][5] == 1:
            while trialClock.getTime() < EVAL_TEXT_TIME + SECOND_RETENTION_INTERVAL + FIRST_CUE_TIME + FIRST_RETENTION_INTERVAL + STIM_TIME + FIXATION_TIME + MEMORY_TEXT_TIME:pass
        evalTextOnScreen.setAutoDraw(False)
        
        

        ratingScaleText.setAutoDraw(True)

        win.flip()
        if trialsArray[curRow][5] == 0:
            while trialClock.getTime() < EVAL_FIXATION_TIME + EVAL_TEXT_TIME + EVAL_BEFORE_RETRO_BLANK + FIRST_RETENTION_INTERVAL + STIM_TIME + FIXATION_TIME + MEMORY_TEXT_TIME: pass
        if trialsArray[curRow][5] == 1:
            while trialClock.getTime() < EVAL_FIXATION_TIME + EVAL_TEXT_TIME + SECOND_RETENTION_INTERVAL + FIRST_CUE_TIME + FIRST_RETENTION_INTERVAL + STIM_TIME + FIXATION_TIME + MEMORY_TEXT_TIME:pass
        #Create evaluated stimulus
        evaluatedstimulus = visual.ImageStim(win=win,image = evalImgName, pos=[0,0], size=(SIZE,SIZE))
        evaluatedstimulus.setAutoDraw(True)
        win.flip()
        

        eventClock.reset()
        stimOnScreen = True
        keyResp.status = NOT_STARTED
        evalErrorCode = -1
        evalErrorName = ''
        noResponseYet = True
        probeOnScreen = True
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
                
                
            #check for a keyboard response
            theseKeys = event.getKeys(keyList=['1','2','3','4'])
            if len(theseKeys) > 0: #test if atleast one key pressed
                if keyResp.keys == []:
                    keyResp.keys = theseKeys[-1] #just the last key pressed
                    keyResp.rt = keyResp.clock.getTime()
                    evalResponse = keyResp.keys
                    evalRT = keyResp.rt
                    noResponseYet = False
            
            if stimOnScreen and t > EVAL_STIM_ON_SCREEN:
                evaluatedstimulus.setAutoDraw(False)
                win.flip()
                stimOnScreen = False
            
            
            # check for quit (the [Esc] key)
            if event.getKeys(["escape"]):
                core.quit()

        
        
        fixationVertical.setAutoDraw(True);fixationHorizontal.setAutoDraw(True)
        evaluatedstimulus.setAutoDraw(False)
        ratingScaleText.setAutoDraw(False)
        win.flip()
        if trialsArray[curRow][5] == 0:
            while trialClock.getTime() < FIXATION_TIME + evalRT + EVAL_FIXATION_TIME + EVAL_TEXT_TIME + EVAL_BEFORE_RETRO_BLANK + FIRST_RETENTION_INTERVAL + STIM_TIME + FIXATION_TIME + MEMORY_TEXT_TIME: pass
        if trialsArray[curRow][5] == 1:
            while trialClock.getTime() < FIXATION_TIME + evalRT + EVAL_FIXATION_TIME + EVAL_TEXT_TIME + SECOND_RETENTION_INTERVAL + FIRST_CUE_TIME + FIRST_RETENTION_INTERVAL + STIM_TIME + FIXATION_TIME + MEMORY_TEXT_TIME:pass





        if trialsArray[curRow][5] == 0:
            #Fixation on Screen
            fixationVertical.setAutoDraw(True);fixationHorizontal.setAutoDraw(True)
            win.flip()
            while trialClock.getTime() < FIXATION_TIME + FIXATION_TIME + evalRT + EVAL_FIXATION_TIME + EVAL_TEXT_TIME + EVAL_BEFORE_RETRO_BLANK + FIRST_RETENTION_INTERVAL + STIM_TIME + FIXATION_TIME + MEMORY_TEXT_TIME: pass
            
            #First cue arrow on screen
            firstCueArrow.setAutoDraw(True)
            #Take fixation cross off screen
            fixationVertical.setAutoDraw(False);fixationHorizontal.setAutoDraw(False)
            win.flip()
            while trialClock.getTime() < FIRST_CUE_TIME + FIXATION_TIME + FIXATION_TIME + evalRT + EVAL_FIXATION_TIME + EVAL_TEXT_TIME + EVAL_BEFORE_RETRO_BLANK + FIRST_RETENTION_INTERVAL + STIM_TIME + FIXATION_TIME + MEMORY_TEXT_TIME: pass
        
            #Fixation on Screen
            fixationVertical.setAutoDraw(True);fixationHorizontal.setAutoDraw(True)
            #Take off first cue arrow
            firstCueArrow.setAutoDraw(False)
            win.flip()
            while trialClock.getTime() < SECOND_RETENTION_INTERVAL + FIRST_CUE_TIME + FIXATION_TIME + FIXATION_TIME + evalRT + EVAL_FIXATION_TIME + EVAL_TEXT_TIME + EVAL_BEFORE_RETRO_BLANK + FIRST_RETENTION_INTERVAL + STIM_TIME + FIXATION_TIME + MEMORY_TEXT_TIME: pass
            fixationVertical.setAutoDraw(False);fixationHorizontal.setAutoDraw(False)
        if trialsArray[curRow][5] == 1:
            while trialClock.getTime() < EVAL_AFTER_RETRO_BLANK + FIXATION_TIME + evalRT + EVAL_FIXATION_TIME + EVAL_TEXT_TIME + SECOND_RETENTION_INTERVAL + FIRST_CUE_TIME + FIRST_RETENTION_INTERVAL + STIM_TIME + FIXATION_TIME + MEMORY_TEXT_TIME:pass


        #Back to Memory Task
        fixationVertical.setAutoDraw(False);fixationHorizontal.setAutoDraw(False)
        rememberTextOnScreen = visual.TextStim(win=win, ori=0, name='rememberTextOnScreen', text='Same?',    font=u'Arial', pos=[0, 0], height=0.75, wrapWidth=None, color='black', colorSpace=u'rgb', opacity=1, depth=-1.0)
        rememberTextOnScreen.setAutoDraw(True)
        win.flip()
        if trialsArray[curRow][5] == 0:
            while trialClock.getTime() < REMEMBER_TEXT_TIME + SECOND_RETENTION_INTERVAL + FIRST_CUE_TIME + FIXATION_TIME + FIXATION_TIME + evalRT + EVAL_FIXATION_TIME + EVAL_TEXT_TIME + EVAL_BEFORE_RETRO_BLANK + FIRST_RETENTION_INTERVAL + STIM_TIME + FIXATION_TIME + MEMORY_TEXT_TIME: pass
        if trialsArray[curRow][5] == 1:
            while trialClock.getTime() < REMEMBER_TEXT_TIME + EVAL_AFTER_RETRO_BLANK + FIXATION_TIME + evalRT + EVAL_FIXATION_TIME + EVAL_TEXT_TIME + SECOND_RETENTION_INTERVAL + FIRST_CUE_TIME + FIRST_RETENTION_INTERVAL + STIM_TIME + FIXATION_TIME + MEMORY_TEXT_TIME:pass
        rememberTextOnScreen.setAutoDraw(False)
        
        
        
        
        fixationVertical.setAutoDraw(True);fixationHorizontal.setAutoDraw(True)
        win.flip()
        if trialsArray[curRow][5] == 0:
            while trialClock.getTime() < FIXATION_TIME + REMEMBER_TEXT_TIME + SECOND_RETENTION_INTERVAL + FIRST_CUE_TIME + FIXATION_TIME + FIXATION_TIME + evalRT + EVAL_FIXATION_TIME + EVAL_TEXT_TIME + EVAL_BEFORE_RETRO_BLANK + FIRST_RETENTION_INTERVAL + STIM_TIME + FIXATION_TIME + MEMORY_TEXT_TIME: pass
        if trialsArray[curRow][5] == 1:
            while trialClock.getTime() < FIXATION_TIME + REMEMBER_TEXT_TIME + EVAL_AFTER_RETRO_BLANK + FIXATION_TIME + evalRT + EVAL_FIXATION_TIME + EVAL_TEXT_TIME + SECOND_RETENTION_INTERVAL + FIRST_CUE_TIME + FIRST_RETENTION_INTERVAL + STIM_TIME + FIXATION_TIME + MEMORY_TEXT_TIME:pass
        fixationVertical.setAutoDraw(False);fixationHorizontal.setAutoDraw(False)
        
        
        
    #First Probe
        firstProbeRand = random.randint(0,2)#Random number for if it's an uncued stimulus being probed
        firstPosition = POSARRAY[firstCuePos]#position of first cued stimulus
        firstCuedUncuedRand = random.randint(0,1)#Random number for whether cued or uncued is probed
        if firstCuedUncuedRand == 0:#Cued Stim is Probed
            if colourArray.index('Blue') < 4:
                if firstPosition == BluePos:FirstProbe = visual.ImageStim(win=win,image= 'Images/Blue/Blue' + str(BlueCount) + '.bmp', pos= [0,0], size=(SIZE,SIZE));firstProbeStim = 'Blue' + str(BlueCount)
            if colourArray.index('Green') < 4:
                if firstPosition == GreenPos:FirstProbe = visual.ImageStim(win=win,image= 'Images/Green/Green' + str(GreenCount) + '.bmp', pos= [0,0], size=(SIZE,SIZE));firstProbeStim = 'Green' + str(GreenCount)
            if colourArray.index('Purple') < 4:
                if firstPosition == PurplePos:FirstProbe = visual.ImageStim(win=win,image= 'Images/Purple/Purple' + str(PurpleCount) + '.bmp', pos= [0,0], size=(SIZE,SIZE));firstProbeStim = 'Purple' + str(PurpleCount)
            if colourArray.index('Pink') < 4:
                if firstPosition == PinkPos:FirstProbe = visual.ImageStim(win=win,image= 'Images/Pink/Pink' + str(PinkCount) + '.bmp', pos= [0,0], size=(SIZE,SIZE));firstProbeStim = 'Pink' + str(PinkCount)
            if colourArray.index('Orange') < 4:
                if firstPosition == OrangePos:FirstProbe = visual.ImageStim(win=win,image= 'Images/Orange/Orange' + str(OrangeCount) + '.bmp', pos= [0,0], size=(SIZE,SIZE));firstProbeStim = 'Orange' + str(OrangeCount)
        if firstCuedUncuedRand == 1:#Uncued Stim is Probed
            UncuedProbedStim = POSARRAY.index(firstPosition)
            if UncuedProbedStim == 0:
                if firstProbeRand == 0:FirstProbePos = POSARRAY[1]
                if firstProbeRand == 1:FirstProbePos = POSARRAY[2]
                if firstProbeRand == 2:FirstProbePos = POSARRAY[3]
            if UncuedProbedStim == 1:
                if firstProbeRand == 0:FirstProbePos = POSARRAY[0]
                if firstProbeRand == 1:FirstProbePos = POSARRAY[2]
                if firstProbeRand == 2:FirstProbePos = POSARRAY[3]
            if UncuedProbedStim == 2:
                if firstProbeRand == 0:FirstProbePos = POSARRAY[0]
                if firstProbeRand == 1:FirstProbePos = POSARRAY[1]
                if firstProbeRand == 2:FirstProbePos = POSARRAY[3]
            if UncuedProbedStim == 3:
                if firstProbeRand == 0:FirstProbePos = POSARRAY[0]
                if firstProbeRand == 1:FirstProbePos = POSARRAY[1]
                if firstProbeRand == 2:FirstProbePos = POSARRAY[2]
            
            if colourArray.index('Blue') < 4:
                if FirstProbePos == BluePos:FirstProbe = visual.ImageStim(win=win,image= 'Images/Blue/Blue' + str(BlueCount) + '.bmp', pos= [0,0], size=(SIZE,SIZE));firstProbeStim = 'Blue' + str(BlueCount)
            if colourArray.index('Green') < 4:
                if FirstProbePos == GreenPos:FirstProbe = visual.ImageStim(win=win,image= 'Images/Green/Green' + str(GreenCount) + '.bmp', pos= [0,0], size=(SIZE,SIZE));firstProbeStim = 'Green' + str(GreenCount)
            if colourArray.index('Purple') < 4:
                if FirstProbePos == PurplePos:FirstProbe = visual.ImageStim(win=win,image= 'Images/Purple/Purple' + str(PurpleCount) + '.bmp', pos= [0,0], size=(SIZE,SIZE));firstProbeStim = 'Purple' + str(PurpleCount)
            if colourArray.index('Pink') < 4:
                if FirstProbePos == PinkPos:FirstProbe = visual.ImageStim(win=win,image= 'Images/Pink/Pink' + str(PinkCount) + '.bmp', pos= [0,0], size=(SIZE,SIZE));firstProbeStim = 'Pink' + str(PinkCount)
            if colourArray.index('Orange') < 4:
                if FirstProbePos == OrangePos:FirstProbe = visual.ImageStim(win=win,image= 'Images/Orange/Orange' + str(OrangeCount) + '.bmp', pos= [0,0], size=(SIZE,SIZE));firstProbeStim = 'Orange' + str(OrangeCount)
                
                
        FirstProbe.setAutoDraw(True)
        win.flip()
        
        
        
        eventClock.reset()
        stimOnScreen = True
        keyResp.status = NOT_STARTED
        firstProbeErrorCode = -1
        firstProbeErrorName = ''
        noResponseYet = True
        probeOnScreen = True
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
                
                
            #check for a keyboard response
            theseKeys = event.getKeys(keyList=['up','down'])
            if noResponseYet == True:
                if len(theseKeys) > 0: #test if atleast one key pressed
                    if keyResp.keys == []:
                        FirstProbe.setAutoDraw(False)
                        keyResp.keys = theseKeys[-1] #just the last key pressed
                        keyResp.rt = keyResp.clock.getTime()
                        FirstProbeResponse = keyResp.keys
                        FirstProbeRT = keyResp.rt
                        if buttonCounterbalance == 0:
                            if keyResp.keys == 'up' and firstCuedUncuedRand == 1:
                               firstProbeErrorCode = 2
                               firstProbeErrorName = 'incorrect response'
                            if keyResp.keys == 'down' and firstCuedUncuedRand == 0:
                               firstProbeErrorCode = 2
                               firstProbeErrorName = 'incorrect response'
                        if buttonCounterbalance == 1:
                            if keyResp.keys == 'down' and firstCuedUncuedRand == 1:
                               firstProbeErrorCode = 2
                               firstProbeErrorName = 'incorrect response'
                            if keyResp.keys == 'up' and firstCuedUncuedRand == 0:
                               firstProbeErrorCode = 2
                               firstProbeErrorName = 'incorrect response'
                        noResponseYet = False
            
            if stimOnScreen and t > FIRST_PROBE_ON_SCREEN:
                FirstProbe.setAutoDraw(False)
                win.flip()
                stimOnScreen = False
            
            
            # check for quit (the [Esc] key)
            if event.getKeys(["escape"]):
                core.quit()

        FirstProbe.setAutoDraw(False)
        
        fixationVertical.setAutoDraw(True);fixationHorizontal.setAutoDraw(True)
        win.flip()
        
        if trialsArray[curRow][5] == 0:
            while trialClock.getTime() < THIRD_RETENTION_INTERVAL + FirstProbeRT + FIXATION_TIME + REMEMBER_TEXT_TIME + SECOND_RETENTION_INTERVAL + FIRST_CUE_TIME + FIXATION_TIME + FIXATION_TIME + evalRT + EVAL_FIXATION_TIME + EVAL_TEXT_TIME + EVAL_BEFORE_RETRO_BLANK + FIRST_RETENTION_INTERVAL + STIM_TIME + FIXATION_TIME + MEMORY_TEXT_TIME: pass
        if trialsArray[curRow][5] == 1:
            while trialClock.getTime() < THIRD_RETENTION_INTERVAL + FirstProbeRT + FIXATION_TIME + REMEMBER_TEXT_TIME + EVAL_AFTER_RETRO_BLANK + FIXATION_TIME + evalRT + EVAL_FIXATION_TIME + EVAL_TEXT_TIME + SECOND_RETENTION_INTERVAL + FIRST_CUE_TIME + FIRST_RETENTION_INTERVAL + STIM_TIME + FIXATION_TIME + MEMORY_TEXT_TIME:pass
        
        
        fixationVertical.setAutoDraw(False)
        fixationHorizontal.setAutoDraw(False)
        secondCueArrow.setAutoDraw(True)
        win.flip()
        if trialsArray[curRow][5] == 0:
            while trialClock.getTime() < SECOND_CUE_TIME + THIRD_RETENTION_INTERVAL + FirstProbeRT + FIXATION_TIME + REMEMBER_TEXT_TIME + SECOND_RETENTION_INTERVAL + FIRST_CUE_TIME + FIXATION_TIME + FIXATION_TIME + evalRT + EVAL_FIXATION_TIME + EVAL_TEXT_TIME + EVAL_BEFORE_RETRO_BLANK + FIRST_RETENTION_INTERVAL + STIM_TIME + FIXATION_TIME + MEMORY_TEXT_TIME: pass
        if trialsArray[curRow][5] == 1:
            while trialClock.getTime() < SECOND_CUE_TIME + THIRD_RETENTION_INTERVAL + FirstProbeRT + FIXATION_TIME + REMEMBER_TEXT_TIME + EVAL_AFTER_RETRO_BLANK + FIXATION_TIME + evalRT + EVAL_FIXATION_TIME + EVAL_TEXT_TIME + SECOND_RETENTION_INTERVAL + FIRST_CUE_TIME + FIRST_RETENTION_INTERVAL + STIM_TIME + FIXATION_TIME + MEMORY_TEXT_TIME:pass

        fixationVertical.setAutoDraw(True)
        fixationHorizontal.setAutoDraw(True)
        secondCueArrow.setAutoDraw(False)
        win.flip()
        if trialsArray[curRow][5] == 0:
            while trialClock.getTime() < FOURTH_RETENTION_INTERVAL + SECOND_CUE_TIME + THIRD_RETENTION_INTERVAL + FirstProbeRT + FIXATION_TIME + REMEMBER_TEXT_TIME + SECOND_RETENTION_INTERVAL + FIRST_CUE_TIME + FIXATION_TIME + FIXATION_TIME + evalRT + EVAL_FIXATION_TIME + EVAL_TEXT_TIME + EVAL_BEFORE_RETRO_BLANK + FIRST_RETENTION_INTERVAL + STIM_TIME + FIXATION_TIME + MEMORY_TEXT_TIME: pass
        if trialsArray[curRow][5] == 1:
            while trialClock.getTime() < FOURTH_RETENTION_INTERVAL + SECOND_CUE_TIME + THIRD_RETENTION_INTERVAL + FirstProbeRT + FIXATION_TIME + REMEMBER_TEXT_TIME + EVAL_AFTER_RETRO_BLANK + FIXATION_TIME + evalRT + EVAL_FIXATION_TIME + EVAL_TEXT_TIME + SECOND_RETENTION_INTERVAL + FIRST_CUE_TIME + FIRST_RETENTION_INTERVAL + STIM_TIME + FIXATION_TIME + MEMORY_TEXT_TIME:pass


    #Second Probe
        
        secondProbeRand = random.randint(0,2)#Random number for if it's an uncued stimulus being probed
        secondPosition = POSARRAY[secondCuePos]#position of second cued stimulus
        secondCuedUncuedRand = random.randint(0,1)#Random number for whether cued or uncued is probed
        if secondCuedUncuedRand == 0:#Cued Stim is Probed
            if colourArray.index('Blue') < 4:
                if secondPosition == BluePos:SecondProbe = visual.ImageStim(win=win,image= 'Images/Blue/Blue' + str(BlueCount) + '.bmp', pos= [0,0], size=(SIZE,SIZE));secondProbeStim = 'Blue' + str(BlueCount)
            if colourArray.index('Green') < 4:
                if secondPosition == GreenPos:SecondProbe = visual.ImageStim(win=win,image= 'Images/Green/Green' + str(GreenCount) + '.bmp', pos= [0,0], size=(SIZE,SIZE));secondProbeStim = 'Green' + str(GreenCount)
            if colourArray.index('Purple') < 4:
                if secondPosition == PurplePos:SecondProbe = visual.ImageStim(win=win,image= 'Images/Purple/Purple' + str(PurpleCount) + '.bmp', pos= [0,0], size=(SIZE,SIZE));secondProbeStim = 'Purple' + str(PurpleCount)
            if colourArray.index('Pink') < 4:
                if secondPosition == PinkPos:SecondProbe = visual.ImageStim(win=win,image= 'Images/Pink/Pink' + str(PinkCount) + '.bmp', pos= [0,0], size=(SIZE,SIZE));secondProbeStim = 'Pink' + str(PinkCount)
            if colourArray.index('Orange') < 4:
                if secondPosition == OrangePos:SecondProbe = visual.ImageStim(win=win,image= 'Images/Orange/Orange' + str(OrangeCount) + '.bmp', pos= [0,0], size=(SIZE,SIZE));secondProbeStim = 'Orange' + str(OrangeCount)
        if secondCuedUncuedRand == 1:#Uncued Stim is Probed
            UncuedProbedStim = POSARRAY.index(secondPosition)
            if UncuedProbedStim == 0:
                if secondProbeRand == 0:SecondProbePos= POSARRAY[1]
                if secondProbeRand == 1:SecondProbePos = POSARRAY[2]
                if secondProbeRand == 2:SecondProbePos = POSARRAY[3]
            if UncuedProbedStim == 1:
                if secondProbeRand == 0:SecondProbePos = POSARRAY[0]
                if secondProbeRand == 1:SecondProbePos = POSARRAY[2]
                if secondProbeRand == 2:SecondProbePos = POSARRAY[3]
            if UncuedProbedStim == 2:
                if secondProbeRand == 0:SecondProbePos = POSARRAY[0]
                if secondProbeRand == 1:SecondProbePos = POSARRAY[1]
                if secondProbeRand == 2:SecondProbePos = POSARRAY[3]
            if UncuedProbedStim == 3:
                if secondProbeRand == 0:SecondProbePos = POSARRAY[0]
                if secondProbeRand == 1:SecondProbePos = POSARRAY[1]
                if secondProbeRand == 2:SecondProbePos = POSARRAY[2]
            
            if colourArray.index('Blue') < 4:
                if SecondProbePos == BluePos:SecondProbe = visual.ImageStim(win=win,image= 'Images/Blue/Blue' + str(BlueCount) + '.bmp', pos= [0,0], size=(SIZE,SIZE));secondProbeStim = 'Blue' + str(BlueCount)
            if colourArray.index('Green') < 4:
                if SecondProbePos == GreenPos:SecondProbe = visual.ImageStim(win=win,image= 'Images/Green/Green' + str(GreenCount) + '.bmp', pos= [0,0], size=(SIZE,SIZE));secondProbeStim = 'Green' + str(GreenCount)
            if colourArray.index('Purple') < 4:
                if SecondProbePos == PurplePos:SecondProbe = visual.ImageStim(win=win,image= 'Images/Purple/Purple' + str(PurpleCount) + '.bmp', pos= [0,0], size=(SIZE,SIZE));secondProbeStim = 'Purple' + str(PurpleCount)
            if colourArray.index('Pink') < 4:
                if SecondProbePos == PinkPos:SecondProbe = visual.ImageStim(win=win,image= 'Images/Pink/Pink' + str(PinkCount) + '.bmp', pos= [0,0], size=(SIZE,SIZE));secondProbeStim = 'Pink' + str(PinkCount)
            if colourArray.index('Orange') < 4:
                if SecondProbePos == OrangePos:SecondProbe = visual.ImageStim(win=win,image= 'Images/Orange/Orange' + str(OrangeCount) + '.bmp', pos= [0,0], size=(SIZE,SIZE));secondProbeStim = 'Orange' + str(OrangeCount)
                
        SecondProbe.setAutoDraw(True)
        win.flip()
        
        
        
        
        eventClock.reset()
        stimOnScreen = True
        keyResp.status = NOT_STARTED
        secondProbeErrorCode = -1
        secondProbeErrorName = ''
        noResponseYet = True
        probeOnScreen = True
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
                
                
            #check for a keyboard response
            theseKeys = event.getKeys(keyList=['up','down'])
            if noResponseYet == True:
                if len(theseKeys) > 0: #test if atleast one key pressed
                    if keyResp.keys == []:
                        SecondProbe.setAutoDraw(False)
                        keyResp.keys = theseKeys[-1] #just the last key pressed
                        keyResp.rt = keyResp.clock.getTime()
                        SecondProbeResponse = keyResp.keys
                        SecondProbeRT = keyResp.rt
                        if buttonCounterbalance == 0:
                            if keyResp.keys == 'up' and secondCuedUncuedRand == 1:
                               secondProbeErrorCode = 2
                               secondProbeErrorName = 'incorrect response'
                            if keyResp.keys == 'down' and secondCuedUncuedRand == 0:
                               secondProbeErrorCode = 2
                               secondProbeErrorName = 'incorrect response'
                        if buttonCounterbalance == 1:
                            if keyResp.keys == 'down' and secondCuedUncuedRand == 1:
                               secondProbeErrorCode = 2
                               secondProbeErrorName = 'incorrect response'
                            if keyResp.keys == 'up' and secondCuedUncuedRand == 0:
                               secondProbeErrorCode = 2
                               secondProbeErrorName = 'incorrect response'
                        noResponseYet = False
            
            if stimOnScreen and t > FIRST_PROBE_ON_SCREEN:
                SecondProbe.setAutoDraw(False)
                win.flip()
                stimOnScreen = False
            
            
            # check for quit (the [Esc] key)
            if event.getKeys(["escape"]):
                core.quit()

        SecondProbe.setAutoDraw(False)

        fixationVertical.setAutoDraw(True);fixationHorizontal.setAutoDraw(True)
        win.flip()
    
    
    #Inter-trial interval
    eventClock.reset()
    fixationHorizontal.setAutoDraw(False);fixationVertical.setAutoDraw(False)
    win.flip()
    while eventClock.getTime() < INTER_TRIAL_INTERVAL: pass
    
    if trialsArray[curRow][5] == 0 or trialsArray[curRow][5] == 1:
        fourTrialsAgo = threeTrialsAgo
        threeTrialsAgo = twoTrialsAgo
        twoTrialsAgo = previousTrial
        previousTrial = 0
        if firstProbeErrorCode == -1 and secondProbeErrorCode == -1:
           previousTrial = 1
        lastFourTrialsArray = [previousTrial,twoTrialsAgo,threeTrialsAgo,fourTrialsAgo]
        totalACC = previousTrial + twoTrialsAgo + threeTrialsAgo + fourTrialsAgo
        accValue = totalACC/4
        if totalTrials > 3:
            if accValue > .8:
               STIM_TIME = STIM_TIME - 0.05
            if accValue < .7:
               STIM_TIME = STIM_TIME + 0.05
        
        if STIM_TIME < 0.15:
            STIM_TIME = 0.15
        if STIM_TIME > 1.0:
            STIM_TIME = 1.0
    
    
    blocktrial = blocktrial + 1
    totalTrials = totalTrials + 1
    
    if blocktrial == 16:
        blocktrial = 0
        breakTextOnScreen = visual.TextStim(win=win, ori=0, name='breakTextOnScreen', text='Take a Quick Break\nPress the space bar to start the next block...',    font=u'Arial', pos=[0, 0], height=0.75, wrapWidth=None, color='black', colorSpace=u'rgb', opacity=1, depth=-1.0)
        buttonReminderTextOnScreen = visual.TextStim(win=win, ori=0, name='buttonReminderTextOnScreen', text='Remember, press the ' + butVar1 + ' key to answer YES. Press the ' + butVar2 + ' key to answer NO.',    font=u'Arial', pos=[0, -3], height=0.75, wrapWidth=40, color='black', colorSpace=u'rgb', opacity=1, depth=-1.0)
        breakTextOnScreen.setAutoDraw(True)
        buttonReminderTextOnScreen.setAutoDraw(True)
        win.flip()
        event.waitKeys()

        breakTextOnScreen.setAutoDraw(False)
        buttonReminderTextOnScreen.setAutoDraw(False)
        win.flip()
 
    outStr = str(runTime) + '\t'
    outStr = outStr + str(totalTrials) + '\t'
    outStr = outStr + str(TrialType) + '\t'
    outStr = outStr + 'Blue' + str(BlueCount) + '\t'
    if colourArray.index('Blue') < 4:
        outStr = outStr + str(POSARRAY[colourArray.index('Blue')]) + '\t'
    if colourArray.index('Blue') == 4:
        outStr = outStr + 'novelcolour' + '\t'
    outStr = outStr + 'Green' + str(GreenCount) + '\t'
    if colourArray.index('Green') < 4:
        outStr = outStr + str(POSARRAY[colourArray.index('Green')]) + '\t'
    if colourArray.index('Green') == 4:
        outStr = outStr + 'novelcolour' + '\t'
    outStr = outStr + 'Purple' + str(PurpleCount) + '\t'
    if colourArray.index('Purple') < 4:
        outStr = outStr + str(POSARRAY[colourArray.index('Purple')]) + '\t'
    if colourArray.index('Purple') == 4:
        outStr = outStr + 'novelcolour' + '\t'
    outStr = outStr + 'Pink' + str(PinkCount) + '\t'
    if colourArray.index('Pink') < 4:
        outStr = outStr + str(POSARRAY[colourArray.index('Pink')]) + '\t'
    if colourArray.index('Pink') == 4:
        outStr = outStr + 'novelcolour' + '\t'
    outStr = outStr + 'Orange' + str(OrangeCount) + '\t'
    if colourArray.index('Orange') < 4:
        outStr = outStr + str(POSARRAY[colourArray.index('Orange')]) + '\t'
    if colourArray.index('Orange') == 4:
        outStr = outStr + 'novelcolour' + '\t'
    if firstCuePos == 0 or firstCuePos == 1:
        outStr = outStr + '0' + '\t'
    if firstCuePos == 2 or firstCuePos == 3:
        outStr = outStr + '1' + '\t'
    outStr = outStr + str(POSARRAY[firstCuePos]) + '\t'
    if trialsArray[curRow][5] < 2:
        outStr = outStr + str(secondPosition) + '\t'
        outStr = outStr + str(firstProbeStim) + '\t'
        outStr = outStr + str(firstCuedUncuedRand) + '\t'
        outStr = outStr + str(FirstProbeResponse) + '\t'
        if firstProbeErrorCode == -1:
            outStr = outStr + '1' + '\t'
        if firstProbeErrorCode == 2:
            outStr = outStr + '0' + '\t'
        if firstProbeErrorCode == 5:
            outStr = outStr + '0' + '\t'
        if firstProbeErrorCode == 6:
            outStr = outStr + '0' + '\t'
        outStr = outStr + str(FirstProbeRT) + '\t'
        outStr = outStr + str(firstProbeErrorCode) + '\t'
        outStr = outStr + str(firstProbeErrorName) + '\t'
        outStr = outStr + str(secondProbeStim) + '\t'
        outStr = outStr + str(secondCuedUncuedRand) + '\t'
        outStr = outStr + str(SecondProbeResponse) + '\t'
        if secondProbeErrorCode == -1:
            outStr = outStr + '1' + '\t'
        if secondProbeErrorCode == 2:
            outStr = outStr + '0' + '\t'
        if secondProbeErrorCode == 5:
            outStr = outStr + '0' + '\t'
        if secondProbeErrorCode == 6:
            outStr = outStr + '0' + '\t'
        outStr = outStr + str(SecondProbeRT) + '\t'
        outStr = outStr + str(secondProbeErrorCode) + '\t'
        outStr = outStr + str(secondProbeErrorName) + '\t'
        evalImgName2 = evalImgName.rsplit("/")[-1]
        outStr = outStr + str(evalImgName2) + '\t'
        outStr = outStr + str(trialsArray[curRow][4]) + '\t'
        outStr = outStr + str(evalResponse) + '\t'
        outStr = outStr + str(evalRT) + '\t'
        outStr = outStr + str(evalErrorCode) + '\t'
        outStr = outStr + str(evalErrorName) + '\t'
    if trialsArray[curRow][5] == 2:
        outStr = outStr + 'searchtask\tsearchtask\tsearchtask\tsearchtask\tsearchtask\tsearchtask\tsearchtask\tsearchtask\tsearchtask\tsearchtask\tsearchtask\tsearchtask\tsearchtask\tsearchtask\tsearchtask\tsearchtask\tsearchtask\tsearchtask\tsearchtask\tsearchtask\tsearchtask\t'
    outStr = outStr + str(STIM_TIME) + '\t'
    outStr = outStr + str(trialsArray[curRow][5]) + '\t'
    if trialsArray[curRow][5] == 2:
        outStr = outStr + str(singType) + '\t'
        outStr = outStr + str(singColName) + '\t'
        outStr = outStr + str(singPos) + '\t'
        if searchStim[1].ori == 0:
            outStr = outStr + 'left' + '\t'
        if searchStim[1].ori == 180:
            outStr = outStr + 'right' + '\t'
        if targetOri == 90:
            outStr = outStr + 'up' + '\t'
        if targetOri == 270:
            outStr = outStr + 'down' + '\t'
        outStr = outStr + str(tarPos) + '\t'
        outStr = outStr + str(searchResponse) + '\t'
        outStr = outStr + str(searchRT) + '\t'
        outStr = outStr + str(searchErrorCode) + '\t'
        outStr = outStr + str(searchErrorName) + '\t'
    if trialsArray[curRow][5] < 2:
        outStr = outStr + 'nosearch\tnosearch\tnosearch\tnosearch\tnosearch\tnosearch\tnosearch\tnosearch\tnosearch\tnosearch\t'
    outStr = outStr + '1' + '\t'
    outStr = outStr + str(expInfo2['age']) + '\t'
    outStr = outStr + str(expInfo3['gender']) + '\t'
    outStr = outStr + str(expInfo4['handedness']) + '\t'
    outStr = outStr + str(expInfo5['glasses/contacts?']) + '\t'
    outputFile.write(outStr + 'eol\n')

breakTextOnScreen = visual.TextStim(win=win, ori=0, name='breakTextOnScreen', text='The first half of the experiment is done.\nPlease go get the experimenter.',    font=u'Arial', pos=[0, 0], height=0.75, wrapWidth=None, color='black', colorSpace=u'rgb', opacity=1, depth=-1.0)
breakTextOnScreen.setAutoDraw(True)
win.flip()
event.waitKeys()
event.waitKeys()
event.waitKeys()
event.waitKeys()
event.waitKeys()
event.waitKeys()
event.waitKeys()
breakTextOnScreen.setAutoDraw(False)

Instruct1 = visual.ImageStim(win=win,image= 'Slide30.jpg', pos= [0,0], size=(36,23))
Instruct1.setAutoDraw(True)
win.flip()
event.waitKeys()
event.waitKeys()
Instruct1.setAutoDraw(False)


TrialType = "SecondHalf"

for trial in range(0, 136):
    random.shuffle(colourArray)
    
    runTime = time.strftime("%c")
    
    curRow = idxTrialsArray2[trial]
    
    
    #put memory task text on screen
    memTextOnScreen = visual.TextStim(win=win, ori=0, name='memTextOnScreen', text='Memorize',    font=u'Arial', pos=[0, 0], height=0.75, wrapWidth=None, color='black', colorSpace=u'rgb', opacity=1, depth=-1.0)
    memTextOnScreen.setAutoDraw(True)
    win.flip()
    trialClock.reset()
    while trialClock.getTime() < MEMORY_TEXT_TIME:pass
    
    #Fixation Cross
    memTextOnScreen.setAutoDraw(False)
    fixationVertical.setAutoDraw(True);fixationHorizontal.setAutoDraw(True)
    win.flip()
    while trialClock.getTime() < FIXATION_TIME + MEMORY_TEXT_TIME: pass
    
    #Decide Positions of Each Color
    FirstColour = colourArray[0]
    SecondColour = colourArray[1]
    ThirdColour = colourArray[2]
    FourthColour = colourArray[3]
    FirstPos = POSARRAY[0]
    SecondPos = POSARRAY[1]
    ThirdPos = POSARRAY[2]
    FourthPos = POSARRAY[3]
    
    #Create Stimuli
    BlueStimCount = BlueStimCount + 1
    GreenStimCount = GreenStimCount + 1
    PurpleStimCount = PurpleStimCount + 1
    PinkStimCount = PinkStimCount + 1
    OrangeStimCount = OrangeStimCount + 1
    BlueCount = idxBlueStim[BlueStimCount]
    GreenCount = idxGreenStim[GreenStimCount]
    PurpleCount = idxPurpleStim[PurpleStimCount]
    PinkCount = idxPinkStim[PinkStimCount]
    OrangeCount = idxOrangeStim[OrangeStimCount]
    
    if colourArray.index('Blue') < 4:
        BluePos = POSARRAY[colourArray.index('Blue')]
        FirstItem = visual.ImageStim(win=win,image= 'Images/Blue/Blue' + str(BlueCount) + '.bmp', pos= BluePos, size=(SIZE,SIZE))
    if colourArray.index('Green') < 4:
        GreenPos = POSARRAY[colourArray.index('Green')]
        SecondItem = visual.ImageStim(win=win,image= 'Images/Green/Green' + str(GreenCount) + '.bmp', pos= GreenPos, size=(SIZE,SIZE))
    if colourArray.index('Purple') < 4:
        PurplePos = POSARRAY[colourArray.index('Purple')]
        ThirdItem = visual.ImageStim(win=win,image= 'Images/Purple/Purple' + str(PurpleCount) + '.bmp', pos= PurplePos, size=(SIZE,SIZE))
    if colourArray.index('Pink') < 4:
        PinkPos = POSARRAY[colourArray.index('Pink')]
        FourthItem = visual.ImageStim(win=win,image= 'Images/Pink/Pink' + str(PinkCount) + '.bmp', pos= PinkPos, size=(SIZE,SIZE))
    if colourArray.index('Orange') < 4:
        OrangePos = POSARRAY[colourArray.index('Orange')]
        if colourArray.index('Blue') == 4:
            FirstItem = visual.ImageStim(win=win,image= 'Images/Orange/Orange' + str(OrangeCount) + '.bmp', pos= OrangePos, size=(SIZE,SIZE))
        if colourArray.index('Green') == 4:
            SecondItem = visual.ImageStim(win=win,image= 'Images/Orange/Orange' + str(OrangeCount) + '.bmp', pos= OrangePos, size=(SIZE,SIZE))
        if colourArray.index('Purple') == 4:
            ThirdItem = visual.ImageStim(win=win,image= 'Images/Orange/Orange' + str(OrangeCount) + '.bmp', pos= OrangePos, size=(SIZE,SIZE))
        if colourArray.index('Pink') == 4:
            FourthItem = visual.ImageStim(win=win,image= 'Images/Orange/Orange' + str(OrangeCount) + '.bmp', pos= OrangePos, size=(SIZE,SIZE))
            
    
    #Put Stimulus Array on Screen
    FirstItem.setAutoDraw(True);SecondItem.setAutoDraw(True);ThirdItem.setAutoDraw(True);FourthItem.setAutoDraw(True)
    win.flip()
    while trialClock.getTime() < STIM_TIME + FIXATION_TIME + MEMORY_TEXT_TIME: pass
    
    #Take Stimulus Array off Screen
    FirstItem.setAutoDraw(False);SecondItem.setAutoDraw(False);ThirdItem.setAutoDraw(False);FourthItem.setAutoDraw(False)
    win.flip()
    while trialClock.getTime() < FIRST_RETENTION_INTERVAL + STIM_TIME + FIXATION_TIME + MEMORY_TEXT_TIME: pass

    #decide where first cue points
    if trialsArray2[curRow][1] == 0 and trialsArray2[curRow][2] == 0:firstCuePos=1#left top
    if trialsArray2[curRow][1] == 0 and trialsArray2[curRow][2] == 1:firstCuePos=0#left bottom
    if trialsArray2[curRow][1] == 1 and trialsArray2[curRow][2] == 0:firstCuePos=2#right top
    if trialsArray2[curRow][1] == 1 and trialsArray2[curRow][2] == 1:firstCuePos=3#right bottom
    firstCueArrow = visual.ImageStim(win=win,image= arrowArray[firstCuePos], pos= [0,0], size=(1,1))
        
    if trialsArray2[curRow][5] == 0 or trialsArray2[curRow][5] == 1:
        #where second cue points
        if firstCuePos == 0:#left bottom
            if trialsArray2[curRow][3] == 0:secondCuePos=2#diagonal from left bottom is right top
            if trialsArray2[curRow][3] == 1:secondCuePos=3#horizontal from left bottom is right bottom
        if firstCuePos == 1:#left top
            if trialsArray2[curRow][3] == 0:secondCuePos=3#diagonal from left top is right bottom
            if trialsArray2[curRow][3] == 1:secondCuePos=2#horizontal from left top is right top
        if firstCuePos == 2:#right top
            if trialsArray2[curRow][3] == 0:secondCuePos=0#diagonal from right top is left bottom
            if trialsArray2[curRow][3] == 1:secondCuePos=1#horizontal from right top is left top
        if firstCuePos == 3:#right bottom
            if trialsArray2[curRow][3] == 0:secondCuePos=1#diagonal from right bottom is left top
            if trialsArray2[curRow][3] == 1:secondCuePos=0#horizontal from right bottom is left bottom

        secondCueArrow = visual.ImageStim(win=win,image= arrowArray[secondCuePos], pos= [0,0], size=(1,1))

            
        #Find out position of evaluated stimulus
        if trialsArray2[curRow][4] == 0:#NeverCuedStimSecondCuedSide
            if secondCuePos==0:EvalPos=POSARRAY[1]
            if secondCuePos==1:EvalPos=POSARRAY[0]
            if secondCuePos==2:EvalPos=POSARRAY[3]
            if secondCuePos==3:EvalPos=POSARRAY[2]
        if trialsArray2[curRow][4] == 1:#FirstCuedStim
            EvalPos=POSARRAY[firstCuePos]
            

        #Determine which actual stimulus will be evaluated
        if colourArray.index('Blue') < 4:
            if EvalPos == BluePos:evalImgName = 'Images/Blue/Blue' + str(BlueCount) + '.bmp'
        if colourArray.index('Green') < 4:
            if EvalPos == GreenPos:evalImgName = 'Images/Green/Green' + str(GreenCount) + '.bmp'
        if colourArray.index('Purple') < 4:
            if EvalPos == PurplePos:evalImgName = 'Images/Purple/Purple' + str(PurpleCount) + '.bmp'
        if colourArray.index('Pink') < 4:
            if EvalPos == PinkPos:evalImgName = 'Images/Pink/Pink' + str(PinkCount) + '.bmp'
        if colourArray.index('Orange') < 4:
            if EvalPos == OrangePos:evalImgName = 'Images/Orange/Orange' + str(OrangeCount) + '.bmp'


    if trialsArray2[curRow][5] == 0:#Evaluate before RetroCue
        while trialClock.getTime() < EVAL_BEFORE_RETRO_BLANK + FIRST_RETENTION_INTERVAL + STIM_TIME + FIXATION_TIME + MEMORY_TEXT_TIME: pass
    if trialsArray2[curRow][5] == 1 or trialsArray2[curRow][5] == 2:#Evaluate After RetroCue or SearchTask
        #First cue arrow on screen
        firstCueArrow.setAutoDraw(True)
        #Take fixation cross off screen
        fixationVertical.setAutoDraw(False);fixationHorizontal.setAutoDraw(False)
        win.flip()
        while trialClock.getTime() < FIRST_CUE_TIME + FIRST_RETENTION_INTERVAL + STIM_TIME + FIXATION_TIME + MEMORY_TEXT_TIME: pass
    
        #Fixation on Screen
        fixationVertical.setAutoDraw(True);fixationHorizontal.setAutoDraw(True)
        #Take off first cue arrow
        firstCueArrow.setAutoDraw(False)
        win.flip()
        while trialClock.getTime() < SECOND_RETENTION_INTERVAL + FIRST_CUE_TIME + FIRST_RETENTION_INTERVAL + STIM_TIME + FIXATION_TIME + MEMORY_TEXT_TIME: pass
    if trialsArray2[curRow][5] == 2:#Search Task
        #determine singleton type
        singType = trialsArray2[curRow][6]#0=activematching,1=accessorymatching,2=novelcolour
        #setup target locations in a circle around fixation
        targetPositions = []
        for pos in range(0, NUM_TARGET_POS):#8 target positions
            angle = math.radians(360 / NUM_TARGET_POS * pos)
            targetPositions.append([math.cos(angle)*SEARCH_ECCEN, math.sin(angle)*SEARCH_ECCEN])#setup target locations in a circle around fixation

        #set stimulus properties
        distractorOris = [0, 180] #orientations for the landolt c stimuli #gap pointing left or right for all distractors.
        idxDistractorOris = range(len(distractorOris))
        targetOris = [90,270]
        idxTargetOris = range(len(targetOris))

        #setup search stim 
        searchStim = [] #create a list of 8 distractor stim to be used on each trial -- these stim are all leftOpen so later on we will randomly assign them an orientation (90 or 180) so they become top/bottom open
        for distractor in range (0, NUM_SEARCH_POS):
            distractor = visual.ShapeStim(win, lineColorSpace='rgb', fillColorSpace = 'rgb', fillColor=bCol, lineColor=sCol, vertices=GetVertices(), closeShape=False, lineWidth = 9)
            searchStim.append(distractor)

        #set colour of singleton based on condition
        if singType == 0:#activematching
            singCol = colourArray[firstCuePos]
        elif singType == 1:#accessorymatching
            secondCuedRand = random.randint(0,1)#0=top,1=bottom
            if firstCuePos == 0 or firstCuePos == 1:
                if secondCuedRand == 0:
                    singCol = colourArray[2]
                if secondCuedRand == 1:
                    singCol = colourArray[3]
            if firstCuePos == 2 or firstCuePos == 3:
                if secondCuedRand == 0:
                    singCol = colourArray[1]
                if secondCuedRand == 1:
                    singCol = colourArray[0]
        else:#novelmatching
            singCol = colourArray[4]
            
        if singCol == 'Blue':
            singColName = 'Blue'
            singCol = [-.875,-.827,.639]
        if singCol == 'Green':
            singColName = 'Green'
            singCol = [-.671,.129,-.537]
        if singCol == 'Purple':
            singColName = 'Purple'
            singCol = [.545,-.576,.78]
        #if singCol == 'Yellow':
        #    singCol = [.843,.835,-.522]
        if singCol == 'Orange':
            singColName = 'Orange'
            singCol = [.435,-.255,-.741]
        if singCol == 'Pink':
            singColName = 'Pink'
            singCol = [.89,.231,.757]
        #if singCol == 'Red':
        #    singCol = [.075,-.757,-.725]
        
        random.shuffle(idxSearchPos) #randomly shuffle the list of positions in the search array

        #Search display #create 8 distractors
        for item in range (0, NUM_TARGET_POS):
            random.shuffle(idxDistractorOris)
            searchStim[item].ori=distractorOris[idxDistractorOris[0]]
            searchStim[item].pos = targetPositions[idxSearchPos[item]]
            searchStim[item].setAutoDraw(True)
            
        tarPos = searchStim[0].pos
        singPos = searchStim[1].pos

        #here you're changing one of the previously created distractors to be the target. So first item in SearchStim list is being changed to have targetOrientation.
        random.shuffle(idxTargetOris)
        targetPos = 0
        targetOri = targetOris[idxTargetOris[0]]
        searchStim[targetPos].ori=targetOri
        searchStim[targetPos].setAutoDraw(True)

        #here you're changing one of the previously created distractors to be the singleton. So second item in SearchStim list is being changed to singletoncolour.
        singletonPos = 1
#        if searchCond == 4:
        searchStim[singletonPos].setLineColor(singCol)
#        else:
#            searchStim[singletonPos].setLineColor('blue')
        searchStim[singletonPos].setAutoDraw(True)

        #put the whole search task on the screen including target, singleton, and 6 neutral distractors
        win.flip()
            
        #SEARCH TASK: wait for response
        #io.clearEvents('all')
        eventClock.reset()
        keyResp.status = NOT_STARTED
        searchErrorCode = -1
        searchErrorName = ''
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
                
                
            #check for a keyboard response
            theseKeys = event.getKeys(keyList=['up','down'])
            if len(theseKeys) > 0: #test if atleast one key pressed
                if keyResp.keys == []:
                    keyResp.keys = theseKeys[-1] #just the last key pressed
                    keyResp.rt = keyResp.clock.getTime()
                    searchResponse = keyResp.keys
                    searchRT = keyResp.rt
                    noResponseYet = False
                    if (targetOri != 90 and keyResp.keys=='up') or (targetOri != 270 and keyResp.keys=='down'):
                        searchErrorCode = 2
                        searchErrorName = "Incorrect response"
            
            
            
            # check for quit (the [Esc] key)
            if event.getKeys(["escape"]):
                core.quit()

        #Search delay
        for item in range (0, NUM_TARGET_POS):
            searchStim[item].setAutoDraw(False)
        win.flip()
        
    else:
        
        #Evaluation Task
        fixationVertical.setAutoDraw(False); fixationHorizontal.setAutoDraw(False)
        evalTextOnScreen = visual.TextStim(win=win, ori=0, name='evalTextOnScreen', text='Evaluate',    font=u'Arial', pos=[0, 0], height=0.75, wrapWidth=None, color='black', colorSpace=u'rgb', opacity=1, depth=-1.0)
        evalTextOnScreen.setAutoDraw(True)
        win.flip()
        if trialsArray2[curRow][5] == 0:
            while trialClock.getTime() < EVAL_TEXT_TIME + EVAL_BEFORE_RETRO_BLANK + FIRST_RETENTION_INTERVAL + STIM_TIME + FIXATION_TIME + MEMORY_TEXT_TIME: pass
        if trialsArray2[curRow][5] == 1:
            while trialClock.getTime() < EVAL_TEXT_TIME + SECOND_RETENTION_INTERVAL + FIRST_CUE_TIME + FIRST_RETENTION_INTERVAL + STIM_TIME + FIXATION_TIME + MEMORY_TEXT_TIME:pass
        evalTextOnScreen.setAutoDraw(False)
        
        

        ratingScaleText.setAutoDraw(True)

        win.flip()
        if trialsArray2[curRow][5] == 0:
            while trialClock.getTime() < EVAL_FIXATION_TIME + EVAL_TEXT_TIME + EVAL_BEFORE_RETRO_BLANK + FIRST_RETENTION_INTERVAL + STIM_TIME + FIXATION_TIME + MEMORY_TEXT_TIME: pass
        if trialsArray2[curRow][5] == 1:
            while trialClock.getTime() < EVAL_FIXATION_TIME + EVAL_TEXT_TIME + SECOND_RETENTION_INTERVAL + FIRST_CUE_TIME + FIRST_RETENTION_INTERVAL + STIM_TIME + FIXATION_TIME + MEMORY_TEXT_TIME:pass
        #Create evaluated stimulus
        evaluatedstimulus = visual.ImageStim(win=win,image = evalImgName, pos=[0,0], size=(SIZE,SIZE))
        evaluatedstimulus.setAutoDraw(True)
        win.flip()
        

        eventClock.reset()
        stimOnScreen = True
        keyResp.status = NOT_STARTED
        evalErrorCode = -1
        evalErrorName = ''
        noResponseYet = True
        probeOnScreen = True
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
                
                
            #check for a keyboard response
            theseKeys = event.getKeys(keyList=['1','2','3','4'])
            if len(theseKeys) > 0: #test if atleast one key pressed
                if keyResp.keys == []:
                    keyResp.keys = theseKeys[-1] #just the last key pressed
                    keyResp.rt = keyResp.clock.getTime()
                    evalResponse = keyResp.keys
                    evalRT = keyResp.rt
                    noResponseYet = False
            
            if stimOnScreen and t > EVAL_STIM_ON_SCREEN:
                evaluatedstimulus.setAutoDraw(False)
                win.flip()
                stimOnScreen = False
            
            
            # check for quit (the [Esc] key)
            if event.getKeys(["escape"]):
                core.quit()

        
        
        fixationVertical.setAutoDraw(True);fixationHorizontal.setAutoDraw(True)
        evaluatedstimulus.setAutoDraw(False)
        ratingScaleText.setAutoDraw(False)
        win.flip()
        if trialsArray2[curRow][5] == 0:
            while trialClock.getTime() < FIXATION_TIME + evalRT + EVAL_FIXATION_TIME + EVAL_TEXT_TIME + EVAL_BEFORE_RETRO_BLANK + FIRST_RETENTION_INTERVAL + STIM_TIME + FIXATION_TIME + MEMORY_TEXT_TIME: pass
        if trialsArray2[curRow][5] == 1:
            while trialClock.getTime() < FIXATION_TIME + evalRT + EVAL_FIXATION_TIME + EVAL_TEXT_TIME + SECOND_RETENTION_INTERVAL + FIRST_CUE_TIME + FIRST_RETENTION_INTERVAL + STIM_TIME + FIXATION_TIME + MEMORY_TEXT_TIME:pass





        if trialsArray2[curRow][5] == 0:
            #Fixation on Screen
            fixationVertical.setAutoDraw(True);fixationHorizontal.setAutoDraw(True)
            win.flip()
            while trialClock.getTime() < FIXATION_TIME + FIXATION_TIME + evalRT + EVAL_FIXATION_TIME + EVAL_TEXT_TIME + EVAL_BEFORE_RETRO_BLANK + FIRST_RETENTION_INTERVAL + STIM_TIME + FIXATION_TIME + MEMORY_TEXT_TIME: pass
            
            #First cue arrow on screen
            firstCueArrow.setAutoDraw(True)
            #Take fixation cross off screen
            fixationVertical.setAutoDraw(False);fixationHorizontal.setAutoDraw(False)
            win.flip()
            while trialClock.getTime() < FIRST_CUE_TIME + FIXATION_TIME + FIXATION_TIME + evalRT + EVAL_FIXATION_TIME + EVAL_TEXT_TIME + EVAL_BEFORE_RETRO_BLANK + FIRST_RETENTION_INTERVAL + STIM_TIME + FIXATION_TIME + MEMORY_TEXT_TIME: pass
        
            #Fixation on Screen
            fixationVertical.setAutoDraw(True);fixationHorizontal.setAutoDraw(True)
            #Take off first cue arrow
            firstCueArrow.setAutoDraw(False)
            win.flip()
            while trialClock.getTime() < SECOND_RETENTION_INTERVAL + FIRST_CUE_TIME + FIXATION_TIME + FIXATION_TIME + evalRT + EVAL_FIXATION_TIME + EVAL_TEXT_TIME + EVAL_BEFORE_RETRO_BLANK + FIRST_RETENTION_INTERVAL + STIM_TIME + FIXATION_TIME + MEMORY_TEXT_TIME: pass
            fixationVertical.setAutoDraw(False);fixationHorizontal.setAutoDraw(False)
        if trialsArray2[curRow][5] == 1:
            while trialClock.getTime() < EVAL_AFTER_RETRO_BLANK + FIXATION_TIME + evalRT + EVAL_FIXATION_TIME + EVAL_TEXT_TIME + SECOND_RETENTION_INTERVAL + FIRST_CUE_TIME + FIRST_RETENTION_INTERVAL + STIM_TIME + FIXATION_TIME + MEMORY_TEXT_TIME:pass


        #Back to Memory Task
        fixationVertical.setAutoDraw(False);fixationHorizontal.setAutoDraw(False)
        rememberTextOnScreen = visual.TextStim(win=win, ori=0, name='rememberTextOnScreen', text='Same?',    font=u'Arial', pos=[0, 0], height=0.75, wrapWidth=None, color='black', colorSpace=u'rgb', opacity=1, depth=-1.0)
        rememberTextOnScreen.setAutoDraw(True)
        win.flip()
        if trialsArray2[curRow][5] == 0:
            while trialClock.getTime() < REMEMBER_TEXT_TIME + SECOND_RETENTION_INTERVAL + FIRST_CUE_TIME + FIXATION_TIME + FIXATION_TIME + evalRT + EVAL_FIXATION_TIME + EVAL_TEXT_TIME + EVAL_BEFORE_RETRO_BLANK + FIRST_RETENTION_INTERVAL + STIM_TIME + FIXATION_TIME + MEMORY_TEXT_TIME: pass
        if trialsArray2[curRow][5] == 1:
            while trialClock.getTime() < REMEMBER_TEXT_TIME + EVAL_AFTER_RETRO_BLANK + FIXATION_TIME + evalRT + EVAL_FIXATION_TIME + EVAL_TEXT_TIME + SECOND_RETENTION_INTERVAL + FIRST_CUE_TIME + FIRST_RETENTION_INTERVAL + STIM_TIME + FIXATION_TIME + MEMORY_TEXT_TIME:pass
        rememberTextOnScreen.setAutoDraw(False)
        
        
        
        
        fixationVertical.setAutoDraw(True);fixationHorizontal.setAutoDraw(True)
        win.flip()
        if trialsArray2[curRow][5] == 0:
            while trialClock.getTime() < FIXATION_TIME + REMEMBER_TEXT_TIME + SECOND_RETENTION_INTERVAL + FIRST_CUE_TIME + FIXATION_TIME + FIXATION_TIME + evalRT + EVAL_FIXATION_TIME + EVAL_TEXT_TIME + EVAL_BEFORE_RETRO_BLANK + FIRST_RETENTION_INTERVAL + STIM_TIME + FIXATION_TIME + MEMORY_TEXT_TIME: pass
        if trialsArray2[curRow][5] == 1:
            while trialClock.getTime() < FIXATION_TIME + REMEMBER_TEXT_TIME + EVAL_AFTER_RETRO_BLANK + FIXATION_TIME + evalRT + EVAL_FIXATION_TIME + EVAL_TEXT_TIME + SECOND_RETENTION_INTERVAL + FIRST_CUE_TIME + FIRST_RETENTION_INTERVAL + STIM_TIME + FIXATION_TIME + MEMORY_TEXT_TIME:pass
        fixationVertical.setAutoDraw(False);fixationHorizontal.setAutoDraw(False)
        
        
        
    #First Probe
        firstProbeRand = random.randint(0,2)#Random number for if it's an uncued stimulus being probed
        firstPosition = POSARRAY[firstCuePos]#position of first cued stimulus
        firstCuedUncuedRand = random.randint(0,1)#Random number for whether cued or uncued is probed
        if firstCuedUncuedRand == 0:#Cued Stim is Probed
            if colourArray.index('Blue') < 4:
                if firstPosition == BluePos:FirstProbe = visual.ImageStim(win=win,image= 'Images/Blue/Blue' + str(BlueCount) + '.bmp', pos= [0,0], size=(SIZE,SIZE));firstProbeStim = 'Blue' + str(BlueCount)
            if colourArray.index('Green') < 4:
                if firstPosition == GreenPos:FirstProbe = visual.ImageStim(win=win,image= 'Images/Green/Green' + str(GreenCount) + '.bmp', pos= [0,0], size=(SIZE,SIZE));firstProbeStim = 'Green' + str(GreenCount)
            if colourArray.index('Purple') < 4:
                if firstPosition == PurplePos:FirstProbe = visual.ImageStim(win=win,image= 'Images/Purple/Purple' + str(PurpleCount) + '.bmp', pos= [0,0], size=(SIZE,SIZE));firstProbeStim = 'Purple' + str(PurpleCount)
            if colourArray.index('Pink') < 4:
                if firstPosition == PinkPos:FirstProbe = visual.ImageStim(win=win,image= 'Images/Pink/Pink' + str(PinkCount) + '.bmp', pos= [0,0], size=(SIZE,SIZE));firstProbeStim = 'Pink' + str(PinkCount)
            if colourArray.index('Orange') < 4:
                if firstPosition == OrangePos:FirstProbe = visual.ImageStim(win=win,image= 'Images/Orange/Orange' + str(OrangeCount) + '.bmp', pos= [0,0], size=(SIZE,SIZE));firstProbeStim = 'Orange' + str(OrangeCount)
        if firstCuedUncuedRand == 1:#Uncued Stim is Probed
            UncuedProbedStim = POSARRAY.index(firstPosition)
            if UncuedProbedStim == 0:
                if firstProbeRand == 0:FirstProbePos = POSARRAY[1]
                if firstProbeRand == 1:FirstProbePos = POSARRAY[2]
                if firstProbeRand == 2:FirstProbePos = POSARRAY[3]
            if UncuedProbedStim == 1:
                if firstProbeRand == 0:FirstProbePos = POSARRAY[0]
                if firstProbeRand == 1:FirstProbePos = POSARRAY[2]
                if firstProbeRand == 2:FirstProbePos = POSARRAY[3]
            if UncuedProbedStim == 2:
                if firstProbeRand == 0:FirstProbePos = POSARRAY[0]
                if firstProbeRand == 1:FirstProbePos = POSARRAY[1]
                if firstProbeRand == 2:FirstProbePos = POSARRAY[3]
            if UncuedProbedStim == 3:
                if firstProbeRand == 0:FirstProbePos = POSARRAY[0]
                if firstProbeRand == 1:FirstProbePos = POSARRAY[1]
                if firstProbeRand == 2:FirstProbePos = POSARRAY[2]
            
            if colourArray.index('Blue') < 4:
                if FirstProbePos == BluePos:FirstProbe = visual.ImageStim(win=win,image= 'Images/Blue/Blue' + str(BlueCount) + '.bmp', pos= [0,0], size=(SIZE,SIZE));firstProbeStim = 'Blue' + str(BlueCount)
            if colourArray.index('Green') < 4:
                if FirstProbePos == GreenPos:FirstProbe = visual.ImageStim(win=win,image= 'Images/Green/Green' + str(GreenCount) + '.bmp', pos= [0,0], size=(SIZE,SIZE));firstProbeStim = 'Green' + str(GreenCount)
            if colourArray.index('Purple') < 4:
                if FirstProbePos == PurplePos:FirstProbe = visual.ImageStim(win=win,image= 'Images/Purple/Purple' + str(PurpleCount) + '.bmp', pos= [0,0], size=(SIZE,SIZE));firstProbeStim = 'Purple' + str(PurpleCount)
            if colourArray.index('Pink') < 4:
                if FirstProbePos == PinkPos:FirstProbe = visual.ImageStim(win=win,image= 'Images/Pink/Pink' + str(PinkCount) + '.bmp', pos= [0,0], size=(SIZE,SIZE));firstProbeStim = 'Pink' + str(PinkCount)
            if colourArray.index('Orange') < 4:
                if FirstProbePos == OrangePos:FirstProbe = visual.ImageStim(win=win,image= 'Images/Orange/Orange' + str(OrangeCount) + '.bmp', pos= [0,0], size=(SIZE,SIZE));firstProbeStim = 'Orange' + str(OrangeCount)
                
                
        FirstProbe.setAutoDraw(True)
        win.flip()
        
        
        
        eventClock.reset()
        stimOnScreen = True
        keyResp.status = NOT_STARTED
        firstProbeErrorCode = -1
        firstProbeErrorName = ''
        noResponseYet = True
        probeOnScreen = True
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
                
                
            #check for a keyboard response
            theseKeys = event.getKeys(keyList=['up','down'])
            if noResponseYet == True:
                if len(theseKeys) > 0: #test if atleast one key pressed
                    if keyResp.keys == []:
                        FirstProbe.setAutoDraw(False)
                        keyResp.keys = theseKeys[-1] #just the last key pressed
                        keyResp.rt = keyResp.clock.getTime()
                        FirstProbeResponse = keyResp.keys
                        FirstProbeRT = keyResp.rt
                        if buttonCounterbalance == 0:
                            if keyResp.keys == 'up' and firstCuedUncuedRand == 1:
                               firstProbeErrorCode = 2
                               firstProbeErrorName = 'incorrect response'
                            if keyResp.keys == 'down' and firstCuedUncuedRand == 0:
                               firstProbeErrorCode = 2
                               firstProbeErrorName = 'incorrect response'
                        if buttonCounterbalance == 1:
                            if keyResp.keys == 'down' and firstCuedUncuedRand == 1:
                               firstProbeErrorCode = 2
                               firstProbeErrorName = 'incorrect response'
                            if keyResp.keys == 'up' and firstCuedUncuedRand == 0:
                               firstProbeErrorCode = 2
                               firstProbeErrorName = 'incorrect response'
                        noResponseYet = False
            
            if stimOnScreen and t > FIRST_PROBE_ON_SCREEN:
                FirstProbe.setAutoDraw(False)
                win.flip()
                stimOnScreen = False
            
            
            # check for quit (the [Esc] key)
            if event.getKeys(["escape"]):
                core.quit()

        FirstProbe.setAutoDraw(False)
        
        fixationVertical.setAutoDraw(True);fixationHorizontal.setAutoDraw(True)
        win.flip()
        
        if trialsArray2[curRow][5] == 0:
            while trialClock.getTime() < THIRD_RETENTION_INTERVAL + FirstProbeRT + FIXATION_TIME + REMEMBER_TEXT_TIME + SECOND_RETENTION_INTERVAL + FIRST_CUE_TIME + FIXATION_TIME + FIXATION_TIME + evalRT + EVAL_FIXATION_TIME + EVAL_TEXT_TIME + EVAL_BEFORE_RETRO_BLANK + FIRST_RETENTION_INTERVAL + STIM_TIME + FIXATION_TIME + MEMORY_TEXT_TIME: pass
        if trialsArray2[curRow][5] == 1:
            while trialClock.getTime() < THIRD_RETENTION_INTERVAL + FirstProbeRT + FIXATION_TIME + REMEMBER_TEXT_TIME + EVAL_AFTER_RETRO_BLANK + FIXATION_TIME + evalRT + EVAL_FIXATION_TIME + EVAL_TEXT_TIME + SECOND_RETENTION_INTERVAL + FIRST_CUE_TIME + FIRST_RETENTION_INTERVAL + STIM_TIME + FIXATION_TIME + MEMORY_TEXT_TIME:pass
        
        
        fixationVertical.setAutoDraw(False)
        fixationHorizontal.setAutoDraw(False)
        secondCueArrow.setAutoDraw(True)
        win.flip()
        if trialsArray2[curRow][5] == 0:
            while trialClock.getTime() < SECOND_CUE_TIME + THIRD_RETENTION_INTERVAL + FirstProbeRT + FIXATION_TIME + REMEMBER_TEXT_TIME + SECOND_RETENTION_INTERVAL + FIRST_CUE_TIME + FIXATION_TIME + FIXATION_TIME + evalRT + EVAL_FIXATION_TIME + EVAL_TEXT_TIME + EVAL_BEFORE_RETRO_BLANK + FIRST_RETENTION_INTERVAL + STIM_TIME + FIXATION_TIME + MEMORY_TEXT_TIME: pass
        if trialsArray2[curRow][5] == 1:
            while trialClock.getTime() < SECOND_CUE_TIME + THIRD_RETENTION_INTERVAL + FirstProbeRT + FIXATION_TIME + REMEMBER_TEXT_TIME + EVAL_AFTER_RETRO_BLANK + FIXATION_TIME + evalRT + EVAL_FIXATION_TIME + EVAL_TEXT_TIME + SECOND_RETENTION_INTERVAL + FIRST_CUE_TIME + FIRST_RETENTION_INTERVAL + STIM_TIME + FIXATION_TIME + MEMORY_TEXT_TIME:pass

        fixationVertical.setAutoDraw(True)
        fixationHorizontal.setAutoDraw(True)
        secondCueArrow.setAutoDraw(False)
        win.flip()
        if trialsArray2[curRow][5] == 0:
            while trialClock.getTime() < FOURTH_RETENTION_INTERVAL + SECOND_CUE_TIME + THIRD_RETENTION_INTERVAL + FirstProbeRT + FIXATION_TIME + REMEMBER_TEXT_TIME + SECOND_RETENTION_INTERVAL + FIRST_CUE_TIME + FIXATION_TIME + FIXATION_TIME + evalRT + EVAL_FIXATION_TIME + EVAL_TEXT_TIME + EVAL_BEFORE_RETRO_BLANK + FIRST_RETENTION_INTERVAL + STIM_TIME + FIXATION_TIME + MEMORY_TEXT_TIME: pass
        if trialsArray2[curRow][5] == 1:
            while trialClock.getTime() < FOURTH_RETENTION_INTERVAL + SECOND_CUE_TIME + THIRD_RETENTION_INTERVAL + FirstProbeRT + FIXATION_TIME + REMEMBER_TEXT_TIME + EVAL_AFTER_RETRO_BLANK + FIXATION_TIME + evalRT + EVAL_FIXATION_TIME + EVAL_TEXT_TIME + SECOND_RETENTION_INTERVAL + FIRST_CUE_TIME + FIRST_RETENTION_INTERVAL + STIM_TIME + FIXATION_TIME + MEMORY_TEXT_TIME:pass


    #Second Probe
        
        secondProbeRand = random.randint(0,2)#Random number for if it's an uncued stimulus being probed
        secondPosition = POSARRAY[secondCuePos]#position of second cued stimulus
        secondCuedUncuedRand = random.randint(0,1)#Random number for whether cued or uncued is probed
        if secondCuedUncuedRand == 0:#Cued Stim is Probed
            if colourArray.index('Blue') < 4:
                if secondPosition == BluePos:SecondProbe = visual.ImageStim(win=win,image= 'Images/Blue/Blue' + str(BlueCount) + '.bmp', pos= [0,0], size=(SIZE,SIZE));secondProbeStim = 'Blue' + str(BlueCount)
            if colourArray.index('Green') < 4:
                if secondPosition == GreenPos:SecondProbe = visual.ImageStim(win=win,image= 'Images/Green/Green' + str(GreenCount) + '.bmp', pos= [0,0], size=(SIZE,SIZE));secondProbeStim = 'Green' + str(GreenCount)
            if colourArray.index('Purple') < 4:
                if secondPosition == PurplePos:SecondProbe = visual.ImageStim(win=win,image= 'Images/Purple/Purple' + str(PurpleCount) + '.bmp', pos= [0,0], size=(SIZE,SIZE));secondProbeStim = 'Purple' + str(PurpleCount)
            if colourArray.index('Pink') < 4:
                if secondPosition == PinkPos:SecondProbe = visual.ImageStim(win=win,image= 'Images/Pink/Pink' + str(PinkCount) + '.bmp', pos= [0,0], size=(SIZE,SIZE));secondProbeStim = 'Pink' + str(PinkCount)
            if colourArray.index('Orange') < 4:
                if secondPosition == OrangePos:SecondProbe = visual.ImageStim(win=win,image= 'Images/Orange/Orange' + str(OrangeCount) + '.bmp', pos= [0,0], size=(SIZE,SIZE));secondProbeStim = 'Orange' + str(OrangeCount)
        if secondCuedUncuedRand == 1:#Uncued Stim is Probed
            UncuedProbedStim = POSARRAY.index(secondPosition)
            if UncuedProbedStim == 0:
                if secondProbeRand == 0:SecondProbePos= POSARRAY[1]
                if secondProbeRand == 1:SecondProbePos = POSARRAY[2]
                if secondProbeRand == 2:SecondProbePos = POSARRAY[3]
            if UncuedProbedStim == 1:
                if secondProbeRand == 0:SecondProbePos = POSARRAY[0]
                if secondProbeRand == 1:SecondProbePos = POSARRAY[2]
                if secondProbeRand == 2:SecondProbePos = POSARRAY[3]
            if UncuedProbedStim == 2:
                if secondProbeRand == 0:SecondProbePos = POSARRAY[0]
                if secondProbeRand == 1:SecondProbePos = POSARRAY[1]
                if secondProbeRand == 2:SecondProbePos = POSARRAY[3]
            if UncuedProbedStim == 3:
                if secondProbeRand == 0:SecondProbePos = POSARRAY[0]
                if secondProbeRand == 1:SecondProbePos = POSARRAY[1]
                if secondProbeRand == 2:SecondProbePos = POSARRAY[2]
            
            if colourArray.index('Blue') < 4:
                if SecondProbePos == BluePos:SecondProbe = visual.ImageStim(win=win,image= 'Images/Blue/Blue' + str(BlueCount) + '.bmp', pos= [0,0], size=(SIZE,SIZE));secondProbeStim = 'Blue' + str(BlueCount)
            if colourArray.index('Green') < 4:
                if SecondProbePos == GreenPos:SecondProbe = visual.ImageStim(win=win,image= 'Images/Green/Green' + str(GreenCount) + '.bmp', pos= [0,0], size=(SIZE,SIZE));secondProbeStim = 'Green' + str(GreenCount)
            if colourArray.index('Purple') < 4:
                if SecondProbePos == PurplePos:SecondProbe = visual.ImageStim(win=win,image= 'Images/Purple/Purple' + str(PurpleCount) + '.bmp', pos= [0,0], size=(SIZE,SIZE));secondProbeStim = 'Purple' + str(PurpleCount)
            if colourArray.index('Pink') < 4:
                if SecondProbePos == PinkPos:SecondProbe = visual.ImageStim(win=win,image= 'Images/Pink/Pink' + str(PinkCount) + '.bmp', pos= [0,0], size=(SIZE,SIZE));secondProbeStim = 'Pink' + str(PinkCount)
            if colourArray.index('Orange') < 4:
                if SecondProbePos == OrangePos:SecondProbe = visual.ImageStim(win=win,image= 'Images/Orange/Orange' + str(OrangeCount) + '.bmp', pos= [0,0], size=(SIZE,SIZE));secondProbeStim = 'Orange' + str(OrangeCount)
                
        SecondProbe.setAutoDraw(True)
        win.flip()
        
        
        
        
        eventClock.reset()
        stimOnScreen = True
        keyResp.status = NOT_STARTED
        secondProbeErrorCode = -1
        secondProbeErrorName = ''
        noResponseYet = True
        probeOnScreen = True
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
                
                
            #check for a keyboard response
            theseKeys = event.getKeys(keyList=['up','down'])
            if noResponseYet == True:
                if len(theseKeys) > 0: #test if atleast one key pressed
                    if keyResp.keys == []:
                        SecondProbe.setAutoDraw(False)
                        keyResp.keys = theseKeys[-1] #just the last key pressed
                        keyResp.rt = keyResp.clock.getTime()
                        SecondProbeResponse = keyResp.keys
                        SecondProbeRT = keyResp.rt
                        if buttonCounterbalance == 0:
                            if keyResp.keys == 'up' and secondCuedUncuedRand == 1:
                               secondProbeErrorCode = 2
                               secondProbeErrorName = 'incorrect response'
                            if keyResp.keys == 'down' and secondCuedUncuedRand == 0:
                               secondProbeErrorCode = 2
                               secondProbeErrorName = 'incorrect response'
                        if buttonCounterbalance == 1:
                            if keyResp.keys == 'down' and secondCuedUncuedRand == 1:
                               secondProbeErrorCode = 2
                               secondProbeErrorName = 'incorrect response'
                            if keyResp.keys == 'up' and secondCuedUncuedRand == 0:
                               secondProbeErrorCode = 2
                               secondProbeErrorName = 'incorrect response'
                        noResponseYet = False
            
            if stimOnScreen and t > FIRST_PROBE_ON_SCREEN:
                SecondProbe.setAutoDraw(False)
                win.flip()
                stimOnScreen = False
            
            
            # check for quit (the [Esc] key)
            if event.getKeys(["escape"]):
                core.quit()

        SecondProbe.setAutoDraw(False)

        fixationVertical.setAutoDraw(True);fixationHorizontal.setAutoDraw(True)
        win.flip()
    
    
    #Inter-trial interval
    eventClock.reset()
    fixationHorizontal.setAutoDraw(False);fixationVertical.setAutoDraw(False)
    win.flip()
    while eventClock.getTime() < INTER_TRIAL_INTERVAL: pass
    
    if trialsArray2[curRow][5] == 0 or trialsArray2[curRow][5] == 1:
        fourTrialsAgo = threeTrialsAgo
        threeTrialsAgo = twoTrialsAgo
        twoTrialsAgo = previousTrial
        previousTrial = 0
        if firstProbeErrorCode == -1 and secondProbeErrorCode == -1:
           previousTrial = 1
        lastFourTrialsArray = [previousTrial,twoTrialsAgo,threeTrialsAgo,fourTrialsAgo]
        totalACC = previousTrial + twoTrialsAgo + threeTrialsAgo + fourTrialsAgo
        accValue = totalACC/4
        if totalTrials > 3:
            if accValue > .8:
               STIM_TIME = STIM_TIME - 0.05
            if accValue < .7:
               STIM_TIME = STIM_TIME + 0.05
        
        if STIM_TIME < 0.15:
            STIM_TIME = 0.15
        if STIM_TIME > 1.0:
            STIM_TIME = 1.0
    
    
    blocktrial = blocktrial + 1
    totalTrials = totalTrials + 1
    
    if blocktrial == 16:
        blocktrial = 0
        breakTextOnScreen = visual.TextStim(win=win, ori=0, name='breakTextOnScreen', text='Take a Quick Break\nPress the space bar to start the next block...',    font=u'Arial', pos=[0, 0], height=0.75, wrapWidth=None, color='black', colorSpace=u'rgb', opacity=1, depth=-1.0)
        buttonReminderTextOnScreen = visual.TextStim(win=win, ori=0, name='buttonReminderTextOnScreen', text='Remember, press the ' + butVar1 + ' key to answer YES. Press the ' + butVar2 + ' key to answer NO.',    font=u'Arial', pos=[0, -3], height=0.75, wrapWidth=40, color='black', colorSpace=u'rgb', opacity=1, depth=-1.0)
        breakTextOnScreen.setAutoDraw(True)
        buttonReminderTextOnScreen.setAutoDraw(True)
        win.flip()
        event.waitKeys()

        breakTextOnScreen.setAutoDraw(False)
        buttonReminderTextOnScreen.setAutoDraw(False)
        win.flip()
 
    outStr = str(runTime) + '\t'
    outStr = outStr + str(totalTrials) + '\t'
    outStr = outStr + str(TrialType) + '\t'
    outStr = outStr + 'Blue' + str(BlueCount) + '\t'
    if colourArray.index('Blue') < 4:
        outStr = outStr + str(POSARRAY[colourArray.index('Blue')]) + '\t'
    if colourArray.index('Blue') == 4:
        outStr = outStr + 'novelcolour' + '\t'
    outStr = outStr + 'Green' + str(GreenCount) + '\t'
    if colourArray.index('Green') < 4:
        outStr = outStr + str(POSARRAY[colourArray.index('Green')]) + '\t'
    if colourArray.index('Green') == 4:
        outStr = outStr + 'novelcolour' + '\t'
    outStr = outStr + 'Purple' + str(PurpleCount) + '\t'
    if colourArray.index('Purple') < 4:
        outStr = outStr + str(POSARRAY[colourArray.index('Purple')]) + '\t'
    if colourArray.index('Purple') == 4:
        outStr = outStr + 'novelcolour' + '\t'
    outStr = outStr + 'Pink' + str(PinkCount) + '\t'
    if colourArray.index('Pink') < 4:
        outStr = outStr + str(POSARRAY[colourArray.index('Pink')]) + '\t'
    if colourArray.index('Pink') == 4:
        outStr = outStr + 'novelcolour' + '\t'
    outStr = outStr + 'Orange' + str(OrangeCount) + '\t'
    if colourArray.index('Orange') < 4:
        outStr = outStr + str(POSARRAY[colourArray.index('Orange')]) + '\t'
    if colourArray.index('Orange') == 4:
        outStr = outStr + 'novelcolour' + '\t'
    if firstCuePos == 0 or firstCuePos == 1:
        outStr = outStr + '0' + '\t'
    if firstCuePos == 2 or firstCuePos == 3:
        outStr = outStr + '1' + '\t'
    outStr = outStr + str(POSARRAY[firstCuePos]) + '\t'
    if trialsArray2[curRow][5] < 2:
        outStr = outStr + str(secondPosition) + '\t'
        outStr = outStr + str(firstProbeStim) + '\t'
        outStr = outStr + str(firstCuedUncuedRand) + '\t'
        outStr = outStr + str(FirstProbeResponse) + '\t'
        if firstProbeErrorCode == -1:
            outStr = outStr + '1' + '\t'
        if firstProbeErrorCode == 2:
            outStr = outStr + '0' + '\t'
        if firstProbeErrorCode == 5:
            outStr = outStr + '0' + '\t'
        if firstProbeErrorCode == 6:
            outStr = outStr + '0' + '\t'
        outStr = outStr + str(FirstProbeRT) + '\t'
        outStr = outStr + str(firstProbeErrorCode) + '\t'
        outStr = outStr + str(firstProbeErrorName) + '\t'
        outStr = outStr + str(secondProbeStim) + '\t'
        outStr = outStr + str(secondCuedUncuedRand) + '\t'
        outStr = outStr + str(SecondProbeResponse) + '\t'
        if secondProbeErrorCode == -1:
            outStr = outStr + '1' + '\t'
        if secondProbeErrorCode == 2:
            outStr = outStr + '0' + '\t'
        if secondProbeErrorCode == 5:
            outStr = outStr + '0' + '\t'
        if secondProbeErrorCode == 6:
            outStr = outStr + '0' + '\t'
        outStr = outStr + str(SecondProbeRT) + '\t'
        outStr = outStr + str(secondProbeErrorCode) + '\t'
        outStr = outStr + str(secondProbeErrorName) + '\t'
        evalImgName2 = evalImgName.rsplit("/")[-1]
        outStr = outStr + str(evalImgName2) + '\t'
        outStr = outStr + str(trialsArray2[curRow][4]) + '\t'
        outStr = outStr + str(evalResponse) + '\t'
        outStr = outStr + str(evalRT) + '\t'
        outStr = outStr + str(evalErrorCode) + '\t'
        outStr = outStr + str(evalErrorName) + '\t'
    if trialsArray2[curRow][5] == 2:
        outStr = outStr + 'searchtask\tsearchtask\tsearchtask\tsearchtask\tsearchtask\tsearchtask\tsearchtask\tsearchtask\tsearchtask\tsearchtask\tsearchtask\tsearchtask\tsearchtask\tsearchtask\tsearchtask\tsearchtask\tsearchtask\tsearchtask\tsearchtask\tsearchtask\tsearchtask\t'
    outStr = outStr + str(STIM_TIME) + '\t'
    outStr = outStr + str(trialsArray2[curRow][5]) + '\t'
    if trialsArray2[curRow][5] == 2:
        outStr = outStr + str(singType) + '\t'
        outStr = outStr + str(singColName) + '\t'
        outStr = outStr + str(singPos) + '\t'
        if searchStim[1].ori == 0:
            outStr = outStr + 'left' + '\t'
        if searchStim[1].ori == 180:
            outStr = outStr + 'right' + '\t'
        if targetOri == 90:
            outStr = outStr + 'up' + '\t'
        if targetOri == 270:
            outStr = outStr + 'down' + '\t'
        outStr = outStr + str(tarPos) + '\t'
        outStr = outStr + str(searchResponse) + '\t'
        outStr = outStr + str(searchRT) + '\t'
        outStr = outStr + str(searchErrorCode) + '\t'
        outStr = outStr + str(searchErrorName) + '\t'
    if trialsArray2[curRow][5] < 2:
        outStr = outStr + 'nosearch\tnosearch\tnosearch\tnosearch\tnosearch\tnosearch\tnosearch\tnosearch\tnosearch\tnosearch\t'
    outStr = outStr + '2' + '\t'
    outStr = outStr + str(expInfo2['age']) + '\t'
    outStr = outStr + str(expInfo3['gender']) + '\t'
    outStr = outStr + str(expInfo4['handedness']) + '\t'
    outStr = outStr + str(expInfo5['glasses/contacts?']) + '\t'
    outputFile.write(outStr + 'eol\n')
