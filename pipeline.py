from agents.damage_agent import analyze_damage
from agents.search_agent import find_similar
from agents.guidance_agent import generate_guidance
from agents.coordinator import save_outputs

def run_pipeline(image_path):
    print("Step 1: Analyzing damage...")
    damage_report = analyze_damage(image_path)

    print("Step 2: Searching for similar references...")
    references,ref_meta= find_similar(image_path, damage_report)

    print("Step 3: Generating reconstruction guidance...")
    guidance = generate_guidance(damage_report, references)

    print("Step 4: Saving outputs...")
    save_outputs(damage_report, references, guidance)

    print("Done. Check /outputs folder.")
    return guidance