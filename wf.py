# This module should contain everything I need to
# create a wireframe object.

# This is the first major step in creating my game
# engine.

# Special note:  For some reason, in
# "wireframe.__init__", the function "re.sub"
# insists on adding '' whenever there's whitespace.
# I don't know if this is a 'feature' or if I'm
# doing something wrong there...but it's nonetheless
# annoying.

from vertex import *
from movable import *

import re

# Finally, I create the infamous wireframe class!
# This class has been superceded by the combination of
# classes wf_data and position; it's left here for backwards
# compatibility.
class wireframe(movable):
   'The class that represents 3D objects.'
   
   def __init__(self, filename, beta=0, axis=Up, pos=Zero, beta_f=0, axis_f=Up):
     movable.__init__(self, beta, axis, pos, beta_f, axis_f)
     self.vertices = []
     self.edges = []
     self.faces = []

     # Each stage of processing the data file has a
     # special function that will be referenced in
     # a special loop.
     def vertices(ln):
        'Converts a list to a vertex format for wireframe.'
        v = vector(float(ln[0]), float(ln[1]), float(ln[2]))
        self.vertices.append(v)
     def edges(ln):
        'Converts a list to an edge format for wireframe.'
        e = edge(int(ln[0]), int(ln[1]), ln[2])
        self.edges.append(e)
     def faces(ln):
        'Converts a list to a face format for wireframe.'
        vlist = []
        for n in ln[:-1]:
           vlist.append(int(n))
        edges = []
        self.faces.append(face(vlist, edges, ln[-1]))
     def finished(ln):
        pass
     stage = [vertices, edges, faces, finished]

     myfile = file(filename)
     i = 0
     for eachline in myfile:
        eachline = re.sub('#.*', '', eachline)
           # to remove comments that start with '#'
        eachline = re.split('\s+', eachline)
           # the '+' is needed to keep lots of ''
           #   from being added

        # since sub insists on putting lots of '' in
        # the lists, we need to add this loop.
        mylist = []
        for item in eachline:
           if item:  mylist.append(item)

        if mylist:
           if mylist[0] == 'end':
            # if we reach the end of one stage, go to
            # the next
              i+=1
           else:
           # Add vertex, edge or face according to
           # the right stage
              stage[i](mylist)

   def drawOnto(self, camera):
      """This function draws the wireframe onto the given camera."""
      # Note that this might be a good time to use a line like
      # self.setworld()
      
      viewport = camera.camera_mx*self.world

      vtcs = []
      for i in self.vertices:
         vtx = viewport.proj(i)
         # For non-homogeneous vertices:
         #    vtcs.append([319*(vtx.x/vtx.e-1)/2,
         #               399*(vtx.y/vtx.e-1)/2])
         vtcs.append([vtx.x, vtx.y])
         # For non-homogeneous vertices:
         #   vtcs.append([vtx.x/vtx.e, vtx.y/vtx.e])

      # Now let's draw the lines!
      for i in self.edges:
         pygame.draw.line(camera.film, egacolor[i.color], (vtcs[i.v1][0], vtcs[i.v1][1]), (vtcs[i.v2][0], vtcs[i.v2][1]))
         
      # Finally, I should draw the faces! but not for now...

   def __str__(self):
      string = ''
      for vtx in self.vertices:
         string += str(vtx) + '\n'
      for edge in self.edges:
         string += str(edge) + '\n'
      for face in self.faces:
         string += str(face) + '\n'
      return string
