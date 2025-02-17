import json
import os
from Bio import SeqIO

# Define base directory dynamically (change this to match your actual file location)
base_dir = os.path.expanduser("/Users/melikeberksoz/Desktop/VEGF_binder_trial/Bindcraft/VEGF")

# Define correct file paths
design_fasta = os.path.join(base_dir, "design.fasta")
target_fasta = os.path.join(base_dir, "rcsb_pdb_2VPF.fasta")
output_json = os.path.join(base_dir, "output.json")


def create_alphafold3_json(design_fasta, target_fasta, output_json):
    """
    Reads the first 4 sequences from a design FASTA file and pairs them with a single target sequence
    to create a batch JSON file for AlphaFold 3 complex prediction.

    Args:
    - design_fasta (str): Path to the FASTA file containing design sequences.
    - target_fasta (str): Path to the FASTA file containing the target sequence.
    - output_json (str): Path to save the generated JSON file.

    Returns:
    - Saves JSON to output_json file.
    """

    # Check if files exist before proceeding
    if not os.path.exists(design_fasta):
        raise FileNotFoundError(f"❌ ERROR: Design FASTA file not found: {design_fasta}")
    if not os.path.exists(target_fasta):
        raise FileNotFoundError(f"❌ ERROR: Target FASTA file not found: {target_fasta}")

    print(f"✅ Found Design FASTA: {design_fasta}")
    print(f"✅ Found Target FASTA: {target_fasta}")

    # Read the first 4 sequences from the design FASTA file
    design_sequences = []
    for record in SeqIO.parse(design_fasta, "fasta"):
        design_sequences.append(str(record.seq))
        if len(design_sequences) == 4:  # Take only the first 4 sequences
            break

    if len(design_sequences) < 4:
        print(f"⚠️ WARNING: Only {len(design_sequences)} sequences found in {design_fasta}. Expected 4.")

    # Read the target sequence (assume only 1 sequence in the target FASTA file)
    target_records = list(SeqIO.parse(target_fasta, "fasta"))
    if len(target_records) == 0:
        raise ValueError("❌ ERROR: The target FASTA file is empty or incorrectly formatted.")
    
    target_sequence = str(target_records[0].seq)  # Take the first sequence

    # Create JSON structure for complex predictions
    complexes = []
    for i, design_seq in enumerate(design_sequences):
        complex_entry = {
            "name": f"Complex Prediction {i+1}",
            "modelSeeds": [],
            "sequences": [
                {
                    "proteinChain": {
                        "sequence": design_seq,
                        "count": 1  # Assuming each design chain occurs once
                    }
                },
                {
                    "proteinChain": {
                        "sequence": target_sequence,
                        "count": 1  # Target sequence occurs once in the complex
                    }
                }
            ],
            "dialect": "alphafoldserver",
            "version": 1
        }
        complexes.append(complex_entry)

    # Save JSON output
    with open(output_json, "w") as json_file:
        json.dump(complexes, json_file, indent=4)

    print(f"✅ AlphaFold 3 JSON file successfully created: {output_json}")

# Run the script
create_alphafold3_json(design_fasta, target_fasta, output_json)


    