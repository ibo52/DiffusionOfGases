import pygame

from settings import *
from Objects import *
from time import sleep

numOfMolecules=16

x_1=40;x_2=Resolution[0];y_1=40;y_2=Resolution[1]

maviL=generateMolecules_at_special_point(numOfMolecules,x_1,(x_2-90)//2,40,(y_2-90)//2,mcolor=BLUE,rad=4,temp=53.15)
kırmızıL=generateMolecules_at_special_point(numOfMolecules,(x_2-90)//2,x_2-90,40,(y_2-90)//2,rad=8)
yeşilL=generateMolecules_at_special_point(numOfMolecules,(x_2-90)//2,x_2-90,(y_2-90)//2,y_2-90,rad=12,mcolor=GREEN,temp=413.15)
morL=generateMolecules_at_special_point(numOfMolecules,x_1,(x_2-90)//2,(y_2-90)//2,y_2-90,rad=4,mcolor=MAGENTA,temp=123.15)

l=maviL+kırmızıL+yeşilL+morL

maviT=Text(text="blue average T:",x=20,y=-8)
kırmızıT=Text(text="red average T:",x=(Resolution[0]//2)+100,y=-8)
yeşilT=Text(text="green average T:",x=20,y=28)
morT=Text(text="magenta average T:",x=(Resolution[0]//2)+100,y=28)
elapsedTime=Text("time:",x=Resolution[0]-40,y=Resolution[1]-80)
entropyText=Text("Entropy distributions",x=Resolution[0]-180,y=Resolution[1]-30)

textArray=[Text(text=" 4-molecule sim",x=Resolution[0]-70,y=-8),maviT,kırmızıT,yeşilT,morT,elapsedTime,entropyText]


lines=[line_(20,20,Resolution[0]-50,20),
       line_(20,20,20,Resolution[1]-50),
       line_(Resolution[0]-50,Resolution[1]-50,Resolution[0]-50,20),
       line_(Resolution[0]-50,Resolution[1]-50,20,Resolution[1]-50)]

yatay_araÇizgi=line_(20,(Resolution[1]-50)//2,(Resolution[0]-50),(Resolution[1]-50)//2,GREEN,5)
araÇizgi=line_((Resolution[0]-50)//2,20,(Resolution[0]-50)//2,(Resolution[1]-50),GREEN,5)

lines.append( araÇizgi )
lines.append(yatay_araÇizgi)

def run():
    threadList=[]
    done =False
    registerToFile=False
    tcounter=0 ##simulasyon süresi örn:60 saniyeye kadar çalışması için
    while not done:
        Clock.tick(FPS)

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                done=True

            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_SPACE:
                    print("space bastın")

            elif event.type==pygame.MOUSEBUTTONDOWN:
                x,y=pygame.mouse.get_pos()

                #button1
                if (set_mol_connection_BUTTON.rect.x<= x <= set_mol_connection_BUTTON.rect.width+set_mol_connection_BUTTON.rect.x
                        and
                set_mol_connection_BUTTON.rect.y <= y <=set_mol_connection_BUTTON.rect.y+set_mol_connection_BUTTON.rect.height):
                    #,set_mol_connection_BUTTON.rect.y)<=(x,y)<=(set_mol_connection_BUTTON.rect.x+set_mol_connection_BUTTON.rect.width,set_mol_connection_BUTTON.rect.y+set_mol_connection_BUTTON.rect.height):
                    set_mol_connection_BUTTON.change_trigger()
                    print("connect closer molecule variable changed to:",set_mol_connection_BUTTON.trigger)

                #button2
                elif (connectIfMoleculesGetsClose_BUTTON.rect.x <= x <=connectIfMoleculesGetsClose_BUTTON.rect.x+connectIfMoleculesGetsClose_BUTTON.rect.width
                        and
                connectIfMoleculesGetsClose_BUTTON.rect.y<= y <=connectIfMoleculesGetsClose_BUTTON.rect.y+connectIfMoleculesGetsClose_BUTTON.rect.height):
                    connectIfMoleculesGetsClose_BUTTON.change_trigger()
                    print("connect all molecule variable changed to:",connectIfMoleculesGetsClose_BUTTON.trigger)

                #button3
                elif (setTubeVolBUTTON.rect.x <= x <= setTubeVolBUTTON.rect.x+setTubeVolBUTTON.rect.width
                and
                setTubeVolBUTTON.rect.y <= y <= setTubeVolBUTTON.rect.y+setTubeVolBUTTON.rect.height):
                    setTubeVolBUTTON.change_trigger()
                    print(f"Remove the dividing line changed to {setTubeVolBUTTON.trigger}:")
                    if setTubeVolBUTTON.trigger==True:
                        lines.remove(araÇizgi)
                        lines.remove(yatay_araÇizgi)
                    else:
                        lines.append(araÇizgi)
                        lines.append(yatay_araÇizgi)

        Screen.fill( WHITE )
        objects_collides(l, connectIfMoleculesGetsClose_BUTTON.trigger, set_mol_connection_BUTTON.trigger,lines)

        #mass distribution-entropy calc
        mass_distribution_entropy(maviL,BLUE)
        mass_distribution_entropy(kırmızıL,RED)
        mass_distribution_entropy(yeşilL,GREEN)
        mass_distribution_entropy(morL,MAGENTA)

        [o.update() for o in lines]

        #for m in l:
        [m.move() for m in l]#update molecules

        maviT.update(text=str(calc_average_T(maviL)) )
        kırmızıT.update(text=str(calc_average_T(kırmızıL)) )
        yeşilT.update(text=str(calc_average_T(yeşilL)))
        morT.update(text=str(calc_average_T(morL)))
        elapsedTime.update(text=str(tcounter))

        [t.show() for t in textArray]

        [button.update() for button in buttons]#update buttons
        if registerToFile:
            if len(threadList)==0:
                threadList.append( Thread(target=register,args=(maviL, kırmızıL, done,tcounter,"/home/ibrahim","mavi-kırmızı.txt") ) )
                threadList.append( Thread(target=register,args=(yeşilL, morL, done,tcounter,"/home/ibrahim","yeşil-mor.txt",) ) )
                threadList[0].start()
                threadList[1].start()

            #register(maviL, kırmızıL, done, counter=tcounter)
            if not threadList[0].is_alive() and not threadList[1].is_alive():

                threadList=[]
                tcounter+=1

                if tcounter>60:
                    done=True


        pygame.display.flip()


if __name__=="__main__":
    run()
    exit(0)