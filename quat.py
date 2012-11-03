# quat.py

# This module defines an entirely new number:  the dual quaternion.
# Since a normal quaternion is just a dual quaternion with a zero
# idempotent part, I have chosen to define a single class---quat---and
# that will act as both quaternion and dual quaternion.

# Observe two things, though:
#    First, I tried to keep small numbers as "zeros"
# by rounding divisions (see __div__ and norm) to
# five significant digits.  So if a number is one
# like 5.2e-6, it will be rounded to 0.
#   To allow for experimentation, though, I decided to
# change the roundoff to ROUNDOFF, set in vertex.
#    Second, to make sure that division works
# appropriately, I initialized the original quaternion
# with float(etc).
from math import sqrt, acos
import exceptions
#from mm import multimethod

from vertex import *
from matrix import *


class DivideByPureDualException(exceptions.Exception):
   def __init__(self):
      return

   def __str__(self):
      print "","Attempt to find Inverse for Pure Dual Quaternion."

class DualDistanceException(exceptions.Exception):
   def __init__(self):
      return

   def __str__(self):
      print "","Attempt to find dist() for Pure Dual Quaternion."


class quat(object):
   #@multimethod(quat, float, vector, float, vector)
   def __init__(self, r=0, I=Zero, er=0, eI=Zero):
      # This initialization uses vectors rather than numbers.
      # This initializes to 0.
      self.r = float(r)
      self.I = I
      self.er = float(er)
      self.eI = eI

   #@multimethod(quat, float, float, float, float, float, 
   #        float, float, float)
   #def __init__(self, r, i, j, k, er, ei, ej, ek):
   def real_quat(self, r, i, j, k, er, ei, ej, ek):
      # This is an initialization using numbers.
      self.r = float(r)
      self.I = vector(i, j, k)
      # Alternate to using vector definitions:
      #self.i = float(i)
      #self.j = float(j)
      #self.k = float(k)

      self.er = float(er)
      self.eI = vector(ei, ej, ek)
      # Alternate to using vector definitions:
      #self.ei = float(ei)
      #self.ej = float(ej)
      #self.ek = float(ek)
      # Note that this will be the only function that shows this
      # alternative, unless I decide to switch to this alternative.

   #@multimethod(quat, int, vector)
   #def __init__(self, beta, r):
   def rotation(self, beta, r):
      # This initialization creates a unit quaternion.
      self.r = tcos(beta/2)
      self.I = r.norm()*tsin(beta/2)
      self.er = float(0)
      self.eI = Zero

   #@multimethod(quat, vector)
   #def __init__(self, t):
   def vector(self, t):
      # This initialization creates a unit dual quaternion.
      # As __init__, it is meant to be used for two purposes:
      #  to multiply vectors as dual quaternions;
      # and to initialize traslation dual quaternions.

      # For the latter purpose, it's important to remember to
      # divide the vector by two before initializing the
      # quaternion.
      self.r = float(1)
      self.I = Zero
      self.er = float(0)
      self.eI = t
      
   def pureVector(self, t):
      """This sets the quat to be a pure quaternion with a
      vector value of t; this is useful if all we want to do with
      a given vector is rotate it."""
      self.r = float(0)
      self.I = t
      self.er = float(0)
      self.eI = Zero
      
   def extractVector(self):
      """When we translate and/or rotate a vector, we are going
      to want to get the new vector information somehow.  This
      function returns the vector from a unit dual quaternion.
      
      Recall that a vector as a dual quaternion has the form
               1 + eI.dot(v) where I = (i, j, k) and e**2==0."""
      return self.eI

   def extractPureVector(self):
      """When we only rotate a vector, we are going
      to want to get the new vector information somehow.  This
      function returns the vector from a pure vector quaternion.
      
      Recall that a vector as a pure quaternion has the form
               I.dot(v) where I = (i, j, k)."""
      return self.I

   def translation(self, t):
      # This initialization creates a unit dual quaternion
      # for translations.
      self.r = float(1)
      self.I = Zero
      self.er = float(0)
      self.eI = t/2

   def purequat(self):
      # We'll check to see if each of these items are non-zero.
      # If any one of them is non-zero, then this is not a pure
      # quaternion.
      return not(self.er != 0 or self.eI.x != 0 or
               self.eI.y != 0 or self.eI.z != 0)

   def puredual(self):
      # We'll check to see if each of these items are non-zero
      # If any one of them is non-zero, then this is not a purely
      # dual quaternion.
      return not(self.r != 0 or self.I.x != 0 or
               self.I.y != 0 or self.I.z != 0)

   def puretrans(self):
      # This identifies a dual quaternion that is purely a translation.
      return (self.r == 1 and self.I.x == 0 and self.I.y == 0
               and self.I.z == 0 and self.er == 0)

   def __add__(self, v):
      r = self.r+v.r
      I = self.I+v.I
      er = self.er+v.er
      eI = self.eI+v.eI
      return quat(r, I, er, eI)

   def __sub__(self, v):
      r = self.r-v.r
      I = self.I-v.I
      er = self.er-v.er
      eI = self.eI-v.eI
      return quat(r, I, er, eI)

   def __neg__(self):
      return quat(-self.r, -self.I, -self.er, -self.eI)

   def __mul__(self, q):
      if isinstance(q, quat):
         # Do quaternion multiplication
         if self.purequat() and q.purequat():
            r = round(q.r*self.r - self.I.dot(q.I), ROUNDOFF)
            I = q.I*self.r + self.I*q.r + self.I.cross(q.I)
            return quat(r, I)
         else:
            r = round(self.r*q.r - self.I.dot(q.I), ROUNDOFF)
            I = q.I*self.r + self.I*q.r + self.I.cross(q.I)
            er = round((self.r*q.er - self.I.dot(q.eI)) + \
                        (self.er*q.r - self.eI.dot(q.I)), ROUNDOFF)
            eI = (q.eI*self.r + self.I*q.er+self.I.cross(q.eI) + \
                        q.I*self.er + self.eI*q.r + self.eI.cross(q.I))
            return quat(r, I, er, eI)
      else:
         # Do scalar multiplication
         r = round(self.r*q, ROUNDOFF)
         I = self.I*q
         er = round(self.er*q, ROUNDOFF)
         eI = self.eI*q
         return quat(r, I, er, eI)

   def conj(self):
      # Quaternionic conjugation
      return quat(self.r, -self.I, self.er, -self.eI)

   def pconj(self):
      # Pure Quaternionic conjugation
      return quat(self.r, -self.I)

   def econj(self):
      # Dual quaternionic conjugation
      return quat(self.r, self.I, -self.er, -self.eI)

   def bconj(self):
      # Quaternionic and Dual Quaternionic conjugation together
      return quat(self.r, -self.I, -self.er, self.eI)

   def dot(self, v):
      # I'm not sure if this makes sense for dual quaternions.
      return round(self.r*v.r + self.I.dot(v.I) + self.er*v.er \
             + self.eI.dot(v.eI), ROUNDOFF)

   def dist(self):
      if self.purequat():
         return round(sqrt(self.r*self.r + self.I.dot(self.I)), \
                   ROUNDOFF)
      else:
         r = round(sqrt(self.r*self.r + self.I.dot(self.I)), \
                   ROUNDOFF)
         if r == 0:
            raise DualDistanceException
         dot = float(self.I.dot(self.eI))
         if dot == 0:
            return round(r, ROUNDOFF)
         else:
            return quat(round(r, ROUNDOFF), Zero, \
                      round(dot/r, ROUNDOFF), Zero)

   def norm(self):
      d = self.dist()
      if self.purequat():
         return quat(self.r/d, self.I/d)
      else:
         return quat(self.r/d, self.I/d, self.er/d, self.eI/d)

   def inverse(self):
      if self.purequat():
         # Pure quaternion inverse:  this is rather easy!
         return self.pconj() / sqrt(self.r*self.r + self.I.dot(self.I))
      else:
         # Dual quaternionic inverse:  a little more challenging.
         if self.puredual():
            # If the non-idempotent part is 0, we can't find
            # the inverse.
            raise DivideByPureDualException
         else:
            # the inverse is 1/q_0 - e(q_e/((q_0)^2) --- yikes!
            r_sq = self.r*self.r
            I_dot = self.I.dot(self.I)

            t = 1.0/(r_sq + I_dot)

            new_r = r_sq - I_dot
            new_I = self.I*(1.0/(new_r*new_r + 4*r_sq*I_dot))

            er = -self.er*new_r - self.eI.dot(new_I)
            eI = -(new_I*self.er + self.eI*new_r + self.eI.cross(new_I))

            return quat(self.r*t, -self.I*t, round(er, ROUNDOFF), eI)

   def __div__(self, q):
      # Theoretically, I ought to repeat the above, simplified, to
      # streamline execution.
      # For now, I am NOT going to do that!
      if isinstance(q, quat):
         return (self*q.inverse())
      else:
         r = round(self.r/q, ROUNDOFF)
         I = self.I/q
         er = round(self.er/q, ROUNDOFF)
         eI = self.I/q
         return quat(r, I, er, eI)

   def normalize(self):
      self = self.norm()

   def matrix(self):
      # Here are a few calculations that will be used to
      # convert our dual quaternion to a matrix!

      # To speed things up, we'll recognize three types of
      # matrices.

      # Note that, theoretically, we should normalize the
      # dual quaternion first.

      if self.purequat():
         # This is the rotation quaternion...
         w = self.r        # = tcos(beta/2)
         x = self.I.x      # = tsin(beta/2)*axis.x
         y = self.I.y      # = tsin(beta/2)*axis.y
         z = self.I.z      # = tsin(beta/2)*axis.z

         # Now we'll pull out the translation information...
         xx2 = 2*x*x; yy2 = 2*y*y; zz2 = 2*z*z
         wx2 = 2*w*x; wy2 = 2*w*y; wz2 = 2*w*z
         xy2 = 2*x*y; xz2 = 2*x*z; yz2 = 2*y*z

         quat_mx = matrix()
         quat_mx.mx = [ [1-yy2-zz2, xy2+wz2, xz2-wy2, 0],
                  [xy2-wz2, 1-xx2-zz2, yz2+wx2, 0],
                  [xz2+wy2, yz2-wx2, 1-xx2-yy2, 0],
                  [0, 0, 0, 1] ]

         return quat_mx

      elif self.puretrans():
         # This is a purely translational dual quaternion.
         quat_mx = matrix()
         quat_mx.mx = [ [1, 0, 0, 2*self.eI.x],
                  [0, 1, 0, 2*self.eI.y],
                  [0, 0, 1, 2*self.eI.z],
                  [0, 0, 0, 1] ]

         return quat_mx

      else:
         # This is the rotation quaternion...
         w = self.r        # = tcos(beta/2)
         x = self.I.x      # = tsin(beta/2)*axis.x
         y = self.I.y      # = tsin(beta/2)*axis.y
         z = self.I.z      # = tsin(beta/2)*axis.z

         # Now we'll pull out the translation information...
         ew = self.er
         ex = self.eI.x
         ey = self.eI.y
         ez = self.eI.z

         t = 2*(-ew*x + ex*w - ey*z + ez*y)
         u = 2*(-ew*y + ex*z + ey*w - ez*x)
         v = 2*(-ew*z - ex*y + ey*x + ez*w)

         xx2 = 2*x*x; yy2 = 2*y*y; zz2 = 2*z*z
         wx2 = 2*w*x; wy2 = 2*w*y; wz2 = 2*w*z
         xy2 = 2*x*y; xz2 = 2*x*z; yz2 = 2*y*z

         quat_mx = matrix()
         quat_mx.mx = [ [1-yy2-zz2, xy2+wz2, xz2-wy2, t],
                  [xy2-wz2, 1-xx2-zz2, yz2+wx2, u],
                  [xz2+wy2, yz2-wx2, 1-xx2-yy2, v],
                  [0, 0, 0, 1] ]

         return quat_mx

   def __str__(self):
      return " %s + I %s + e(%s + I %s)" % (self.r, self.I, \
                self.er, self.eI)

   def get_angle_axis(self):
      # This returns (beta, axis) from a quaternion.  Note that
      # this assumes that the quaternion is pure; this function
      # should probably throw an exception if it isn't pure.

      # Note that we convert from radians to bradians.
      beta = int(round(2*acos(self.r)*128/pi))
      if beta == 0:
         # In this case, we have an "identity" rotation;
         # thus, we could use any vector we would like.
         # Here, we'll default to the Up vector.
         v = Up
      else:
         sin = tsin(beta/2)
         if sin == 0:
            # If beta is 1 or -1, then it will be a valid rotation;
            # in this case, we'll approximate the sine.
            sin = tsin(beta)
         x = self.I.x/sin
         y = self.I.y/sin
         z = self.I.z/sin

         v = vector(x, y, z)
         v = v.norm()

      return (beta, v)

   def get_translation(self):
      """This returns the translation vector from a translation
      quaternion. It assumes that the dual quaternion is purely
      translation.  If it isn't, I should probably throw an 
      exception."""
      return vector(2*self.eI.x, 2*self.eI.y, 2*self.eI.z)
   
   def get_angle_axis_translation(self):
      """ This returns the angle-axis and tranlation information
      from a dual quaternion; this does NOT assume that this is
      purely a translation or a quaternion.
      
      Every dual quaternion represents a combination of rotation
      and translation; in thinking about the relationships of
      these two, I have been able to come up with this."""
      
      # First, we get the individual information; I use quaternions
      # for both for efficiency reasons.  (It takes less adds and
      # mults to multiply pure quaternions.
      rotation = quat(self.r, self.I) # this is the rotation information
      translation = quat(self.er, self.eI)  # This is ALMOST
                                       # the translation info
      
      # Now, we'll remove the rotation info from the
      # translation portion.
      translation = translation*rotation.inverse()
      
      beta, axis = rotation.get_angle_axis()
      pos = vector(translation.I.x*2, translation.I.y*2, \
                translation.I.z*2)
      
      return beta, axis, pos

# Here are a few quaternion constants that are nice to
# define:  in particular, note that [Left, Up, Fwd]
# is a left-hand coord system, while [Right, Up, Fwd]
# represents a right-hand one.
BetaRight = [0, 64, 128, 192]
Identity = quat(1, Zero)

XTrans = quat(); XTrans.translation(vector(100, 0, 0))
YTrans = quat(); YTrans.translation(vector(0, 100, 0))
ZTrans = quat(); ZTrans.translation(vector(0, 0, 100))

XRot0 = quat(); XRot0.rotation(BetaRight[0], vector(1,0, 0))
XRot64 = quat(); XRot64.rotation(BetaRight[1], vector(1,0, 0))
XRot128 = quat(); XRot128.rotation(BetaRight[2], vector(1,0, 0))
XRot192 = quat(); XRot192.rotation(BetaRight[3], vector(1,0, 0))

YRot0 = quat(); YRot0.rotation(BetaRight[0], vector(0,1, 0))
YRot64 = quat(); YRot64.rotation(BetaRight[1], vector(0,1, 0))
YRot128 = quat(); YRot128.rotation(BetaRight[2], vector(0,1, 0))
YRot192 = quat(); YRot192.rotation(BetaRight[3], vector(0,1, 0))

ZRot0 = quat(); ZRot0.rotation(BetaRight[0], vector(0, 0, 1))
ZRot64 = quat(); ZRot64.rotation(BetaRight[1], vector(0, 0, 1))
ZRot128 = quat(); ZRot128.rotation(BetaRight[2], vector(0, 0, 1))
ZRot192 = quat(); ZRot192.rotation(BetaRight[3], vector(0, 0, 1))

