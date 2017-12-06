import random
import math
from music21 import *
from music21 import tempo

notesDict = {'C3': 0,
        'C#3': 1,
        'D3' : 2,
        'D#3': 3,
        'E3' : 4,
        'F3':  5,
        'F#3': 6,
        'G3' : 7,
        'G#3': 8,
        'A3' : 9,
        'A#3': 10,
        'B3' : 11,
        'C4' : 12,
        'C#4': 13,
        'D4' : 14,
        'D#4': 15,
        'E4' : 16,
        'F4':  17,
        'F#4': 18,
        'G4' : 19,
        'G#4': 20,
        'A4' : 21,
        'A#4': 22,
        'B4' : 23,
        'C5' : 24}

lengthDict = {'whole' : 4, 'half' : 2, 'quarter' : 1, 'eighth' : 0.5, "16th": 0.25}
lengthDictPySynth = {'whole' : 1, 'half' : 2, 'quarter' : 4, 'eighth' : 8, "16th": 16}

notes = ['C3', 'C#3', 'D3', 'D#3', 'E3', 'F3', 'F#3', 'G3', 'G#3', 'A3', 'A#3', 'B3',
         'C4', 'C#4', 'D4', 'D#4', 'E4', 'F4', 'F#4', 'G4', 'G#4', 'A4', 'A#4', 'B4', 'C5']

# Given a root note and a type of scale, returns that scale
def generateScale(tonic, style):
    # Empty scale to be returned
    scale = []

    # Scale generation for a major scale
    if(style == 'major'):
        # Set first index in the scale to tonic
        index = notesDict[tonic]
        # Loop through 8 notes
        for i in range(8):
            # Half Steps
            if i == 2 or i == 6:
                scale.append(notes[index])
                index += 1
            # Whole Steps
            else:
                scale.append(notes[index])
                index += 2

    # Scale generation for a natural minor scale
    if style == 'naturalMinor':
        # Set first index in the scale to tonic
        index = notesDict[tonic]
        # Loop through 8 notes
        for i in range(8):
            # Half Steps
            if i == 1 or i == 4:
                scale.append(notes[index])
                index += 1
            # Whole Steps
            else:
                scale.append(notes[index])
                index += 2

    # Scale generation for a harmonic minor scale
    if style == 'harmonicMinor':
        # Set first index in the scale to tonic
        index = notesDict[tonic]
        # Loop through 8 notes
        for i in range(8):
            # Half Steps
            if i == 1 or i == 4 or i == 6:
                scale.append(notes[index])
                index += 1
            # 1.5 Steps
            elif i == 5:
                scale.append(notes[index])
                index += 3
            # Whole Steps
            else:
                scale.append(notes[index])
                index += 2

    # Scale generation for a major pentatonic scale
    if style == 'majorPentatonic':
        # Set first index in the scale to tonic
        index = notesDict[tonic]
        # Loop through 6 notes
        for i in range(6):
            # 1.5 Steps
            if i==2 or i == 4:
                scale.append(notes[index])
                index += 3
            # Whole Steps
            else:
                scale.append(notes[index])
                index += 2

    # Scale generation for a minor pentatonic scale
    if style == 'minorPentatonic':
        # Set first index in the scale to tonic
        index = notesDict[tonic]
        # Loop through 6 notes
        for i in range(6):
            # 1.5 Steps
            if i== 0 or i == 3:
                scale.append(notes[index])
                index += 3
            # Whole Steps
            else:
                scale.append(notes[index])
                index += 2

    return scale

# Generates the list of notes that the random generator will sample from
def generateSampleNotes(tonic , style, tonality):
    # List for sample notes
    sample = []
    # Gets the scale
    scale = generateScale(tonic , style)
    # Ratio is the tonality over 100
    ratio = tonality / 100.0

    # Scales where the chord tones lie on 1 3 5 8 and have 8 notes
    if style == 'major' or style == 'naturalMinor' or style == 'harmonicMinor':
        chordToneNum = (12.5 * ratio) + 12.5
        nonChordToneNum = 25 - chordToneNum
        for i in range(8):
            # adds in chord tones
            if i == 0 or i == 2 or i == 4 or i == 7:
                for k in range(int(chordToneNum)):
                    sample.append(scale[i])
            # adds in non-chord tones
            else:
                for k in range(int(nonChordToneNum)):
                    sample.append(scale[i])

    # Scales that have no chord tones
    if style == 'majorPentatonic' or style == 'minorPentatonic':
        sample = scale

    return sample

# generate sample of note lengths
def generateSampleLengths(energy):
    sample = []
    if energy <= 30:
        for i in range(16 - abs(15 - energy)):
            sample.append('whole')
    if energy <= 60:
        for i in range(30 - abs(30 - energy)):
            sample.append('half')
    if energy <= 70 and energy >= 30:
        for i in range(50 - abs(50 - energy)):
            sample.append('quarter')
    if energy <= 100 and energy >= 40:
        for i in range(30 - abs(70 - energy)):
            sample.append('eighth')
    if energy <= 100 and energy >= 70:
        for i in range(16 - abs(85 - energy)):
            sample.append('16th')
    return sample

# creates a note object with length and note
def createNote(pitch, length):
    tempNote = note.Note(pitch)
    duration1 = duration.Duration(length)
    tempNote.duration = duration1
    return tempNote

# creates a random song to the specifications
def createTune(tonic, style, tonality, energy, tempo, timeSignature, measures):
    songStream = stream.Stream()
    # generate samples
    sampleNotes = generateSampleNotes(tonic , style, tonality)
    sampleLengths = generateSampleLengths(energy)
    # generates song stream
    measureLength = 0
    if timeSignature == '4/4':
        for i in range(measures):
            while measureLength < 4:
                tempNote = note.Note()
                pitch = random.choice(sampleNotes)
                length = random.choice(sampleLengths)
                if measureLength + lengthDict[length] > 4:
                    break
                else:
                    measureLength = measureLength + lengthDict[length]
                    tempNote = createNote(pitch, length)
                    songStream.append(tempNote)
            measureLength = 0
        return songStream
    if timeSignature == '3/4' or timeSignature == '6/8':
        for i in range(measures):
            while measureLength < 3:
                tempNote = note.Note()
                pitch = random.choice(sampleNotes)
                length = random.choice(sampleLengths)
                if measureLength + lengthDict[length] > 3:
                    break
                else:
                    measureLength = measureLength + lengthDict[length]
                    tempNote = createNote(pitch, length)
                    songStream.append(tempNote)
            measureLength = 0
        return songStream

def generateOutputString(number):
    start = "static/"
    start = start + str(number)
    start = start + ".wav"
    return start

def songMidiLocation(number):
    start = "static/"
    start = start + str(number)
    start = start + ".midi"
    return start












