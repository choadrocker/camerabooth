#!/usr/bin/env python

import pygame

pygame.init()
screen = pygame.display.set_mode((800,480),pygame.FULLSCREEN)
background = pygame.Surface(screen.get_size())
background = background.convert()

# colors
black = (0,0,0)
red = (200,0,0)

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

updateDisplay("hello!")
