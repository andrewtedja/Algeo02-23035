from audio_load import preprocess_midi, preprocess_wav

# Windowing
def apply_sliding_window(data, window, step): 
    segments = []
    
    for i in range(0, len(data) + 1 - window, step):
        segment = data[i:i + window]
        segments.append(segment)
    return segments;

# Audio Processing
def get_processed_audio(file_path):
    if file_path.endswith('.wav'):
        pitch_data = preprocess_wav(file_path)
    elif file_path.lower().endswith(('.mid', '.midi')):
        pitch_data = preprocess_midi(file_path)
    else:
        raise ValueError("Unsupported file format")

    # Windowing
    segments = apply_sliding_window(pitch_data, 40, 8)
    pitches = []
    for segment in segments:
        for p in segment:
            if p > 0:
                pitches.append(p)
    if len(pitches) == 0:
        print("Pitches list is empty.")
        return pitch_data

    # # Normalisasi Pitch (Opsional)
    # mu = np.mean(pitches)
    # sigma = np.std(pitches)
    
    # if (sigma == 0):
    #     sigma = 1

    # processed_pitch_data = []
    # for p in pitch_data:
    #     if p > 0:
    #         normalized_value = (p - mu) / sigma
    #         processed_pitch_data.append(normalized_value)
    #     else:
    #         processed_pitch_data.append(0)
    return segments