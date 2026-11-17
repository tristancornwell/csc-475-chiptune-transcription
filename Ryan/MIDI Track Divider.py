from pathlib import Path
from mido import MidiFile, MidiTrack

#Loads the original MIDI file
midi = MidiFile("Duck Tales.mid")

#Marks the output folder for generated MIDI files
output_dir = Path("split_midis")
output_dir.mkdir(exist_ok=True)

#First track is at index 0
base_index = 0

#Display all existing tracks in the midi file
for i, track in enumerate(midi.tracks):
    print(f"{i}: {track.name}")

#Generate a different MIDI for each track, assuming that the first track (holding
# broader / grand scale events) is required, it is paired up with each other track
for i, track in enumerate(midi.tracks):
    if i == base_index:
        continue

    #Prepares a new MidiFile object for use
    new_midi = MidiFile(type=1,ticks_per_beat=midi.ticks_per_beat)

    #Copy the essential track holding larger-scale events
    new_midi.tracks.append(MidiTrack(msg.copy() for msg in midi.tracks[base_index]))

    #Copy the additional track
    new_midi.tracks.append(MidiTrack(msg.copy() for msg in track))

    #Save the tracks under individual names that don't conflict.
    name = track.name or f"track_{i}"
    safe_name = "".join(c if c.isalnum() or c in "-_" else "_" for c in name)

    #Re-sets filename to the new name to be used in saving the tracks as individual MIDIs
    filename = output_dir / f"{i}_{safe_name}.mid"
    new_midi.save(filename)

    print(f"Created: {filename}")

print("Finished!")