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

recording_length = 3

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
    time.sleep(1)
    #updateDisplay("")
    #time.sleep(.4)

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

def record():
  """Record the recording"""
  updateDisplay("Get ready to record!", standard_text, red)
  time.sleep(2)
  updateDisplay("You have 30 seconds", standard_text, red)
  time.sleep(2)
  countDown("Recording in", 3, red, black)
  startRecording()
  countDown("Recording", recording_length, black, red)
  stopRecording()
  updateDisplay("Thank you", large_text)
  time.sleep(10)
  updateDisplay("#fuckyourburn", tiny_text)
  time.sleep(.5)
  updateDisplay("Touch the screen to tell your story", standard_text)


def main_loop():
  """Main Loop"""
  updateDisplay("Touch the screen to tell your story", standard_text)
  while True:
    clock.tick(15)
    for event in pygame.event.get():
      if event.type == pygame.MOUSEBUTTONDOWN:
        print(event)
        record()

#flashDisplay("Loading...", 3, standard_text, red, black)
#game_intro()
#game_loop()
main_loop()
#pygame.quit()
#quit()
