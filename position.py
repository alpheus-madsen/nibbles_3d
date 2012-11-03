# movable.py  -- This module defines a class from
# which 3D objects, such as cameras and wireframes,
# can inherit.  In doing so, they become manipulable
# by various means...particularly by matrices.

from movable import *

class position(movable):
   # This class should have position information, including its
   # own matrix! but it shouldn't have much more than that.
   def __init__(self, wf_data, beta=0, axis=Up, pos=Zero,
                beta_f=0, axis_f=Up, fwd=Fwd, left=Left, up=Up):
      """This class separates the position of a data set from
      the data set itself.  Since my nibbles program will be
      using the same vector data set for worms, I realized that
      I just needed to keep track of the position information for
      each segment!"""
      movable.__init__(self, beta, axis, pos, beta_f, axis_f, fwd, left, up)

      self.wf_data = wf_data

   # This function should draw the wireframe onto the camera!

   # Come to think of it, this function assumes that position is a
   # wireframe of some sort.  Instead, I should call this
   # draw_wf_Onto(self, camera) or something like that.

   # Of course, if I create some sort of world, that world will
   # probably be responsible for drawing things anyway, so
   # I'm not sure what to think exactly...
   def drawOnto(self, camera):
      # Note that this might be a good time to use a line like
      # self.setworld()
      # On second thought:  No, it wouldn't be a good place!
      # If the world matrix hasn't changed, there is no reason
      # to reset it!

      viewport = camera.camera_mx*self.world

      vtcs = []
      for i in self.wf_data.vertices:
         vtx = viewport.proj(i)
         # For non-homogeneous vertices:
         #    vtcs.append([319*(vtx.x/vtx.e-1)/2,
         #               399*(vtx.y/vtx.e-1)/2])
         vtcs.append([vtx.x, vtx.y])
         # For non-homogeneous vertices:
         #   vtcs.append([vtx.x/vtx.e, vtx.y/vtx.e])

      # Now let's draw the lines!
      for i in self.wf_data.edges:
         pygame.draw.line(camera.film, egacolor[i.color], \
                  (vtcs[i.v1][0], vtcs[i.v1][1]), (vtcs[i.v2][0], vtcs[i.v2][1]))

      # Finally, I should draw the faces! but not for now...

   def sketchOnto(self, camera):
      """This function 'sketches' the wireframe onto the given camera.
      That is, this function sorts through the faces and edges, and
      decides what should be drawn first, or even what should be drawn
      at all.

      This will allow whatever is drawing the scene to sort through all
      the objects, to determine what order things should be drawn.

      I *think* this assumes objects are simply connected and convex!

      Rather, this function *ought* to 'sketch' a wireframe!  For now,
      it just draws it."""
      viewport = camera.camera_mx*self.world

      pVertices = []
      zValues = []
      for i in self.wf_data.vertices:
         vtx = viewport.proj(i)
         pVertices.append([vtx.x, vtx.y])
         # zValues.append([vtx.z])

      # Now let's figure out which lines and faces get drawn!
      # First, we initialize two arrays; they default to "True"
      #visibleFaces = [ True for i in range(len(self.wf_data.faces))]
      #visibleEdges = [ True for i in range(len(self.wf_data.edges))]

      # I should probably calculate the zValues for the faces
      # and edges; at least, the ones that will be drawn!

      # Next, we go through the faces, to see which ones will
      # be drawn:
      #fwd = camera.getFwdCoord()
      #viewCenter = camera.getCenterCoord()
      #for i, f in enumerate(self.wf_data.faces):
         #dot = f.normal.dot(fwd)
         #if dot > 0:
            #visibleFaces[i] = False
            #for j in f.edges:
               #visibleEdges[j] = False
         ## We now calculate the vector from the center of the camera
         ## to the center of the face.
         #elif dot == 0:
            #center = viewCenter - f.center
            #if f.normal.dot(center) > 0:
               #visibleFaces[i] = False
               #for j in f.edges:
                  #visibleEdges[j] = False
         #print dot,
      #print
      #print "visFace ", visibleFaces
      #print "visEdges ", visibleEdges

      # Actually, instead of deciding which faces and edges I *won't*
      # draw, I will decide which I *will* draw.  This will be especially
      # important for the edges, because if I decide not to draw a face,
      # I may still want to draw one of its edges.  Thus, I will
      # initialize these as false.
      visibleFaces = [ False for i in range(len(self.wf_data.faces))]
      visibleEdges = [ False for i in range(len(self.wf_data.edges))]

      # I should probably calculate the zValues for the faces
      # and edges; at least, the ones that will be drawn!

      # Next, we go through the faces, to see which ones will
      # be drawn:
      fwd = camera.getFwdCoord()
      viewCenter = camera.getCenterCoord()
      for i, f in enumerate(self.wf_data.faces):
         dot = f.normal.dot(fwd)
         center = viewCenter - f.center
         #if dot < 0 or f.normal.dot(center) < 0:
         if dot >  0:
            visibleFaces[i] = True
            for j in f.edges:
               visibleEdges[j] = True
         # We now calculate the vector from the center of the camera
         # to the center of the face.
         #elif dot == 0:
         #   center = viewCenter - f.center
         #   if f.normal.dot(center) < 0:
         #      visibleFaces[i] = True
         #      for j in f.edges:
         #         visibleEdges[j] = True
         # print dot,
      # print
      # print "visFace ", visibleFaces
      # print "visEdges ", visibleEdges

      # Now, let's draw the faces that will be shown!
      for i, f in enumerate(self.wf_data.faces):
         if visibleFaces[i]:
            vList = []
            for j in f.vertices:
               vList.append(pVertices[j])
            pygame.draw.polygon(camera.film, egacolor[f.color], vList)


      # Next let's draw the edges!  At least, the ones that deserve to be drawn!
      for i, e in enumerate(self.wf_data.edges):
         if visibleEdges[i]:
            pygame.draw.line(camera.film, egacolor[e.color],
                 (pVertices[e.v1][0], pVertices[e.v1][1]),
                 (pVertices[e.v2][0], pVertices[e.v2][1]))

      # Finally (for debugging purposes) let's draw the normals!
      for i, e in enumerate(self.wf_data.normals):
         if visibleFaces[i]:
            pygame.draw.line(camera.film, egacolor[e.color],
                 (pVertices[e.v1][0], pVertices[e.v1][1]),
                 (pVertices[e.v2][0], pVertices[e.v2][1]))

      # Finally, let's draw the coordinate frame for the camera.
      #fwdAxis = viewport.proj(camera.getFwdCoord())
      #upAxis = viewport.proj(camera.getUpCoord())
      #leftAxis = viewport.proj(camera.getLeftCoord())
      #centerPt = viewport.proj(camera.getCenterCoord())
      
      # The above axis information ignores an important fact:
      # the axis information is centered at the world center
      # coordinate (0, 0, 0), but it needs to be centered at
      # the center coordinate!  Thus, we need to change it to:
      centerOfAxisVector = camera.getCenterCoord()
      fwdAxisVector = camera.getFwdCoord()*50 + centerOfAxisVector
      upAxisVector = camera.getUpCoord()*50 + centerOfAxisVector
      leftAxisVector = camera.getLeftCoord()*50 + centerOfAxisVector
      
      # Now we project these four vectors onto the screen.
      centerPt = viewport.proj(centerOfAxisVector)
      fwdAxis = viewport.proj(fwdAxisVector)
      upAxis = viewport.proj(upAxisVector)
      leftAxis = viewport.proj(leftAxisVector)

      pygame.draw.line(camera.film, egacolor['blue'],
            (upAxis.x, upAxis.y), (centerPt.x, centerPt.y))
      pygame.draw.circle(camera.film, egacolor['blue'], (int(centerPt.x), int(centerPt.y)), 10)
      pygame.draw.line(camera.film, egacolor['green'],
            (fwdAxis.x, fwdAxis.y), (centerPt.x, centerPt.y))
      pygame.draw.line(camera.film, egacolor['red'],
            (leftAxis.x, leftAxis.y), (centerPt.x, centerPt.y))
            
      # print "Fwd ", camera.getFwdCoord(), "Up ", camera.getUpCoord(), "Left ", camera.getLeftCoord(), "Center ", camera.getCenterCoord()

   def __str__(self):
      return movable.__str__(self)
