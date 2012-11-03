# movable.py  -- This module defines a class from
# which 3D objects, such as cameras and wireframes,
# can inherit.  In doing so, they become manipulable
# by various means...particularly by matrices.

from vertex import *
from matrix import *
from quat import *

class movable(object):
   def __init__(self, beta=0, axis=Up, pos=Zero, beta_f=0, axis_f=Up, fwd=Fwd, left=Left, up=Up):
      """Sets angle, axis vector, and position vector;
      also sets up a coordinate axis.

      Since rotations require a normalized axis, we
      take the norm of the axis we want to rotate by.

      Note that the angle is given in bradians.

      Note that the position is set *without* altering
      the coordinate system.  To match the
      coordinate system with the current rotations,
      call match_coordinates()."""
      self.beta = beta
      self.axis = axis.norm()
      self.pos = pos

      self.beta_f = beta_f
      self.axis_f = axis_f

      # We'll set up the object's coordinate system now:
      self.Up = up
      self.Fwd = fwd
      self.Left = left

      self.coordination = quat(1)  # this is the identity rotation.

      # These are the dual quaternions used for the wireframe's position.
      # First, we rotate around the center; then translate; finally rotate again.
      self.init_rotation = quat(); self.init_rotation.rotation(self.beta, self.axis)
      self.translation = quat(); self.translation.translation(self.pos)
      self.final_rotation = quat(); self.final_rotation.rotation(self.beta_f, self.axis_f)

      self.orientation = self.final_rotation*self.translation*self.init_rotation
      self.world = self.orientation.matrix()

   def get_world(self):
      #if self.orientation_changed:
      self.orientation = self.final_rotation*self.translation*self.init_rotation
      self.world = self.orientation.matrix()

   def setworld(self):
      self.orientation = self.final_rotation*self.translation*self.init_rotation
      self.world = self.orientation.matrix()

   # The following methods are used to set rotations and translations.

   # Note that, since multiple rotations and translations can be applied to
   # something, it's up to the programmer to call setworld() to make these
   # changes effective.

   # Also note that, typically, setworld() would be called by the function
   # that draws this darn thing!
   def set_init_rotation(self, beta, axis):
      self.beta = beta
      self.axis = axis
      self.init_rotation.rotation(self.beta, self.axis)

   def set_init_angle(self, beta):
      self.beta = beta
      self.init_rotation.rotation(self.beta, self.axis)

   def set_init_axis(self, axis):
      self.axis = axis
      self.init_rotation.rotation(self.beta, self.axis)

   def add_init_rotation(self, beta, axis):
      addition = quat()
      addition.rotation(beta, axis)

      self.init_rotation = addition*self.init_rotation
      self.beta, self.axis = self.init_rotation.get_angle_axis()

   def add_translation(self, pos):
      addition = quat()
      addition.translation(pos)

      self.translation = self.translation * addition
      self.pos = self.translation.get_translation()

   def set_translation(self, pos):
      self.translation.translation(pos)
      self.pos = pos

   def set_final_angle(self, beta):
      self.beta_f = beta
      self.final_rotation.rotation(self.beta_f, self.axis_f)

   def set_init_axis(self, axis):
      self.axis_f = axis
      self.final_rotation.rotation(self.beta_f, self.axis_f)

   def add_final_rotation(self, beta, axis):
      addition = quat()
      addition.rotation(beta, axis)

      self.final_rotation = addition*self.final_rotation
      self.beta_f, self.axis_f = self.final_rotation.get_angle_axis()

   def get_combined_orientation(self):
      """Gets the axis-angle and position information
      that comes from self.orientation, which combines
      the initial angle-axis, the position, and the final angle-axis."""
      return self.orientation.get_angle_axis_translation()

   def get_coordinate_orientation(self):
      """Gets the angle-axis orientation of the local coordinate
      axis system."""
      return self.coordination.get_angle_axis()

   def match_coordinates(self):
      """Matches the initial coordinate system with the current
      rotation information given for the object."""
      # Note that I can't just use orientation:  the coordinate
      # system is never translated.  Thus, I will simply combine
      # the rotations.

      # It's important to remember:  order matters.  I decided
      # that this is the correct order from thinking about the
      # position dual quaternion:
      #     final_rot * trans * init_rot
      self.coordination = self.final_rotation * self.init_rotation

   def rotate_by_Fwd(self, beta=2):
      """Rotates by the object's forward axis; also rotates
      the remaining two axes by the same amount."""

      # To avoid round-off errors, we'll keep the coordinate
      # axes constant, and just keep track of their orientation
      # (called self.coordination).
      fwdQuat = quat()
      fwdQuat.pureVector(self.Fwd)
      fwd = self.coordination*fwdQuat*self.coordination.inverse()

      rotation = quat()
      rotation.rotation(beta, fwd.extractPureVector())

      self.init_rotation = self.init_rotation*rotation
      self.beta, self.axis = self.init_rotation.get_angle_axis()

      # Now, we'll "rotate" the coordinate system, by applying
      # the same rotation to the coordinate system quaternion.
      self.coordination = rotation * self.coordination

   def rotate_by_Left(self, beta=2):
      """Rotates by the object's left axis; also rotates
      the remaining two axes by the same amount."""

      # To avoid round-off errors, we'll keep the coordinate
      # axes constant, and just keep track of their orientation
      # (called self.coordination).
      leftQuat = quat()
      leftQuat.pureVector(self.Left)
      left = self.coordination*leftQuat*self.coordination.inverse()

      rotation = quat()
      rotation.rotation(beta, left.extractPureVector())

      self.init_rotation = self.init_rotation*rotation
      self.beta, self.axis = self.init_rotation.get_angle_axis()

      # Now, we'll "rotate" the coordinate system, by applying
      # the same rotation to the coordinate system quaternion.
      self.coordination = rotation * self.coordination

   def rotate_by_Up(self, beta=2):
      """Rotates by the object's up axis; also rotates
      the remaining two axes by the same amount."""

      # To avoid round-off errors, we'll keep the coordinate
      # axes constant, and just keep track of their orientation
      # (called self.coordination).
      upQuat = quat()
      upQuat.pureVector(self.Up)
      up = self.coordination*upQuat*self.coordination.inverse()

      rotation = quat()
      rotation.rotation(beta, up.extractPureVector())

      self.init_rotation = self.init_rotation*rotation
      self.beta, self.axis = self.init_rotation.get_angle_axis()

      # Now, we'll "rotate" the coordinate system, by applying
      # the same rotation to the coordinate system quaternion.
      self.coordination = rotation * self.coordination

   def translate_by_Up(self, velocity=1):
      """Tranlsates by the object's Up axis, multiplied by velocity."""

      # To avoid round-off errors, we'll keep the coordinate
      # axes constant, and just keep track of their orientation
      # (called self.coordination).

      # First, we need to calculate the Up vector.
      upQuat = quat()
      upQuat.pureVector(self.Up)
      up = self.coordination*upQuat*self.coordination.inverse()

      # Second, we create the translation
      translate = quat()
      translate.translation(up.extractPureVector()*velocity)

      # Finally, we apply the translation!
      self.translation = self.translation*translate
      self.pos = self.translation.get_translation()

   def translate_by_Fwd(self, velocity=1):
      """Tranlsates by the object's Fwd axis, multiplied by velocity."""

      # To avoid round-off errors, we'll keep the coordinate
      # axes constant, and just keep track of their orientation
      # (called self.coordination).

      # First, we need to calculate the Fwd vector.
      fwdQuat = quat()
      fwdQuat.pureVector(self.Fwd)
      fwd = self.coordination*fwdQuat*self.coordination.inverse()

      # Second, we create the translation
      translate = quat()
      translate.translation(fwd.extractPureVector()*velocity)

      # Finally, we apply the translation!
      self.translation = self.translation*translate
      self.pos = self.translation.get_translation()

   def translate_by_Left(self, velocity=1):
      """Tranlsates by the object's Left axis, multiplied by velocity."""

      # To avoid round-off errors, we'll keep the coordinate
      # axes constant, and just keep track of their orientation
      # (called self.coordination).

      # First, we need to calculate the Left vector.
      leftQuat = quat()
      leftQuat.pureVector(self.Left)
      left = self.coordination*leftQuat*self.coordination.inverse()

      # Second, we create the translation
      translate = quat()
      translate.translation(left.extractPureVector()*velocity)

      # Finally, we apply the translation!
      self.translation = self.translation*translate
      self.pos = self.translation.get_translation()

   # -----------------------------------------------------------------------------
   # Note that the following methods  are provided for backwards
   # compatibility; MOST should probably be elliminated.
   # -----------------------------------------------------------------------------

   # The nice thing about the following methods is
   # that, once the world matrix is set, the points
   # will be moved "automatically" when they are
   # projected.

   # Also, if further things are needed (like
   # multiplying with other matrices) these could
   # be over-ridden...but after things are set,
   # we don't have to worry about the object again.
   def setangle(self, beta):
      self.beta = beta
      self.init_rotation.rotation(self.beta, self.axis)

      # self.world = getworld(self.beta, self.axis, self.pos)
      self.setworld()
      # self.get_world(False)

   def setaxis(self, axis):
      self.axis = axis.norm()
      self.init_rotation.rotation(self.beta, self.axis)

      # self.world = getworld(self.beta, self.axis, self.pos)
      self.setworld()
      # self.get_world(False)

   def setrot(self, beta, axis):
      self.beta = beta
      self.axis = axis.norm()
      self.init_rotation.rotation(self.beta, self.axis)

      #self.world = getworld(self.beta, self.axis, self.pos)
      self.setworld()
      # self.get_world(False)

   def settrans(self, pos):
      self.pos = pos
      self.translation.translation(self.pos)

      # self.world = getworld(self.beta, self.axis, self.pos)
      self.setworld()
      # self.get_world(False)

   def setmove(self, beta=0, axis=Up, pos=Zero, beta_f=0, axis_f=Up):
      self.__init__(beta, axis, pos, beta_f, axis_f)

   def getorient(self):
      return (self.beta, self.axis, self.pos, self.beta_f, self.axis_f)

   def getcoordsys(self):
      inv = self.coordination.inverse()
      
      up = quat()
      up.pureVector(self.Up)
      up = self.coordination*up*inv
      
      left = quat()
      left.pureVector(self.Left)
      left = self.coordination*left*inv
      
      fwd = quat()
      fwd.pureVector(self.Fwd)
      fwd = self.coordination*fwd*inv
      return (fwd.extractPureVector(), left.extractPureVector(), up.extractPureVector())

   def getUpCoord(self):
      up = quat()
      up.pureVector(self.Up)
      up = self.coordination*up*self.coordination.inverse()
      return up.extractPureVector()

   def getLeftCoord(self):
      left = quat()
      left.pureVector(self.Left)
      left = self.coordination*left*self.coordination.inverse()
      return left.extractPureVector()

   def getFwdCoord(self):
      fwd = quat()
      fwd.pureVector(self.Fwd)
      fwd = self.coordination*fwd*self.coordination.inverse()
      return fwd.extractPureVector()

   def getCenterCoord(self):
      """Returns the position of the center of this object, after
      it has been translated and rotated about."""
      
      # To understand what I am about to do:  imagine multiplying
      # a 4x4 Matrix with the "Zero" vector (0, 0, 0, 1).  We
      # get the last three bits (the tranlsation bits) of the matrix!
      return vector(self.world.mx[0][3], self.world.mx[1][3], self.world.mx[2][3])

   def __str__(self):
      string = '-----position-----\n'
      string += 'beta-axis: %s %s\n' % (self.beta, self.axis)
      string += 'position:  %s\n' % (self.pos)
      string += 'beta_f-axis_f:  %s %s\n' % (self.beta_f, self.axis_f)
      string += '--------------------\n'
      string += str(self.world)
      string += '--------------------\n'

      return string

   # I need to use a position string for pygame.Font.render(), because
   # Pygame can't handle the newline '\n' character.
   def getPosStr(self):
      return '%s ~ %s || %s || %s ~ %s' % (self.beta, self.axis, self.pos, self.beta_f, self.axis_f)

   def getCoordSystemStr(self):
      inv = self.coordination.inverse()
      up = self.coordination*self.Up*inv
      left = self.coordination*self.Left*inv
      fwd = self.coordination*self.Fwd*inv
      return 'Fwd:  %s || Left:  %s || Up:  %s' % (fwd, left, up)

# I initially tried to add methods like "addrot()",
# but the quaternion math involved was too complex.
# Part of the problem is that this class is based
# on angle-axis rotations rather than quaternion
# rotations, so I couldn't take advantage of
# combining rotations via quaternionic
# multiplication.

# Eventually I should probably re-write this so
# that I could use quaternions instead of angle-axis
# rotations.  I chose to ignore this for now,
# though, and focus on getting the camera to work.
