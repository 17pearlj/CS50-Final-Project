from helpers import generateScale, generateSampleNotes, generateSampleLengths, createNote, createTune, createPySynthTune
from pysynth_b import *
from midi2audio import FluidSynth


stream1 = createTune("A3", 'major', 50, 70, 20, 0)
song = stream1.write("midi", "blah.midi")

fluid_synth_sfload(fs, 'FluidR3_GM.sf2', TRUE )
