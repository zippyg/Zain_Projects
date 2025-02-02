import pygame, math, sys, random, copy
from pygame.locals import *
import pygame_menu  # this is the pygame module that makes this task so simple, as it handles the imputs and the GUI
pygame.init()
surface = pygame.display.set_mode((1200, 800))  # sets the scren dimensions

mytheme = pygame_menu.themes.THEME_DARK.copy()
mytheme.title_background_color=(0, 0, 0)
myimage = pygame_menu.baseimage.BaseImage(image_path="background.jpg",
    drawing_mode=pygame_menu.baseimage.IMAGE_MODE_FILL
)
mytheme.background_color = myimage
SCREENWIDTH, SCREENHEIGHT = 1200, 800 #Sets the screen's height & width
DISPLAYSURF = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT), 0, 32) #Main screen that I will add stuff on
WHITE = (255, 255, 255)
GREEN = (124, 255,   0)
RED   = (255,   0,   0)
BLACK = (  0,   0,   0)
BLUE =  (  0,   0, 255)
FPS = 30 #Frames per second

#Initialise pygame
import pygame, math, sys, random, copy
from pygame.locals import *

#Importing classes needed
class Button:
    def __init__(self, Label, PosXStart, PosYStart, Width, Length, Surface):
        self.Label = Label
        self.PosXStart = PosXStart
        self.PosYStart = PosYStart
        self.Width = Width
        self.Length = Length
        self.BackgroundColour = (51,255,51) #green colour for all buttons
        self.Surface = Surface
        self.Font = pygame.font.Font(None, 32)
        self.TextColour = (0,0,0) #Black

    def DisplayButton(self): #Method used to draw the button
        Button = pygame.draw.rect(self.Surface, self.BackgroundColour, (self.PosXStart, self.PosYStart, self.Length, self.Width))
        self._MakeLabel()

    def _MakeLabel(self):
        LabelX = (self.PosXStart + 10)
        LabelY = (self.PosYStart + (self.Length//20))
        ButtonText = self.Font.render(self.Label,1,self.TextColour)
        self.Surface.blit(ButtonText, (LabelX,LabelY))

    def ClickInRange(self, PositionTuple):
        if (PositionTuple[0] in range(self.PosXStart, self.PosXStart+self.Length+1)) and (PositionTuple[1] in range(self.PosYStart, self.PosYStart+self.Width+1)):
            return True
        else:
            return False
class CheckBox:
    def __init__(self, PosX, PosY, Width,Surface,Label,WordDistance):
        self.Surface = Surface #What surface the box will be drawn on
        self.StartX = PosX
        self.StartY = PosY
        self.Width = Width #Determines the dimensions of the box (will always be a*a dimensions)
        self.Thickness = 8 #Determines thickness of tick
        self.GREEN = (0,255,0) #The colour of the tick
        self.BLACK = (0,0,0) #Box outline colour
        self.Clicked = False
        self.Label = Label
        self.Font= pygame.font.Font(None,25) #Using Pygame's default font
        self.TextColour = self.BLACK #Text colour will be black
        self.WordDistance = WordDistance #Allows the user to customise how far away the checkbox is away from the user

    def MakeBox(self): #Makes box by drawing lines on the surface
        TopLine = pygame.draw.line(self.Surface, self.BLACK,(self.StartX-2,self.StartY),
                                   (self.StartX+self.Width+2,self.StartY),1)
        LeftLine = pygame.draw.line(self.Surface,self.BLACK,(self.StartX-2,self.StartY),
                                    (self.StartX-2,self.StartY+self.Width+2),1)
        BottomLine = pygame.draw.line(self.Surface,self.BLACK,(self.StartX-2,self.StartY+self.Width+2),
                                    (self.StartX+self.Width+2,self.StartY+self.Width+2),1)
        RightLine = pygame.draw.line(self.Surface,self.BLACK,(self.StartX+self.Width+2,self.StartY),
                                    (self.StartX+self.Width+2,self.StartY+self.Width+2),1)
        self._AddLabel() #Adds a label to the checkbox
        if self.Clicked == True:
            self._AddTick() #Adds tick

    def ClickInRange(self, PositionTuple): #Checks if a mouse click is in range of the checkbox
        if (PositionTuple[0] in range(self.StartX, self.StartX+self.Width+1)) and (PositionTuple[1] in range(self.StartY, self.StartY+self.Width+1)):
            #This allows you to check and uncheck the box
            if self.Clicked == True:
                self.Clicked = False
            else:
                self.Clicked = True

    def _TickCoordinates(self): #A private method that allows me to get the coordinates of 2 lines which will form to make one tick
        X1 = self.StartX
        Y1 = self.StartY + (self.Width//2)
        X2 = self.StartX + (self.Width//2)
        Y2 = self.StartY + self.Width
        X3 = self.StartX + self.Width
        Y3 = self.StartY
        return X1,Y1,X2,Y2, X3,Y3

    def _AddTick(self):
           #Initialise coordinates
           FirstX,FirstY,SecondX,SecondY,ThirdX,ThirdY = self._TickCoordinates() #Private methods used to get coordinates of tick
           #Actually Draws Lines => making the tick
           pygame.draw.line(self.Surface, self.GREEN, (FirstX,FirstY),(SecondX,SecondY),self.Thickness)
           pygame.draw.line(self.Surface, self.GREEN, (SecondX, SecondY),(ThirdX,ThirdY),self.Thickness)

    def _AddLabel(self): #Private method used to add a label to a checkbox
        LabelX = self.StartX - self.WordDistance
        LabelY = self.StartY + 8
        Text = self.Font.render(self.Label,1,self.TextColour)
        self.Surface.blit(Text, (LabelX,LabelY))
class RandomButton(Button): #Use of inheritence
                            #Makes  a random button in pygame
    def __init__(self,Label, PosXStart, PosYStart, Width, Length, Surface, Range):
        super().__init__(Label, PosXStart, PosYStart, Width, Length, Surface) #Inhereits all fields and methods from button class
        self._Range = Range #Range must be given as a tuple

    def GetNumInRange(self): #Gets a random real number in a given range to 1dp
        return str(round(random.uniform(self._Range[0], self._Range[1]),1))
class InputBox: #Class used to make input box
    def __init__(self,PosX, PosY, Label,WordDistance,LengthValidation,RangeTuple):
        self.StartX = PosX
        self.StartY = PosY
        self.Variable = "" #String which can vary
        self.Width = 30
        self.Length = 200
        self.Label = Label #Label given to box. E.g. Displacement(m): []
        self.Surface = DISPLAYSURF
        self.Font = pygame.font.Font(None,25)
        self.BLACK = (0,0,0)
        self.TextColour = self.BLACK #Input text colour
        self.WordDistance = WordDistance #How far away you want the label to be from the box
        self.Clicked = False #Checks if the input box has been clicked or not
        self.StringLength = LengthValidation #Ensures that the length of the string doesn't exceed a certain length. E.g No more than 5 characters
        self.Range = RangeTuple #Range of results allowed. E.g. 0 - 100.0 inclusive

    def MakeBox(self):
        #Makes the input box
        TopLine = pygame.draw.line(self.Surface, self.BLACK,(self.StartX-2,self.StartY),
                                   (self.StartX+self.Length+2,self.StartY),1)
        LeftLine = pygame.draw.line(self.Surface,self.BLACK,(self.StartX-2,self.StartY),
                                    (self.StartX-2,self.StartY+self.Width+2),1)
        BottomLine = pygame.draw.line(self.Surface,self.BLACK,(self.StartX-2,self.StartY+self.Width+2),
                                    (self.StartX+self.Length+2,self.StartY+self.Width+2),1)
        RightLine = pygame.draw.line(self.Surface,self.BLACK,(self.StartX+self.Length+2,self.StartY),
                                    (self.StartX+self.Length+2,self.StartY+self.Width+2),1)

        self._AddLabel() #Adds a label to the checkbox
        self._DisplayVariable() #Shows Variable on screen
        self._DisplayRange() #Displays the minimum & maximum value that can be entered

    def _AddLabel(self): #Private method used to add a label to a checkbox
        LabelX = self.StartX - self.WordDistance - 5
        LabelY = self.StartY + 3
        Text = self.Font.render(self.Label,1,self.TextColour)
        #Display the label
        self._AddText(Text, (LabelX,LabelY))

    def _DisplayVariable(self): #Private method which is meant to display the variable
        XStart = self.StartX + 5
        YStart = self.StartY + 3
        Text = self.Font.render(self.Variable,1,self.TextColour)
        #Display the variable
        self._AddText(Text, (XStart,YStart))

    def _DisplayRange(self): #Private method which enables the user to see the range of values permitted
        XStart = self.StartX + self.Length + 15
        YStart = self.StartY - 5
        MinText = self.Font.render('Min: ' + str(float(self.Range[0])),1,self.TextColour)
        MaxText = self.Font.render("Max: " + str(float(self.Range[1])),1,self.TextColour)
        #Display Range
        self._AddText(MinText, (XStart,YStart))
        self._AddText(MaxText, (XStart, YStart+20))

    def _AddText(self, Text, CoordinatesTuple): #Private method used to display text
        self.Surface.blit(Text, (CoordinatesTuple[0], CoordinatesTuple[1]))

    def ClickInRange(self, PositionTuple): #Checks if a mouse click is in range of the checkbox
        if (PositionTuple[0] in range(self.StartX, self.StartX+self.Length+1)) and (PositionTuple[1] in range(self.StartY, self.StartY+self.Width+1)):
            self.Clicked = True
        else:
            self.Clicked = False #This means that if the click is out of the box you can no longer enter variables in the box

    def AddCharacter(self, Input): #Adds character from alphabet -> ['1','2','3','4,'5','6','7','8','9','.',BACKSPACE]
        if (Input == K_1) and (len(self.Variable)<self.StringLength):
            if self._NumInRange(1)==True:
                if "." in self.Variable:
                    self.Variable = self._AdjustVariable(1)
                else:
                    self.Variable += "1"
        elif (Input == K_2) and (len(self.Variable)<self.StringLength):
            if self._NumInRange(2)==True:
                if "." in self.Variable:
                    self.Variable = self._AdjustVariable(2)
                else:
                    self.Variable += "2"
        elif (Input == K_3) and (len(self.Variable)<self.StringLength):
            if self._NumInRange(3)==True:
                if "." in self.Variable:
                    self.Variable = self._AdjustVariable(3)
                else:
                    self.Variable += "3"
        elif (Input == K_4) and (len(self.Variable)<self.StringLength):
            if self._NumInRange(4)==True:
                if "." in self.Variable:
                    self.Variable = self._AdjustVariable(4)
                else:
                    self.Variable += "4"
        elif (Input == K_5) and (len(self.Variable)<self.StringLength):
            if self._NumInRange(5)==True:
                if "." in self.Variable:
                    self.Variable = self._AdjustVariable(5)
                else:
                    self.Variable += "5"
        elif (Input == K_6) and (len(self.Variable)<self.StringLength):
            if self._NumInRange(6)==True:
                if "." in self.Variable:
                    self.Variable = self._AdjustVariable(6)
                else:
                    self.Variable += "6"
        elif (Input == K_7) and (len(self.Variable)<self.StringLength):
            if self._NumInRange(7)==True:
                if "." in self.Variable:
                    self.Variable = self._AdjustVariable(7)
                else:
                    self.Variable += "7"
        elif (Input == K_8) and (len(self.Variable)<self.StringLength):
            if self._NumInRange(8)==True:
                if "." in self.Variable:
                    self.Variable = self._AdjustVariable(8)
                else:
                    self.Variable += "8"
        elif (Input == K_9) and (len(self.Variable)<self.StringLength):
            if self._NumInRange(9)==True:
                if "." in self.Variable:
                    self.Variable = self._AdjustVariable(9)
                else:
                    self.Variable += "9"
        elif (Input == K_0) and (len(self.Variable)<self.StringLength):
            if self._NumInRange(0)==True:
                if "." in self.Variable:
                    self.Variable = self._AdjustVariable(0)
                else:
                    self.Variable += "0"
        elif (Input == K_PERIOD) and (len(self.Variable)<self.StringLength):
            if "." not in self.Variable: #You should only be able to enter a decimal ('.') if the variable doesn't already have one
                self.Variable += "."

        elif (Input == K_BACKSPACE): #Deletes the final character in 'Variable'
            self.Variable = self.Variable[:-1]

    def _AdjustVariable(self,String): #Private method that adjusts the input so that it is always to 1dp
        self.Variable += str(String)
        self.Variable = "%0.2f" % float(self.Variable)
        return self.Variable[:-1]

    def _NumInRange(self, Num): #Checks if the number will be in range and returns if this is the case or not
        if (float(self.Variable + str(Num))>=self.Range[0]) and (float(self.Variable + str(Num))<=self.Range[1]):
            return True
        else:
            return False

pygame.init()

#Global parameters
BALL = pygame.image.load("missle.png")
BALL = pygame.transform.scale(BALL,(70,30))
Font = pygame.font.Font(None, 64) #Initialises Pygame's default font
SCREENWIDTH, SCREENHEIGHT = 900, 600 #Sets the screen's height & width
WHITE = (255, 255, 255)
GREEN = (124, 255,   0)
RED   = (255,   0,   0)
BLACK = (  0,   0,   0)
BLUE =  (  0,   0, 255)
FPS = 30 #Frames per second
fpsClock = pygame.time.Clock()
DISPLAYSURF = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT), 0, 32) #Main screen that I will add stuff on
pygame.display.set_caption("Zain's coursework simulation v3") #Caption of the simulation


def InputScreen(): #Makes the input screen for projectile motion #Make sure you pass parameters
    Title = Font.render("Projectile Motion Input Screen", 1, RED) #Title
    DisplacementBox, InitialVBox, AngleBox, MassBox, AIcheck, HideCheck, SubmitButton, RandomDisplacement, RandomInitialV, RandomAngle, RandomMass = MakeWidgets()
    Running = True
    while Running:
        DISPLAYSURF.fill(WHITE)
        DISPLAYSURF.blit(Title,(120,60)) #Adds title to the top of the screen
        #Display All buttons, input boxes & checkbox
        DisplayWidgets(DisplacementBox, InitialVBox, AngleBox, MassBox, AIcheck, HideCheck, SubmitButton, RandomDisplacement, RandomInitialV, RandomAngle, RandomMass)
        #If the above doesn't work, just copy & paste back here and it 100%. Done for sole purpose of making my code neater.
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN: #Can check multiple things at once as they'll never overlap
                (PosX,PosY)  = pygame.mouse.get_pos()
                #Checks if the box has been clicked on or not- Will cancel out the click if it's not the case
                InitialVBox.ClickInRange((PosX,PosY))
                DisplacementBox.ClickInRange((PosX,PosY))
                AngleBox.ClickInRange((PosX,PosY))
                MassBox.ClickInRange((PosX,PosY))
                #Allows you to check\uncheck the hide checkbox
                HideCheck.ClickInRange((PosX,PosY))
                AIcheck.ClickInRange((PosX,PosY))
                if SubmitButton.ClickInRange((PosX,PosY)) == True: #Checks if submit button has been clicked
                    Running = False #Stops the animation loop
                elif RandomDisplacement.ClickInRange((PosX,PosY)):
                    DisplacementBox.Variable = RandomDisplacement.GetNumInRange()
                elif RandomInitialV.ClickInRange((PosX,PosY)):
                    InitialVBox.Variable = RandomInitialV.GetNumInRange()
                elif RandomAngle.ClickInRange((PosX,PosY)):
                    AngleBox.Variable = RandomAngle.GetNumInRange()
                elif RandomMass.ClickInRange((PosX,PosY)):
                    MassBox.Variable = RandomMass.GetNumInRange()
            elif (event.type == KEYDOWN) and (DisplacementBox.Clicked == True):
                DisplacementBox.AddCharacter(event.key)
            elif (event.type == KEYDOWN) and (InitialVBox.Clicked == True): #Adds values to the initial velocity
                InitialVBox.AddCharacter(event.key)
            elif (event.type == KEYDOWN) and (AngleBox.Clicked == True): #Adds values to the angle
                AngleBox.AddCharacter(event.key)
            elif (event.type == KEYDOWN) and (MassBox.Clicked == True): #Adds characters to the mass
                MassBox.AddCharacter(event.key)
        #Updates event every 1/30th of a second
        pygame.display.update()
        fpsClock.tick(FPS)


    s, u, Angle = Convert(DisplacementBox.Variable,InitialVBox.Variable,AngleBox.Variable) #Tries to convert the inputs to real numbers
    if (u!="") and ((Angle!="") or (s!="")):
        s, u, v, t, Angle,Mode = Solve_ProjMotion(s,u,Angle) #Solves remaining parameters using SUVAT equations
        ProjMotionSimulation(s,u,v,t,Angle,AIcheck.Clicked,HideCheck.Clicked,Mode)#Simulation for Proj_Motion
    else:
        ErrorMsg_NotEnough_Proj() #Function which shows the user that not enough inputs were entered



def ProjMotionSimulation(s,u,v,t,Angle,AI,Hide,Mode):
    #Making Widgets
    if u < 25 or Angle < 25 :
        InputScreen()
    print(AI)
    InputButton = Button("Inputs", 600, 400, 35,200,DISPLAYSURF)
    ExplainButton = Button("Explain", 600, 540, 35, 200, DISPLAYSURF)
    HIDE = CheckBox(500,400,30,DISPLAYSURF,"Hide Parameters:",160)
    HIDE.Clicked = Hide
    Input = False
    Explain = False
    GROUNDLEVEL = 350
    s = s
    PosX = 50
    PosY = GROUNDLEVEL #As the particle will start at the ground
    g = -9.8
    ANGLEDEGREES = round(Angle,1)
    ANGLERADIANS = math.radians(ANGLEDEGREES)
    u = u
    i = u * round(math.cos(ANGLERADIANS), 1) #Gives horizontal velocity#round(degrees, 1) rounds to 1dp
    j = u * round(math.sin(ANGLERADIANS), 1) #Gives vertical velocity
    SCALEFACTOR = 1.3 #Has to be >=1 #Makes the animation fit to screen more appropriately
    CoordinatesList = GetLists(i,j,PosX,PosY)
    TrailList = copy.deepcopy(CoordinatesList)
    TrailList = AdjustTrail(TrailList)
    Motion = True #So the ball moves whilst the ball is on the list #Used to stop the pointer from going out of the range of the list
    Pointer = 0
    DISPLAYSURF.fill(WHITE)
    Running = True
    PosXAI = 500
    PosYAI = GROUNDLEVEL
    intercepter=pygame.image.load('flare.png')
    collision = False
    while Running:
        DISPLAYSURF.fill(WHITE)
        InputButton.DisplayButton()
        ExplainButton.DisplayButton()
        HIDE.MakeBox()

        if HIDE.Clicked == False:
            PrintParameters(s,u,v,t,ANGLEDEGREES)
        if Motion == True:
            PosX, PosY = CoordinatesList[Pointer][0], CoordinatesList[Pointer][1]
            #print('(',PosX,',',PosY,')')
            DISPLAYSURF.blit(BALL, (PosX, PosY))
            if AI==True:

                diffX = PosXAI - PosX
                diffY = PosYAI - PosY
                #print('(',diffX,',',diffY,')')
                moveX = diffX / 50
                moveY = diffY / 50
                x=random.randint(-2,2)
                y=random.randint(-2,2)
                PosXAI -= (moveX + x)
                PosYAI -= (moveY + y)
                DISPLAYSURF.blit(intercepter, (PosXAI, PosYAI))
                maxPosX = PosX + 20
                maxPosY = PosY + 20
                minPosX = PosX - 20
                minPosY = PosY - 20
                if (PosXAI < maxPosX and PosXAI > minPosX) and (PosYAI < maxPosY and PosYAI > minPosY)   :
                    collision = True
                    print("collision is ",collision )
                if collision == True:
                    collisionimg=pygame.image.load('collide.png')
                    collisionimg=pygame.transform.scale(collisionimg,(50,50))
                    Motion=False

            if Pointer == (len(CoordinatesList)-1):
                Motion = False
            else:
                Pointer +=1

        if Motion == False:
            if collision == True:
                DISPLAYSURF.blit(collisionimg, (PosX, PosY))
            else:
                PosY = GROUNDLEVEL
                PosX = CoordinatesList[Pointer][0]
                DISPLAYSURF.blit(BALL, (PosX, PosY))
        #Makes trail
        if Pointer>1:
            pygame.draw.aalines(DISPLAYSURF, BLUE,False, TrailList[:Pointer],5)#MakeTrail(Pointer)
        #Makes ground by drawing a thick, green line
        pygame.draw.line(DISPLAYSURF, BLUE, (0,GROUNDLEVEL+25), (SCREENWIDTH,GROUNDLEVEL+25),8) #+25 makes simulation look better

        for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == MOUSEBUTTONDOWN:
                    (PosX, PosY) = pygame.mouse.get_pos() #Get position of mouse click
                    HIDE.ClickInRange((PosX,PosY))
                    if InputButton.ClickInRange((PosX,PosY)) == True:
                        Input = True #It will be true which implies that that user must enter inputs again
                        Running = False
                    elif ExplainButton.ClickInRange((PosX,PosY)) == True:
                        Explain = True
                        Running = False



        pygame.display.update()
        fpsClock.tick(FPS)
    if Input == True:
        InputScreen()
    elif Explain == True:
        if Mode == 1:
            Explain_ProjMotion1(s,u,v,t,ANGLEDEGREES,HIDE.Clicked,Mode)
        elif Mode == 2:
            Explain_ProjMotion2(s,u,v,t,ANGLEDEGREES,HIDE.Clicked,Mode)

#Functions Needed
def Explain_ProjMotion1(s,u,v,t,Angle,Hide,Method):
    ExplainFont = pygame.font.Font(None,32) #Initialises PyGame's initial font of size 32
    Running = True
    VExplain1 = ExplainFont.render("v = -u",1,BLACK)
    VExplain2 = ExplainFont.render("v = -{0}".format(str(u)),1,BLACK)
    AngleExplain1 = ExplainFont.render("Rearrange v^2 =u^2 + 2as where v = 0",1,BLACK)
    AngleExplain2 = ExplainFont.render("=> usinθ = √(2gs) => θ = arcsin((√2gs))/u",1,BLACK)
    AngleExplain3 = ExplainFont.render("=> θ = arcsin(√(2*g*{0}))/{1}".format(str(s),str(u)),1,BLACK)
    TimeExplain1 = ExplainFont.render("Rearrange s = ut + 0.5at^2 where s = 0",1,BLACK)
    TimeExplain2 = ExplainFont.render("=> t = usinθ/4.9",1,BLACK)
    TimeExplain3 = ExplainFont.render("=> t = {0}sin({1})/4.9".format("%.1f"%u,"%.1f"%Angle),1,BLACK)
    OKButton = Button("OK",400,500,35,100,DISPLAYSURF) #(Label, PosXStart, PosYStart, Width, Length, Surface)
    while Running:
            DisplayExplainProjMotion(VExplain1, VExplain2,AngleExplain1, AngleExplain2, AngleExplain3, TimeExplain1, TimeExplain2, TimeExplain3, OKButton)
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    (PosX, PosY) = pygame.mouse.get_pos() #Get position of mouse
                    if OKButton.ClickInRange((PosX,PosY)) == True:
                        Running = False
            pygame.display.update()
            fpsClock.tick(FPS)
    ProjMotionSimulation(s,u,v,t,Angle,Hide,Method)

def Explain_ProjMotion2(s,u,v,t,Angle,Hide,Method):
    ExplainFont = pygame.font.Font(None,32) #Initialises PyGame's initial font of size 32
    Running = True
    VExplain1 = ExplainFont.render("v = -u",1,BLACK)
    VExplain2 = ExplainFont.render("v = -{0}".format("%.1f"%u),1,BLACK)
    TimeExplain1 = ExplainFont.render("Rearrange s = ut + 0.5at^2 where s = 0",1,BLACK)
    TimeExplain2 = ExplainFont.render("=> t = usinθ/4.9",1,BLACK)
    TimeExplain3 = ExplainFont.render("=> t = {0}sin({1})/4.9".format("%.1f"%u,"%.1f"%Angle),1,BLACK)
    DisplacementExplain1 = ExplainFont.render("At time, t/2, height is at a max => using s = ut + 0.5at^2",1,BLACK)
    DisplacementExplain2 = ExplainFont.render("=> s = usinθ(t/2) - 4.9(t/2)^2",1,BLACK)
    DisplacementExplain3 = ExplainFont.render("=> s = {0}sin({1})({2}/2) - 4.9({2}/2)^2".format("%.1f"%u,"%.1f"%Angle,"%.1f"%t),1,BLACK)
    OKButton = Button("OK",400,500,35,100,DISPLAYSURF) #(Label, PosXStart, PosYStart, Width, Length, Surface)
    while Running:
            DisplayExplainProjMotion(VExplain1,VExplain2, TimeExplain1,TimeExplain2,TimeExplain3,DisplacementExplain1,DisplacementExplain2,DisplacementExplain3,OKButton)
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    (PosX, PosY) = pygame.mouse.get_pos() #Get position of mouse
                    if OKButton.ClickInRange((PosX,PosY)) == True:
                        Running = False
            pygame.display.update()
            fpsClock.tick(FPS)
    ProjMotionSimulation(s,u,v,t,Angle,Hide,Method)

def DisplayExplainProjMotion(a,b,c,d,e,f,g,h,Button): #Made to display the process of finding the answer. #Used as there was repeating code
     DISPLAYSURF.fill(WHITE)
     DISPLAYSURF.blit(a,(40,30))
     DISPLAYSURF.blit(b,(40,70))
     DISPLAYSURF.blit(c,(40,120))
     DISPLAYSURF.blit(d,(40,170))
     DISPLAYSURF.blit(e,(40,220))
     DISPLAYSURF.blit(f,(40,270))
     DISPLAYSURF.blit(g,(40,320))
     DISPLAYSURF.blit(h,(40,370))
     Button.DisplayButton()

def MakeWidgets(): #Makes all neccassary input widgets needed for the Projectile Motion input screen
    DisplacementBox = InputBox(310, 150, "Displacement (m):", 163, 6, (0.1,100))
    InitialVBox = InputBox(310, 210, "Initial Velocity (ms^-1):", 213, 6, (0.1,100))
    AngleBox = InputBox(310, 270, "Angle Of Projection (°):", 213, 4,(0.1,90))
    MassBox = InputBox(310,330, "Mass (kg):", 90, 4, (0.1,10))
    HideCheck = CheckBox(430, 400, 30, DISPLAYSURF, "Hide Variables:",140)
    AIcheck = CheckBox(430, 450, 30, DISPLAYSURF, "AI:",140)
    SubmitButton = Button("Submit", 380, 500, 40, 100,DISPLAYSURF)
    RandomDisplacement = RandomButton("Random", 640, 150, 30, 115, DISPLAYSURF, (0.1,100))
    RandomInitialV = RandomButton("Random", 640, 210, 30, 115, DISPLAYSURF, (0.1,100))
    RandomAngle = RandomButton("Random", 640, 270, 30, 115, DISPLAYSURF, (0.1,90))
    RandomMass = RandomButton("Random", 640, 330, 30, 115, DISPLAYSURF, (0.1,10))
    return DisplacementBox, InitialVBox, AngleBox, MassBox, AIcheck, HideCheck, SubmitButton, RandomDisplacement, RandomInitialV, RandomAngle, RandomMass

def DisplayWidgets(DisplacementBox, InitialVBox, AngleBox, MassBox, AIcheck, HideCheck, SubmitButton, RandomDisplacement, RandomInitialV, RandomAngle, RandomMass):
        return DisplacementBox.MakeBox() , InitialVBox.MakeBox(), AngleBox.MakeBox(),MassBox.MakeBox(),AIcheck.MakeBox(), HideCheck.MakeBox(), SubmitButton.DisplayButton() ,RandomDisplacement.DisplayButton(), RandomInitialV.DisplayButton(),RandomAngle.DisplayButton(),RandomMass.DisplayButton()

def VerticalCoordinates(j, g, PosY, UP, DOWN): #Generates vertical coordinates for projectile motion using recursion
    SCALEFACTOR = 2 #Makes simulation prettier
    GROUNDLEVEL = 350
    if UP == True:
        PosY = PosY - (SCALEFACTOR*(j/FPS))
        j = j + (g/FPS)
        if j<=0:
            UP = False
            DOWN = True
            return [PosY] + VerticalCoordinates(j, g, PosY, False, True)
        return [PosY] + VerticalCoordinates(j, g, PosY, True, False)

    elif DOWN == True:
        PosY = PosY - (SCALEFACTOR*(j/FPS))
        j = j + (g/FPS) #Have to add 'g' as it's negative
        if PosY >= GROUNDLEVEL:
            PosY = GROUNDLEVEL
            return [PosY]
        return [PosY] + VerticalCoordinates(j, g, PosY,False, True)

def RoundAllValues(List):
    for count in range(len(List)):
        List[count][0] = round(List[count][0],1)
        List[count][1] = round(List[count][1],1)
    return List

def HorizontalCoordinates(i,PosX, LengthOfVertList):
    SCALEFACTOR = 2
    List = []
    for count in range(LengthOfVertList):
        PosX += (SCALEFACTOR*(i/FPS))
        List.append(PosX)
    return List

def Convert(List):
    if List[-1]<0:
        List[-1] = 0
    return List[-1]

def JoinLists(ListX, ListY):
    ListXY = [] #Returns coordinates of projectile
    for count in range(len(ListX)):
        ListXY.append([ListX[count], ListY[count]])
    ListXY = RoundAllValues(ListXY)
    return ListXY

def GetLists(i,j,PosX,PosY):
    g = -9.8 #Defining as negative- the acceleration is downwards
    VerticalList= VerticalCoordinates(j,g,PosY, True, False)
    HorizontalList = HorizontalCoordinates(i,PosX, len(VerticalList))
    MainList = JoinLists(HorizontalList, VerticalList)
    return MainList

def AdjustTrail(Trail): #Function used to adjust trail to make it more aesthetically pleasing
    for index in range(len(Trail)):
        Trail[index][0],Trail[index][1] = Trail[index][0]+2, Trail[index][1]+13 #Arbitary values are there to adjust trail position
    return Trail

def PrintParameters(s,u,v,t,Angle):
    ParameterFont = pygame.font.Font(None, 30) #Initialises Pygame's default font this time a size smaller to fit onto screen
    S = ParameterFont.render("S = {0} m".format("%.1f"%s),1,BLACK)
    U = ParameterFont.render("U = {0} ms^-1".format("%.1f"%u),1,BLACK)
    V = ParameterFont.render("V = {0} ms^-1".format("%.1f"%v),1,BLACK)
    A = ParameterFont.render("A = -g = -9.8 ms^-2",1,BLACK) #Ask if client wants '-g' as well
    T = ParameterFont.render("T = {0} s".format("%.1f"%t),1,BLACK)
    ANGLE = ParameterFont.render("θ = {0}°".format("%.1f"%Angle),1,BLACK)
    DISPLAYSURF.blit(S,(40, 400))
    DISPLAYSURF.blit(U,(40, 430))
    DISPLAYSURF.blit(V,(40, 460))
    DISPLAYSURF.blit(A,(40, 490))
    DISPLAYSURF.blit(T,(40, 520))

def ErrorMsg_NotEnough_Proj():
    Title1 = Font.render("Please Enter The Initial Velocity &", 1, RED)
    Title2 = Font.render("EITHER The Angle Of Projection",1,RED)
    Title3 = Font.render("OR The Displacement",1,RED)
    OKButton =  Button("OK", 380, 450, 40, 100,DISPLAYSURF)
    Running =True
    while Running:
        DISPLAYSURF.fill(WHITE)
        DISPLAYSURF.blit(Title1,(85,100))
        DISPLAYSURF.blit(Title2,(100,200))
        DISPLAYSURF.blit(Title3,(170,300))
        OKButton.DisplayButton()
        for event in pygame.event.get():
            if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                (PosX,PosY)  = pygame.mouse.get_pos()
                if OKButton.ClickInRange((PosX,PosY)) == True: #Know you get to go to the input screen
                    Running = False
        pygame.display.update()
        fpsClock.tick(FPS)
    InputScreen() #Goes back to the input screen

def Solve_ProjMotion(s,u,Angle): #Solves remaining parameters using SUVAT equations
    #Actually solve other parameters
    g = 9.8 #Numerical value of acceleration due to gravity
    if (s!="") and (Angle==""): #i.e. when the angle is unknown
        if math.sqrt(2*g*s)/u>1: #To prevent otherwise impossible situations #-1<=Sin(x)<=1
            NotPossible()
        else:
            Mode = 1
            v = -u
            Angle = math.asin(math.sqrt(2*g*s)/u) #Rearranging v**2 = u**2 + 2as where v = 0
            t = (u*math.sin(Angle))/4.9 #Using s=ut+0.5at**2 where s=0
            return s, u, v, t, math.degrees(Angle), Mode
    elif (s=="") and (Angle!=""): #i.e. when the vertical maximum displacement is unknown
        Mode = 2
        v = -u
        t = (u*math.sin(Angle))/4.9 #Gives total time for the projectile
        s = (u*math.sin(Angle)*(t/2)) - (4.9 * (t/2)**2) #Gives maximum vertical height of projectile
        return s, u, v, t, math.degrees(Angle), Mode
    elif (s!="") and (Angle!="") and (u!=""): #i.e. When all parameters are given
        ErrorMsg_NotEnough_Proj() #Entering all 3 can lead to impossible situations

def NotPossible(): #Displays an error message which tells the user that the inputs entered are not feasible
    Title1 = Font.render("The inputs are not valid.", 1, RED) #Error message
    Title2 = Font.render("The value for Displacement is too high", 1, RED) #Error message
    Title3 = Font.render("for the given velocity.", 1, RED)
    Title4 = Font.render("Such a situation shouldn't occur.", 1, RED) #Error message
    Title5 = Font.render("Please reload the program.", 1, RED)
    OKButton =  Button("OK", 350, 500, 40, 100,DISPLAYSURF)
    Running =True
    while Running:
        DISPLAYSURF.fill(WHITE)
        DISPLAYSURF.blit(Title1,(150,50))
        DISPLAYSURF.blit(Title2,(40,130))
        DISPLAYSURF.blit(Title3,(175,210))
        DISPLAYSURF.blit(Title4,(70,290))
        DISPLAYSURF.blit(Title5,(180,370))
        OKButton.DisplayButton()
        for event in pygame.event.get():
            if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN: #Can check multiple things at once as they'll never overlap
                (PosX,PosY)  = pygame.mouse.get_pos()
                if OKButton.ClickInRange((PosX,PosY)) == True:
                    Running = False
                    #InputScreen()
        pygame.display.update()
        fpsClock.tick(FPS)
    ()


def Convert(s,u,Angle): #Function that attempts to convert the varaibles-s,u,Angle to floats
                                     #If it's anything but a number, like '.' or ' ', it will treat the input as " "
    try:
        s = float(s)
    except:
        s = ""
    try:
        u = float(u)
    except:
        u = ""
    try:
        Angle = float(Angle)
        Angle = math.radians(Angle) #As pygame works in radians not degrees
    except:
        Angle = ""
    return s, u, Angle

def units():
    lvl1Font = pygame.font.Font(None,33) # smaller font
    Title1 = lvl1Font.render("displacement, letter s, measured in meters, unit symbol m", 1, RED)
    Title2 = lvl1Font.render("initial velocity, letter u, measured in meters per second, unit symbol m/s",1,RED)
    Title3 = lvl1Font.render("final velocity, letter v, measured in meters per second, unit symbol m/s",1,RED)
    Title4 = lvl1Font.render("acceleration, letter a, measured in meters per second squared, unit symbol m/s^2",1,RED)
    Title5 = lvl1Font.render("time, letter t, measured in seconds, unit symbol s",1,RED)
    OKButton =  Button("OK", 380, 550, 40, 100,DISPLAYSURF)
    Running =True
    while Running:
        DISPLAYSURF.fill(WHITE)
        DISPLAYSURF.blit(Title1,(0,50))
        DISPLAYSURF.blit(Title2,(0,150))
        DISPLAYSURF.blit(Title3,(0,250))
        DISPLAYSURF.blit(Title4,(0,350))
        DISPLAYSURF.blit(Title5,(0,450))
        OKButton.DisplayButton()
        for event in pygame.event.get():
            if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                (PosX,PosY)  = pygame.mouse.get_pos()
                if OKButton.ClickInRange((PosX,PosY)) == True: #Know you get to go to the input screen
                    Running = False
        pygame.display.update()
        fpsClock.tick(FPS)

def components():
    lvl1Font = pygame.font.Font(None,33) # smaller font
    Title1 = lvl1Font.render("every force is made up of two components, horizontal and vertical, as shown in the diagram", 1, RED)
    Title2 = lvl1Font.render("you can find the horizontal comonent by doing Fcos(angle)",1,RED)
    Title3 = lvl1Font.render("you can find the vertical comonent by doing Fsin(angle)",1,RED)
    OKButton =  Button("OK", 380, 550, 40, 100,DISPLAYSURF)
    Running =True
    image_comp=pygame.image.load('components .png')
    while Running:
        DISPLAYSURF.fill(WHITE)
        DISPLAYSURF.blit(Title1,(0,50))
        DISPLAYSURF.blit(Title2,(0,150))
        DISPLAYSURF.blit(Title3,(0,250))
        DISPLAYSURF.blit(image_comp, (300,300))
        OKButton.DisplayButton()
        for event in pygame.event.get():
            if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                (PosX,PosY)  = pygame.mouse.get_pos()
                if OKButton.ClickInRange((PosX,PosY)) == True: #Know you get to go to the input screen
                    Running = False
        pygame.display.update()
        fpsClock.tick(FPS)

def velocity_level():
    lvl1Font = pygame.font.Font(None,30) # smaller font
    lvl3Font = pygame.font.Font(None,55) # smaller font
    Title1 = Font.render("velocity is the rate of change of distance", 1, RED)
    Title2 = lvl3Font.render("you can find the velocity by doing distance/time",1,RED)
    Title3 = lvl1Font.render("remember velocity is a vector, so depending on the direction can be negative or positive",1,RED)
    OKButton =  Button("OK", 380, 550, 40, 100,DISPLAYSURF)
    Running =True
    image_comp=pygame.image.load('velocitydiagram.png')
    while Running:
        DISPLAYSURF.fill(WHITE)
        DISPLAYSURF.blit(Title1,(0,50))
        DISPLAYSURF.blit(Title2,(10,150))
        DISPLAYSURF.blit(Title3,(10,250))
        DISPLAYSURF.blit(image_comp, (70,300))
        OKButton.DisplayButton()
        for event in pygame.event.get():
            if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                (PosX,PosY)  = pygame.mouse.get_pos()
                if OKButton.ClickInRange((PosX,PosY)) == True: #Know you get to go to the input screen
                    Running = False
        pygame.display.update()
        fpsClock.tick(FPS)

def acceleration_level():
    lvl1Font = pygame.font.Font(None,30) # smaller font
    lvl3Font = pygame.font.Font(None,55)
    lvl4Font = pygame.font.Font(None,25) # smaller font
    Title1 = lvl3Font.render("acceleration is the rate of change of velocity", 1, RED)
    Title2 = lvl3Font.render("you can find the acceleration by doing (v-u)/t",1,RED)
    Title3 = lvl1Font.render("remember accleration is a vector, so depending on the direction can be negative or positive",1,RED)
    Title4 = lvl1Font.render("Newton's 2nd law : F=ma, you can also use this to find acceleration",1,RED)
    Title5 = lvl4Font.render("in projectile motion, the only acceleration on the object is g, so acceleration always equals to -9.81 m/s^2",1,RED)
    OKButton =  Button("OK", 380, 550, 40, 100,DISPLAYSURF)
    Running =True
    while Running:
        DISPLAYSURF.fill(WHITE)
        DISPLAYSURF.blit(Title1,(40,50))
        DISPLAYSURF.blit(Title2,(30,150))
        DISPLAYSURF.blit(Title3,(0,250))
        DISPLAYSURF.blit(Title4,(100,350))
        DISPLAYSURF.blit(Title5,(15,450))
        OKButton.DisplayButton()
        for event in pygame.event.get():
            if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                (PosX,PosY)  = pygame.mouse.get_pos()
                if OKButton.ClickInRange((PosX,PosY)) == True: #Know you get to go to the input screen
                    Running = False
        pygame.display.update()
        fpsClock.tick(FPS)



def load_level_1():
    print("level 1 loading ... ")
    units()

def load_level_2():
    print("level 2 loading ... ")
    components()

def load_level_3():
    print("level 3 loading ... ")
    velocity_level()

def load_level_4():
    print("level 4 loading ... ")
    acceleration_level()

def load_level_5():
    print("level 5 loading ... ")
    level = 5
    InputScreen()

def load_level_6():
    print("level 6 loading ... ")

def load_level_7():
    print("level 7 loading ... ")

def load_level_8():
    print("level 8 loading ... ")



'''
def load_level_9():
    print("level 9 loading ... ")

def load_level_10():
    print("level 10 loading ... ")

def load_level_11():
    print("level 11 loading ... ")

def load_level_12():
    print("level 12 loading ... ")

def load_level_13():
    print("level 13 loading ... ")

def load_level_14():
    print("level 14 loading ... ")
    '''



menu = pygame_menu.Menu("Zain's projectile cs cw game", 900, 600,
                       theme=mytheme)   # sets the dimensions of the menu itsef, its cpation and the theme.
                                                               # this is a basic default theme from the pygame.menu library


menu.add.button('level 1 : units and conversions ', load_level_1)
menu.add.button('level 2 : components  ',load_level_2)
menu.add.button('level 3 : velocity',load_level_3)
menu.add.button('level 4 : acceleration ',load_level_4)
#menu.add.button('level 5 : free fall',load_level_5)
#menu.add.button('level 6 : straight line motion ',load_level_6)
#menu.add.button('level 7 : v = u + a*t ',load_level_7)
#menu.add.button('level 8 : s = 0.5(u+v)t',load_level_8)
#menu.add.button('level 9 : v^2=u^2 + 2*a*s ',load_level_9)
#menu.add.button('level 10 : s = ut + 0.5(a*t^0.5)',load_level_10)
menu.add.button('level 5 : exam questions 1 ',load_level_5)
menu.add.button('level 6 : exam questions 2 ',load_level_6)
menu.add.button('level 7 : exam questions 3 ',load_level_7)
menu.add.button('level 8 : exam questions 4 ',load_level_8)


# the load_level functions had to be commented out as they are not yetr defined and would cause errors

menu.add.button('Quit', pygame_menu.events.EXIT) # this simply makes a button called quit to halt the code
menu.mainloop(surface)
