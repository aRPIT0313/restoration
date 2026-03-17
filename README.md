# 🏛️ Murti Restoration Assistant

> A multi-agent AI-assisted system for digital restoration of broken cultural artifacts from a single image using damage detection, web-based reference retrieval, and guided 3D reconstruction.

![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat-square&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.41.1-red?style=flat-square&logo=streamlit)
![Gemini](https://img.shields.io/badge/Gemini-Vision-green?style=flat-square&logo=google)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)

---

## 📌 Overview

Broken murtis (Hindu idols and cultural statues) are a common challenge in heritage preservation. Traditional restoration is time-consuming, requires expert knowledge, and lacks structured guidance.

This project introduces an **AI-powered multi-agent pipeline** that:
- Automatically detects damaged and missing parts from a single photo
- Retrieves visually similar intact murti references from the web
- Generates step-by-step Blender reconstruction guidance for 3D artists
- Feeds into a 3D reconstruction workflow using Rodin HyperD and Blender

This transforms a manual, unstructured process into a **semi-automated, AI-guided digital restoration pipeline**.

---

## 🎯 Key Features

- **🔍 AI Damage Detection** — Gemini Vision analyzes the uploaded image and identifies broken regions, missing parts, damage severity, murti type, and reconstruction priority
- **🖼️ Automatic Reference Retrieval** — Searches DuckDuckGo and Wikimedia Commons for visually similar intact murtis — no manual searching needed
- **🔧 Blender Reconstruction Guidance** — AI generates practical, step-by-step geometry hints, symmetry tips, and Blender tool suggestions specific to the damage found
- **📋 Structured Damage Report** — Outputs a clean JSON report with all damage information
- **📥 Downloadable Guidance** — Export the reconstruction guide as a `.txt` file
- **📱 Responsive UI** — Works on desktop, tablet, and mobile

---

## 🧠 How It Works
```
User uploads broken murti image
            ↓
    [Agent 1] Damage Analysis
    Gemini Vision detects broken regions,
    missing parts, severity, murti type
            ↓
    [Agent 2] Reference Retrieval
    DuckDuckGo + Wikimedia search for
    similar intact murti references
            ↓
    [Agent 3] Reconstruction Guidance
    Gemini generates Blender-specific
    restoration instructions
            ↓
    [Agent 4] Coordinator
    Saves damage report, references,
    and guidance to outputs folder
            ↓
    Artist uses guidance in Blender
    + Rodin HyperD for 3D mesh
```

---

## 🛠️ Tech Stack

| Layer | Tool | Purpose |
|---|---|---|
| Vision AI | Gemini Vision | Damage detection and guidance generation |
| Image Search | DuckDuckGo | Primary reference image search |
| Image Search | Wikimedia Commons | Fallback reference image search |
| UI | Streamlit | Web interface |
| Image Processing | Pillow | Image handling |
| 3D Mesh | Rodin HyperD | Base 3D model generation |
| 3D Reconstruction | Blender | Manual AI-guided repair |

---

## 📁 Project Structure
```
murti-restoration/
├── agents/
│   ├── __init__.py
│   ├── damage_agent.py        # Gemini Vision damage detection
│   ├── search_agent.py        # DuckDuckGo + Wikimedia search
│   ├── guidance_agent.py      # Blender reconstruction guidance
│   └── coordinator.py         # Pipeline orchestration + output saving
├── outputs/                   # Auto-generated results (gitignored)
├── app.py                     # Streamlit UI
├── pipeline.py                # Main pipeline runner
├── requirements.txt
├── .python-version
├── .env                       # Your API keys (gitignored)
├── .env.example               # Template for API keys
├── .gitignore
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.11
- Gemini API key (free) from [aistudio.google.com](https://aistudio.google.com)

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/murti-restoration.git
cd murti-restoration
```

### 2. Create virtual environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac / Linux
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up API keys
```bash
cp .env.example .env
```
Open `.env` and add your Gemini API key:
```
GEMINI_API_KEY=your_gemini_api_key_here
```

### 5. Run the app
```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501`

---

## 🔑 API Keys

| Key | Where to Get | Cost |
|---|---|---|
| Gemini API Key | [aistudio.google.com](https://aistudio.google.com) | Free — 1500 req/day |

No other API keys required. Reference image search uses DuckDuckGo and Wikimedia Commons which are completely free with no authentication.

---

## 📸 Usage

1. Open the app in your browser
2. Upload a photo of a broken murti (JPG or PNG)
3. Click **Analyze & Generate Guidance**
4. Wait 15–20 seconds for the pipeline to run
5. View results across three tabs:
   - **📋 Damage Report** — AI-detected damage with severity and priority
   - **🖼️ References** — Similar intact murtis found online
   - **🔧 Blender Guidance** — Step-by-step reconstruction instructions
6. Download the guidance as a `.txt` file
7. Use the guidance and references in Blender to reconstruct the missing parts
8. Import base mesh from Rodin HyperD into Blender

---

## 🌐 Live Demo

🔗 [murti-restoration.streamlit.app](https://murti-restoration.streamlit.app)

---

## 🗺️ Pipeline in Detail

### Agent 1 — Damage Analysis
Uses Gemini Vision to analyze the uploaded image and returns a structured JSON containing damaged regions, missing parts, damage severity (low/medium/high), murti type, pose description, and reconstruction priority order.

### Agent 2 — Reference Retrieval
Builds a targeted search query from the damage report and searches DuckDuckGo Images first. Falls back to Wikimedia Commons if DuckDuckGo is unavailable. Downloads the top 3 matching reference images locally for use in guidance generation.

### Agent 3 — Reconstruction Guidance
Feeds the damage report and downloaded reference images back into Gemini Vision to generate detailed Blender reconstruction guidance including geometry hints, proportions, symmetry tips, and specific Blender tools and modifiers to use.

### Agent 4 — Coordinator
Orchestrates the full pipeline, handles errors gracefully, saves all outputs (damage report JSON, reference images, guidance text) to a timestamped folder inside `/outputs`.

---

## 🔮 Future Scope

- [ ] Support for multiple image inputs (multi-angle reconstruction)
- [ ] Automatic Blender Python script generation
- [ ] Integration with Unity for AR/VR visualization
- [ ] Fine-tuned damage detection model on murti dataset
- [ ] 3D part suggestion using generative AI
- [ ] Community database of murti references

---

## 🤝 Contributing

Pull requests are welcome. For major changes please open an issue first to discuss what you would like to change.

---


## 🙏 Acknowledgements

- [Google Gemini](https://aistudio.google.com) for Vision AI
- [Wikimedia Commons](https://commons.wikimedia.org) for open reference images
- [Rodin HyperD](https://hyper3d.ai) for 3D mesh generation
- [Streamlit](https://streamlit.io) for the web framework

---

<p align="center">
Made with ❤️ for Heritage Preservation
</p>
