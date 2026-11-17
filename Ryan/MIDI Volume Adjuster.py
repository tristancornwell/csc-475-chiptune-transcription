


from pathlib import Path
import mido


def fix_nes_midi(input_file):

    midi = mido.MidiFile(input_file)

    #Generate output filename
    path = Path(input_file)
    output_file = path.with_name(path.stem + "_fixed.mid")

    #Ideal velocity targets based off what Google says
    VELOCITY_RANGES = {"p1": (70, 105),"p2": (85, 100),"tr": (90, 90),"no": (75, 95)}

    DEFAULT_RANGE = (75, 105)

    #Approximate NES percussion sounds
    NOISE_MAPPING = {6:42, 14:38, 15:36}


    #Adjusts the velocity of the various tracks
    def scale_velocity(value, old_min, old_max,
                       new_min, new_max):

        #Checks if the notes have different velocities, and returns a midpoint
        if old_min == old_max:
            return (new_min + new_max) // 2

        #Sets normalized to represent the note's relationship to its volume in the original notes
        normalized = ((value - old_min) / (old_max - old_min))

        #Returns velocity adjustment
        return max(1, min(127, round(new_min + normalized * (new_max - new_min))))

    #Loops through each track
    for index, track in enumerate(midi.tracks):

        name = track.name.lower().strip()
        target_min, target_max = VELOCITY_RANGES.get(name, DEFAULT_RANGE)
        velocities = [msg.velocity for msg in track if msg.type == "note_on" and msg.velocity > 0]

        if not velocities:
            continue

        old_min = min(velocities)
        old_max = max(velocities)

        #Identify NES percussion track
        is_noise = name in ("no", "noise")

        for msg in track:

            #Normalize note velocities
            if msg.type == "note_on" and msg.velocity > 0:
                msg.velocity = scale_velocity(msg.velocity,old_min, old_max,target_min, target_max)

            #Map NES noise pitches to GM percussion
            if is_noise and msg.type in ("note_on", "note_off"):
                msg.note = NOISE_MAPPING.get(msg.note, msg.note)

                #GM percussion channel
                msg.channel = 9

            #Fix volume and expression
            if msg.type == "control_change":

                if msg.control == 7:
                    msg.value = 100

                elif msg.control == 11:
                    msg.value = 127

        print(f"{name or f'Track {index}'}: "f"{len(velocities)} notes, "f"velocity {old_min}-{old_max} "f"-> {target_min}-{target_max}")

    midi.save(output_file)

    print(f"\nSaved: {output_file}")
    return str(output_file)


#Example
fix_nes_midi("Kirby's Adventure.mid")
fix_nes_midi("Yoshi's Cookie.mid")
