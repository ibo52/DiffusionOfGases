import pygame

from settings import *
from Objects import *
from time import sleep

numOfMolecules=20*2*2

maviL=generateMolecules_at_special_point(numOfMolecules,40,(Resolution[0]-90)//2,40,(Resolution[1]-90),mcolor=BLUE,rad=4,temp=100)
kırmızıL=generateMolecules_at_special_point(numOfMolecules,(Resolution[0]-90)//2,Resolution[0]-90,40,Resolution[1]-90,rad=8)
l=maviL+kırmızıL

maviT=Text(text="blue average T:",x=20,y=-8)
kırmızıT=Text(text="red average T:",x=(Resolution[0]//2)+100,y=-8)
elapsedTime=Text("time:",x=Resolution[0]-40,y=Resolution[1]-80)
entropyText=Text("Entropy distributions",x=Resolution[0]-180,y=Resolution[1]-30)

textArray=[Text(text="test",x=Resolution[0]-125,y=20),maviT,kırmızıT,elapsedTime,entropyText]


lines=[line_(20,20,Resolution[0]-50,20),
       line_(20,20,20,Resolution[1]-50),
       line_(Resolution[0]-50,Resolution[1]-50,Resolution[0]-50,20),
       line_(Resolution[0]-50,Resolution[1]-50,20,Resolution[1]-50)]

#yatay araÇizgi=line_(20,(Resolution[1]-50)//2,(Resolution[0]-50),(Resolution[1]-50)//2,GREEN,5)
araÇizgi=line_((Resolution[0]-50)//2,20,(Resolution[0]-50)//2,(Resolution[1]-50),GREEN,5)

lines.append( araÇizgi )

def run():
    threadList=[]
    done =False
    tcounter=0 ##simulasyon süresi örn:60 saniyeye kadar çalışması için
    registerToFile=False #dump results over (artifiacal)time
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
                    else:
                        lines.append(araÇizgi)

        Screen.fill( WHITE )
        objects_collides(l, connectIfMoleculesGetsClose_BUTTON.trigger, set_mol_connection_BUTTON.trigger,lines)

        #mass distribution-entropy calc
        mass_distribution_entropy(maviL,BLUE)
        mass_distribution_entropy(kırmızıL,RED)

        [o.update() for o in lines]

        #for m in l:
        [m.move() for m in l]#update molecules

        maviT.update(text=str(calc_average_T(maviL)) )
        kırmızıT.update(text=str(calc_average_T(kırmızıL)) )
        elapsedTime.update(text=str(tcounter))
        [t.show() for t in textArray]

        [button.update() for button in buttons]#update buttons
        if registerToFile:
            if len(threadList)==0:
                threadList.append( Thread(target=register,args=(maviL, kırmızıL, done,tcounter,) ) )
                threadList[0].start()

            #register(maviL, kırmızıL, done, counter=tcounter)
            if not threadList[0].is_alive():

                threadList=[]
                tcounter+=1

                if tcounter>60:
                    done=True


        pygame.display.flip()


if __name__=="__main__":
    run()
    exit(0)