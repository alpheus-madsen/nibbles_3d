# camera.py  -- This is the culmination of all that
# I've been working on for the last couple of days:
# the two different camera systems! Naturally, it
# depends on several libraries:
from vertex import *
from matrix import *

from movable import *
from wf import *

import sys
import pygame

# This definition will likely call for massive
# simplification.  For example, I doubt that it's
# necessary to specify coords, since they'll be
# changed by changing the position anyway.

# The only possible exception would be
# "coords[3] == eye", although "position[3] == pos"
# alters the position of eye...

Sx = 320; Sy = 400
Near = 500; Far = 10000; Fov = 45*(256/360)
# That is, beta is 45 degrees.

projmx = { 'standard':getproj, 'fov':getfovproj }

# note that type can be specified at the very end...
# default is 'standard'.
class camera(movable):
   def __init__(self, sx=Sx, sy=Sy, near=Near, farfov=Far,
                  beta=0, axis=Up, pos=Zero, beta_f=0, axis_f = Up, camtype='standard',
                  fwd=Fwd, left=Left, up=Up, eye = vector(0, 0, -Near)):
      """This creates self.world."""

      # Position needs to be negative, because the
      # only things it affects are "-coords.dot(eye)",
      # where coords are the three coordinate
      # vectors of the camera.

      # Since eye is the thing that gets translated,
      # we need "-coords.dot(eye+pos) ==
      # coords.dot(-eye-pos)".
      movable.__init__(self, beta, axis, pos, beta_f, axis_f, fwd, left, up)
      self.Eye = eye

      self.Sx = sx; self.Sy = sy
      self.near = near; self.farfov = farfov

      self.top = top = sy/2;
      self.bottom = bottom = -self.top

      self.right = right = sx/2
      self.left = left = -self.right


      # Until further notice, neither the projection
      # nor the film matrices will be changing! and
      # the coordinate matrix will never change...

      # Note:  fovproj uses a right-hand coordinate
      # system.  (This would probably be easy to
      # change, though...by changing the last row
      # of fovproj from [0,0,1,0] to [0,0,-1,0])
      self.proj = projmx[camtype](left, right, top,
                          bottom, near, farfov)
      self.cam = getcam(self.Fwd, self.Left, self.Up, self.Eye)
      self.film = pygame.Surface((sx, sy))

      # Please remember at all times that
      #    self.proj = getproj()*getcam()
      # ...unless proj changes, there is no reason
      # to keep these separate.

      # Also note that self.world correctly positions
      # the coordinate/eye system.
      self.camera_mx = self.proj*self.world*self.cam

   # We will have to call this ourselves if we change
   # the projection matrix without changing the
   # position of the camera...
   def reorient(self):
      #self.proj = projmx[camtype](left, right, top,
                          #bottom, near, farfov)* \
           #getcam(left, up, fwd, eye)
      self.camera_mx = self.proj*self.world

   def setworld(self):
      movable.setworld(self)
      self.camera_mx = self.proj*self.world*self.cam

  # We need to overload the following functions:
   def setangle(self, beta):
      movable.setangle(self, beta)
      self.reorient()
   def setaxis(self, axis):
      movable.setaxis(self, axis)
      self.reorient()
   def setrot(self, beta, axis):
      movable.setrot(self, beta, axis)
      self.reorient()
   # Just a brief reminder:  -pos needs to be
   # negative to translate "eye" correctly.
   def settrans(self, pos):
      movable.settrans(self, -pos)
      self.reorient()

   def setmove(self, beta, axis, pos):
      movable.setmove(self, beta, axis, pos)
      self.reorient()

   # We might also want to add another method or two
   # to alter the matrices:
   #    def setproj() and variants
   #    def seteye()

   # This has been moved to wireframe as
   # drawOnto(self, camera).  It is left here for backwards
   # compatibility.
   def draw_wf(self, wf):
      # This line should be
      #    "viewport = proj*camera*wf.world"
      # but for now this isn't a part of wireframe.
      viewport = self.camera_mx*wf.world

      vtcs = []
      for i in wf.vertices:
         vtx = viewport.proj(i)
         # For non-homogeneous vertices:
         #    vtcs.append([319*(vtx.x/vtx.e-1)/2,
         #               399*(vtx.y/vtx.e-1)/2])
         vtcs.append([vtx.x, vtx.y])
         # For non-homogeneous vertices:
         #   vtcs.append([vtx.x/vtx.e, vtx.y/vtx.e])

      # Now let's draw the lines!
      for i in wf.edges:
         pygame.draw.line(self.film, egacolor[i.color], (vtcs[i.v1][0], vtcs[i.v1][1]), (vtcs[i.v2][0], vtcs[i.v2][1]))

   def drawOnto(self, screen, offset=(0,0)):
      return screen.blit(self.film, offset)
