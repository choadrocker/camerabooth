#!/usr/bin/env python

import os
#import datetime as dt
#from pygame.locals import *
#from signal import pause
import pygame
import time
#from subprocess import Popen

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

# standard text sizes
tiny_text = 20
small_text = 30
standard_text = 60
large_text = 90

def startRecording():
  """Touch a start recording hook for picam"""
  print("start recording")
  screen.fill(red)
  pygame.display.update()
  open('%s/hooks/start_record' % picam_home, 'w').close()

def stopRecording():
  """Touch a stop recording hook for picam"""
  print("stop recording")
  screen.fill(black)
  pygame.display.update()
  open('%s/hooks/stop_record' % picam_home, 'w').close()

def countDown(message, timer=30, color=red, bg=black):
  """Flash a count down message and timer to the display"""
  for tick in range(0, timer):
    nmessage = "%s: %i" % (message, (timer - tick))
    updateDisplay(nmessage, standard_text, color, bg)
    time.sleep(.6)
    updateDisplay("")
    time.sleep(.4)

def updateDisplay(message, size=standard_text, color=red, bg=black):
  """Update the display optionally with a message"""
  background.fill(bg)
  font = pygame.font.Font(None, size)
  text = font.render(message, 1, color)
  textpos = text.get_rect()
  textpos.centerx = background.get_rect().centerx
  textpos.centery = background.get_rect().centery
  background.blit(text, textpos)
  screen.blit(background, (0,0))
  pygame.display.update()

def flashDisplay(message, flashes=5, size=standard_text, color=red, bg=red):
  """Flash a message to the display"""
  for flash in range(0, flashes):
    updateDisplay(message, size, color, bg)
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

  smallText = pygame.font.Font(None, tiny_text)
  textSurf, textRect = text_objects(msg, smallText)
  textRect.center = ( (x+(w/2)), (y+(h/2)) )
  screen.blit(textSurf, textRect)

def game_loop():
  updateDisplay("Get ready to record!", standard_text, red)
  time.sleep(2)
  updateDisplay("You have 30 seconds", standard_text, red)
  countDown("Recording in", 3, red, black)
  startRecording()
  countDown("Recording", 30, black, red)
  stopRecording()
  updateDisplay("Thank you", large_text)
  time.sleep(10)
  updateDisplay("#fuckyourburn", tiny_text)
  time.sleep(.5)


def quitgame():
  pygame.quit()

def text_objects(text, font):
  textSurface = font.render(text, True, black)
  return textSurface, textSurface.get_rect()

def game_intro():
  intro = True
  updateDisplay("Touch screen to begin", standard_text)
  while intro:
    for event in pygame.event.get():
      print(event)
      if event.type == pygame.QUIT:
        pygame.quit()
        quit()

      updateDisplay("Ready to tell your story?", standard_text)
      button("GO!",150,400,100,50,green,bright_green,game_loop)
      button("Quit",550,400,100,50,red,bright_red,quitgame)

      pygame.display.update()
      clock.tick(60)


flashDisplay("Loading...", 3, standard_text, red, black)
game_intro()
game_loop()
pygame.quit()
quit()
