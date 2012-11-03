#  worm.py.

# This is the class that produces the worm I will
# likely use in my worms3D game.
from wf_data import *
from position import *
from camera import *

# First, let's define some directional constants
# that will likely be useful:

CLOCKWISE = 0
COUNTERCLOCKWISE = 1
FORWARD = 2
BACKWARD = 3
UP = 4
LEFT = 5
DOWN = 6
RIGHT = 7

BORDER = 8

# Since worm is a collection of objects, it doesn't have a position; we
# will keep track of our position via the nose.
class worm(object):
   def __init__(self, beta=0, axis=Up, pos=Zero, beta_f=0, axis_f = Up,
            length = 3, velocity = 100, up = Up, fwd = Fwd, left = Left,
            sx=Sx, sy=Sy, near=Near, farfov=Far, eye=vector(0, 0, 500), camtype='standard'):
      
      self.nose_data = wf_data('worm_head_tail.dat')
      self.middle_data = wf_data('worm_middle_segment.dat')
      self.elbow_data = wf_data('worm_elbow.dat')

      self.nose = position(self.nose_data, beta, axis, pos, beta_f, axis_f, up, fwd, left)
      self.nose.rotate_by_Up(128)
      self.nose.setworld()

      # The Orientation axis of our worm; this is important for figuring out
      # translations and rotations!
      #self.Up = up
      #self.Fwd = fwd
      #self.Left = left

      self.length = length
      self.velocity = velocity

      self.flyVelocity = 10
      #self.flyUp = up
      #self.flyFwd = fwd
      #self.flyLeft = left

      # This is the camera that will follow our worm!
      # Note that the camera position needs appropriate coordinates! based
      # on the initial position of the nose.


      cam_beta = beta
      cam_axis = axis
      cam_pos = pos
      cam_beta_f = beta_f
      cam_axis_f = axis_f
      self.noseCamera = camera(sx, sy, near, farfov,
               cam_beta, cam_axis, cam_pos, cam_beta_f, cam_axis_f, camtype, fwd, left, up, eye)

      self.flyCamera = camera(sx, sy, near, farfov,
               cam_beta, cam_axis, cam_pos, cam_beta_f, cam_axis_f, camtype, fwd, left, up, eye)

      self.cameraList = [self.noseCamera, self.flyCamera]
      self.curCamera = 0
      self.camera = self.cameraList[self.curCamera]

      # This is where we'll keep the segments of our worm.
      self.segments = []

   def add_segment(self, direction):
      # We'll use the direction and our current position to determine
      # what pieces we'll add to self.segments.

      # Note that clockwise and counterclockwise will only rotate the camera;
      # although they should also rotate the orientation of the nose (so that
      # UP doesn't become RIGHT)!
      if direction == CLOCKWISE:
         # rotate self.Up, self.Left by the bradian-axis pair (192, self.Fwd)
         # rotate camera by the bradian-axis pair (192, camera.fwd)
         print "clockwise"
      elif direction == COUNTERCLOCKWISE:
         # rotate self.Up, self.Left by the bradian-axis pair (64, self.Fwd)
         # rotate camera by the bradian-axis pair (64, camera.fwd)
         print "counterclockwise"
      elif direction == FORWARD:
         new_segment = position(self.middle_data, self.nose.beta, 
                  self.nose.axis, self.nose.pos,
                  self.nose.beta_f, self.nose.axis_f)
         self.segments.append(new_segment)

         self.nose.add_translation(self.Fwd*self.velocity)
         self.nose.setworld()

         # Note that this works *opposite* of what I would expect!
         # I need to figure out why...
         self.noseCamera.add_translation(-self.Fwd*self.velocity)
         self.noseCamera.setworld()
      elif direction == UP:
         # First, add the elbow
         new_segment = position(self.elbow_data, self.nose.beta,
                  self.nose.axis, self.nose.pos,
                  self.nose.beta_f, self.nose.axis_f)
         new_segment.add_init_rotation(64, self.Fwd)
         new_segment.setworld()
         self.segments.append(new_segment)

         # Rotate the nose and the noseCamera
         self.nose.add_init_rotation(64, self.Left)
         self.noseCamera.add_init_rotation(64, self.Left)
         print self.nose.axis, self.noseCamera.axis

         # Now we'll want to rotate the nose's coordinate system!
         rotate_system = quat(); rotate_system.rotation(64, self.Left)
         rotate_mx = rotate_system.matrix()
         self.Up = rotate_mx * self.Up
         self.Fwd = rotate_mx * self.Fwd
         # self.Left is fixed by this rotation!

         # Now, we'll advance the nose and camera!

         self.nose.add_translation(self.Fwd*self.velocity)
         self.noseCamera.add_translation(-self.Fwd*self.velocity)

         self.nose.setworld()
         self.noseCamera.setworld()
      elif direction == LEFT:
         # First, add the elbow
         new_segment = position(self.elbow_data, self.nose.beta, 
                  self.nose.axis, self.nose.pos,
                  self.nose.beta_f, self.nose.axis_f)
         # new_segment.add_init_rotation(64, self.Up)
         new_segment.setworld()
         self.segments.append(new_segment)

         # Rotate the nose and the noseCamera
         self.nose.add_init_rotation(64, self.Up)
         self.noseCamera.add_init_rotation(64, self.Up)
         print self.nose.axis, self.noseCamera.axis

         # Now we'll want to rotate the nose's coordinate system!
         rotate_system = quat(); rotate_system.rotation(64, self.Up)
         rotate_mx = rotate_system.matrix()
         self.Left = rotate_mx * self.Left
         self.Fwd = rotate_mx * self.Fwd
         # self.Left is fixed by this rotation!

         # Now, we'll advance the nose and camera!

         self.nose.add_translation(self.Fwd*self.velocity)
         self.noseCamera.add_translation(-self.Fwd*self.velocity)

         self.nose.setworld()
         self.noseCamera.setworld()
         print "left"
         pass
      elif direction == DOWN:
         print "down"
         pass
      elif direction == RIGHT:
         print "right"
         pass
      elif direction == BACKWARD:
         print "backward"
         pass
      elif direction == BORDER:
         print "border"
         pass

   def remove_segment(self):
      # This will remove a segment from the end of the snake, and
      # advance the tail accordingly
      pass

   def set_length(self, length):
      self.length = length

   def set_velocity(self, velocity):
      self.velocity = velocity

   def drawWorm(self):
      # This is the function that will draw itself; by default it will draw on
      # its own camera.

      # Now, the nose is the front of this thing; the next segment, however, is
      # the last item in this list; and the item before that is there, too.
      #  Thus, we need to reverse it!
      self.segments.reverse()

      # Draw the nose...
      self.nose.sketchOnto(self.camera)
      for segment in self.segments:

         # First, we'll need to check to see if we should draw it...

         # If so, we'll then do this:
         segment.sketchOnto(self.camera)

      # We now restore the list to its original order.
      self.segments.reverse()
      # Now we draw the tail.
      # self.tail.drawOnto(self.camera)

   # For debugging purposes, I wanted a camera I could move independently
   # of the main camera.
   def move_flyCamera(self, direction, button):
      """For debugging purposes, I wanted a camera I could move independently
      of the main camera."""
      if direction == CLOCKWISE:
         self.flyCamera.rotate_by_Fwd(2)
         self.flyCamera.setworld()
      elif direction == COUNTERCLOCKWISE:
         self.flyCamera.rotate_by_Fwd(-2)
         self.flyCamera.setworld()
         print "counterclockwise"
      elif direction == FORWARD:
         if button == 1:
            self.flyCamera.translate_by_Fwd(self.flyVelocity)
            self.flyCamera.setworld()
         elif button == 3:
            self.flyCamera.rotate_by_Fwd(2)
            self.flyCamera.setworld()
            print "clockwise"
      elif direction == BACKWARD:
         if button == 1:
            self.flyCamera.translate_by_Fwd(-self.flyVelocity)
            self.flyCamera.setworld()
         elif button == 3:
            self.flyCamera.rotate_by_Fwd(-2)
            self.flyCamera.setworld()
            print "counterclockwise"
      elif direction == UP:
         if button == 1:
            self.flyCamera.translate_by_Up(self.flyVelocity)
            self.flyCamera.setworld()
         elif button == 3:
            self.flyCamera.rotate_by_Left(2)
            self.flyCamera.setworld()
      elif direction == LEFT:
         if button == 1:
            self.flyCamera.translate_by_Left(self.flyVelocity)
            self.flyCamera.setworld()
         elif button == 3:
            self.flyCamera.rotate_by_Up(2)
            self.flyCamera.setworld()
      elif direction == DOWN:
         if button == 1:
            self.flyCamera.translate_by_Up(-self.flyVelocity)
            self.flyCamera.setworld()
         elif button == 3:
            self.flyCamera.rotate_by_Left(-2)
            self.flyCamera.setworld()
      elif direction == RIGHT:
         if button == 1:
            self.flyCamera.translate_by_Left(-self.flyVelocity)
            self.flyCamera.setworld()
         elif button == 3:
            self.flyCamera.rotate_by_Up(-2)
            self.flyCamera.setworld()

   def cycleCamera(self):
      self.curCamera = (self.curCamera+1)%len(self.cameraList)
      self.camera = self.cameraList[self.curCamera]

   def pop(self):
      """The sole purpose of this function is to check whether or not
      the wireframe data given to wf_data is really independent of the position
      data given to each wf_data instance.  If it is, then this should cause
      the vertex to "pop out" for all the segments drawn; otherwise, it
      would have no effect at all.
      
      The wireframe data *is* independent, as desired!"""
      self.middle_data.vertices[0] = vector(100, 100, 100)