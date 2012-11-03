# vertex.py

# This module contains all the things for creating
# and using vertices...starting with vector, and
# going on to edge and face.

# Observe two things, though:
#    First, I tried to keep small numbers as "zeros"
# by rounding divisions (see __div__ and norm) to
# five significant digits.  So if a number is one
# like 5.2e-6, it will be rounded to 0.
#    Second, to make sure that division works
# appropriately, I initialized the original vector
# with float(etc).
from math import sqrt

import pygame

ROUNDOFF = 5

class vector(object):
   def __init__(self, x, y, z):
      # Note that despite the w, these are
      # still 3D vectors.

      # Also note that I'd like to remove the w, but I cannot for now.
      self.x = float(x)
      self.y = float(y)
      self.z = float(z)
      # self.w = 1.0

   def __add__(self, v):
      x = self.x+v.x
      y = self.y+v.y
      z = self.z+v.z
      return vector(x, y, z)

   def __sub__(self, v):
      x = self.x-v.x
      y = self.y-v.y
      z = self.z-v.z
      return vector(x, y, z)

   def __mul__(self, s):
      x = round(self.x*s, ROUNDOFF)
      y = round(self.y*s, ROUNDOFF)
      z = round(self.z*s, ROUNDOFF)
      return vector(x, y, z)

   def __div__(self, s):
      x = round(self.x/s, ROUNDOFF)
      y = round(self.y/s, ROUNDOFF)
      z = round(self.z/s, ROUNDOFF)
      return vector(x, y, z)

   def __neg__(self):
      return vector(-self.x, -self.y, -self.z)

   def dot(self, v):
      return round(self.x*v.x + self.y*v.y + self.z*v.z, ROUNDOFF)

   def cross(self, v):
      x = round(self.y*v.z - self.z*v.y, ROUNDOFF)
      y = round(self.z*v.x - self.x*v.z, ROUNDOFF)
      z = round(self.x*v.y - self.y*v.x, ROUNDOFF)
      return vector(x, y, z)

   def dist(self):
      return round(sqrt(self.x*self.x + self.y*self.y + self.z*self.z), ROUNDOFF)
      # return sqrt(self.x*self.x + self.y*self.y + self.z*self.z)

   # For some reason, I can't get full rotations to work out
   # if I don't allow for the possibility that self.dist() might
   # be zero...
   #def norm(self):
   #   return self/self.dist()

   def norm(self):
      d = self.dist()
      if d == 0:
         return self
      else:
         return self/d

   def __str__(self):
      return "<%s, %s, %s>" % (self.x, self.y, self.z)

# Here are a few vector constants that are nice to
# define:  in particular, note that [Left, Up, Fwd]
# is a left-hand coord system, while [Right, Up, Fwd]
# represents a right-hand one.
Zero = vector(0, 0, 0)
Up = vector(0, 1, 0)
Left = vector(1, 0, 0)
Right = vector(-1, 0, 0)
Fwd = vector(0, 0, 1)

# I defined these functions separately from the
# classes because it seems more natural to say
# "x = dist(v)" rather than "x = v.dist()", etc.

def dist(v):
   return round(sqrt(v.x*v.x + v.y*v.y + v.z*v.z), ROUNDOFF)

def norm(v):
   return v/dist(v), 5

def orthonorm(x, y, z):
   """Returns a tuple of orthonormal vectors via the
      Gramm-Schmidt process.  See Apostal's Linear
      Algebra, pg. 111, or another LinAlg book for
      the theoretical background of this process."""
   q1 = x
   q2 = y - q1*(y.dot(q1)/q1.dot(q1))
   q3 = z - q1*(z.dot(q1)/q1.dot(q1)) - \
              q2*(z.dot(q2)/q2.dot(q2))

   return (q1.norm(), q2.norm(), q3.norm())

# Now that we have our vector defined, we could
# define the things that will make our vector a
# vertex.

class edge(object):
   def __init__(self, v1, v2, color='none'):
      """Initializes an edge for a wireframe.
      v1, v2 are vertex indices, and color is the
      default color with which to draw the edge.

      For purposes of comparison, each edge is stored
      with the first vertex index less than or equal
      to the second vertex index."""
      if v1 < v2:
         self.v1 = v1
         self.v2 = v2
      else:
         self.v1 = v2
         self.v2 = v1
      self.color = color

   def __eq__(self, e):
      """Returns true if both vertex indices are equal."""
      return (self.v1 == e.v1) and (self.v2 == e.v2)

   def __ne__(self, e):
      """Returns true if one one of the vertex indices
      is unequal."""
      return (self.v1 != e.v1) or (self.v2 != e.v2)

   def __str__(self):
      return "[ %s, %s ] %s" % (self.v1, self.v2, self.color)

class face(object):
   def __init__(self, vertices, edges, color='none'):
      """Initializes a face for a wireframe.

      In addition to vertices and color, this class also
      keeps track of edges, center, normal and norm*Vertex
      of the face.

      Note that the normal is calculated assuming that
      the vertices are in a clockwise order around the
      face when viewed from the outside of the wirefame."""

      # This is a list of indices for vertices.
      self.vertices = vertices
      self.color = color

      # This is a list of the indices of the edges.
      self.edges = edges
      
      # Note that, ideally, this class should have a
      # function that calculates its center and normal;
      # since only a wireframe class has this information,
      # however, only a wirframe class can calculate it!
      
   def __str__(self):
      return "%s  <%s>" % (self.vertices, self.color)

# These colors are included with vertices so that
# faces and edges can have colors.
#egacolors = { 'none':-1, 'black':0, 'blue':1,
   #'green':2, 'cyan':3, 'red':4, 'purple':5,
   #'brown':6, 'gray':7, 'brightblack':8,
   #'darkgray':8, 'brightblue':9, 'brightgreen':10,
   #'brightcyan':11, 'brightred':12, 'pink':12,
   #'brightpurple':13, 'brightbrown':14, 'yellow':14,
   #'brightgray': 15, 'white':15 }

# These colors are included with vertices so that
# faces and edges can have colors.

# Now that I'm using pygame, these need to be tweaked!
egacolor = { 'none': -1, 'black':  pygame.color.Color('black'),
   'blue': pygame.color.Color('blue'), 'green': pygame.color.Color('green'),
   'cyan': pygame.color.Color('cyan'), 'red': pygame.color.Color('red'),
   'purple': pygame.color.Color('purple'), 'brown': pygame.color.Color('brown'), 'gray': pygame.color.Color('gray'),
   'darkgray': pygame.color.Color('darkgray'), 'lightblue': pygame.color.Color('lightblue'),
   'lightgreen': pygame.color.Color('lightgreen'), 'lightcyan': pygame.color.Color('lightcyan'),
   'pink': pygame.color.Color('pink'),
   'lightpurple': pygame.color.Color('red'), 'yellow': pygame.color.Color('yellow'),
   'white': pygame.color.Color('white') }

bwcolor = {}
for i in range(0, 16):
   bwcolor['black%s' % (i)] = (i*16, i*16, i*16, 255)
