# CSC 475 Project: Chiptune Transcription

## Background and Motivation

Automatic music transcription is challenging because most music audio files contain no details about the notes played, their durations, instruments, etc. This difficulty increases further when considering multiple notes from multiple sources played simultaneously. Chiptune music's clearly defined sound generation and few sound channels make it more reliable to work with versus other forms of music. 

The motivations for this project come from both a practical point of view, as well as a genuine interest in the process. Transcription is generally a tedious, manual process. Once completed, the program could transcribe, analyze, preserve, and arrange chiptune music, allowing us to expand our understanding of the translation of digital signals into music structure.

## Methodology

Though we plan to tackle the various sections of this project as needed, we'll generally prioritize the work that we deem to be the most foundational and the earliest in the program flow. From there, we'll delve more into the advanced aspects. The basics are audio processing and translating gathered data into a MIDI file. The more intermediate focuses are reliably separating 'parts' or 'voices', obtaining accurate tempo and timing, and providing some form of useful transcription. The advanced items will be a more detailed musical structure (key signatures, time signatures, whether notes are considered C\# or Db, etc.), more exact rhythms/beat tracking, and generating conventional sheet music.

**Basics:**

- Process audio  
- Pitch detection  
- Amplitude \+ phase estimation  
- Translate into MIDI

**Expected:**

- Stem Separation  
- Accurate tempo and beat position  
- Useful transcription of music

**Advanced:**

- Details on musical structure  
- Key Signature Estimation  
- Downbeat (time signature) estimation, tempo estimation  
- Generating conventional symbolic sheet music  
- Rhythmic Quantification

### Dataset

The NES Music Database (NESMD) \[1\] provides a nice dataset for us, since it contains many chiptune examples in various formats and a Python package to facilitate working with and analyzing the data. It contains thousands of chiptune tracks stored in MIDI and score formats, which we will use to evaluate the accuracy at various stages of our transcription pipeline. 

In particular, we will work with particular tracks and compare our MIDI output with the NESMD data, using the NESMD files as a ground truth. This workflow will also allow MIDI-to-score translation independent of earlier stages of the pipeline, since we can simply start from the existing MIDI files in NESMD. 

The nesmd package provides support mainly for rendering generated music, but also provides some useful tools for converting to and from various formats. Specifically, it provides tools for converting any of its provided formats to WAV files, which will be the starting point for our pipeline. 

### Pipeline and Tools

The pipeline will start with using nesmdb's midi\_to\_wav function \[1\] to convert a chiptune MIDI file to a WAV file. The goal of this project is to convert this WAV file to a score. It will be implemented in Python using NumPy and SciPy for general numerical processing, mido \[7\] for processing MIDI files, librosa \[3\] for general MIR functionality, music21 \[5\] for working with symbolic scores, and mir\_eval \[4\] to evaluate different components of the produced score (more details in the evaluation section). MuseScore may be used to validate produced scores qualitatively. We will use Git and GitHub for version control.

**Program Flow:**

1. Analyze audio (basic)  
   1. Extract necessary info  
   2. Determine pitch and starting times

2. Separate voices/parts (expected)  
   1. Isolate up to 5 musical parts to be handled individually  
   2. Perhaps start with two parts (voice/melody & instrumental) and work up to 5 parts (melody, harmony 1, harmony 2, bass, percussion?)

3. Detect timing (basic)  
   1. Tempo estimation  
   2. Beat position  
   3. Onset detection vs. beat tracking

4. Create/Store notes and note info (basic)  
   1. Compile gathered data and store into specific notes  
   2. Pitch, start time, duration, and voice/part

5. Refine music details (expected/advanced)  
   1. Use current data to extrapolate additional info  
   2. More specific beat tracking/beat position  
   3. Time signature  
   4. Key of the song \-\> whether notes should be written as C\# vs. Db

6. Generate MIDI file (basic)  
   1. Translate gathered data into MIDI format

7. Generate a score (basic/expected)  
   1. Utilize music21 to create a MusicXML file of the sheet music

8. Evaluate results of score and audio (basic)  
   1. Compare MIDI data of original audio file to the MIDI data we've generated  
   2. Compare the symbolic score we generated to the symbolic score directly generated from the original MIDI file.

### Evaluation Metrics

To evaluate our methods, we will utilize mir\_eval \[4\] and either F1-score or accuracy depending on the subtask. Table 1 shows the evaluation metrics we will use for each subtask. Our reference values will be computed using the test dataset.

Table 1: Evaluation Metrics

| Subtask | Evaluation Metric(s) | Tool |
| :---- | :---- | :---- |
| Beat Tracking / Downbeat Estimation | F-measure | mir\_eval.beat |
| Stem Separation | F1-score | museval \[6\] |
| Pitch Detection | F1-score | mir\_eval.multipitch |
| Onset / Offset Detection | F1-score | mir\_eval.onset |
| Tempo Estimation | Weighted precision | mir\_eval.tempo |
| Symbolic Scoring / Overall Transcription | F1-score | mir\_eval.transcription |
| Key Detection | Weighted score depending on relationship | mir\_eval.key |
| Instrument Identification | Per-instrument accuracy over the test dataset | Self-developed |

## Timeline and Individual Objectives

Table 2 contains the overall timeline we will follow and individual objectives.

Table 2: Timeline and Individual Objectives

| Date | Ari | Rafael | Ryan | Tristan |
| :---- | :---- | :---- | :---- | :---- |
| **Oct 19** | Design Spec | Design Spec | Design Spec | Design Spec |
| **Nov 2 (basic)** | Stem separation | Lit review of existing wav \-\> score tools/pipelines | Generate basic score from MIDI file (tempo and key signature not necessary) | Pitch detection / Onset \+ Offset detection |
| **Nov 16 (expected)** | Beat tracking | Tempo estimation | Generate a more advanced score (e.g., time sig, key) | Downbeat estimation |
| **Nov 30 (advanced)** | Extra score information including "chip" identification | Key detection | Incorporate MIDI \-\> score into pipeline, evaluate accuracy of tool | WAV \-\> MIDI conversion using existing pipeline parts Evaluate accuracy |

## References

\[1\] C. Donahue, H. H. Mao, and J. McAuley, "The NES Music Database: A multi-instrumental dataset with expressive performance attributes," in *ISMIR*, 2018\.  
\[2\] C. Hawthorne *et al.*, "Onsets and Frames: Dual-Objective Piano Transcription," 2018\. \[Online\]. Available: http\://arxiv.org/abs/1710.11153  
\[3\] B. McFee *et al.*, "librosa: Audio and Music Signal Analysis in Python," 01 2015, pp. 18-24. doi: 10.25080/Majora-7b98e3ed-003.  
\[4\] C. Raffel *et al.*, "mir\_eval: A Transparent Implementation of Common MIR Metrics," 10 2014\.  
\[5\] M. S. Cuthbert and C. T. Ariza, "music21: A Toolkit for Computer-Aided Musicology and Symbolic Music Data," Aug. 2010, *International Society for Music Information Retrieval*. \[Online\]. Available: http\://hdl.handle.net/1721.1/84963  
\[6\] F.-R. Stöter and A. Liutkus, *museval 0.3.0*. Zenodo, 2019\. doi: 10.5281/zenodo.3376621.  
\[7\] O. M. Bjørndalen, *Mido: MIDI Objects for Python*. GitHub, 2024\. \[Online\]. Available: https\://github.com/olemb/mido