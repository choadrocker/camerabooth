#!/usr/bin/env python

import os
import datetime as dt
from pygame.locals import *
from signal import pause
import pygame
import time
from subprocess import Popen

# 1000% dependent on picam installed and running as a service
picam_home = '/home/pi/picam'

pygame.init()
#pygame.mouse.set_visible(False)
screen = pygame.display.set_mode((800,480),pygame.FULLSCREEN)
background = pygame.Surface(screen.get_size())
background = background.convert()
clock = pygame.time.Clock()

# colors
black = (0,0,0)
white = (255,255,255)
red = (200,0,0)
bright_red = (255,0,0)
green = (0,200,0)
bright_green = (0,255,0)

def startRecording():
  print("start recording")
  #pid = os.spawnl(os.P_NOWAIT, 'picam', '/home/pi/picam/picam', '--preview', '--alsadev',  'hw:1,0', '--opacity', '120', '--ex', 'auto')
  #pid = Popen(["/home/pi/picam/picam", "--preview", "--alsadev",  "hw:1,0", "--opacity", "120", "--ex", "auto"]).pid
  #os.mknod('%s/hooks/start_record' % picam_home, 0777)
  open('%s/hooks/start_record' % picam_home, 'w').close()
  #f = open('%s/hooks/start_record' % picam_home, 'w')
  #f.write("filename=%s.ts" % dt.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'))
  #f.close
  #os.remove('%s/hooks/start_record' % picam_home)
  #return(pid)

def stopRecording():
  print("stop recording")
  open('%s/hooks/stop_record' % picam_home, 'w').close()
  #os.remove('%s/hooks/stop_record' % picam_home)
  #os.mknod("%s/hooks/stop_record" % picam_home, 0777)
  #time.sleep(.2)
  #os.kill(pid,9)

def countDown(message, timer=30):
  for tick in range(0, timer):
    nmessage = "%s: %i" % (message, (timer - tick))
    updateDisplay(nmessage, 60)
    time.sleep(.6)
    updateDisplay("")
    time.sleep(.4)

# updateDisplay("foo", 300, "green")
def updateDisplay(message, size=180, color=red):
  background.fill(black)
  font = pygame.font.Font(None, size)
  text = font.render(message, 1, color)
  textpos = text.get_rect()
  textpos.centerx = background.get_rect().centerx
  textpos.centery = background.get_rect().centery
  background.blit(text, textpos)
  screen.blit(background, (0,0))
  pygame.display.flip()

# flashDisplay("You lose!", 3, 60, red)
def flashDisplay(message, flashes=5, size=180, color=red):
  for flash in range(0, flashes):
    updateDisplay(message, size, color)
    time.sleep(.6)
    updateDisplay("")
    time.sleep(.4)

def button(msg,x,y,w,h,ic,ac,action=None):
  mouse = pygame.mouse.get_pos()
  click = pygame.mouse.get_pressed()
  print(click)
  if x+w > mouse[0] > x and y+h > mouse[1] > y:
    pygame.draw.rect(screen, ac,(x,y,w,h))

    if click[0] == 1 and action != None:
      action()
  else:
    pygame.draw.rect(screen, ic,(x,y,w,h))

  smallText = pygame.font.Font(None, 20)
  textSurf, textRect = text_objects(msg, smallText)
  textRect.center = ( (x+(w/2)), (y+(h/2)) )
  screen.blit(textSurf, textRect)

def game_loop():
  # flashDisplay("You lose!", 3, 60, red)
  updateDisplay("Get ready to record!", 40, red)
  time.sleep(2)
  updateDisplay("You have 30 seconds", 40, red)
  #time.sleep(2)
  #pid = Popen(["%s/picam" % picam_home, "--preview", "--alsadev",  "hw:1,0", "--opacity", "120", "--ex", "auto", "-q"]).pid
  #time.sleep(.2)
  countDown("Recording in", 3)
  startRecording()
  countDown("Recording", 30)
  stopRecording()
  #time.sleep(.2)
  #os.kill(pid,15)
  updateDisplay("Thank you", 120)
  time.sleep(10)
  updateDisplay("#fuckyourburn", 20)
  time.sleep(.5)


def quitgame():
  pygame.quit()

def text_objects(text, font):
  textSurface = font.render(text, True, black)
  return textSurface, textSurface.get_rect()

def game_intro():
  intro = True
  updateDisplay("Touch screen to begin", 60)
  while intro:
    for event in pygame.event.get():
      print(event)
      if event.type == pygame.QUIT:
        pygame.quit()
        quit()

      updateDisplay("Ready to tell your story?", 60)
      button("GO!",150,400,100,50,green,bright_green,game_loop)
      button("Quit",550,400,100,50,red,bright_red,quitgame)

      pygame.display.update()
      clock.tick(15)


flashDisplay("Loading...", 3)
game_intro()
game_loop()
pygame.quit()
quit()
