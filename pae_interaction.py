import json
import numpy as np

def calculate_pae_interaction(pae_matrix, binder_length):
    """
    Compute PAE interaction scores from a given PAE matrix.

    Parameters:
    - pae_matrix (numpy.ndarray): The full PAE matrix.
    - binder_length (int): The length of the binder region.

    Returns:
    - dict: Dictionary containing PAE interaction scores.
    """
    pae_interaction1 = np.mean(pae_matrix[:binder_length, binder_length:])
    pae_interaction2 = np.mean(pae_matrix[binder_length:, :binder_length])
    pae_binder = np.mean(pae_matrix[:binder_length, :binder_length])
    pae_target = np.mean(pae_matrix[binder_length:, binder_length:])
    pae_interaction_total = (pae_interaction1 + pae_interaction2) / 2

    return {
        "pae_binder": pae_binder,
        "pae_target": pae_target,
        "pae_interaction": pae_interaction_total
    }

# Load JSON and extract PAE
def extract_pae_and_calculate(json_path, binder_length):
    """
    Loads a JSON file, extracts the PAE matrix, and computes interaction scores.

    Parameters:
    - json_path (str): Path to the JSON file.
    - binder_length (int): Number of residues in the binder.

    Returns:
    - dict: Computed PAE interaction scores.
    """
    with open(json_path, "r") as f:
        data = json.load(f)

    # Extract the PAE matrix
    pae_matrix = np.array(data["pae"])  # Convert list to NumPy array

    # Compute PAE interaction scores
    return calculate_pae_interaction(pae_matrix, binder_length)


# Example usage
json_file = "/Users/melikeberksoz/Desktop/VEGF_RF_MPNN_trial/2vpf/AF3_complexes/fold_complex_prediction_1/fold_complex_prediction_1_full_data_0.json"  # Replace with actual JSON file path
binder_length = 100  # Adjust based on your structure

pae_scores = extract_pae_and_calculate(json_file, binder_length)
print(pae_scores)
