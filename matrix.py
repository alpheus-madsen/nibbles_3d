# matrix.py -- A module for the creation of matrices
# for purposes of projecting things to the screen.
# Eventually these should be ported to C or C++ for
# better efficiency!

# Note that while I've been ignoring exceptions, I
# should probably create a MatrixException class
# that would include "AddException" or
# "MultException" when invalid matrix arithmetic
# is attempted

# Also note that this module needs the following:
#   ttable.py, for bradian trig table functions
#   vertex.py, for vectors
from ttable import *
from vertex import *

class matrix(object):
   def __init__(self):
      self.mx = []

   # Note that I decided to do away with __add__ and
   # __sub__, since they aren't used much in computer
   # graphics.

   def __mul__(self, m):
      """Multiplies two matrices, or a matrix and scalar, or a matrix and a vector..

         This should also throw an exception if the two matrices provided cannot be multiplied
         together.  (This isn't implemented, though. As it currently stands, it allows multi-
         plication of matrices that are sufficiently similar...that is, any two matrices for
         which the index doesn't go out of range before the algorithm is finished.

         For example, it's possible to "multiply" two 3x2 matrices.)"""
      if isinstance(m, matrix):
         r = matrix()
         for i in range(0, len(self.mx)):
            r.mx.append([])
            for j in range(0, len(m.mx[0])):
               r.mx[i].append(0)
               for k in range(0, len(m.mx)):
                  r.mx[i][j] += self.mx[i][k]*m.mx[k][j]
         return r
      elif isinstance(m, vector):
         return self.proj(m)
      else:
         r = matrix()
         for i in range(0, len(self.mx)):
            r.mx.append([])
            for j in range(0, len(m.mx[0])):
               r.mx[i].append(self.mx[i][j]*m)
         return r

   def proj(self, v):
      """Multiplies a matrix with a vector.

         I call it "proj" because it will be how I
         will project a vector using my camera
         matrix."""
         
         # Note that I've removed v.w from this matrix; the
         # last element should be self.mx[j][3]*v.w
         
         # Instead, I assume that w==1.
      x = float(self.mx[0][0]*v.x + self.mx[0][1]*v.y + \
            self.mx[0][2]*v.z + self.mx[0][3])

      y = float(self.mx[1][0]*v.x + self.mx[1][1]*v.y + \
            self.mx[1][2]*v.z + self.mx[1][3])

      z = float(self.mx[2][0]*v.x + self.mx[2][1]*v.y + \
            self.mx[2][2]*v.z + self.mx[2][3])

      w = float(self.mx[3][0]*v.x + self.mx[3][1]*v.y + \
            self.mx[3][2]*v.z + self.mx[3][3])

      # We might as well return a homogeneous vector!
      if w == 0:
         return vector(x, y, z)
      else:
         return vector(x/w, y/w, z/w)

   def __str__(self):
      """Creates a string representation of a matrix."""
      string = ''
      for i in self.mx:
         string += '[ %s ]\n' % i
      return string

def getproj(left, right, top, bottom, near, far):
   """Takes values given and returns a projection matrix.

   This function is based on the general description
   given in 3D Game Engine Design, p. 86...This
   matrix also incorporates the two equations

   (Sx-1)*(x+1)/2 and (Sy-1)*(y+1)/2.

   that will project the vectors onto the screen.
   (As described in 3D Game Engine Design, the matrix
   doesn't do this.)"""
   Sx = right-left
   Sy = top-bottom
   Sz = far-near

   # To translate the point to screen coordinates,
   # I'll need the following constants:
   PSx = (Sx-1)/2
   PSy = (Sy-1)/2

   mx = matrix()
   mx.mx = [
      [2*near/Sx*PSx, 0, (right+left)/Sx-PSx, 0],
      [0, 2*near/Sy*PSy, (top+bottom)/Sy-PSy, 0],
      [0, 0, -(far+near)/Sz, -2*(far*near)/Sz],
      [0, 0, -1, 0] ]
   return mx

def getfovproj(left, right, top, bottom, near, beta):
   """Takes values given and returns a fov projection matrix.

   This function is based on the technique described
   in Linux 3D Programming, p. 381.  Unlike the
   original setproj(), the vectors returned are given
   as screen coordinates."""
   Sy = float(top - bottom)
   Sx = float(right - left)
   fov = tcot(beta/2)

   mx = matrix()
   mx.mx = [ [(Sx/2)*fov, 0, Sx/2, 0],
             [0, -(Sy/2)*fov*(Sx/Sy), Sy/2, 0],
             [0, 0, near, 1],
             [0, 0, 1, 0] ]
   print "Sy=%s, Sx=%s, fov=%s" % (Sy, Sx, fov)
   print mx
   return mx

# Here we assume that left, up, fd form an
# orthonormal basis.  I would expect that
# interesting things would happen if these
# vectors -weren't- orthonormal! but I haven't
# tried it yet, to see what would happen.
def getcam(fwd, left, up, eye):
   """Takes given vectors and returns a coord-changing matrix.

   That is, a matrix that transfers "world"
   coordinates to camera ones, and then translates
   them  via the eye to the right spot."""
   mx = matrix()
   mx.mx = [ [left.x, left.y, left.z, -left.dot(eye)],
             [up.x, up.y, up.z, -up.dot(eye)],
             [fwd.x, fwd.y, fwd.z, -fwd.dot(eye)],
             [0, 0, 0, 1] ]
   #mx.mx = [ [fwd.x, fwd.y, fwd.z, -fwd.dot(eye)],
   #          [left.x, left.y, left.z, -left.dot(eye)],
   #          [up.x, up.y, up.z, -up.dot(eye)],
   #          [0, 0, 0, 1] ]
   #mx.mx = [ [fwd.x, left.x, up.x, -fwd.dot(eye)],
   #          [fwd.y, left.y, up.y, -left.dot(eye)],
   #          [fwd.z, left.z, up.z, -up.dot(eye)],
   #          [0, 0, 0, 1] ]
   return mx

# Here we assume that axis is normalized...but pos
# shouldn't be! The default is the identity matrix...
def getworld(beta=0, axis=Up, pos=Zero):
   """Takes values and returns a rotation/translation matrix.

   In particular, it rotates the object beta bradians
   around given axis (it needs to be pre-normalized)
   and then translates the object via pos."""

   # This is the rotation quaternion...
   w = tcos(beta/2)
   x = tsin(beta/2)*axis.x
   y = tsin(beta/2)*axis.y
   z = tsin(beta/2)*axis.z

   # Here are a few calculations that will be used to
   # create our special matrix!
   xx2 = 2*x*x; yy2 = 2*y*y; zz2 = 2*z*z
   wx2 = 2*w*x; wy2 = 2*w*y; wz2 = 2*w*z
   xy2 = 2*x*y; xz2 = 2*x*z; yz2 = 2*y*z

   quat_mx = matrix()
   quat_mx.mx = [ [1-yy2-zz2, xy2+wz2, xz2-wy2, 0],
             [xy2-wz2, 1-xx2-zz2, yz2+wx2, 0],
             [xz2+wy2, yz2-wx2, 1-xx2-yy2, 0],
             [0, 0, 0, 1] ]

   # Now we'll add the translation portion; here we assume that
   # the rotation is done first, and then the translation.
   quat_mx.mx[0][3] = quat_mx.mx[0][0]*pos.x + quat_mx.mx[0][1]*pos.y + quat_mx.mx[0][2]*pos.z
   quat_mx.mx[1][3] = quat_mx.mx[1][0]*pos.x + quat_mx.mx[1][1]*pos.y + quat_mx.mx[1][2]*pos.z
   quat_mx.mx[2][3] = quat_mx.mx[2][0]*pos.x + quat_mx.mx[2][1]*pos.y + quat_mx.mx[2][2]*pos.z
   
   return quat_mx

def gettrans(pos=Zero):
   mx = matrix()
   mx.mx = [ [1, 0, 0, pos.x],
             [0, 1, 0, pos.y],
             [0, 0, 1, pos.z],
             [0, 0, 0, 1] ]
   return mx

def getskew(r, s, t, pos=Zero):
   mx = matrix()
   mx.mx = [ [r, 0, 0, pos.x],
             [0, s, 0, pos.y],
             [0, 0, t, pos.z],
             [0, 0, 0, 1] ]
   return mx
