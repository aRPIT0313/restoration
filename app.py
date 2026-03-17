import streamlit as st
from PIL import Image
import tempfile
import os
import json
import gc

st.set_page_config(
    page_title="Murti Restoration Assistant",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* ── fonts & base ── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* ── page background ── */
    .stApp {
        background-color: #0f0f0f;
        color: #f0f0f0;
    }

    /* ── main container ── */
    .block-container {
        padding: 2rem 2rem 2rem 2rem;
        max-width: 1200px;
        margin: auto;
    }

    /* ── hide streamlit defaults ── */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* ── hero banner ── */
    .hero {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        border-radius: 16px;
        padding: 2.5rem 2rem;
        text-align: center;
        margin-bottom: 2rem;
        border: 1px solid #ffffff15;
    }
    .hero h1 {
        font-size: clamp(1.8rem, 4vw, 3rem);
        font-weight: 700;
        color: #ffffff;
        margin: 0 0 0.5rem 0;
    }
    .hero p {
        font-size: clamp(0.9rem, 2vw, 1.1rem);
        color: #a0aec0;
        margin: 0;
    }

    /* ── cards ── */
    .card {
        background: #1a1a1a;
        border: 1px solid #2a2a2a;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }

    /* ── step badges ── */
    .steps-row {
        display: flex;
        gap: 1rem;
        flex-wrap: wrap;
        margin-bottom: 2rem;
    }
    .step-item {
        flex: 1;
        min-width: 140px;
        background: #1a1a1a;
        border: 1px solid #2a2a2a;
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
    }
    .step-icon {
        font-size: 1.8rem;
        margin-bottom: 0.4rem;
    }
    .step-title {
        font-size: 0.85rem;
        font-weight: 600;
        color: #e2e8f0;
        margin-bottom: 0.2rem;
    }
    .step-desc {
        font-size: 0.75rem;
        color: #718096;
    }

    /* ── upload zone ── */
    .uploadedFile {
        background: #1a1a1a !important;
        border: 2px dashed #4a5568 !important;
        border-radius: 12px !important;
    }
    [data-testid="stFileUploadDropzone"] {
        background: #1a1a1a;
        border: 2px dashed #4a5568;
        border-radius: 12px;
        padding: 2rem;
    }

    /* ── buttons ── */
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 1.5rem;
        font-size: 1rem;
        font-weight: 600;
        cursor: pointer;
        transition: opacity 0.2s;
    }
    .stButton > button:hover {
        opacity: 0.9;
        color: white;
        border: none;
    }

    /* ── download button ── */
    .stDownloadButton > button {
        width: 100%;
        background: #1a1a1a;
        color: #667eea;
        border: 1px solid #667eea;
        border-radius: 10px;
        padding: 0.6rem 1.5rem;
        font-weight: 600;
    }

    /* ── tabs ── */
    .stTabs [data-baseweb="tab-list"] {
        background: #1a1a1a;
        border-radius: 10px;
        padding: 0.3rem;
        gap: 0.3rem;
        overflow-x: auto;
        flex-wrap: nowrap;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        color: #a0aec0;
        font-weight: 500;
        white-space: nowrap;
        padding: 0.5rem 1rem;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea, #764ba2) !important;
        color: white !important;
    }

    /* ── metrics ── */
    [data-testid="metric-container"] {
        background: #1a1a1a;
        border: 1px solid #2a2a2a;
        border-radius: 10px;
        padding: 1rem;
    }
    [data-testid="metric-container"] label {
        color: #a0aec0 !important;
        font-size: 0.8rem !important;
    }
    [data-testid="metric-container"] [data-testid="stMetricValue"] {
        color: #f0f0f0 !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
    }

    /* ── progress bar ── */
    .stProgress > div > div {
        background: linear-gradient(135deg, #667eea, #764ba2);
        border-radius: 10px;
    }

    /* ── reference image card ── */
    .ref-card {
        background: #1a1a1a;
        border: 1px solid #2a2a2a;
        border-radius: 10px;
        padding: 0.75rem;
        margin-bottom: 1rem;
        text-align: center;
    }
    .ref-title {
        font-size: 0.78rem;
        color: #a0aec0;
        margin-top: 0.5rem;
        word-break: break-word;
    }

    /* ── damage tag ── */
    .tag {
        display: inline-block;
        background: #2d2d2d;
        border: 1px solid #3a3a3a;
        border-radius: 20px;
        padding: 0.25rem 0.75rem;
        font-size: 0.8rem;
        color: #e2e8f0;
        margin: 0.2rem;
    }

    /* ── sidebar ── */
    [data-testid="stSidebar"] {
        background: #111111;
        border-right: 1px solid #2a2a2a;
    }
    [data-testid="stSidebar"] * {
        color: #a0aec0;
    }

    /* ── expander ── */
    .streamlit-expanderHeader {
        background: #1a1a1a !important;
        border-radius: 8px !important;
        color: #a0aec0 !important;
    }

    /* ── responsive: tablet ── */
    @media (max-width: 768px) {
        .block-container {
            padding: 1rem;
        }
        .hero {
            padding: 1.5rem 1rem;
        }
        .step-item {
            min-width: 100px;
        }
    }

    /* ── responsive: phone ── */
    @media (max-width: 480px) {
        .steps-row {
            flex-direction: column;
        }
        .step-item {
            min-width: unset;
        }
    }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🏛️ About")
    st.markdown("""
    An AI-powered pipeline for digital restoration
    of broken murtis using damage detection,
    web-based reference retrieval, and guided
    3D reconstruction in Blender.
    """)
    st.divider()
    st.markdown("#### 🛠️ Tech Stack")
    st.markdown("- **Gemini Vision** — damage analysis")
    st.markdown("- **DuckDuckGo / Wikimedia** — references")
    st.markdown("- **Streamlit** — UI")
    st.markdown("- **Blender** — 3D reconstruction")
    st.markdown("- **Rodin HyperD** — 3D mesh generation")
    st.divider()
    st.markdown("#### 📊 Free Tier Limits")
    st.markdown("- Gemini: 1500 req/day")
    st.markdown("- Image search: unlimited")
    st.divider()
    st.markdown("<small style='color:#4a5568'>College Project — Heritage Preservation</small>", unsafe_allow_html=True)

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <h1>🏛️ Murti Restoration Assistant</h1>
    <p>Multi-agent AI pipeline for digital restoration of broken cultural artifacts</p>
</div>
""", unsafe_allow_html=True)

# ── How It Works Steps ────────────────────────────────────────────────────────
st.markdown("""
<div class="steps-row">
    <div class="step-item">
        <div class="step-icon">📸</div>
        <div class="step-title">Upload</div>
        <div class="step-desc">Photo of broken murti</div>
    </div>
    <div class="step-item">
        <div class="step-icon">🔍</div>
        <div class="step-title">Analyze</div>
        <div class="step-desc">Gemini detects damage</div>
    </div>
    <div class="step-item">
        <div class="step-icon">🖼️</div>
        <div class="step-title">References</div>
        <div class="step-desc">Web finds intact murtis</div>
    </div>
    <div class="step-item">
        <div class="step-icon">🔧</div>
        <div class="step-title">Guidance</div>
        <div class="step-desc">AI guides Blender repair</div>
    </div>
    <div class="step-item">
        <div class="step-icon">🧊</div>
        <div class="step-title">Restore</div>
        <div class="step-desc">Reconstruct in Blender</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Upload Section ────────────────────────────────────────────────────────────
left, right = st.columns([1, 1], gap="large")

with left:
    st.markdown("### 📸 Upload Image")
    uploaded = st.file_uploader(
        "Upload broken murti image",
        type=["jpg", "png", "jpeg"],
        help="Upload a clear photo of the broken murti",
        label_visibility="collapsed"
    )

    if uploaded:
        image = Image.open(uploaded)
        st.image(image, caption="Uploaded Image", use_column_width=True)
    else:
        st.markdown("""
        <div style="
            background:#1a1a1a;
            border:2px dashed #4a5568;
            border-radius:12px;
            padding:3rem 1rem;
            text-align:center;
            color:#4a5568;
        ">
            <div style="font-size:3rem">🏛️</div>
            <div style="margin-top:0.5rem">Upload a murti image to begin</div>
        </div>
        """, unsafe_allow_html=True)

with right:
    st.markdown("### ⚙️ Run Pipeline")

    if not uploaded:
        st.info("👈 Upload an image first to run the analysis")
    else:
        st.markdown(f"""
        <div class="card">
            <div style="color:#a0aec0; font-size:0.85rem">File ready</div>
            <div style="font-weight:600; margin-top:0.3rem">{uploaded.name}</div>
            <div style="color:#718096; font-size:0.8rem">{round(uploaded.size/1024, 1)} KB</div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("🔍 Analyze & Generate Guidance", type="primary"):

            tmp_path = None

            try:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
                    tmp_path = tmp.name

                image_to_save = image.convert("RGB")
                image_to_save.save(tmp_path)

                progress = st.progress(0, text="Starting pipeline...")

                progress.progress(10, text="Step 1: Analyzing damage with Gemini Vision...")
                from agents.damage_agent import analyze_damage
                damage_report = analyze_damage(tmp_path)

                progress.progress(40, text="Step 2: Searching for reference images...")
                from agents.search_agent import find_similar
                reference_paths, ref_meta = find_similar(tmp_path, damage_report)

                progress.progress(70, text="Step 3: Generating Blender reconstruction guidance...")
                from agents.guidance_agent import generate_guidance
                guidance = generate_guidance(damage_report, reference_paths, ref_meta)

                progress.progress(90, text="Step 4: Saving outputs...")
                from agents.coordinator import save_outputs
                save_outputs(damage_report, reference_paths, guidance)

                progress.progress(100, text="✅ Done!")
                st.success("Analysis complete!")

                # ── Results ──
                st.divider()
                tab1, tab2, tab3 = st.tabs(["📋 Damage Report", "🖼️ References", "🔧 Blender Guidance"])

                with tab1:
                    st.subheader("Damage Analysis")

                    m1, m2 = st.columns(2)
                    with m1:
                        if "murti_type" in damage_report:
                            st.metric(
                                "Murti Type",
                                damage_report["murti_type"].split("(")[0].strip()
                            )
                    with m2:
                        if "damage_severity" in damage_report:
                            severity = damage_report["damage_severity"]
                            color = {"low": "🟢", "medium": "🟡", "high": "🔴"}.get(severity.lower(), "⚪")
                            st.metric("Severity", f"{color} {severity.upper()}")

                    if "damaged_regions" in damage_report:
                        st.markdown("**🔴 Damaged Regions**")
                        tags_html = "".join([f'<span class="tag">🔴 {r}</span>' for r in damage_report["damaged_regions"]])
                        st.markdown(tags_html, unsafe_allow_html=True)
                        st.markdown("")

                    if "missing_parts" in damage_report:
                        st.markdown("**❌ Missing Parts**")
                        tags_html = "".join([f'<span class="tag">❌ {p}</span>' for p in damage_report["missing_parts"]])
                        st.markdown(tags_html, unsafe_allow_html=True)
                        st.markdown("")

                    if "reconstruction_priority" in damage_report:
                        st.markdown("**📌 Reconstruction Priority**")
                        for i, item in enumerate(damage_report["reconstruction_priority"], 1):
                            st.markdown(f"{i}. {item}")

                    if "pose_description" in damage_report:
                        st.markdown("**🧘 Pose Description**")
                        st.markdown(f"> {damage_report['pose_description']}")

                    with st.expander("🔎 Raw JSON"):
                        st.json(damage_report)

                with tab2:
                    st.subheader("Reference Images")

                    if ref_meta:
                        ref_cols = st.columns(min(len(ref_meta), 3))
                        for i, (col, ref) in enumerate(zip(ref_cols, ref_meta[:3])):
                            with col:
                                st.markdown('<div class="ref-card">', unsafe_allow_html=True)
                                if i < len(reference_paths) and os.path.exists(reference_paths[i]):
                                    try:
                                        ref_img = Image.open(reference_paths[i])
                                        st.image(ref_img, use_column_width=True)
                                    except Exception:
                                        if ref.get("thumbnail"):
                                            st.image(ref["thumbnail"], use_column_width=True)
                                elif ref.get("thumbnail"):
                                    st.image(ref["thumbnail"], use_column_width=True)

                                st.markdown(f'<div class="ref-title">{ref.get("title","")[:60]}</div>', unsafe_allow_html=True)
                                st.markdown(f"[View Source ↗]({ref.get('url','#')})")
                                st.markdown('</div>', unsafe_allow_html=True)
                    else:
                        st.warning("No reference images found. Guidance below is still valid.")
                        st.markdown("You can manually search for references using the damage report above.")

                with tab3:
                    st.subheader("Blender Reconstruction Guidance")
                    st.markdown(guidance)
                    st.divider()
                    st.download_button(
                        label="📥 Download Guidance (.txt)",
                        data=guidance,
                        file_name="reconstruction_guide.txt",
                        mime="text/plain",
                        use_container_width=True
                    )

            except Exception as e:
                st.error(f"Pipeline error: {str(e)}")
                with st.expander("🔧 Troubleshooting"):
                    st.markdown("- Check your Gemini API key in `.env`")
                    st.markdown("- Check your internet connection")
                    st.markdown("- Gemini free tier limit may be reached for today")
                    st.markdown("- Try again after a few minutes")

            finally:
                try:
                    gc.collect()
                    if tmp_path and os.path.exists(tmp_path):
                        os.unlink(tmp_path)
                except PermissionError:
                    pass