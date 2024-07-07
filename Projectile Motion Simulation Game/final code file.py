
'''
in progress comments and notes :

create random objects in path of the Ai to projectile
    - be OOP instantiantions
get the AI to go around these objects ( stuck counter, etc... )
if AI wins too much then add more objects to level making it harder for the AI


Screen_View.blit(air_mine_img,(200,200))


^^^  no longer needed -- comment out the code i did

all i need to do is to include a variable difficulty
this will be based on a global variable measuring the AI's effectiveness
if ai is strong difficulty decreases vice versa
dificulty will be implemeneted by altering the speed of the AI using the division factor thhing for diffy/diffX
add the difficulty scroller back to the menu -- in sample things

'''

import pygame, math, sys, random, copy
from pygame.locals import *
import pygame_menu  # this is the pygame module that makes this task so simple, as it handles the imputs and the GUI
pygame.init()
surface = pygame.display.set_mode((1200, 800))  # sets the scren dimensions

mytheme = pygame_menu.themes.THEME_DARK.copy()
#mytheme.title_background_color=(0, 0, 0)
myimage = pygame_menu.baseimage.BaseImage(image_path="images/background.jpg",
    drawing_mode=pygame_menu.baseimage.IMAGE_MODE_FILL
)
mytheme.background_color = myimage
X_view, Y_view = 1200, 800 # sets screen dimensions
Screen_View = pygame.display.set_mode((X_view, Y_view), 0, 32) #Main screen that I will add stuff on

WHITE = (255, 255, 255)
BLACK = (  0,   0,   0)
CYAN =  (  0, 255, 255)
MAGNETA=(255,   0, 255)
GREEN = (  1,  50,  32)
GREY =  (211, 211, 211)
RED =   (255,   0,   0)
FPS = 30 #defines how many times the screen will refresh per seccond
global AI_win_count
AI_win_count = 0
global AI_difficulty
AI_difficulty = 100
#air_mine_img = pygame.image.load('airmine.png')
#air_mine_img = pygame.transform.scale(air_mine_img,(20,15))

'''
for these clases below i did folow a tutorial
'''

class Button:   # this is a class i have mad eto handle the buttons (tutorial)
    def __init__(self, Label, PosXStart, PosYStart, Width, Length, Surface):
        self.Label = Label
        self.Font = pygame.font.Font(None, 32)
        self.TextColour = (255,255,255)    #(  0,  0,  0)     #white text
        self.PosXStart = PosXStart
        self.Width = Width
        self.Length = Length
        self.PosYStart = PosYStart
        self.BackgroundColour = (  10, 200,  52)  # green buttons
        self.Surface = Surface
    def DisplayButton(self): # function called to actually draw
        Button = pygame.draw.rect(self.Surface, self.BackgroundColour, (self.PosXStart, self.PosYStart, self.Length, self.Width))
        self._MakeLabel()

    def _MakeLabel(self):
        LabelX = (self.PosXStart + 10)
        LabelY = (self.PosYStart + (self.Length//20))
        ButtonText = self.Font.render(self.Label,1,self.TextColour)
        self.Surface.blit(ButtonText, (LabelX,LabelY))

    def click_seen(self, PositionTuple):
        if (PositionTuple[0] in range(self.PosXStart, self.PosXStart+self.Length+1)) and (PositionTuple[1] in range(self.PosYStart, self.PosYStart+self.Width+1)):
            return True
        else:
            return False
class CheckBox:
    def __init__(self, PosX, PosY, Width,Surface,Label,WordDistance):
        self.Font= pygame.font.Font(None,25)
        self.WHITE = (255,255,255)
        self.TextColour = self.WHITE
        self.WordDistance = WordDistance
        self.Surface = Surface
        self.GREEN = (0,255,0) #tick colour
        self.Clicked = False
        self.StartX = PosX
        self.StartY = PosY
        self.Width = Width    #button box dimensions
        self.Thickness = 8
        self.Label = Label
    def MakeBox(self): # draws the box by darwing lines in a rectangle
        TopLine = pygame.draw.line(self.Surface, self.WHITE,(self.StartX-2,self.StartY),
                                   (self.StartX+self.Width+2,self.StartY),1)
        BottomLine = pygame.draw.line(self.Surface,self.WHITE,(self.StartX-2,self.StartY+self.Width+2),
                                   (self.StartX+self.Width+2,self.StartY+self.Width+2),1)
        RightLine = pygame.draw.line(self.Surface,self.WHITE,(self.StartX+self.Width+2,self.StartY),
                                    (self.StartX+self.Width+2,self.StartY+self.Width+2),1)
        LeftLine = pygame.draw.line(self.Surface,self.WHITE,(self.StartX-2,self.StartY),
                                    (self.StartX-2,self.StartY+self.Width+2),1)

        self._AddLabel()
        if self.Clicked == True:
            self._AddTick()
    def click_seen(self, PositionTuple): # to see if user has clicked in the area
        if (PositionTuple[0] in range(self.StartX, self.StartX+self.Width+1)) and (PositionTuple[1] in range(self.StartY, self.StartY+self.Width+1)):
            if self.Clicked == True:
                self.Clicked = False
            else:
                self.Clicked = True

    def _TickCoordinates(self): # retrives the tick position (private)
        X1 = self.StartX
        Y1 = self.StartY + (self.Width//2)
        X2 = self.StartX + (self.Width//2)
        Y2 = self.StartY + self.Width
        X3 = self.StartX + self.Width
        Y3 = self.StartY
        return X1,Y1,X2,Y2, X3,Y3

    def _AddTick(self):
           FirstX,FirstY,SecondX,SecondY,ThirdX,ThirdY = self._TickCoordinates()
           pygame.draw.line(self.Surface, self.GREEN, (FirstX,FirstY),(SecondX,SecondY),self.Thickness)
           pygame.draw.line(self.Surface, self.GREEN, (SecondX, SecondY),(ThirdX,ThirdY),self.Thickness)
    def _AddLabel(self):
        LabelX = self.StartX - self.WordDistance
        LabelY = self.StartY + 8
        Text = self.Font.render(self.Label,1,self.TextColour)
        self.Surface.blit(Text, (LabelX,LabelY))
class RandomButton(Button):  # inheritance
    def __init__(self,Label, PosXStart, PosYStart, Width, Length, Surface, Range):
        super().__init__(Label, PosXStart, PosYStart, Width, Length, Surface)
        self._Range = Range

    def GetNumInRange(self):
        return str(round(random.uniform(self._Range[0], self._Range[1]),1))
class InputBox: #class for taking an input
    def __init__(self,PosX, PosY, Label,WordDistance,LengthValidation,RangeTuple):
        self.StartX = PosX
        self.StringLength = LengthValidation # inout validation <5 characters
        self.Range = RangeTuple # input validate of min and max range
        self.StartY = PosY
        self.Variable = ""
        self.Width = 30
        self.Length = 200
        self.WordDistance = WordDistance
        self.Clicked = False
        self.Label = Label    # ID given to box
        self.Surface = Screen_View
        self.Font = pygame.font.Font(None,25)
        self.WHITE = (255,255,255)
        self.TextColour = self.WHITE
    def MakeBox(self):   # draws the user input box
        TopLine = pygame.draw.line(self.Surface, self.WHITE,(self.StartX-2,self.StartY),
                                   (self.StartX+self.Length+2,self.StartY),1)
        BottomLine = pygame.draw.line(self.Surface,self.WHITE,(self.StartX-2,self.StartY+self.Width+2),
                                    (self.StartX+self.Length+2,self.StartY+self.Width+2),1)
        RightLine = pygame.draw.line(self.Surface,self.WHITE,(self.StartX+self.Length+2,self.StartY),
                                    (self.StartX+self.Length+2,self.StartY+self.Width+2),1)
        LeftLine = pygame.draw.line(self.Surface,self.WHITE,(self.StartX-2,self.StartY),
                                    (self.StartX-2,self.StartY+self.Width+2),1)
        self._AddLabel()
        self._DisplayVariable()
    def _AddLabel(self):
        LabelX = self.StartX - self.WordDistance - 5
        LabelY = self.StartY + 3
        Text = self.Font.render(self.Label,1,self.TextColour)
        self._AddText(Text, (LabelX,LabelY))
    def _DisplayVariable(self):
        XStart = self.StartX + 5
        YStart = self.StartY + 3
        Text = self.Font.render(self.Variable,1,self.TextColour)
        self._AddText(Text, (XStart,YStart))
    def _AddText(self, Text, CoordinatesTuple):
        self.Surface.blit(Text, (CoordinatesTuple[0], CoordinatesTuple[1]))
    def click_seen(self, PositionTuple):
        if (PositionTuple[0] in range(self.StartX, self.StartX+self.Length+1)) and (PositionTuple[1] in range(self.StartY, self.StartY+self.Width+1)):
            self.Clicked = True
        else:
            self.Clicked = False
    def AddCharacter(self, Input):
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
            if "." not in self.Variable:
                self.Variable += "."

        elif (Input == K_BACKSPACE):
            self.Variable = self.Variable[:-1]
    def _AdjustVariable(self,String):
        self.Variable += str(String)
        self.Variable = "%0.2f" % float(self.Variable)
        return self.Variable[:-1]
    def _NumInRange(self, Num):
        if (float(self.Variable + str(Num))>=self.Range[0]) and (float(self.Variable + str(Num))<=self.Range[1]):
            return True
        else:
            return False


TARGET= pygame.image.load("images/soilder.png")
TARGET = pygame.transform.scale(TARGET,(20,40))
BALL = pygame.image.load("images/missle.png")
BALL = pygame.transform.scale(BALL,(40,15))
Font = pygame.font.Font(None, 64) #
questionfont=pygame.font.Font(None, 20)
fpsClock = pygame.time.Clock()
X_view, Y_view = 900, 600 # screendimensions
Screen_View = pygame.display.set_mode((X_view, Y_view), 0, 32)
main_background = pygame.image.load("images/main_back.jpg")
main_background = pygame.transform.scale(main_background,(900,375))
pygame.display.set_caption("Zain's coursework simulation v3")
global win_loss_screen
win_loss_screen = False
global level
level = 0


def InputScreen(): # the main screen where users pass values in
    Title = Font.render("Answer/variable Input Screen", 1, WHITE)
    warning = questionfont.render("to input, select the box and type (max 2 digits), enter the given variables",1,RED)
    question= questionfont.render("If a missile is launched from ground level with an initial velocity of x at an angle of theta degrees",1,CYAN)
    questiona= questionfont.render("a) Calculate the time taken until it detonates the target",1,CYAN)
    questionb= questionfont.render("b) How far was the target from the launch site",1,CYAN)
    questionc= questionfont.render("c) If the target changed to being y kilometres away, what angle would you have to fire at assuming velocity is unchanged.",1,CYAN)
    questiond1= questionfont.render("d) Still firing at this new target, the shells have been changed thus altering the initial velocity.",1,CYAN)
    questiond2= questionfont.render("Provide a combination of theta and initial velocity that these new shells will hit the target.",1,CYAN)
    DisplacementBox, InitialVBox, AngleBox, MassBox, AIcheck, HideCheck, SubmitButton= create_widgets()
    Running = True
    Px = random.randint(10,100)
    Py = random.randint(10,100)
    Ptheta = random.randint(10,85)
    x = questionfont.render(("x =" + str(Px)),1,MAGNETA)
    theta = questionfont.render(("theta =" + str(Ptheta)),1,MAGNETA)
    y = questionfont.render(("y =" + str(Py)),1,MAGNETA)
    radPtheta = Ptheta*((math.pi)/180)
    global a_ans
    a_ans = (math.sin(radPtheta)*Px*2)/9.81
    print(a_ans)
    global b_ans
    b_ans = math.cos(radPtheta) *Px * a_ans  ## need to fix this
    print(b_ans)
    print(level)
    '''
    get the answers working
    '''
    while Running:
        Screen_View.fill(BLACK)
        Screen_View.blit(Title,(120,5)) # displays the title
        Screen_View.blit(warning,(230,55))
        #pygame.draw.line(Screen_View, GREEN, (450,0), (450,600),5)
        if level == 5:
            Screen_View.blit(question,(160,80)) #displays the questions
            Screen_View.blit(questiona,(280,110))
            Screen_View.blit(x,(430,130))  #displays the random variables
            Screen_View.blit(theta,(420,150))
        elif level == 6:
            Screen_View.blit(questionb,(290,80))
        elif level == 7:
            Screen_View.blit(questionc,(80,80))
            Screen_View.blit(y,(350,130))
        elif level == 8:
            Screen_View.blit(questiond1,(165,80))
            Screen_View.blit(questiond2,(180,110))
        DisplacementBox.MakeBox() , InitialVBox.MakeBox(), AngleBox.MakeBox(),MassBox.MakeBox(),AIcheck.MakeBox(), HideCheck.MakeBox(), SubmitButton.DisplayButton()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                (PosX,PosY)  = pygame.mouse.get_pos()
                InitialVBox.click_seen((PosX,PosY))
                DisplacementBox.click_seen((PosX,PosY))
                AngleBox.click_seen((PosX,PosY))
                MassBox.click_seen((PosX,PosY))
                HideCheck.click_seen((PosX,PosY))
                AIcheck.click_seen((PosX,PosY))
                if SubmitButton.click_seen((PosX,PosY)) == True:
                    Running = False
            elif (event.type == KEYDOWN) and (DisplacementBox.Clicked == True):
            	DisplacementBox.AddCharacter(event.key)
            elif (event.type == KEYDOWN) and (InitialVBox.Clicked == True):
            	InitialVBox.AddCharacter(event.key)
            elif (event.type == KEYDOWN) and (AngleBox.Clicked == True):
            	AngleBox.AddCharacter(event.key)
            elif (event.type == KEYDOWN) and (MassBox.Clicked == True):
            	MassBox.AddCharacter(event.key)
        pygame.display.update()
        fpsClock.tick(FPS)


    h, u, Angle = Convert(DisplacementBox.Variable,InitialVBox.Variable,AngleBox.Variable)
    if (u!="") and ((Angle!="") or (h!="")):
        global b_input
        b_input = h
        h, u, v, t, Angle,Mode = calculate_ans(h,u,Angle)
        run_sim(h,u,v,t,Angle,AIcheck.Clicked,HideCheck.Clicked,Mode)
        error_msg()

def change_AI_difficulty():
    global AI_difficulty
    global AI_win_count
    print("funct",AI_difficulty, AI_win_count)
    '''r
    if AI_win_count == 0:
        pass
    if AI_win_count < 0 :
        AI_difficulty += 50
    if AI_win_count > 0 :

        AI_difficulty -= 50
    #return AI_difficulty#
    #this function is now effectivley obsolete
    '''

def run_sim(h,u,v,t,Angle,AI,Hide,Mode):
    if u < 15 or Angle < 15 :
        InputScreen()
    print(AI)
    global AI_difficulty
    global AI_win_count
    InputButton = Button("Inputs", 600, 400, 35,200,Screen_View)
    ExplainButton = Button("Explain", 600, 470, 35, 200, Screen_View)
    MENUButton =  Button("Return to Main menu", 550, 540, 40, 270,Screen_View)
    HIDE = CheckBox(500,400,30,Screen_View,"Hide Parameters:",160)
    HIDE.Clicked = Hide
    Input = False
    Explain = False
    floorY_co_ord = 350
    h = h
    PosX = 50
    PosY = floorY_co_ord #As the particle will start at the ground
    g = -9.8
    ANGLEDEGREES = round(Angle,1)
    ANGLERADIANS = math.radians(ANGLEDEGREES)
    u = u
    i = u * round(math.cos(ANGLERADIANS), 1) #horizont velcoity compnent
    j = u * round(math.sin(ANGLERADIANS), 1) # vertical velocity component
    SCALEFACTOR = 1.3 # makes it look better
    CoordinatesList = list_get(i,j,PosX,PosY)
    TrailList = copy.deepcopy(CoordinatesList) # this is a recursive call of copying the file over
    TrailList = trail_tweek(TrailList)
    Motion = True
    Pointer = 0
    Screen_View.fill(WHITE)
    Running = True
    PosXAI = 500
    PosYAI = floorY_co_ord
    intercepter=pygame.image.load('images/flare.png')
    collision = False
    win = False
    change_AI_difficulty()
    print("run sim",AI_difficulty, AI_win_count)
    while Running:
        Screen_View.fill(BLACK)
        Screen_View.blit(main_background,(0,0))
        InputButton.DisplayButton()
        ExplainButton.DisplayButton()
        MENUButton.DisplayButton()
        HIDE.MakeBox()
        if HIDE.Clicked == False:
            printvalues(h,u,v,t,ANGLEDEGREES)
        if Motion == True:
            PosX, PosY = CoordinatesList[Pointer][0], CoordinatesList[Pointer][1]
            #print('(',PosX,',',PosY,')')
            Screen_View.blit(BALL, (PosX, PosY))
            r'''

            #Makes trail
            dotimg=pygame.image.load('dot.png')
            dotimg=pygame.transform.scale(dotimg,(5,5))
            Screen_View.blit(dotimg, ((PosX-5), (PosY+5)))
            '''
            if level == 5 or level == 6 or level==7 or level==8 :
                Screen_View.blit(TARGET,((CoordinatesList[-1][0]) ,330))
            if AI==True:
                diffX = PosXAI - PosX
                diffY = PosYAI - PosY
                #print('(',diffX,',',diffY,')')
                moveX = diffX / AI_difficulty
                moveY = diffY / AI_difficulty
                x=random.randint(-2,2)
                y=random.randint(-2,2)
                #x=min((u/(random.randint(-2,2))),2)
                PosXAI -= (moveX + x)
                PosYAI -= (moveY + y)
                Screen_View.blit(intercepter, (PosXAI, PosYAI))
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
                Screen_View.blit(collisionimg, (PosX, PosY))
                win = False
                #global AI_difficulty
                AI_win_count += 1
                AI_difficulty *= 2
                loss_screen(win,h,u,v,t,ANGLEDEGREES,AI,HIDE,Mode)
            if collision == False: #and b_input == ans_b :
                win = True
                print("collision is", collision)
                #print("user : ",b_input ,"ans:",ans_b)
            else:
                PosY = floorY_co_ord
                PosX = CoordinatesList[Pointer][0]
                Screen_View.blit(collisionimg, (PosX, PosY))
            if win == True :
                AI_win_count -= 1
                AI_difficulty /= 2
                win_screen(win,h,u,v,t,ANGLEDEGREES,AI,HIDE,Mode)
        if Pointer>1:
            pygame.draw.aalines(Screen_View, MAGNETA,False,TrailList[:Pointer+1000] ,5)
            pygame.draw.aalines(Screen_View, CYAN,False,TrailList[:Pointer] ,5)

        pygame.draw.line(Screen_View, BLACK, (0,floorY_co_ord+25), (X_view,floorY_co_ord+25),1)  # draws the floor line
        for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == MOUSEBUTTONDOWN:
                    (PosX, PosY) = pygame.mouse.get_pos()
                    HIDE.click_seen((PosX,PosY))
                    if InputButton.click_seen((PosX,PosY)) == True:
                        Input = True #It will be true which implies that that user must enter inputs again
                        Running = False
                    elif ExplainButton.click_seen((PosX,PosY)) == True:
                        Explain = True
                        Running = False
                    elif MENUButton.click_seen((PosX,PosY)) == True:
                        menu.mainloop(surface)
        pygame.display.update()
        fpsClock.tick(FPS)
    if Input == True:
        InputScreen()
    elif Explain == True:
        if Mode == 1:
            explanations1(h,u,v,t,ANGLEDEGREES,AI,HIDE.Clicked,Mode)
        elif Mode == 2:
            explanations2(h,u,v,t,ANGLEDEGREES,AI,HIDE.Clicked,Mode)

def win_screen(win,s,u,v,t,ANGLEDEGREES,AI,HIDE,Mode):
    message = Font.render("You are correct !! ",1,WHITE)
    s,u,v,t,ANGLEDEGREES,HIDE,Mode = s,u,v,t,ANGLEDEGREES,HIDE,Mode
    while win == True:
        win_loss_screen = True
        Screen_View.fill(BLACK)
        Screen_View.blit(message,(260,250))
        MENUButton =  Button("Return to Main menu", 300, 530, 40, 270,Screen_View)
        ExplainButton = Button("Explain", 340, 450, 35, 200, Screen_View)
        MENUButton.DisplayButton()
        ExplainButton.DisplayButton()
        for event in pygame.event.get():
            if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                (PosX,PosY)  = pygame.mouse.get_pos()
                HIDE.click_seen((PosX,PosY))
                if MENUButton.click_seen((PosX,PosY)) == True:
                    win = False
                    menu.mainloop(surface)
                elif ExplainButton.click_seen((PosX,PosY)) == True:
                    Explain = True
                    #Running = False
                    if Explain == True:
                        if Mode == 1:
                            explanations1(s,u,v,t,ANGLEDEGREES,AI,HIDE.Clicked,Mode)
                        elif Mode == 2:
                            explanations2(s,u,v,t,ANGLEDEGREES,AI,HIDE.Clicked,Mode)
        pygame.display.update()
        fpsClock.tick(FPS)


def loss_screen(win,s,u,v,t,ANGLEDEGREES,AI,HIDE,Mode):
    message = Font.render("sadly, you are incorrect, try again ",1,WHITE)
    s,u,v,t,ANGLEDEGREES,HIDE,Mode = s,u,v,t,ANGLEDEGREES,HIDE,Mode
    while win == False:
        win_loss_screen = True
        Screen_View.fill(BLACK)
        Screen_View.blit(message,(120,250))
        MENUButton =  Button("Return to Main menu", 300, 530, 40, 270,Screen_View)
        MENUButton.DisplayButton()
        ExplainButton = Button("Explain", 340, 450, 35, 200, Screen_View)
        ExplainButton.DisplayButton()
        for event in pygame.event.get():
            if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                (PosX,PosY)  = pygame.mouse.get_pos()
                if MENUButton.click_seen((PosX,PosY)) == True:
                    #win = False
                    menu.mainloop(surface)
                elif ExplainButton.click_seen((PosX,PosY)) == True:
                    Explain = True
                    #Running = False
                    if Explain == True:
                        if Mode == 1:
                            explanations1(s,u,v,t,ANGLEDEGREES,AI,HIDE.Clicked,Mode)
                        elif Mode == 2:
                            explanations2(s,u,v,t,ANGLEDEGREES,AI,HIDE.Clicked,Mode)
        pygame.display.update()
        fpsClock.tick(FPS)

#Functions Needed
def explanations1(h,u,v,t,Angle,AI,Hide,Method):
    Method = Method
    ExplainFont = pygame.font.Font(None,32)
    explaining = True
    VExplain2str = "v = -"+ str(u)
    #print("type is", type(VExplain2str))
    TimeExplain3str = "t = "+str(u)+"sin("+str(Angle)+")/4.9"
    AngleExplain3str = "θ = sin^-1(√(2*g*"+str(h)+"))/"+str(u)
    VExplain1 = ExplainFont.render("v = -u",1,WHITE)
    VExplain2 = ExplainFont.render(VExplain2str,1,WHITE)
    AngleExplain1 = ExplainFont.render("Rearrange v^2 =u^2 + 2as where v = 0",1,WHITE)
    AngleExplain2 = ExplainFont.render("usinθ = √(2gs) => θ = sin^-1((√2gs))/u",1,WHITE)
    AngleExplain3 = ExplainFont.render(AngleExplain3str,1,WHITE)
    TimeExplain1 = ExplainFont.render("Rearrange s = ut + 0.5at^2 where s = 0",1,WHITE)
    TimeExplain2 = ExplainFont.render("t = usinθ/4.9",1,WHITE)
    TimeExplain3 = ExplainFont.render(TimeExplain3str,1,WHITE)
    OKButton = Button("OK",400,500,35,100,Screen_View) #(Label, PosXStart, PosYStart, Width, Length, Surface)
    while explaining:
            display_explainations(VExplain1, VExplain2,AngleExplain1, AngleExplain2, AngleExplain3, TimeExplain1, TimeExplain2, TimeExplain3, OKButton)
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    (PosX, PosY) = pygame.mouse.get_pos()
                    if OKButton.click_seen((PosX,PosY)) == True:
                        explaining = False
                        if win_loss_screen == True:
                            menu.mainloop(surface)
            pygame.display.update()
            fpsClock.tick(FPS)
    run_sim(h,u,v,t,Angle,AI,Hide,Method)

def explanations2(h,u,v,t,Angle,AI,Hide,Method):
    Method = Method
    ExplainFont = pygame.font.Font(None,32)
    explaining = True
    VExplain2str = "v = -"+ str(u)
    TimeExplain3str = "t = "+str(u)+"sin("+str(Angle)+")/4.9"
    DisplacementExplain3str = "s = "+str(u)+"sin("+str(Angle)+")("+str(round(t,2))+"/2) - 4.9("+str(round(t,2))+"/2)^2"
    #print("type is", type(VExplain2str))
    VExplain1 = ExplainFont.render("v = -u",1,WHITE)
    VExplain2 = ExplainFont.render(VExplain2str,1,WHITE)
    TimeExplain1 = ExplainFont.render("Rearrange s = ut + 0.5at^2 where s = 0",1,WHITE)
    TimeExplain2 = ExplainFont.render("t = usinθ/4.9",1,WHITE)
    TimeExplain3 = ExplainFont.render(TimeExplain3str,1,WHITE)
    DisplacementExplain1 = ExplainFont.render("At time, t/2, height is at a max => using s = ut + 0.5at^2",1,WHITE)
    DisplacementExplain2 = ExplainFont.render("s = usinθ(t/2) - 4.9(t/2)^2",1,WHITE)
    DisplacementExplain3 = ExplainFont.render(DisplacementExplain3str,1,WHITE)
    OKButton = Button("OK",400,500,35,100,Screen_View) #(Label, PosXStart, PosYStart, Width, Length, Surface)
    while explaining:
            display_explainations(VExplain1,VExplain2, TimeExplain1,TimeExplain2,TimeExplain3,DisplacementExplain1,DisplacementExplain2,DisplacementExplain3,OKButton)
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    (PosX, PosY) = pygame.mouse.get_pos()
                    if OKButton.click_seen((PosX,PosY)) == True:
                        explaining = False
                        if win_loss_screen == True:
                            menu.mainloop(surface)
            pygame.display.update()
            fpsClock.tick(FPS)
    run_sim(h,u,v,t,Angle,AI,Hide,Method)

def display_explainations(a,b,c,d,e,f,g,h,Button): # prints the eplanations out , to avoid repeating code
     Screen_View.fill(BLACK)
     Screen_View.blit(a,(40,30))
     Screen_View.blit(b,(40,70))
     Screen_View.blit(c,(40,120))
     Screen_View.blit(d,(40,170))
     Screen_View.blit(e,(40,220))
     Screen_View.blit(f,(40,270))
     Screen_View.blit(g,(40,320))
     Screen_View.blit(h,(40,370))
     Button.DisplayButton()

def create_widgets(): # used in input screen
    DisplacementBox = InputBox(400, 190, "Displacement (s)(m):", 180, 6, (0.1,1000))
    InitialVBox = InputBox(400, 250, "Initial Velocity (u)(m/s):", 200, 6, (1,100))
    AngleBox = InputBox(400, 310, "Angle (θ)(degrees):", 165, 4,(1,90))
    MassBox = InputBox(400,370, "Mass (kg):", 90, 4, (0.1,10))
    HideCheck = CheckBox(480, 440, 30, Screen_View, "Hide Variables:",140)
    AIcheck = CheckBox(480, 480, 30, Screen_View, "AI (ON/OFF):",120)
    SubmitButton = Button("Submit", 400, 540, 40, 100,Screen_View)
    return DisplacementBox, InitialVBox, AngleBox, MassBox, AIcheck, HideCheck, SubmitButton

def VerticalCoordinates(j, g, PosY, UP, DOWN): # calculates the y co-ordinates
    SCALEFACTOR = 2
    floorY_co_ord = 350
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
        j = j + (g/FPS)
        if PosY >= floorY_co_ord:
            PosY = floorY_co_ord
            return [PosY]
        return [PosY] + VerticalCoordinates(j, g, PosY,False, True)

def Round(List):
    for count in range(len(List)):
        List[count][0] = round(List[count][0],1)
        List[count][1] = round(List[count][1],1)
    return List

def x_coord(i,PosX, LengthOfVertList):
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

def list_merge(ListX, ListY):
    ListXY = []
    for count in range(len(ListX)):
        ListXY.append([ListX[count], ListY[count]])
    ListXY = Round(ListXY)
    return ListXY

def list_get(i,j,PosX,PosY):
    g = -9.8    # vector avriable is now neagative
    VerticalList= VerticalCoordinates(j,g,PosY, True, False)
    HorizontalList = x_coord(i,PosX, len(VerticalList))
    MainList = list_merge(HorizontalList, VerticalList)
    return MainList

def trail_tweek(Trail):   # makes the graphical aspect of the trail smoother
    for index in range(len(Trail)):
        Trail[index][0],Trail[index][1] = Trail[index][0]+2, Trail[index][1]+13
    return Trail

def printvalues(h,u,v,t,Angle):
    ParameterFont = pygame.font.Font(None, 30)
    S = ParameterFont.render("S  = {0} m".format("%.1f"%b_ans),1,WHITE)
    U = ParameterFont.render("U = {0} m/s".format("%.1f"%u),1,WHITE)
    V = ParameterFont.render("V = {0} m/s".format("%.1f"%v),1,WHITE)
    A = ParameterFont.render("A = -g = -9.8 m/s^2",1,WHITE)
    T = ParameterFont.render("T = {0} s".format("%.1f"%t),1,WHITE)
    ANGLE = ParameterFont.render("θ = {0}°".format("%.1f"%Angle),1,WHITE)
    Screen_View.blit(S,(40, 400))
    Screen_View.blit(U,(40, 430))
    Screen_View.blit(V,(40, 460))
    Screen_View.blit(A,(40, 490))
    Screen_View.blit(T,(40, 520))

def error_msg():
    Title1 = Font.render("Please Enter The Initial Velocity &", 1, WHITE)
    Title2 = Font.render("EITHER The Angle Of Projection",1,WHITE)
    Title3 = Font.render("OR The Displacement",1,WHITE)
    OKButton =  Button("OK", 380, 450, 40, 100,Screen_View)
    Running =True

    while Running:
        Screen_View.fill(BLACK)
        Screen_View.blit(Title1,(85,100))
        Screen_View.blit(Title2,(100,200))
        Screen_View.blit(Title3,(170,300))
        OKButton.DisplayButton()
        for event in pygame.event.get():
            if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                (PosX,PosY)  = pygame.mouse.get_pos()
                if OKButton.click_seen((PosX,PosY)) == True:
                    Running = False
        pygame.display.update()
        fpsClock.tick(FPS)
    InputScreen() #Goes back to the input screen

def calculate_ans(h,u,Angle): #calculates using SUVAT
    g = 9.8 # accleration due to gravity, is a constant on the earths surface
    if (h!="") and (Angle==""):
        if math.sqrt(2*g*h)/u>1: #avoid impossiible scearios
            impossible_situation()
        else:
            Mode = 1
            v = -u
            Angle = math.asin(math.sqrt(2*g*h)/u) #Rearranging v**2 = u**2 + 2as, at top v= 0
            t = (u*math.sin(Angle))/4.9 #Using s=ut+0.5at**2
            return h, u, v, t, math.degrees(Angle), Mode
    elif (h=="") and (Angle!=""):
        Mode = 2
        v = -u
        t = (u*math.sin(Angle))/4.9 #total time
        h = (u*math.sin(Angle)*(t/2)) - (4.9 * (t/2)**2) #max vertical displacement
        return h, u, v, t, math.degrees(Angle), Mode
    elif (h!="") and (Angle!="") and (u!=""):
        error_msg()   # impossible scenario

def impossible_situation(): #Displays an error message which tells the user that the inputs entered are not feasible
    Title1 = Font.render("The inputs are not valid.", 1, WHITE) #Error message
    Title2 = Font.render("The value for Displacement is too high", 1, WHITE)
    Title3 = Font.render("for the given velocity.", 1, WHITE)
    Title4 = Font.render("Such a situation shouldn't occur.", 1, WHITE)
    Title5 = Font.render("Please reload the program.", 1, WHITE)
    OKButton =  Button("OK", 350, 500, 40, 100,Screen_View)
    Running =True

    while Running:
        Screen_View.fill(BLACK)
        Screen_View.blit(Title1,(150,50))
        Screen_View.blit(Title2,(40,130))
        Screen_View.blit(Title3,(175,210))
        Screen_View.blit(Title4,(70,290))
        Screen_View.blit(Title5,(180,370))
        OKButton.DisplayButton()
        for event in pygame.event.get():
            if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                (PosX,PosY)  = pygame.mouse.get_pos()
                if OKButton.click_seen((PosX,PosY)) == True:
                    Running = False
                    InputScreen()
        pygame.display.update()
        fpsClock.tick(FPS)



def Convert(s,u,Angle): # converts inputs to float numbers for greater accuracy
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
        Angle = math.radians(Angle) #PYGAME WORKS IN RANDIANS
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
    OKButton =  Button("OK", 380, 550, 40, 100,Screen_View)
    Running =True
    while Running:
        Screen_View.fill(WHITE)
        Screen_View.blit(Title1,(0,50))
        Screen_View.blit(Title2,(0,150))
        Screen_View.blit(Title3,(0,250))
        Screen_View.blit(Title4,(0,350))
        Screen_View.blit(Title5,(0,450))
        OKButton.DisplayButton()
        for event in pygame.event.get():
            if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                (PosX,PosY)  = pygame.mouse.get_pos()
                if OKButton.click_seen((PosX,PosY)) == True:
                    Running = False
        pygame.display.update()
        fpsClock.tick(FPS)

def components():
    lvl1Font = pygame.font.Font(None,33) # smaller font
    Title1 = lvl1Font.render("every force is made up of two components, horizontal and vertical, as shown in the diagram", 1, RED)
    Title2 = lvl1Font.render("you can find the horizontal comonent by doing Fcos(angle)",1,RED)
    Title3 = lvl1Font.render("you can find the vertical comonent by doing Fsin(angle)",1,RED)
    OKButton =  Button("OK", 380, 550, 40, 100,Screen_View)
    Running =True
    image_comp=pygame.image.load('images/components .png')
    while Running:
        Screen_View.fill(WHITE)
        Screen_View.blit(Title1,(0,50))
        Screen_View.blit(Title2,(0,150))
        Screen_View.blit(Title3,(0,250))
        Screen_View.blit(image_comp, (300,300))
        OKButton.DisplayButton()
        for event in pygame.event.get():
            if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                (PosX,PosY)  = pygame.mouse.get_pos()
                if OKButton.click_seen((PosX,PosY)) == True: #Know you get to go to the input screen
                    Running = False
        pygame.display.update()
        fpsClock.tick(FPS)

def velocity_level():
    lvl1Font = pygame.font.Font(None,30) # smaller font
    lvl3Font = pygame.font.Font(None,55) # smaller font
    Title1 = Font.render("velocity is the rate of change of distance", 1, RED)
    Title2 = lvl3Font.render("you can find the velocity by doing distance/time",1,RED)
    Title3 = lvl1Font.render("remember velocity is a vector, so depending on the direction can be negative or positive",1,RED)
    OKButton =  Button("OK", 380, 550, 40, 100,Screen_View)
    Running =True
    image_comp=pygame.image.load('velocitydiagram.png')
    while Running:
        Screen_View.fill(WHITE)
        Screen_View.blit(Title1,(0,50))
        Screen_View.blit(Title2,(10,150))
        Screen_View.blit(Title3,(10,250))
        Screen_View.blit(image_comp, (70,300))
        OKButton.DisplayButton()
        for event in pygame.event.get():
            if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                (PosX,PosY)  = pygame.mouse.get_pos()
                if OKButton.click_seen((PosX,PosY)) == True: #Know you get to go to the input screen
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
    OKButton =  Button("OK", 380, 550, 40, 100,Screen_View)
    Running =True
    while Running:
        Screen_View.fill(WHITE)
        Screen_View.blit(Title1,(40,50))
        Screen_View.blit(Title2,(30,150))
        Screen_View.blit(Title3,(0,250))
        Screen_View.blit(Title4,(100,350))
        Screen_View.blit(Title5,(15,450))

        OKButton.DisplayButton()
        for event in pygame.event.get():
            if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                (PosX,PosY)  = pygame.mouse.get_pos()
                if OKButton.click_seen((PosX,PosY)) == True: #Know you get to go to the input screen
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
    global level
    level = 5
    InputScreen()

def load_level_6():
    print("level 6 loading ... ")
    global level
    level = 6
    InputScreen()

def load_level_7():
    print("level 7 loading ... ")
    global level
    level = 7
    InputScreen()

def load_level_8():
    print("level 8 loading ... ")
    global level
    level = 8
    InputScreen()
'''
def set_difficulty(value, difficulty):
    global difficulty
    if
    difficulty
'''




menu = pygame_menu.Menu("Zain's projectile cs cw game", 900, 600,
                       theme=mytheme)   # sets the dimensions of the menu itsef, its cpation and the theme.
'''
menu = pygame_menu.Menu("Zain's projectile cs cw game", 900, 600,
                       theme=pygame_menu.themes.THEME_DARK)
'''                                                               # this is a basic default theme from the pygame.menu library

# menu.add.selector('Difficulty :', [('Easy', 1), ('Medium', 2), ('Hard', 3)], onchange=set_difficulty)
menu.add.button('level 1 : units and conversions ', load_level_1)
menu.add.button('level 2 : components  ',load_level_2)
menu.add.button('level 3 : velocity',load_level_3)
menu.add.button('level 4 : acceleration ',load_level_4)
menu.add.button('level 5 : exam questions 1 ',load_level_5)
menu.add.button('level 6 : exam questions 2 ',load_level_6)
menu.add.button('level 7 : exam questions 3 ',load_level_7)
menu.add.button('level 8 : exam questions 4 ',load_level_8)


menu.add.button('Quit', pygame_menu.events.EXIT) # this simply makes a button called quit to halt the code
menu.mainloop(surface)
