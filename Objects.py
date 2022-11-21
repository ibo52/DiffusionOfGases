import time,os

from settings import *
import pygame
import random
from math import sin,cos,pi,sqrt
from time import sleep
from threading import Thread


pygame.init()
class vector:
    def __init__(self,x=0,y=0):
        self.x=x
        self.y=y
    def get(self):
        return (self.x,self.y)
    def set(self,x,y):
        self.x,self.y=x,y
    def reverse(self):
        self.x*=-1
        self.y*=-1
    def reverse_x(self):
        self.x*=-1
    def reverse_y(self):
        self.y*=-1
    def get_reverse(self):
        return (-1*self.x,-1*self.y)
    def set_x(self,x):
        self.x=x
    def set_y(self,y):
        self.y=y
class GasMolecule:
    """Simulation and modelling the behaviour of gas molecule
    --default values setted for oxygene(O2) molecule--

    velocity of a molecule -> V=3*R*T/M
            R=gas constant(8.3145)(dont need for now)
            T=temperature (KELVIN)
            M=mass (kilogram/mol)"""
    def __init__(self,temperature=298.15,mass=32,radius=10,color=RED):
        self.temperature=temperature  #equals to room temperature which is 25 degrees
        self.mass = mass              # mass of oxygene
        self.radius = radius          # radius of molecule.Choose big value enough to see easily
        self.color=color              #Choose a color to easily see

        # define random a val to determine motion direction
        k=sqrt(3 * 8.3145 * self.temperature / self.mass)
        self.acceleration = vector(random.uniform(-1, 1) * k / 5
                                   , random.uniform(-1, 1) * k / 5)
        self.velocity = vector(self.acceleration.x, self.acceleration.y)

        self.x=random.randint(0,Resolution[0])    #allocate molecule to random positions
        self.y=random.randint(0,Resolution[1])

    def return_pos(self):
        return (self.x,self.y)

    def move(self):
        self.x+=self.velocity.x
        self.y+=self.velocity.y

        pygame.draw.circle(Screen,self.color,self.return_pos(),self.radius)

#molecules will NOT overflow from screen
def circle_line_collide(xy1,xy2,cxy):
    x1, y1 = xy1
    x2, y2 = xy2
    x3, y3 = cxy
    px = x2 - x1
    py = y2 - y1

    line_length = px * px + py * py

    u=-1
    if line_length!=0:
        u = ((x3 - x1) * px + (y3 - y1) * py) / float(line_length)

    if u > 1:
        xx=x2
        yy=y2
    elif u < 0:
        xx=x1
        yy=y1
    else:
        xx = x1 + u * px
        yy = y1 + u * py


    dx = x3-xx
    dy = y3-yy

    distance = sqrt(dx * dx + dy * dy)

    return [dx,dy,distance]
    #https://stackoverflow.com/questions/849211/shortest-distance-between-a-point-and-a-line-segment
    return [distance,dx,dy]

def check_screenFlow(ObjectList,rectList=[]):

    for obj in ObjectList:#return_pos is position or center of circle object

        #objeler ekranın dışına çıkmasın
        if not 0<=obj.x<=Resolution[0]:
            obj.acceleration.x*=-1
            obj.velocity.x=obj.acceleration.x

        if not 0<=obj.y<=Resolution[1]:
            obj.acceleration.y*=-1
            obj.velocity.y=obj.acceleration.y

        for rect in rectList:

            col=circle_line_collide((rect.x1,rect.y1),(rect.x2,rect.y2), (obj.x,obj.y)  )

            if col[2]<=obj.radius:
                if abs(col[0])>0:

                    if col[0]<0:
                        obj.x-=.11
                    else:
                        obj.x+=.11

                    obj.acceleration.reverse_x()
                    obj.velocity.reverse_x()

                if abs(col[1])>0:

                    if col[1] < 0:
                        obj.y-=.11
                    else:
                        obj.y += .11

                    obj.acceleration.reverse_y()
                    obj.velocity.reverse_y()



            """
            if not rect.x1+obj.radius <= obj.x <= (rect.x2) -obj.radius:
                obj.acceleration.y *= -1
                obj.velocity.y = obj.acceleration.y

            if not rect.y1+obj.radius <= obj.y <= (rect.y2) -obj.radius:
                obj.acceleration.y *= -1
                obj.velocity.y = obj.acceleration.y"""

def collide(obj,ObjectList):
    copiedList = ObjectList.copy()

    for a in range(len(copiedList)):

        x_diff= (obj.x - copiedList[a].x) ** 2
        y_diff= (obj.y - copiedList[a].y) ** 2
        distance=x_diff+y_diff
        distance=abs(distance)
        distance=sqrt(distance)

        if (obj.radius + copiedList[a].radius) >=distance:
            return True;
    return False

def objects_collides(ObjectList,button1,button2,rects_list=[]):
    copiedList=ObjectList.copy()
    check_screenFlow(ObjectList,rects_list)

    for i in range(len(copiedList)):
        obj=copiedList.pop(0)

        for a in range(len(copiedList)):

            #print("checking: ",copiedList.index(obj),a)
            x_diff= (obj.x - copiedList[a].x) ** 2
            y_diff= (obj.y - copiedList[a].y) ** 2
            distance=x_diff+y_diff
            distance=abs(distance)
            distance=sqrt(distance)

            #birbirine yaklaşan molekülleri çizgiyle göster
            if (obj.radius + copiedList[a].radius)*2 >=distance >=(obj.radius + copiedList[a].radius) and button2:
                pygame.draw.line(Screen, GREEN, obj.return_pos(),
                                 copiedList[a].return_pos(),3) # tüm objeleri çizgiyle birbirine bağladık
            #if objects collided;
            if (obj.radius + copiedList[a].radius) >=distance:
                #print("çarpanlar:", obj.return_pos(), copiedList[a].return_pos())

                #print("velocity to change:",obj.velocity.get(),ObjectList[a].velocity.get())
                """there are hesenbergie :D unpredictable events here UPDATE:fixed ,i suppose"""

                #changing acceleration between collided two molecules
                t1,t2=obj.acceleration.get(),copiedList[a].acceleration.get()

                obj.acceleration.set(*t2)
                obj.velocity.set(*t2)

                copiedList[a].acceleration.set(*t1)
                copiedList[a].velocity.set(*t1)


                #heat transfer section
                T_diff=abs(copiedList[a].temperature- obj.temperature)/2

                if obj.temperature>copiedList[a].temperature:
                    is_colder=False
                else:
                    is_colder=True

                if is_colder:
                    obj.temperature+=T_diff
                    copiedList[a].temperature-=T_diff

                elif not is_colder:
                    obj.temperature-=T_diff
                    copiedList[a].temperature+=T_diff
                else:
                    print("heat transfer>> hata line:212 kırmance")

                #print("new velocities:", obj.velocity.get(), ObjectList[a].velocity.get())

            if button1:
                pygame.draw.line(Screen, MAGENTA, obj.return_pos(), copiedList[a].return_pos())

class Text:
    def __init__(self,text="test",x=0,y=0,size=32,color=(128,96,156)):
        self.font=pygame.font.SysFont("monospace",size)
        self.toPrint=text
        self.addition=""
        self.color=color

        self.x=x
        self.y=y

    def show(self):

        self.update()
        renderThis=self.font.render(self.toPrint+self.addition,1,self.color)
        Screen.blit(renderThis,(self.x,self.y))

    def update(self,text=''):
        if text!='':
            self.addition=text

class Button:
    def __init__(self,text,x,y,width,height):
        self.rect=pygame.Rect(x,y,width,height)

        self.trigger=False
        self.txt=text.split()
        self.texts=[Text(self.txt[i],x,self.rect.top+(i*10),10,BLACK) for i in range(len(self.txt))]
    def update(self):

        pygame.draw.rect(Screen,YELLOW,self.rect)
        for text in self.texts:
            text.show()
    def change_trigger(self):
        self.trigger=not self.trigger
class line_:
    def __init__(self,x,y,x2,y2,color=RED,density=3):
        self.x1=x
        self.y1=y
        self.y2=y2
        self.x2=x2
        self.color=color
        self.density=density
    def update(self):
        pygame.draw.line(Screen,self.color,(self.x1,self.y1),(self.x2,self.y2),self.density)



"""class Tube:
    def __init__(self,x=10,y=10,width=Screen.get_width()-20,height=Screen.get_height()-20 ,color=RED):
        self.x=x
        self.y=y
        self.height=height
        self.width=width

        self.color=color
    def update(self):
        pygame.draw.rect(Screen,self.color,(self.x,self.y,self.width,self.height),2)
    def change_x(self,x):
        self.x=x
    def change_y(self,y):
        self.y=y
    def change_width(self,width):
        self.width=width
    def change_height(self,height):
        self.height=height
"""
def generateMolecules_at_special_point(num,x1,x2,y1,y2,mcolor=RED,rad=10,temp=298.15):
    mList=[]
    for m in range(num):
        mx=GasMolecule(color=mcolor,radius=rad,temperature=temp)

        #do-while loop
        mx.x=random.randint(x1,x2)
        mx.y=random.randint(y1,y2)
        while( collide(mx,mList)==True ):
            mx.x=random.randint(x1,x2)
            mx.y=random.randint(y1,y2)

        mList.append(mx)
    return mList

def generateMolecules(num,mcolor=RED,temp=298.15):
    mList=[]
    for m in range(num):
        molx=GasMolecule(color=mcolor,temperature=temp)
        if not collide(molx,mList):
            mList.append(molx)
    return mList


#calc distribuions of masses on given list;on the x-axis
def return_entropy(liste):
    dist_x = 0
    for element in liste:
        dist_x += element.x
    dist_x = dist_x / len(liste)
    return dist_x

def mass_distribution_entropy(liste,color=(0,0,0)):

    dist_x=return_entropy(liste)

    end=Resolution[0]-50,Resolution[1]-25
    start=20,Resolution[1]-25
    mid=(end[0]+start[0])/2,Resolution[1]-25

    pygame.draw.line(Screen,BLACK,mid,(mid[0],mid[1]+10),2)
    pygame.draw.line(Screen, BLACK,start,end, 2)
    pygame.draw.circle(Screen,color,(dist_x,Resolution[1]-25),10)

def calc_average_T(liste):
    T=0
    for obj in liste:
        T+=obj.temperature
    return round(T/len(liste),3)

#thread aç
def register(t1List,t2List,done,counter,savePath=os.path.expanduser('~'),fileName="diffusion results.txt"):

    timeCounter=counter
    mol1len=len(t1List)
    mol2len=len(t2List)
    t1Average=calc_average_T(t1List)
    t2Average=calc_average_T(t2List)

    entropy1=round(return_entropy(t1List),2)
    entropy2=round(return_entropy(t2List),2)
    entropyRange=(Resolution[0]-50) - 20


    with open(savePath + "/"+fileName, "a") as file:
        if timeCounter==0:
            file.write("diffusion simulation (halil ibrahim mut 190315037)\n")
            file.write("(heat)T1({} mols)\tT2({}mols)\tentropy1\tentropy2 (entropy range:0,{})\n".format(mol1len,mol2len,entropyRange))
            file.write("-------------------------------------\n")

        added="T1={}\tT2={}\tentropy1={}\tentropy2={}\ttime={}\n".format(t1Average,t2Average,entropy1,entropy2,timeCounter)

        file.write( added )
        sleep(1.2)



set_mol_connection_BUTTON=Button("connect molecules all together",Resolution[0]-40,100,40,40)
set_mol_connection_BUTTON.change_trigger()
connectIfMoleculesGetsClose_BUTTON=Button("connect if molecules gets closer",Resolution[0]-40,160,40,40)

setTubeVolBUTTON=Button("REMOVE the divider",Resolution[0]-40,50,40,40)

buttons=[set_mol_connection_BUTTON,connectIfMoleculesGetsClose_BUTTON,setTubeVolBUTTON]