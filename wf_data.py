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
# from movable import *

import re

# Finally, I create the infamous wireframe class!

# This is created as data rather than as an item:
# Thus, it is no longer movable.  Since my worm
# will have lots of segments based on the same
# data, I realized that it would be more memory-efficient
# to separate the data from the position information..
class wf_data(object):
   def __init__(self, filename):
     """The class that represents 3D objects; this version
     only keeps track of vertex data, though:  position data
     is kept in the 'position' class."""
     self.vertices = []
     self.edges = []
     self.faces = []
     
     # We'll also want to keep track of normals, as edges.
     self.normals = []
   
     def calcFaceCenterNormal(face):
        """Calculates the Center and Normal for a given face.
         
        Ideally, this would be a function for the face class;
        unfortunately, the face class needs access to information
        that only a wireframe class will have--namely, access
        to the vertices!"""
        
        # Now, we'll calculate the center, by taking
        # the average of the vertices.
        face.center = Zero
        for v in face.vertices:
           face.center += self.vertices[v]
        face.center = face.center/len(face.vertices)
      
        # Next, we'll find the normal to this face.
        # We're assuming that the vertices of the face are
        # in a clockwise order, viewed from outside
        # the wireframe.
        v0 = self.vertices[face.vertices[0]]
        v1 = self.vertices[face.vertices[1]]
        v2 = self.vertices[face.vertices[2]]
        
        edgeV0 = v1-v0
        edgeV1 = v2-v1
        
        face.normal = edgeV0.cross(edgeV1)
        face.normal = face.normal.norm()

        face.normVertex = face.normal*25 + face.center
        
        # Now we'll store the normals as a part of the wireframe
        i = len(self.vertices)
        self.vertices.append(face.normVertex)
        self.vertices.append(face.center)
        self.normals.append(edge(i, i+1, 'black'))

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
        # First, we create the list of vertex indices
        vlist = []
        for n in ln[:-1]:
           vlist.append(int(n))

        # Next, we create the list of edge indices
        length = len(vlist)
        elist = []
        for index, v in enumerate(vlist):
           i = (index+1) % length
           e = edge(v, vlist[i])
           if e in self.edges:
              elist.append(self.edges.index(e))

        # Then we append the new face to our list!
        # Recall that ln[-1] is the color of the face.
        self.faces.append(face(vlist, elist, ln[-1]))
        
        # Finally, we calculate the center and normal for
        # our new face!
        calcFaceCenterNormal(self.faces[-1])

     def finished(ln):
        pass

     stage = [vertices, edges, faces, finished]

     wirefile = file(filename)
     i = 0 # This is the stage reference index.
     for eachline in wirefile:
         # First, remove comments that start with '#'
         eachline = re.sub('#.*', '', eachline)
         # Next, we parse the line by white-space
         eachline = re.split('\s+', eachline)
         # since sub insists on putting lots of empty string '' in
         # the lists, we need to add this loop.
         mylist = []
         for item in eachline:
            if item:  mylist.append(item)

         # This part really bugs me:  it's rather "clever", which is
         # to say, it's rather "un-Pythonic", but I can't think of a
         # more straightforward way of doing this without repeating
         # the first part of the loop!

         # To understand what's going on:  if we reach an 'end',
         # we advance to the next stage; stage[] is an array of
         # functions, each function of which adds vertices, edges
         # and faces to the wireframe.  I suppose later I could add
         # other stages (such as bitmaps for faces) without changing
         # this portion.  (I would just have to define a new function,
         # and then add it to the end of the stages array.)
         if mylist:
            # if we reach the end of one stage, go to
            # the next
            if mylist[0] == 'end':
               i+=1
            else:
               # Add vertex, edge or face according to
               # the right stage
               stage[i](mylist)

   def __str__(self):
      string = ''
      for vtx in self.vertices:
         string += str(vtx) + '\n'
      for edge in self.edges:
         string += str(edge) + '\n'
      for face in self.faces:
         string += str(face) + '\n'
      return string