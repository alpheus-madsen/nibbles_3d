# ttable.py

# The purpose of this module is to define sin, cos,
# tan, cot, etc by using "bradians" (1 bradian is
# 1/256 of a circle), and then make a table for
# looking up these values.

# This should be faster than calculating sin, cos,
# etc directly

# As a result of this, too, all my graphics
# functions will be have to take bradians, as well.
# To remind me of this, I'll use the term "beta"
# instead of "theta" to designate angles.

from math import sin, pi

sinfile = "sintable.dat"
sintable = []

try:
   # open table.dat
   tablefile = file(sinfile, 'r')
   for i in tablefile:
      sintable.append(float(i))
   if len(sintable) != 256:
      raise AttributeError, \
         "current file is not a bradian sin table!"
   tablefile.close()
except IOError:
   # if .sintable.dat doesn't exist, or is
   # corrupted, then create a new table...
   tablefile = file(sinfile, 'w')
   for i in range(256):
      sintable.append(sin(i*pi/128.0))
      print >>tablefile, sintable[i]
   tablefile.close()

# so now we go to the trig functions:
def tsin(beta):
   return sintable[int(round(beta)) % 256]

def tcos(beta):
   return sintable[int(64 - round(beta)) % 256]

def ttan(beta):
   # in all honesty, this would be slightly faster
   # if we were to look up the values rather than
   # resort to tsin and tcos...
   return tsin(beta)/tcos(beta)

def tcot(beta):
   # this has the same caveat as ttan
   return tcos(beta)/tsin(beta)

# Note that I won't worry about defining secant or
# cosecant.  I don't think they're needed, at least
# not for now!

