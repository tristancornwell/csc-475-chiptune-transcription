# takes a monophonic wav file and outputs a midi file with the corresponding track

import sys
import os
import numpy as np
import librosa
import mido
from mido import Message, MidiFile, MidiTrack

# chiptune pitch_detection functions for the different NESMDB tracks
# tracks are constrained to notes in [21Hz, 108Hz]
def pitch_detection(x, srate, fmin=librosa.midi_to_hz(21), fmax=librosa.midi_to_hz(108), output_midi = False):
    f0s, voiced_flags, voiced_probs = librosa.pyin(x, sr=srate, fmin=fmin, fmax=fmax)
    # timestamps for sonification
    times = librosa.times_like(f0s, sr=srate)
    f0s = np.nan_to_num(f0s)
    if output_midi:
        f0s[f0s != 0] = np.rint(librosa.hz_to_midi(f0s[f0s != 0])) # round because midi is int only
    return f0s, times


def pitches_to_midi_track(midi_pitches, times, onsets, mid, tempo=500000) -> MidiTrack:
    track = MidiTrack()
    # default tempo is 500000 = 120 BPM
    track.append(mido.MetaMessage('set_tempo', tempo=tempo, time=0))

    # manual conversion to ticks
    ticks_per_beat = mid.ticks_per_beat
    bpm = mido.tempo2bpm(tempo)
    def sec_to_ticks(sec):
        beats = sec * (bpm / 60.0)
        return int(round(beats * ticks_per_beat))

    # avoid clipping the end of the track
    onsets = np.unique(np.concatenate(([0.0], onsets, [times[-1]])))
    
    last_event_time = 0.0
    for i in range(len(onsets) - 1):
        start_time = onsets[i]
        end_time = onsets[i+1]
        # sample the pitch closest to the middle of onset interval
        midpoint = (start_time + end_time) / 2.0
        pitch = int(midi_pitches[np.abs(times - midpoint).argmin()])
        # only add note if it has a pitch
        if pitch > 0:
            track.append(Message('note_on', note=pitch, velocity=10, time=sec_to_ticks(start_time - last_event_time)))
            track.append(Message('note_off', note=pitch, velocity=0, time=sec_to_ticks(end_time - start_time)))
            # update tracker
            last_event_time = end_time
    return track

def main() -> int:
    # error check early so no wait
    if not sys.argv[-1].endswith(".mid"):
        print("Please provide an output filename ending in .mid after the input filenames")
        return 0
    for input_file in sys.argv[1:-1]:
        if not input_file.endswith(".wav"):
            print("Please input only .wav files")
            return 0
        
    # do actual work here
    midi_output = MidiFile()
    for input_file in sys.argv[1:-1]:
        # load file
        (wav_input,srate) = librosa.load(input_file)
        # get midi pitches and timing
        midi_pitches, pitch_times = pitch_detection(wav_input, srate, output_midi=True)
        # get onsets
        est_onsets = librosa.onset.onset_detect(y=wav_input, sr=srate, units='time')
        # use onsets and pitches to create track and append it
        new_track = pitches_to_midi_track(midi_pitches, pitch_times, est_onsets, midi_output)
        midi_output.tracks.append(new_track)
        
    # output new midi file
    os.makedirs(os.path.dirname("generated_midis/"), exist_ok=True) # make new dir if needed
    midi_output.save(filename=f"generated_midis/{sys.argv[-1]}")
    print(f"MIDI file saved successfully as '{sys.argv[-1]}'")
    return 0
    
if __name__ == '__main__':
    sys.exit(main())
