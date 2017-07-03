
import os
import datetime as dt
from picamera import PiCamera
from pygame.locals import *
from signal import pause
import pygame
import time
#import alsaaudio
#import wave


destination = '/home/pi/Videos'
camera = PiCamera()
pygame.init()
#pygame.mouse.set_visible(False)
screen = pygame.display.set_mode((800,480),pygame.FULLSCREEN)
background = pygame.Surface(screen.get_size())
# <Surface(800x480x32 SW)>
background = background.convert()
clock = pygame.time.Clock()

# alsa card audio setup
#inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE)
#inp.setchannels(1)
#inp.setrate(44100)
#inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)
#inp.setperiodsize(1024)

# colors
black = (0,0,0)
white = (255,255,255)
red = (200,0,0)
bright_red = (255,0,0)
green = (0,200,0)
bright_green = (0,255,0)

def startRecording():
  filename = os.path.join(destination, dt.datetime.now().strftime('%Y-%m-%d_%H.%M.%S'))
  camera.preview_alpha = 120
  camera.start_preview()
  camera.start_recording('%s.h264' % filename)
  #w = wave.open('%s.wav' % filename, 'w')
  #w.setnchannels(1)
  #w.setsampwidth(2)
  #w.setframerate(44100)
  #l, data = inp.read()
  #print len(data)
  #print l
  #if l:
  #  w.writeframes(data)
  #  #time.sleep(.001)


def stopRecording():
  camera.stop_recording()
  #w = wave.close
  camera.stop_preview()

def countDown(message, timer=30):
  for tick in range(0, timer):
    nmessage = "%s: %i" % (message, (timer - tick))
    updateDisplay(nmessage, 60)
    time.sleep(.6)
    updateDisplay("")
    time.sleep(.4)
        
# updateDisplay("foo", 300, "green")
def updateDisplay(message, size=180, color=red):
  print(message)
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
  updateDisplay("Look into the camera and speak clearly", 40, red)
  time.sleep(2)
  updateDisplay("You have 30 seconds", 40, red)
  time.sleep(2)  
  countDown("Get ready", 3)
  startRecording()
  countDown("Recording", 30)
  stopRecording()
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
#startCamera()
game_intro()
game_loop()
pygame.quit()
quit()
