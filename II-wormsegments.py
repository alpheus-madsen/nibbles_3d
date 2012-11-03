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
from vertex import egacolor
from math import sqrt
from worm import *

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
camera = math3d.camera(width-xoffset, height-yoffset,
                   pos=math3d.vector(-500, 0, 0))

# We will be rotating eight different cubes.  The
# following vectors will be used to position each
# cube.

# All of the following is used by the "residue"
# from my initial program
vec = math3d.vector
positions = [ vec(50, 50, 50), vec(-50, 50, 50),
              vec(-50, -50, 50), vec(50, -50, 50),
              vec(50, 50, -50), vec(-50, 50, -50),
              vec(-50, -50, -50), vec(50, -50, -50) ]
cube = []

cube.append(math3d.wireframe('worm_middle_segment.dat',
             pos = vec(0, 0, 0), axis = vec(1, 0, 0)))
#cube.append(math3d.wireframe('worm_head_tail.dat',
#            pos = vec(0, 0, 100), axis = vec(1, 0, 0)))
#cube.append(math3d.wireframe('worm_middle_segment.dat',
#            pos = vec(0, 0, -100), axis = vec(1, 0, 0)))
#cube.append(math3d.wireframe('worm_elbow.dat',
#            pos = vec(0, 0, -200), axis = vec(1, 0, 0), beta=64))
#cube.append(math3d.wireframe('worm_middle_segment.dat',
#            pos = vec(0, -100, -200), axis = vec(1, 0, 0), beta=64))
#cube.append(math3d.wireframe('worm_elbow.dat',
#            pos = vec(0, -200, -200), axis = vec(0, 0, 1), beta=128))
#cube.append(math3d.wireframe('worm_head_tail.dat',
#            pos = vec(0, 0, -100), axis = vec(1, 0, 0), beta=128))
#cube.append(math3d.wireframe('worm_ball_type_I.dat',
#            pos = vec(0, 0, 200), axis = vec(1, 0, 0)))

# For visual reference, we will also draw a
# coordinate axis.
coords = math3d.wireframe('coords.dat')

camera.film.fill(bgcolor)

## This is where I will be experimenting with movement...
nextscreen = 0
pygame.mouse.set_visible(False)
center_x = width/2; center_y = height/2
inner_r = 50*50; outer_r = 100*100
m_0 = (float(height)/width); m_1 =-(float(height)/width)

clockwise_image = \
         pygame.image.load('../images/arrow_rotate_clockwise.png')
counter_clockwise_image = \
         pygame.image.load('../images/arrow_rotate_anticlockwise.png')
fwd_image = pygame.image.load('../images/add.png')
back_image = pygame.image.load('../images/money_yen.png')

up_image = pygame.image.load('../images/arrow_up.png')
left_image = pygame.image.load('../images/arrow_left.png')
right_image = pygame.image.load('../images/arrow_right.png')
down_image = pygame.image.load('../images/arrow_down.png')

cursor_image = up_image

dest_offset = up_image.get_size()
dest_offset = (dest_offset[0]/2, dest_offset[1]/2)
#m_offset = (0, 0)
show_cursor = False

hyp = sqrt(height*height + width*width)
line_y = 100 * height / hyp
line_x = 100 * width / hyp

def direction(pos):
   m_x = pos[0]
   m_y = pos[1]
   cir_x = pos[0] - center_x
   cir_y = pos[1] - center_y
   line_0 = m_0*m_x
   line_1 = m_1*m_x + height
   circle = cir_x * cir_x + cir_y * cir_y
   
   m_offset = (m_x - dest_offset[0], m_y - dest_offset[1])
   # print m_offset
   
   if m_x < offset[0] + dest_offset[0] \
         or m_x > width - offset[0] - dest_offset[0] \
         or m_y < offset[1] + dest_offset[1] \
         or m_y > height - offset[1] - dest_offset[1]:
      return BORDER, m_offset
   else:
      if circle < inner_r:
         if m_y < center_y:
            return FORWARD, m_offset
         else:
            return BACKWARD, m_offset
      elif circle < outer_r:
         if m_y > center_y:
            return CLOCKWISE, m_offset
         else:
            return COUNTERCLOCKWISE, m_offset
      elif m_y < line_0 and m_y < line_1:
         return UP, m_offset
      elif m_y > line_0 and m_y < line_1:
         return LEFT, m_offset
      elif m_y > line_0 and m_y > line_1:
         return DOWN, m_offset
      elif m_y < line_0 and m_y > line_1:
         return RIGHT, m_offset

def cursor(direction):
   if direction == CLOCKWISE:
      return clockwise_image
   elif direction == COUNTERCLOCKWISE:
      return counter_clockwise_image
   elif direction == FORWARD:
      return fwd_image
   elif direction == BACKWARD:
      return back_image
   elif direction == UP:
      return up_image
   elif direction == LEFT:
      return left_image
   elif direction == DOWN:
      return down_image
   elif direction == RIGHT:
      return right_image
   
def drawScene():
   my_worm.camera.film.fill(bgcolor)
   # my_worm.camera.draw_wf(coords)
   
   my_worm.drawWorm()
   my_worm.camera.drawOnto(screen, offset)
   
   # This is debug info; it prints the positions of noseCam and flyCam
   nosePos = 'noseCamera:  ' + str(my_worm.noseCamera.beta)  \
            + ' ~ ' + str(my_worm.noseCamera.axis)
   noseTxt = font.render(nosePos, 
            False, egacolor['white'], egacolor['black'])
   screen.blit(noseTxt, (10, 10))
   nosePos = str(my_worm.noseCamera.pos)
   noseTxt = font.render(nosePos, False, 
            egacolor['white'], egacolor['black'])
   screen.blit(noseTxt, (10, 30))
   nosePos = str(my_worm.noseCamera.beta_f) \
            + ' ~ ' + str(my_worm.noseCamera.axis_f)
   noseTxt = font.render(nosePos, False,
            egacolor['white'], egacolor['black'])
   screen.blit(noseTxt, (10, 50))
   
   flyPos = 'flyCamera:  ' + str(my_worm.flyCamera.beta) \
            + ' ~ ' + str(my_worm.flyCamera.axis)
   flyTxt = font.render(flyPos, False, 
            egacolor['white'], egacolor['black'])
   screen.blit(flyTxt, (10, 70))
   flyPos = str(my_worm.flyCamera.pos)
   flyTxt = font.render(flyPos, False, 
            egacolor['white'], egacolor['black'])
   screen.blit(flyTxt, (10, 90))
   flyPos = str(my_worm.flyCamera.beta_f) \
            + ' ~ ' + str(my_worm.flyCamera.axis_f)
   flyTxt = font.render(flyPos, False, 
            egacolor['white'], egacolor['black'])
   screen.blit(flyTxt, (10, 110))
   
   if show_cursor:
      screen.blit(cursor_image, m_offset)
   
   # I *think* this shows the "cursor crosshairs".
   pygame.draw.circle(screen, egacolor['black'], 
            (center_x, center_y), 50, 1)
   pygame.draw.circle(screen, egacolor['black'], 
            (center_x, center_y), 100, 1)
   pygame.draw.line(screen, egacolor['black'], 
            (center_x-100, center_y), (center_x-50, center_y), 1)
   pygame.draw.line(screen, egacolor['black'], 
            (center_x+50, center_y), (center_x+100, center_y), 1)
   
   pygame.draw.line(screen, egacolor['black'], offset, 
            (center_x-line_x, center_y-line_y), 1)
   pygame.draw.line(screen, egacolor['black'], 
            (center_x+line_x, center_y+line_y), 
            (width-offset[0], height-offset[1]), 1)
   pygame.draw.line(screen, egacolor['black'], 
            (offset[0], height-offset[1]),
            (center_x-line_x, center_y+line_y), 1)
   pygame.draw.line(screen, egacolor['black'], 
            (center_x+line_x, center_y-line_y), 
            (width-offset[0], offset[1]), 1)

   pygame.display.flip()

font = pygame.font.Font(None, 24)
my_worm = worm(sx=width-xoffset, sy=height-yoffset)
useFlyCamera = False
while 1:
   #camera.setrot(i, math3d.Up)

   #for v in cube:
      #camera.draw_wf(v)
      #v.drawOnto(camera)
      # v.setangle(i)

   #i = (i+1)%256
   #for event in pygame.event.get():
   events = pygame.event.get()
   for event in events:
      if event.type == pygame.QUIT:
         sys.exit()
      elif event.type == pygame.KEYDOWN:
         # print event
         print event
         if event.unicode == 'f' or event.unicode == 'F':
            print 'Toggle useFlyCamera!!!'
            if useFlyCamera:
               useFlyCamera = False
            else:
               useFlyCamera = True
            my_worm.cycleCamera()
         elif event.unicode == 'n' or event.unicode == 'N':
            nextscreen = 1
         elif event.unicode == 'p' or event.unicode == 'P':
            my_worm.pop()
      elif event.type == pygame.MOUSEMOTION:
         # print event.dict
         # print event.pos, event.buttons
         mouse_dir, m_offset = direction(event.pos)
         if mouse_dir == BORDER:
            show_cursor = False
         else:
            show_cursor = True
            cursor_image = cursor(mouse_dir)
            # print event.pos, event.button
      #elif event.type == pygame.MOUSEBUTTONDOWN:
         # print event.dict
      elif  event.type == pygame.MOUSEBUTTONDOWN:
         if useFlyCamera:
            print "hello!"
            # i = 0
            button_down = True
            while button_down:
               # print i,
               # i = (i+1)%256
               next_direction, m_offset = direction(event.pos)
               my_worm.move_flyCamera(next_direction, event.button)
               for up_event in pygame.event.get():
                  if up_event.type == pygame.MOUSEBUTTONUP:
                     button_down = False
               drawScene()
         else:
            next_direction, m_offset = direction(event.pos)
            my_worm.add_segment(next_direction)
            # print event.pos, event.button
   drawScene()
   
   if nextscreen == 1:
      break

pygame.mouse.set_visible(True)

#################################
# The following is residue from my previous program
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
      # camera.draw_wf(v)
      v.drawOnto(camera)
      # v.setangle(i)

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
      # v.setangle(i)

   i = (i+1)%256
   camera.drawOnto(screen, offset)
   pygame.display.flip()

## Rotate camera around a diagonal axis
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
      # v.setangle(i)

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
      # v.setangle(i)

   i = (i+1)%256
   camera.drawOnto(screen, offset)
   pygame.display.flip()

## Let the cubes "ride off" in the distance
i = 0
nextscreen = 0
keystrokes = 0
while 1:
   for event in pygame.event.get():
      if event.type == pygame.QUIT:
         sys.exit()
      elif event.type == pygame.KEYDOWN:
         nextscreen += 1
         keystrokes += 1
   if keystrokes == 10:
      break
  # if nextscreen == 1:
   #   break

   camera.film.fill(bgcolor)
   camera.draw_wf(coords)
   camera.settrans(math3d.vector(0, 0, -i*i))

   for v in cube:
      camera.draw_wf(v)
      # v.setangle(i)

   if nextscreen:
      i = i-1
      if i == 0:
         nextscreen = 0
   else:
      i = i+1
      if i == 100:
         nextscreen = 1
   nextscreen = nextscreen % 2
   camera.drawOnto(screen, offset)
   pygame.display.flip()


# Finally, we freeze things into position.
camera.drawOnto(screen, offset)
pygame.display.flip()

# Here we wait until the user presses a key, or turns off the system.
#nextscreen = 0
#while 1:
   #for event in pygame.event.get():
      #if event.type == pygame.QUIT:
         #sys.exit()
      #elif event.type == pygame.KEYDOWN:
         #nextscreen = 1
   #if nextscreen == 1:
      #break
