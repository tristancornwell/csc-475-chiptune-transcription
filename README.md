# csc-475-chiptune-transcription

## Background and Motivation


## Methodology

### Dataset


### Pipeline and Tools
- start with wav file of nesmdb midi file using midi_to_wav (https://github.com/chrisdonahue/nesmdb#midi)
  - pitch detection (basic)
  - amplitude + phase estimation (basic)
  - stem separation (expected)
  - beat tracking (expected)
  - key signature estimation (advanced)
  - downbeat (time signature) estimation (advanced)
  - rhythmic quantification (advanced)
- end up with midi file
- stretch to more conventional score ("modern western format"?)

some tools:
- music21
- librosa
- mido
- other tools for particular pipeline steps

### Evaluation Metrics
- compare our midi to original nesmdb midi
- quantitative and qualitative

## Timeline
Oct 19: Design Spec
Nov 2: Stem Separation, Granular Data Selection, Evaluation Metrics, Midi to .wav
Nov 16: 

1. Stem separation
2. Steps required for midi
3. Extra information needed for score format

### Individual  Objectives
#### Ari
#### Raf
#### Ryan
#### Tristan


## References
- background and motivation
- some defense of evaluation methods
- 
