#!/usr/bin/python2.5
# In this Python program, I test my "camera" by
# drawing a coordinate axis and several rotating
# cubes.

# As much as I wanted to use PyAllegro, I had to move
# to PyGame instead; alpy just needs too much work, is
# too unstable, and is too slow in making progress.

import sys
import pygame

# This module imports all the little modules I will
# need for this program.
import math3d

# First, we need to initialize the graphics system.
pygame.init()

# size = width, height = 320, 400
size = width, height = 625, 400
xoffset = 50
yoffset = 50
offset = xoffset/2, yoffset/2
screen = pygame.display.set_mode(size)

black = 0, 0, 0
white = 255, 255, 255
bgcolor = white

# We can now create a camera object.  This will be
# what we use to draw things to the screen.
camera = math3d.camera(width-xoffset, height-yoffset)

# We will be rotating eight different cubes.  The
# following vectors will be used to position each
# cube.
vec = math3d.vector
positions = [ vec(50, 50, 50), vec(-50, 50, 50),
              vec(-50, -50, 50), vec(50, -50, 50),
              vec(50, 50, -50), vec(-50, 50, -50),
              vec(-50, -50, -50), vec(50, -50, -50) ]
cube = []
for i in range(8):
   cube.append(math3d.wireframe('littlecube.dat',
       pos = positions[i], axis=positions[(i+1)%8]))

# For visual reference, we will also draw a
# coordinate axis.
coords = math3d.wireframe('coords.dat')

camera.film.fill(bgcolor)

# Rotate cubes around Fwd axis
i = 0
nextscreen = 0
while 1:
   for event in pygame.event.get():
      if event.type == pygame.QUIT:
         sys.exit()
      elif event.type == pygame.KEYDOWN:
         nextscreen = 1
   if nextscreen == 1:
      break

   camera.film.fill(bgcolor)
   camera.draw_wf(coords)
   camera.setrot(i, math3d.Fwd)

   for v in cube:
      camera.draw_wf(v)
      v.setangle(i)

   i = (i+1)%256
   camera.drawOnto(screen, offset)
   pygame.display.flip()

## Rotate cubes around Left axis
nextscreen = 0
while 1:
   for event in pygame.event.get():
      if event.type == pygame.QUIT:
         sys.exit()
      elif event.type == pygame.KEYDOWN:
         nextscreen = 1
   if nextscreen == 1:
      break

   camera.film.fill(bgcolor)
   camera.draw_wf(coords)
   camera.setrot(i, math3d.Left)

   for v in cube:
      camera.draw_wf(v)
      v.setangle(i)

   i = (i+1)%256
   camera.drawOnto(screen, offset)
   pygame.display.flip()

## Rotate boxes around Up axis
nextscreen = 0
while 1:
   for event in pygame.event.get():
      if event.type == pygame.QUIT:
         sys.exit()
      elif event.type == pygame.KEYDOWN:
         nextscreen = 1
   if nextscreen == 1:
      break

   camera.film.fill(bgcolor)
   camera.draw_wf(coords)
   camera.setrot(i, math3d.Up)

   for v in cube:
      camera.draw_wf(v)
      v.setangle(i)

   i = (i+1)%256
   camera.drawOnto(screen, offset)
   pygame.display.flip()

## Rotate boxes around a diagonal axis
## (subject to change)
nextscreen = 0
while 1:
   for event in pygame.event.get():
      if event.type == pygame.QUIT:
         sys.exit()
      elif event.type == pygame.KEYDOWN:
         nextscreen = 1
   if nextscreen == 1:
      break

   camera.film.fill(bgcolor)
   camera.draw_wf(coords)
   camera.setrot(i, math3d.vector(5,5,2))

   for v in cube:
      camera.draw_wf(v)
      v.setangle(i)

   i = (i+1)%256
   camera.drawOnto(screen, offset)
   pygame.display.flip()

## Just rotate the cubes
nextscreen = 0
while 1:
   for event in pygame.event.get():
      if event.type == pygame.QUIT:
         sys.exit()
      elif event.type == pygame.KEYDOWN:
         nextscreen = 1
   if nextscreen == 1:
      break

   camera.film.fill(bgcolor)
   camera.draw_wf(coords)

   for v in cube:
      camera.draw_wf(v)
      v.setangle(i)

   i = (i+1)%256
   camera.drawOnto(screen, offset)
   pygame.display.flip()

## Let the cubes "ride off" in the distance
i = 0
nextscreen = 0
while 1:
   for event in pygame.event.get():
      if event.type == pygame.QUIT:
         sys.exit()
      elif event.type == pygame.KEYDOWN:
         nextscreen = 1
   if nextscreen == 1:
      break

   camera.film.fill(bgcolor)
   camera.draw_wf(coords)
   camera.settrans(math3d.vector(0, 0, -i*i))

   for v in cube:
      camera.draw_wf(v)
      v.setangle(i)

   i = i+1
   camera.drawOnto(screen, offset)
   pygame.display.flip()


# Finally, we freeze things into position.
camera.drawOnto(screen, offset)
pygame.display.flip()

# Here we wait until the user presses a key, or turns off the system.
nextscreen = 0
while 1:
   for event in pygame.event.get():
      if event.type == pygame.QUIT:
         sys.exit()
      elif event.type == pygame.KEYDOWN:
         nextscreen = 1
   if nextscreen == 1:
      break
