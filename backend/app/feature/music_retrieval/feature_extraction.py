import numpy as np

# Create Histogram and Normalize
def create_and_normalize_histogram(data, num_bins, val_range = None):
    # Create
    if val_range is None:
        val_range = (0, num_bins)
    histogram, _ = np.histogram(data, bins=num_bins, range=val_range)
    
    # Normalize
    total = np.sum(histogram)
    if total > 0:
        return histogram / total
    else:
        print("Error Warning: Histogram sum 0 atau negatif")
        return histogram

# Extract Features
def extract_features(pitch_data):
    atb_list = []
    rtb_list = []
    ftb_list = []

    for windowed_data in pitch_data:
        # ATB [0, 127]
        bins_atb = 128
        atb_normalized = create_and_normalize_histogram(windowed_data, bins_atb)
        atb_list.append(atb_normalized)

        # RTB [-127, 127] (selisih antara nada-nada berurutan)
        bins_rtb = 255
        rtb_data = [windowed_data[i] - windowed_data[i-1] for i in range(1, len(windowed_data))]
        rtb_normalized = create_and_normalize_histogram(rtb_data, bins_rtb, (-127, 127))
        rtb_list.append(rtb_normalized)
        
        # FTB [-127, 127] (selisih antara nada-nada dengan nada pertama)
        bins_ftb = 255
        if len(windowed_data) > 0:
            ftb_data = [windowed_data[i] - windowed_data[0] for i in range(1, len(windowed_data))]
            ftb_normalized = create_and_normalize_histogram(ftb_data, bins_ftb, (-127, 127))
        else:
            ftb_normalized = np.zeros(bins_ftb, dtype=float)
        ftb_list.append(ftb_normalized)

    # Find avg of each method window histograms
    atb_combined = np.mean(atb_list, axis=0)  
    rtb_combined = np.mean(rtb_list, axis=0)
    ftb_combined = np.mean(ftb_list, axis=0)

    return atb_combined, rtb_combined, ftb_combined