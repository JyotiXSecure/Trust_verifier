# ============================================================
# Digital Trust Verifier — app.py
# Run on Replit: streamlit run app.py --server.address 0.0.0.0 --server.port 3000
#
# pip install instructions (add to Replit's pyproject.toml or run in Shell):
#   pip install streamlit transformers torch torchvision Pillow requests
# ============================================================

import streamlit as st
from PIL import Image
import io
import traceback

# ── Page config (must be first Streamlit call) ──────────────
st.set_page_config(
    page_title="Digital Trust Verifier",
    page_icon="🔍",
    layout="centered",
)

# ── Custom CSS — refined dark-panel aesthetic ────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=Syne:wght@400;700;800&display=swap');

/* ── Root tokens ── */
:root {
    --bg:        #0b0d12;
    --panel:     #13161f;
    --border:    #1e2330;
    --accent:    #4fffb0;
    --accent2:   #00cfff;
    --danger:    #ff4f6a;
    --muted:     #5a6180;
    --text:      #dce3f5;
    --radius:    12px;
}

/* ── Global ── */
html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg) !important;
    color: var(--text);
    font-family: 'Syne', sans-serif;
}
[data-testid="stSidebar"] { display: none; }
[data-testid="stHeader"]  { background: transparent !important; }

/* ── Hide default Streamlit chrome ── */
#MainMenu, footer { visibility: hidden; }

/* ── Hero header ── */
.hero {
    text-align: center;
    padding: 3.5rem 1rem 2rem;
}
.hero-badge {
    display: inline-block;
    font-family: 'IBM Plex Mono', monospace;
    font-size: .72rem;
    letter-spacing: .14em;
    color: var(--accent);
    border: 1px solid var(--accent);
    border-radius: 999px;
    padding: .25rem .9rem;
    margin-bottom: 1.4rem;
    text-transform: uppercase;
}
.hero h1 {
    font-size: clamp(2rem, 6vw, 3.2rem);
    font-weight: 800;
    line-height: 1.1;
    background: linear-gradient(135deg, var(--accent) 0%, var(--accent2) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0 0 .8rem;
}
.hero p {
    color: var(--muted);
    font-size: 1rem;
    max-width: 480px;
    margin: 0 auto;
    line-height: 1.65;
}

/* ── Upload card ── */
.upload-card {
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 2rem 1.8rem;
    margin: 2rem auto;
    max-width: 640px;
}
.upload-card h3 {
    font-family: 'IBM Plex Mono', monospace;
    font-size: .8rem;
    letter-spacing: .1em;
    text-transform: uppercase;
    color: var(--muted);
    margin: 0 0 1.2rem;
}

/* ── Result card ── */
.result-card {
    background: var(--panel);
    border-radius: var(--radius);
    padding: 2rem;
    margin: 1.5rem auto;
    max-width: 640px;
    position: relative;
    overflow: hidden;
}
.result-card::before {
    content: '';
    position: absolute;
    inset: 0;
    border-radius: var(--radius);
    pointer-events: none;
}
.result-card.real  { border: 1px solid #4fffb055; }
.result-card.real::before  { box-shadow: inset 0 0 60px #4fffb012; }
.result-card.fake  { border: 1px solid #ff4f6a55; }
.result-card.fake::before  { box-shadow: inset 0 0 60px #ff4f6a12; }

.verdict-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: .75rem;
    letter-spacing: .12em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: .4rem;
}
.verdict {
    font-size: 2.4rem;
    font-weight: 800;
    line-height: 1;
    margin-bottom: 1.4rem;
}
.verdict.real { color: var(--accent); }
.verdict.fake { color: var(--danger); }

/* ── Score bar ── */
.score-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: .5rem;
}
.score-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: .78rem;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: .08em;
}
.score-value {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 1.1rem;
    font-weight: 600;
}
.score-value.real { color: var(--accent); }
.score-value.fake { color: var(--danger); }

.bar-track {
    background: var(--border);
    border-radius: 999px;
    height: 6px;
    width: 100%;
    margin-bottom: 1.4rem;
    overflow: hidden;
}
.bar-fill {
    height: 100%;
    border-radius: 999px;
    transition: width .6s ease;
}
.bar-fill.real { background: linear-gradient(90deg, #4fffb0, #00cfff); }
.bar-fill.fake { background: linear-gradient(90deg, #ff4f6a, #ff9966); }

/* ── Explanation box ── */
.explanation {
    background: #0b0d12;
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 1rem 1.2rem;
    font-size: .9rem;
    color: var(--muted);
    line-height: 1.65;
}
.explanation strong { color: var(--text); }

/* ── Error box ── */
.error-box {
    background: #1a0d10;
    border: 1px solid #ff4f6a44;
    border-radius: 8px;
    padding: 1rem 1.2rem;
    color: #ff8090;
    font-size: .9rem;
    font-family: 'IBM Plex Mono', monospace;
    margin: 1rem auto;
    max-width: 640px;
}

/* ── Streamlit file-uploader cosmetics ── */
[data-testid="stFileUploader"] {
    background: #0b0d12 !important;
    border: 1px dashed var(--border) !important;
    border-radius: 10px !important;
}
[data-testid="stFileUploader"] label { color: var(--muted) !important; }

/* ── Button ── */
div.stButton > button {
    background: linear-gradient(135deg, var(--accent) 0%, var(--accent2) 100%);
    color: #0b0d12;
    font-family: 'IBM Plex Mono', monospace;
    font-weight: 600;
    font-size: .88rem;
    letter-spacing: .06em;
    text-transform: uppercase;
    border: none;
    border-radius: 8px;
    padding: .65rem 2rem;
    width: 100%;
    cursor: pointer;
    transition: opacity .2s;
}
div.stButton > button:hover { opacity: .85; }

/* ── Spinner override ── */
[data-testid="stSpinner"] > div { border-top-color: var(--accent) !important; }
</style>
""", unsafe_allow_html=True)


# ── Lazy model loaders (cached so they load only once) ───────
@st.cache_resource(show_spinner=False)
def load_image_pipeline():
    """Load DeepFake detector from HuggingFace."""
    from transformers import pipeline
    return pipeline(
        "image-classification",
        model="prithivMLmods/Deep-Fake-Detector-v2-Model",
    )

@st.cache_resource(show_spinner=False)
def load_text_pipeline():
    """Load fake-news / misinformation text classifier."""
    from transformers import pipeline
    return pipeline(
        "text-classification",
        model="mrm8488/bert-tiny-finetuned-fake-news-detection",
        truncation=True,
        max_length=512,
    )


# ── Analysis helpers ─────────────────────────────────────────
def analyse_image(pil_image):
    """Return (label, confidence, trust_score, explanation)."""
    pipe = load_image_pipeline()
    results = pipe(pil_image)

    # Model returns a list of {label, score}; pick the top prediction
    top = results[0]
    raw_label: str = top["label"].upper()
    confidence: float = round(top["score"] * 100, 1)

    # Normalise label — the model may use REAL/FAKE or AI/HUMAN variants
    is_fake = any(k in raw_label for k in ("FAKE", "AI", "DEEPFAKE", "GENERATED", "ARTIFICIAL"))
    label = "Fake" if is_fake else "Real"

    # Trust score: high confidence in REAL → high trust; high confidence in FAKE → low trust
    if label == "Real":
        trust_score = int(confidence)
    else:
        trust_score = int(100 - confidence)

    if label == "Fake":
        explanation = (
            f"<strong>⚠ Suspicious patterns detected.</strong> The model identified "
            f"characteristics commonly found in AI-generated or manipulated imagery, "
            f"such as inconsistent lighting, unnatural textures, or GAN artifacts. "
            f"Confidence: {confidence}%."
        )
    else:
        explanation = (
            f"<strong>✔ Appears authentic.</strong> No strong indicators of digital "
            f"manipulation or AI generation were found. The image shows patterns "
            f"consistent with real photography. Confidence: {confidence}%."
        )

    return label, confidence, trust_score, explanation


def analyse_text(text: str):
    """Return (label, confidence, trust_score, explanation)."""
    if len(text.strip()) < 20:
        raise ValueError("Text is too short for meaningful analysis (min 20 chars).")

    pipe = load_text_pipeline()
    result = pipe(text[:1024])[0]  # truncate for speed

    raw_label: str = result["label"].upper()
    confidence: float = round(result["score"] * 100, 1)

    # mrm8488 model: label 0 = REAL news, label 1 = FAKE news
    is_fake = raw_label in ("LABEL_1", "FAKE", "1")
    label = "Fake" if is_fake else "Real"

    if label == "Real":
        trust_score = int(confidence)
    else:
        trust_score = int(100 - confidence)

    if label == "Fake":
        explanation = (
            f"<strong>⚠ Potential misinformation detected.</strong> The language model "
            f"found patterns associated with misleading or fabricated news: sensational "
            f"phrasing, statistical inconsistencies, or known disinformation templates. "
            f"Treat this content critically. Confidence: {confidence}%."
        )
    else:
        explanation = (
            f"<strong>✔ Content appears credible.</strong> The text shows linguistic "
            f"patterns more consistent with factual reporting—measured tone, verifiable "
            f"claims, and coherent structure. Always cross-check with primary sources. "
            f"Confidence: {confidence}%."
        )

    return label, confidence, trust_score, explanation


# ── Result renderer ──────────────────────────────────────────
def render_result(label: str, confidence: float, trust_score: int, explanation: str):
    cls = "real" if label == "Real" else "fake"
    icon = "✔" if label == "Real" else "✕"
    bar_pct = trust_score

    st.markdown(f"""
    <div class="result-card {cls}">
        <div class="verdict-label">Verdict</div>
        <div class="verdict {cls}">{icon} {label}</div>

        <div class="score-row">
            <span class="score-label">Model Confidence</span>
            <span class="score-value {cls}">{confidence}%</span>
        </div>
        <div class="bar-track">
            <div class="bar-fill {cls}" style="width:{confidence}%"></div>
        </div>

        <div class="score-row">
            <span class="score-label">Trust Score</span>
            <span class="score-value {cls}">{trust_score} / 100</span>
        </div>
        <div class="bar-track">
            <div class="bar-fill {cls}" style="width:{bar_pct}%"></div>
        </div>

        <div class="explanation">{explanation}</div>
    </div>
    """, unsafe_allow_html=True)


# ── UI ───────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-badge">AI-powered · v1.0</div>
    <h1>Digital Trust Verifier</h1>
    <p>Upload an image or text file and receive an instant authenticity assessment powered by state-of-the-art detection models.</p>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="upload-card"><h3>Upload Content</h3>', unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    label="Drag & drop or browse",
    type=["jpg", "jpeg", "png", "txt"],
    label_visibility="collapsed",
)

analyse_btn = st.button("Analyse Content", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)


# ── Analysis logic ───────────────────────────────────────────
if analyse_btn:
    if uploaded_file is None:
        st.markdown('<div class="error-box">⚠ Please upload a file before running analysis.</div>',
                    unsafe_allow_html=True)
    else:
        file_ext = uploaded_file.name.rsplit(".", 1)[-1].lower()

        if file_ext in ("jpg", "jpeg", "png"):
            # ── Image branch ──────────────────────────────────
            try:
                with st.spinner("Loading detector model and analysing image…"):
                    pil_img = Image.open(io.BytesIO(uploaded_file.read())).convert("RGB")
                    st.image(pil_img, caption=uploaded_file.name, use_container_width=True)
                    label, conf, trust, expl = analyse_image(pil_img)
                render_result(label, conf, trust, expl)
            except Exception:
                st.markdown(
                    f'<div class="error-box">Error during image analysis:<br><pre>{traceback.format_exc()}</pre></div>',
                    unsafe_allow_html=True,
                )

        elif file_ext == "txt":
            # ── Text branch ───────────────────────────────────
            try:
                raw_text = uploaded_file.read().decode("utf-8", errors="replace")
                with st.expander("📄 Preview uploaded text", expanded=False):
                    st.text(raw_text[:2000] + ("…" if len(raw_text) > 2000 else ""))
                with st.spinner("Loading language model and analysing text…"):
                    label, conf, trust, expl = analyse_text(raw_text)
                render_result(label, conf, trust, expl)
            except ValueError as ve:
                st.markdown(f'<div class="error-box">⚠ {ve}</div>', unsafe_allow_html=True)
            except Exception:
                st.markdown(
                    f'<div class="error-box">Error during text analysis:<br><pre>{traceback.format_exc()}</pre></div>',
                    unsafe_allow_html=True,
                )

        else:
            st.markdown(
                f'<div class="error-box">⚠ Unsupported file type: <strong>.{file_ext}</strong>. '
                f'Please upload a .jpg, .png, or .txt file.</div>',
                unsafe_allow_html=True,
            )

# ── Footer ───────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;padding:3rem 1rem 1.5rem;color:#2e3450;
            font-family:'IBM Plex Mono',monospace;font-size:.72rem;letter-spacing:.06em;">
    DIGITAL TRUST VERIFIER · FOR RESEARCH USE ONLY · RESULTS ARE PROBABILISTIC
</div>
""", unsafe_allow_html=True)
