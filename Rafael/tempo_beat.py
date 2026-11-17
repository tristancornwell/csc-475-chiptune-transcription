import librosa

DUCK_TALES = "data/093_DuckTales_06_07TheMoon.wav"

def get_tempo(y, sr, onset_envelope):
    """
    Get the tempo of an audio file.

    Parameters:
        y (np.ndarray[float]): Audio time series.
        sr (int): Sampling rate of `y`.
        onset_envelope (np.ndarray[float]): (Optional) Pre-computed onset envelope of the audio signal.

    Returns:
        out (np.ndarray[float]): Estimated tempos in beats per minute (BPM).
    """
    tempo = librosa.feature.tempo(y=y, sr=sr, onset_envelope=onset_envelope, aggregate=None)
    return tempo

def get_beats(y, sr, onset_envelope):
    """
    Get the beats of an audio file.

    Parameters:
        y (np.ndarray[float]): Audio time series.
        sr (int): Sampling rate of `y`.
        onset_envelope (np.ndarray[float]): (Optional) Pre-computed onset envelope of the audio signal.

    Returns:
        out (np.ndarray[float]): Estimated beat frames.
    """
    _, beat_frames = librosa.beat.beat_track(y=y, sr=sr, onset_envelope=onset_envelope)
    return beat_frames  

def main():
    y, sr = librosa.load(DUCK_TALES)
    onset_env = librosa.onset.onset_strength(y=y, sr=sr)
    tempo = get_tempo(y, sr, onset_env)
    beat_frames = get_beats(y, sr, onset_env)

    print(f"Estimated tempos: {tempo}")
    print(f"Estimated beat frames: {beat_frames}")

if __name__ == "__main__":
    main()