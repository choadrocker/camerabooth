#!/usr/bin/env python

import pygame
from pygame.locals import *
import subprocess
import sys
import time

# 1000% dependent on picam installed and running as a service
PICAM_HOME = '/home/pi/picam'
# these are all in seconds
RECORDING_LENGTH = 30
AFTER_PAUSE_LENGTH = 2
PRE_RECORDING_COUNTDOWN_LENGTH = 3

# colors
BLACK = (0, 0, 0)
RED = (200, 0, 0)

# standard text sizes
TINY_TEXT = 20
SMALL_TEXT = 30
STANDARD_TEXT = 60
LARGE_TEXT = 90

pygame.init()
pygame.mouse.set_visible(False)
pygame.event.set_allowed(None)
# since this is running on a touch screen, we only care about mouse clicks
pygame.event.set_allowed(pygame.MOUSEBUTTONDOWN)
screen = pygame.display.set_mode((800, 480), pygame.FULLSCREEN)
background = pygame.Surface(screen.get_size())
background = background.convert()
clock = pygame.time.Clock()

def checkForPicam():
  """If picam isn't running, this is all wasted"""
  try:
    subprocess.check_output(["pgrep", "picam"])
  except:
    sys.exit("Picam isn't running?")

def isRecording():
  """The picam state file is our best resource for the current state"""
  f = open("%s/state/record" % PICAM_HOME, "r")
  state = f.readline()
  f.close()
  return state == "true"

def clearQueue(caller):
  """Pygame seems to queue up events and so to prevent many rapid
     loops, we clear it all by calling get and clear"""
  print("clearQueue called from %s: %i events cleared" % (caller, len(pygame.event.get())))
  pygame.event.clear()

def startRecording():
  """Touch a start recording hook for picam"""
  print("start recording")
  clearQueue("startRecording")

  updateDisplay("Get ready to record!", STANDARD_TEXT, RED)
  time.sleep(2)
  updateDisplay("You have %i seconds" % RECORDING_LENGTH, STANDARD_TEXT, RED)
  time.sleep(2)

  countDown("Recording in", STANDARD_TEXT, PRE_RECORDING_COUNTDOWN_LENGTH, RED, BLACK)

  open('%s/hooks/start_record' % PICAM_HOME, 'w').close()
  screen.fill(RED)

  countDown("Touch the screen to stop recording at any time", SMALL_TEXT, RECORDING_LENGTH, BLACK, RED)

  updateDisplay("Thank you", LARGE_TEXT)
  time.sleep(AFTER_PAUSE_LENGTH)
  updateDisplay("Touch the screen to tell your story", STANDARD_TEXT)
  pygame.display.update()

def stopRecording():
  """Touch a stop recording hook for picam"""
  print("stop recording")
  clearQueue("StopRecording")
  open('%s/hooks/stop_record' % PICAM_HOME, 'w').close()

def countDown(message=None, size=STANDARD_TEXT, timer=30, color=RED, bg=BLACK):
  """Show a count down message and timer to the display"""
  clearQueue("countDown")
  for tick in range(0, timer):
    nmessage = "%s: %i" % (message, (timer - tick))
    print(nmessage)
    updateDisplay(nmessage, size, color, bg)
    if isRecording() and pygame.event.peek(MOUSEBUTTONDOWN):
      print("recording was cancelled")
      return()
    time.sleep(1)

def updateDisplay(message=None, size=STANDARD_TEXT, color=RED, bg=BLACK):
  """Update the display optionally with a message"""
  background.fill(bg)
  font = pygame.font.Font(None, size)
  text = font.render(message, 1, color)
  textpos = text.get_rect()
  textpos.centerx = background.get_rect().centerx
  textpos.centery = background.get_rect().centery
  background.blit(text, textpos)
  screen.blit(background, (0, 0))
  pygame.display.update()

def flashDisplay(message=None, flashes=5, size=STANDARD_TEXT, color=RED, bg=RED):
  """Flash a message to the display"""
  for flash in range(0, flashes):
    print(message)
    updateDisplay(message, size, color, bg)
    time.sleep(.6)
    updateDisplay("")
    time.sleep(.4)

def main_loop():
  """Main Loop"""
  # this should never really happen but does during development where we quit
  # out and the recording continues
  if isRecording():
    print("Camera was already recording, stopping")
    stopRecording()
  updateDisplay("Touch the screen to tell your story", STANDARD_TEXT)
  while True:
    clock.tick(30)
    event = pygame.event.wait()
    clearQueue("main_loop")
    if isRecording():
      stopRecording()
    else:
      startRecording()

if __name__ == "__main__":
  checkForPicam()
  flashDisplay("Loading...", 3, STANDARD_TEXT, RED, BLACK)
  main_loop()
