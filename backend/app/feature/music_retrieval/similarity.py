import numpy as np


# Cosine Similarity
def get_cosine_similarity(vector_A, vector_B):
    dot_product = np.dot(vector_A, vector_B)
    norm_vector_A = np.linalg.norm(vector_A)
    norm_vector_B = np.linalg.norm(vector_B)
    norm_product = norm_vector_A * norm_vector_B

    # check handle division by zero
    if norm_product == 0:
        return 0

    cosine_similarity = dot_product / norm_product
    return cosine_similarity

# def calculate_similarity(query_pitch_data, dataset_pitch_data):
#     atb_query, rtb_query, ftb_query = extract_features(query_pitch_data)
#     atb_dataset, rtb_dataset, ftb_dataset = extract_features(dataset_pitch_data)

#     # Hitung cosine similarity ATB, FTB, FTB terpisah
#     similarity_atb = get_cosine_similarity(atb_query, atb_dataset)
#     similarity_rtb = get_cosine_similarity(rtb_query, rtb_dataset)
#     similarity_ftb = get_cosine_similarity(ftb_query, ftb_dataset)

#     # Rata-rata cosine similarity
#     avg_similarity = (similarity_atb + similarity_rtb + similarity_ftb) / 3
#     return avg_similarity