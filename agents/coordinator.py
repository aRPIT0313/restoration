import json
import os
from datetime import datetime
import shutil

def save_outputs(damage_report, references, guidance):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_dir = f"outputs/restoration_{timestamp}"
    os.makedirs(out_dir, exist_ok=True)

    # save damage report
    with open(f"{out_dir}/damage_report.json", "w") as f:
        json.dump(damage_report, f, indent=2)

    # copy reference images
    ref_dir = f"{out_dir}/references"
    os.makedirs(ref_dir, exist_ok=True)
    for i, ref in enumerate(references):
        shutil.copy(ref, f"{ref_dir}/ref_{i+1}.jpg")

    # save guidance
    with open(f"{out_dir}/reconstruction_guide.txt", "w") as f:
        f.write(guidance)

    print(f"All outputs saved to {out_dir}")