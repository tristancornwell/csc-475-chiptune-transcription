#Nov. 9th, 2026
#Ryan N.
#V01016168


import librosa
import numpy as np
import scipy as sp
import mir_eval
import music21 as m21
import mido
from music21.audioSearch import quarterLengthEstimation
from music21 import *
from collections import defaultdict
import copy

#Changes the provided MIDI file into a Music21 Score representation,
#Identifying down to 64th notes
def midi_to_score(midi):
    return m21.converter.parse(midi, quantizePost=True, quarterLengthDivisors=(4, 8, 16, 32))


#Set the filename for the target MIDI file, use mido
#To create a MidiFile object for easy access
#Hand the MidiFile off to become a Music21 score (and set the 'Too Fast' flag to false)
filename = "Kirby's Adventure.mid"
midi = mido.MidiFile(filename)
score = midi_to_score(filename)
#too_fast = False



#This function investigates a given measure of a Music21 score, and checks to see
#Whether the measure contains many unnecessary notes in quick succession, that can
#potentially be combined on the sheet music into a more readable form
def analyze_measure(measure, min_dur=0.125):

    #Load events with each note and rest in the given measure
    events = list(measure.recurse().notesAndRests)

    #Load with all notes shorter than the minimum duration provided
    notes = [n for n in events if isinstance(n, (note.Note, chord.Chord)) and float(n.duration.quarterLength) < min_dur]

    #Load with all rests shorter than the minimum duration provided
    rests = [r for r in events if isinstance(r, note.Rest) and float(r.duration.quarterLength) < min_dur]

    #Total number of rests and notes in the measure
    total = len(events)

    #Return the measure number, total notes and rest vs. short notes and short rests, and a ratio of how many notes in the measure are
    #quicker/closer than we'd like them to be.
    return {"measure": measure.number, "total_events": total, "short_notes": len(notes), "short_rests": len(rests), "complexity_ratio":
        ((len(notes) + len(rests)) / total if total else 0)}




#Takes a list of notes, and compares them to a given note duration
#That we'd like to stay under for practical playing purposes (per sheet music)
#Not necessarily oscillation, but notes in rapid succession
def detect_oscillation(notes, min_duration=0.25):

    #Return no notes in quick succession, if there are less than 4 notes in the measure
    if len(notes) < 4:
        return False

    #Return no notes in quick succession, if the given notes aren't note objects (rests or chords)
    if not all(isinstance(n, note.Note) for n in notes):
        return False

    #Loads durs with a float representation of the duration for each note in notes
    durs = [float(n.duration.quarterLength)for n in notes]

    #Sets is_fast to true if all the given durations are less than or equal to our
    #desired minimum
    is_fast = all(d <= min_duration for d in durs)

    return is_fast



#Takes a measure, and finds the specific portions that contain notes in rapid succession
def find_oscillations(measure, window_size=8, min_size=4):

    #Sets notes to contain each note element within the measure
    notes = list(measure.recurse().getElementsByClass(note.Note))

    #Declare too_fast, for updating if we determine there are notes too fast to be player
    #And thus, to be combined on the sheet music
    global too_fast

    #Prepare list of oscillations and set i to 0 for use in a loop
    oscillations = []
    i = 0

    #Loop until we've considered every note, and initialize a found flag to false
    while i < len(notes):
        found = False

        #Loop through a window of 8 notes, down to a frame of 4 notes
        for win in range(min(window_size, len(notes) - i), min_size - 1, -1):

            #Load with a sub-list of notes
            sect = notes[i:i + win]

            #If our detect oscillation function returns true, sets
            #our too fast flag, adds the section to the list of
            #'oscillations' in quick succession, increments the length of notes
            #considered by the window length, and sets our found flag, and breaks the loop
            if detect_oscillation(sect):
                too_fast = True
                oscillations.append(sect)
                i += win
                found = True
                break

        #If we haven't found a section that's too fast, we proceed on to the next note.
        if not found:
            i += 1

    #We return any oscillations we've found
    return oscillations




#Takes a given list of notes, and returns the dominant pitch among them
def dominant_pitch(notes):

    #Initializes a dict to count amount of each note
    note_durs = defaultdict(float)

    #Loop through each note
    for n in notes:

        #If n is a Note element (not a chord or a rest), adds the
        # duration of the note to the dictionary
        if n.isNote:
            note_durs[n.pitch.midi] += float(n.duration.quarterLength)


    #Returns None of there's no note more dominant than another
    if not note_durs:
        return None

    #Return the most frequently played note in the list
    return max(note_durs, key=note_durs.get)







#Replace a detected oscillation section with a shorter simpler notation
# marking the area as having 'vibrato'
def make_simplified_note(notes, start, end, pitch_midi):

    #Set the combined notes to be of the dominant pitch provided
    combined = note.Note(pitch_midi)

    #Set the duration of the replacement note to cover the span of the 'oscillation'
    combined.duration.quarterLength = end - start

    #Give the note the quality of being marked with having 'vibrato'
    combined.expressions.append(expressions.TextExpression("vibrato"))

    #Return the combined/dominant note coverage
    return combined






#Replace any rapid oscillations in a measure with the dominant note among them
def simplify_measure(measure):

    #Find the rapid note areas of the given measure
    oscillations = find_oscillations(measure)

    #For each set of oscillation notes, find the dominant pitch among them, or proceed if no
    #dominant pitch is found
    for notes in oscillations:
        pitch = dominant_pitch(notes)

        if pitch is None:
            continue

        #Find the beginning and end of the section oscillation
        start = notes[0].getOffsetInHierarchy(measure)
        end = max(n.getOffsetInHierarchy(measure) + float(n.duration.quarterLength) for n in notes)

        #Create the filler note to replace the oscillation found
        filler = make_simplified_note(notes, start, end, pitch)

        #Remove each note from the original oscillation
        for n in notes:
            measure.remove(n, recurse=True)

        #Insert the filler note at the oscillation's start position
        measure.insert(start, filler)

    #Return the measure with any relevant replacements done
    return measure









#Create a deepcopy of the score object to freely test and edit without altering the original score.
simplified_score = copy.deepcopy(score)

#Test section, utilized to print out the measure details before and after their simplification
for part in simplified_score.parts:
    for measure in part.getElementsByClass(m21.stream.Measure):

        before = analyze_measure(measure)

        simplify_measure(measure)

        after = analyze_measure(measure)

        print(f"Measure {measure.number}")
        print("Before:", before)
        print("After:", after)






#The focus here was to clean and consolidate rests in the ultimate XML file
# it has only been partially successful
#    max_gap: Maximum gap to absorb, in quarter lengths.
#             0.125 = 32nd note
#             0.25  = 16th note
#             0.5   = 8th note
#Returns a new - cleaned - score
def clean_midi_rests(score, max_gap=0.125, extend_notes=True):

    #Copy the score, so as to not alter the original data
    cleaned = copy.deepcopy(score)

    #Set to a tiny value to handle potential floating point errors
    epsilon = 1e-7

    #Loop through each part in the cleaned score
    for part in cleaned.parts:

        #Loop through each measure element within the current part
        for measure in part.getElementsByClass(stream.Measure):

            #Process each track separately
            track = list(measure.getElementsByClass(stream.Voice))
            containers = track if track else [measure]

            #Loop through each object in the given track or measure
            for container in containers:

                #Remove all existing rests
                for rest in list(container.getElementsByClass(note.Rest)):
                    container.remove(rest)

                #Collect the note and chord events chronologically
                events = sorted(list(container.getElementsByClass((note.Note, chord.Chord))),key=lambda e: e.offset)

                #Skip if no note/chord events
                if not events:
                    continue

                #Extend the notes across any small gaps
                if extend_notes:

                    #Loops through consecutive pairs of notes
                    for cur, following in zip(events, events[1:]):

                        #Set the end of the current note/chord to span its duration from the starting point (offset)
                        cur_end = (cur.offset + cur.duration.quarterLength)

                        #Sets the space between notes as the offset of the subsequent note, minus the ending point of
                        #the current note
                        space = following.offset - cur_end

                        #Determines if the space between notes is small enough to safely remove
                        #Must be meaningfully greater than zero, and must be smaller than the
                        #minimum space being allowed.
                        if epsilon < space <= max_gap + epsilon:
                            cur.duration.quarterLength += space

                #Fill the space between notes with appropriate rests
                container.makeRests(fillGaps=True,timeRangeFromBarDuration=True,inPlace=True)

    #Return the cleaned score
    return cleaned




#Cleans the unnecessary rests out of the score
cleaned = clean_midi_rests(score, max_gap=0.125, extend_notes=True)

#Write an XML of the cleaned file
cleaned.write("musicxml", fp="cleaned_score.musicxml")

#Write an XML of the score file
score.write('musicxml', fp='Kirby!.xml')






