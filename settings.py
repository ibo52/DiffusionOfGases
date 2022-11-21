import pygame.display

BLACK=(0,0,0)
WHITE=(255,255,255)
RED=(255,0,0)
BLUE=(0,0,255)
GREEN=(0,255,0)
MAGENTA=(255,0,255)
YELLOW=(255,255,0)
FPS=60
Clock=pygame.time.Clock()
pygame.display.init()
""""
inf=pygame.display.Info() #monitor infromation
print(inf)
autoResolution=inf.current_w,inf.current_h
del inf"""

Resolution=(1140,700)
ResolutionFHD=(1920,1080)
"""i=input("do you want system to set resolution automaticly(type y if yes):\t")
i='n'
if i=='y':
    Resolution=autoResolution"""

Screen=pygame.display.set_mode(Resolution,pygame.RESIZABLE)
pygame.display.set_caption("Diffusion of Gases")

iconPath="/usr/share/icons/desktop-base/256x256/emblems/emblem-debian.png"
#pygame.display.set_icon( pygame.image.load(iconPath) )
