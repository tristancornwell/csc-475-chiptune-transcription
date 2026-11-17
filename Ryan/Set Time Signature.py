import mido


midi = mido.MidiFile("Duck Tales.mid")

#Remove all existing time-signature events for each track
for track in midi.tracks:
    track[:] = [msg for msg in track if not (msg.is_meta and msg.type == "time_signature")]

#Insert 15/8 at the beginning of the metadata track, specifically ofr the purposes of testing DuckTales
midi.tracks[0].insert(0, mido.MetaMessage("time_signature", numerator=15,denominator=8, time=0))

midi.save("Duck Tales.mid")
