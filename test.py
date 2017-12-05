from helpers import generateScale, generateSampleNotes, generateSampleLengths, createNote, createTune, generateOutputString
from pysynth_b import *
from midi2audio import FluidSynth

print(generateScale("A3" , "naturalMinor"))
song = createTune('A3', 'naturalMinor', 65, 80, 120,'4/4', 2)
song.write("midi", 'out.midi')
