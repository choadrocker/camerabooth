#!/usr/bin/env python

import os
import pygame
from pygame.locals import *
import subprocess
import sys
import time

# 1000% dependent on picam installed and running as a service
PICAM_HOME = '/home/pi/picam'
RECORDING_LENGTH = 5
AFTER_PAUSE_LENGTH = 3

# colors
BLACK = (0,0,0)
RED = (200,0,0)

# standard text sizes
TINY_TEXT = 20
SMALL_TEXT = 30
STANDARD_TEXT = 60
LARGE_TEXT = 90

pygame.init()
pygame.mouse.set_visible(False)
screen = pygame.display.set_mode((800,480),pygame.FULLSCREEN)
background = pygame.Surface(screen.get_size())
background = background.convert()
clock = pygame.time.Clock()

def checkForPicam():
  """If picam isn't running, this is all wasted"""
  try:
    subprocess.check_output(["pgrep", "picam"])
  except:
    sys.exit("Picam isn't running?")

def startRecording():
  """Touch a start recording hook for picam"""
  print("start recording")
  open('%s/hooks/start_record' % PICAM_HOME, 'w').close()
  screen.fill(RED)
  pygame.display.update()

def stopRecording():
  """Touch a stop recording hook for picam"""
  print("stop recording")
  open('%s/hooks/stop_record' % PICAM_HOME, 'w').close()
  screen.fill(BLACK)
  pygame.display.update()

def countDown(message, timer=30, color=RED, bg=BLACK):
  """Show a count down message and timer to the display"""
  for tick in range(0, timer):
    nmessage = "%s: %i" % (message, (timer - tick))
    updateDisplay(nmessage, STANDARD_TEXT, color, bg)
    time.sleep(1)
    #updateDisplay("")
    #time.sleep(.4)

def updateDisplay(message, size=STANDARD_TEXT, color=RED, bg=BLACK):
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

def flashDisplay(message, flashes=5, size=STANDARD_TEXT, color=RED, bg=RED):
  """Flash a message to the display"""
  for flash in range(0, flashes):
    updateDisplay(message, size, color, bg)
    time.sleep(.6)
    updateDisplay("")
    time.sleep(.4)

def record():
  """Record the recording"""
  updateDisplay("Get ready to record!", STANDARD_TEXT, RED)
  time.sleep(2)
  updateDisplay("You have 30 seconds", STANDARD_TEXT, RED)
  time.sleep(2)
  countDown("Recording in", 3, RED, BLACK)
  startRecording()
  countDown("Recording", RECORDING_LENGTH, BLACK, RED)
  stopRecording()
  updateDisplay("Thank you", LARGE_TEXT)
  time.sleep(AFTER_PAUSE_LENGTH)
  updateDisplay("#fuckyourburn", TINY_TEXT)
  time.sleep(.5)
  updateDisplay("Touch the screen to tell your story", STANDARD_TEXT)

def main_loop():
  """Main Loop"""
  updateDisplay("Touch the screen to tell your story", STANDARD_TEXT)
  while True:
    clock.tick(15)
    for event in pygame.event.get():
      if event.type == pygame.MOUSEBUTTONDOWN:
        #print(event)
        record()

if __name__ == "__main__":
  checkForPicam()
  flashDisplay("Loading...", 3, STANDARD_TEXT, RED, BLACK)
  main_loop()
