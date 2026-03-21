import io
import re
import traceback

import numpy as np
import streamlit as st
from PIL import Image


st.set_page_config(
    page_title="Digital Trust Verifier",
    page_icon="🔍",
    layout="centered",
)

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=Syne:wght@400;700;800&display=swap');

:root {
    --bg: #0b0d12;
    --panel: #13161f;
    --panel-soft: #10131a;
    --border: #1e2330;
    --accent: #4fffb0;
    --accent2: #00cfff;
    --danger: #ff4f6a;
    --warning: #ffb347;
    --muted: #7b84a6;
    --text: #dce3f5;
    --radius: 14px;
}

html, body, [data-testid="stAppViewContainer"] {
    background:
        radial-gradient(circle at top left, rgba(79, 255, 176, 0.08), transparent 28%),
        radial-gradient(circle at top right, rgba(0, 207, 255, 0.08), transparent 24%),
        var(--bg) !important;
    color: var(--text);
    font-family: 'Syne', sans-serif;
}

[data-testid="stSidebar"] { display: none; }
[data-testid="stHeader"] { background: transparent !important; }
#MainMenu, footer { visibility: hidden; }

.hero {
    text-align: center;
    padding: 3.2rem 1rem 1.7rem;
}

.hero-badge {
    display: inline-block;
    font-family: 'IBM Plex Mono', monospace;
    font-size: .72rem;
    letter-spacing: .14em;
    color: var(--accent);
    border: 1px solid rgba(79, 255, 176, 0.45);
    border-radius: 999px;
    padding: .25rem .9rem;
    margin-bottom: 1.2rem;
    text-transform: uppercase;
    background: rgba(79, 255, 176, 0.06);
}

.hero h1 {
    font-size: clamp(2.2rem, 6vw, 3.5rem);
    font-weight: 800;
    line-height: 1.05;
    background: linear-gradient(135deg, var(--accent) 0%, var(--accent2) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0 0 .8rem;
}

.hero p {
    color: var(--muted);
    font-size: 1rem;
    max-width: 620px;
    margin: 0 auto;
    line-height: 1.7;
}

.card {
    background: linear-gradient(180deg, rgba(19, 22, 31, 0.98), rgba(16, 19, 26, 0.98));
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.45rem;
    margin: 1rem auto;
    max-width: 760px;
    box-shadow: 0 12px 40px rgba(0, 0, 0, 0.18);
}

.section-title {
    font-family: 'IBM Plex Mono', monospace;
    font-size: .8rem;
    letter-spacing: .1em;
    text-transform: uppercase;
    color: var(--muted);
    margin: 0 0 1rem;
}

.metric-grid {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: .9rem;
    margin-top: 1rem;
}

.metric {
    background: rgba(255, 255, 255, 0.02);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: .95rem;
}

.metric-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: .7rem;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: .08em;
    margin-bottom: .45rem;
}

.metric-value {
    font-size: 1.1rem;
    font-weight: 700;
}

.result-card {
    background: linear-gradient(180deg, rgba(19, 22, 31, 0.98), rgba(11, 13, 18, 0.98));
    border-radius: var(--radius);
    padding: 1.7rem;
    margin: 1.2rem auto;
    max-width: 760px;
    position: relative;
    overflow: hidden;
}

.result-card.real { border: 1px solid rgba(79, 255, 176, 0.35); }
.result-card.fake { border: 1px solid rgba(255, 79, 106, 0.35); }

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
    margin-bottom: 1rem;
}

.verdict.real { color: var(--accent); }
.verdict.fake { color: var(--danger); }

.badge-row {
    display: flex;
    gap: .6rem;
    flex-wrap: wrap;
    margin-bottom: 1.2rem;
}

.pill {
    font-family: 'IBM Plex Mono', monospace;
    font-size: .72rem;
    letter-spacing: .06em;
    text-transform: uppercase;
    padding: .35rem .7rem;
    border-radius: 999px;
    border: 1px solid var(--border);
    background: rgba(255, 255, 255, 0.02);
}

.pill.real {
    color: var(--accent);
    border-color: rgba(79, 255, 176, 0.35);
}

.pill.fake {
    color: var(--danger);
    border-color: rgba(255, 79, 106, 0.35);
}

.pill.warn {
    color: var(--warning);
    border-color: rgba(255, 179, 71, 0.35);
}

.score-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin: .7rem 0 .4rem;
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
    font-size: 1.05rem;
    font-weight: 600;
}

.score-value.real { color: var(--accent); }
.score-value.fake { color: var(--danger); }

.bar-track {
    background: var(--border);
    border-radius: 999px;
    height: 8px;
    width: 100%;
    overflow: hidden;
}

.bar-fill {
    height: 100%;
    border-radius: 999px;
}

.bar-fill.real { background: linear-gradient(90deg, #4fffb0, #00cfff); }
.bar-fill.fake { background: linear-gradient(90deg, #ff4f6a, #ff9966); }

.explanation {
    background: rgba(0, 0, 0, 0.18);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 1rem 1.15rem;
    font-size: .94rem;
    color: var(--muted);
    line-height: 1.65;
    margin-top: 1.1rem;
}

.signal-list {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: .75rem;
    margin-top: 1rem;
}

.signal {
    background: rgba(255, 255, 255, 0.02);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: .8rem .9rem;
}

.signal-title {
    font-family: 'IBM Plex Mono', monospace;
    font-size: .7rem;
    color: var(--muted);
    text-transform: uppercase;
    margin-bottom: .35rem;
}

.signal-text {
    font-size: .9rem;
    line-height: 1.5;
}

.error-box {
    background: #1a0d10;
    border: 1px solid rgba(255, 79, 106, 0.28);
    border-radius: 10px;
    padding: 1rem 1.1rem;
    color: #ff96a7;
    font-size: .92rem;
    margin: 1rem auto;
    max-width: 760px;
}

[data-testid="stFileUploader"] {
    background: #0b0d12 !important;
    border: 1px dashed var(--border) !important;
    border-radius: 12px !important;
}

[data-testid="stFileUploader"] label {
    color: var(--muted) !important;
}

div.stButton > button {
    background: linear-gradient(135deg, var(--accent) 0%, var(--accent2) 100%);
    color: #0b0d12;
    font-family: 'IBM Plex Mono', monospace;
    font-weight: 700;
    font-size: .88rem;
    letter-spacing: .05em;
    text-transform: uppercase;
    border: none;
    border-radius: 10px;
    padding: .75rem 1.5rem;
    width: 100%;
    cursor: pointer;
}

div.stButton > button:hover {
    opacity: .9;
}

[data-testid="stSpinner"] > div {
    border-top-color: var(--accent) !important;
}

@media (max-width: 720px) {
    .metric-grid, .signal-list {
        grid-template-columns: 1fr;
    }
}
</style>
""",
    unsafe_allow_html=True,
)


IMAGE_MODEL_NAME = "prithivMLmods/Deep-Fake-Detector-v2-Model"
TEXT_MODEL_NAME = "mrm8488/bert-tiny-finetuned-fake-news-detection"


@st.cache_resource(show_spinner=False)
def load_image_pipeline():
    from transformers import pipeline

    return pipeline("image-classification", model=IMAGE_MODEL_NAME)


@st.cache_resource(show_spinner=False)
def load_text_pipeline():
    from transformers import pipeline

    return pipeline(
        "text-classification",
        model=TEXT_MODEL_NAME,
        truncation=True,
        max_length=512,
    )


def safe_ratio(numerator: float, denominator: float) -> float:
    return numerator / denominator if denominator else 0.0


def format_bytes(size: int) -> str:
    units = ["B", "KB", "MB", "GB"]
    value = float(size)
    for unit in units:
        if value < 1024 or unit == units[-1]:
            return f"{value:.1f} {unit}"
        value /= 1024
    return f"{size} B"


def risk_level(trust_score: int) -> str:
    if trust_score >= 75:
        return "Low Risk"
    if trust_score >= 45:
        return "Medium Risk"
    return "High Risk"


def confidence_band(confidence: float) -> str:
    if confidence >= 85:
        return "High Confidence"
    if confidence >= 65:
        return "Moderate Confidence"
    return "Low Confidence"


def image_signals(pil_image: Image.Image) -> list[dict]:
    grayscale = pil_image.convert("L")
    arr = np.asarray(grayscale, dtype=np.float32)
    width, height = pil_image.size

    brightness = float(arr.mean())
    contrast = float(arr.std())
    diff_x = np.abs(np.diff(arr, axis=1)).mean() if width > 1 else 0.0
    diff_y = np.abs(np.diff(arr, axis=0)).mean() if height > 1 else 0.0
    edge_density = float((diff_x + diff_y) / 2)
    aspect = round(width / height, 2) if height else 0

    findings = []
    findings.append(
        {
            "title": "Resolution",
            "text": f"{width} × {height}px with aspect ratio {aspect}. Higher-resolution images usually give the detector more signal.",
        }
    )
    findings.append(
        {
            "title": "Lighting",
            "text": f"Average brightness is {brightness:.1f}/255. Extreme darkness or overexposure can reduce reliability.",
        }
    )
    findings.append(
        {
            "title": "Texture Consistency",
            "text": f"Estimated contrast {contrast:.1f} and edge density {edge_density:.1f}. Synthetic imagery often shows unusual texture smoothness or sharp transitions.",
        }
    )

    if min(width, height) < 256:
        findings.append(
            {
                "title": "Caution",
                "text": "This image is relatively small, so the model has less visual detail to inspect.",
            }
        )

    return findings


def text_signals(text: str) -> list[dict]:
    words = re.findall(r"\b\w+\b", text)
    sentences = [part.strip() for part in re.split(r"[.!?]+", text) if part.strip()]
    uppercase_chars = sum(1 for char in text if char.isupper())
    alpha_chars = sum(1 for char in text if char.isalpha())
    caps_ratio = safe_ratio(uppercase_chars, alpha_chars) * 100
    exclamations = text.count("!")
    question_marks = text.count("?")
    urls = len(re.findall(r"https?://|www\.", text))
    sensational = len(
        re.findall(
            r"\b(shocking|breaking|unbelievable|secret|exposed|urgent|must see|viral)\b",
            text,
            flags=re.IGNORECASE,
        )
    )

    return [
        {
            "title": "Structure",
            "text": f"{len(words)} words across {max(len(sentences), 1)} sentence-like segments.",
        },
        {
            "title": "Tone",
            "text": f"Uppercase ratio {caps_ratio:.1f}%, exclamations {exclamations}, question marks {question_marks}. High-intensity tone can be a risk signal.",
        },
        {
            "title": "Claims",
            "text": f"Detected {urls} URL references and {sensational} sensational trigger phrases.",
        },
    ]


def build_image_explanation(label: str, confidence: float, trust_score: int, findings: list[dict]) -> str:
    if label == "Fake":
        lead = "The detector found patterns more consistent with manipulated or AI-generated imagery."
    else:
        lead = "The detector found stronger alignment with natural photographic patterns than with synthetic manipulation."

    return (
        f"<strong>Assessment summary:</strong> {lead} "
        f"Model confidence is {confidence:.1f}%, producing a trust score of {trust_score}/100. "
        f"Use the visual signals below as supporting context, not proof."
    )


def build_text_explanation(label: str, confidence: float, trust_score: int, findings: list[dict]) -> str:
    if label == "Fake":
        lead = "The language model found stronger similarity to fabricated or misleading reporting patterns."
    else:
        lead = "The language model found stronger similarity to factual reporting patterns than to fabricated news."

    return (
        f"<strong>Assessment summary:</strong> {lead} "
        f"Model confidence is {confidence:.1f}%, producing a trust score of {trust_score}/100. "
        f"Review the writing-signal diagnostics below before making a final judgment."
    )


def analyse_image(pil_image: Image.Image):
    pipe = load_image_pipeline()
    results = pipe(pil_image)
    top = results[0]
    raw_label = str(top["label"]).upper()
    confidence = round(float(top["score"]) * 100, 1)

    is_fake = any(
        token in raw_label
        for token in ("FAKE", "AI", "DEEPFAKE", "GENERATED", "ARTIFICIAL")
    )
    label = "Fake" if is_fake else "Real"
    trust_score = int(confidence) if label == "Real" else int(100 - confidence)
    findings = image_signals(pil_image)
    explanation = build_image_explanation(label, confidence, trust_score, findings)

    metadata = {
        "Content Type": "Image",
        "Model": IMAGE_MODEL_NAME,
        "Image Size": f"{pil_image.size[0]} × {pil_image.size[1]} px",
        "Trust Risk": risk_level(trust_score),
    }
    return label, confidence, trust_score, explanation, findings, metadata


def analyse_text(text: str):
    cleaned = text.strip()
    if len(cleaned) < 40:
        raise ValueError("Text is too short for meaningful analysis. Please provide at least 40 characters.")

    pipe = load_text_pipeline()
    result = pipe(cleaned[:1024])[0]
    raw_label = str(result["label"]).upper()
    confidence = round(float(result["score"]) * 100, 1)

    is_fake = raw_label in ("LABEL_1", "FAKE", "1")
    label = "Fake" if is_fake else "Real"
    trust_score = int(confidence) if label == "Real" else int(100 - confidence)
    findings = text_signals(cleaned)
    explanation = build_text_explanation(label, confidence, trust_score, findings)

    words = re.findall(r"\b\w+\b", cleaned)
    metadata = {
        "Content Type": "Text",
        "Model": TEXT_MODEL_NAME,
        "Word Count": str(len(words)),
        "Trust Risk": risk_level(trust_score),
    }
    return label, confidence, trust_score, explanation, findings, metadata


def render_metrics(metrics: dict):
    cells = []
    for label, value in metrics.items():
        cells.append(
            f"""
            <div class="metric">
                <div class="metric-label">{label}</div>
                <div class="metric-value">{value}</div>
            </div>
            """
        )
    st.markdown(f'<div class="metric-grid">{"".join(cells)}</div>', unsafe_allow_html=True)


def render_signal_list(signals: list[dict]):
    blocks = []
    for signal in signals:
        blocks.append(
            f"""
            <div class="signal">
                <div class="signal-title">{signal["title"]}</div>
                <div class="signal-text">{signal["text"]}</div>
            </div>
            """
        )
    st.markdown(f'<div class="signal-list">{"".join(blocks)}</div>', unsafe_allow_html=True)


def render_result(label: str, confidence: float, trust_score: int, explanation: str, findings: list[dict], metadata: dict):
    cls = "real" if label == "Real" else "fake"
    icon = "✔" if label == "Real" else "✕"

    st.markdown(
        f"""
        <div class="result-card {cls}">
            <div class="verdict-label">Verdict</div>
            <div class="verdict {cls}">{icon} {label}</div>
            <div class="badge-row">
                <span class="pill {cls}">{confidence_band(confidence)}</span>
                <span class="pill {'real' if trust_score >= 60 else 'warn' if trust_score >= 40 else 'fake'}">{risk_level(trust_score)}</span>
            </div>

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
                <div class="bar-fill {cls}" style="width:{trust_score}%"></div>
            </div>

            <div class="explanation">{explanation}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="card"><div class="section-title">Analysis Details</div>', unsafe_allow_html=True)
    render_metrics(metadata)
    render_signal_list(findings)
    st.markdown("</div>", unsafe_allow_html=True)


def render_error(message: str):
    st.markdown(f'<div class="error-box">{message}</div>', unsafe_allow_html=True)


def file_metadata(uploaded_file) -> dict:
    return {
        "Filename": uploaded_file.name,
        "Size": format_bytes(uploaded_file.size),
        "Extension": uploaded_file.name.rsplit(".", 1)[-1].lower(),
    }


st.markdown(
    """
<div class="hero">
    <div class="hero-badge">AI-powered · Advanced Analyzer</div>
    <h1>Digital Trust Verifier</h1>
    <p>Inspect images and text with transformer-based detectors, richer diagnostics, and clearer trust signals built for fast research triage.</p>
</div>
""",
    unsafe_allow_html=True,
)

mode = st.radio(
    "Choose input mode",
    options=["Upload File", "Paste Text"],
    horizontal=True,
)

st.markdown('<div class="card"><div class="section-title">Input</div>', unsafe_allow_html=True)

uploaded_file = None
manual_text = ""

if mode == "Upload File":
    uploaded_file = st.file_uploader(
        label="Drag & drop or browse",
        type=["jpg", "jpeg", "png", "txt"],
        label_visibility="collapsed",
    )
    if uploaded_file is not None:
        render_metrics(file_metadata(uploaded_file))
else:
    manual_text = st.text_area(
        "Paste text to verify",
        height=220,
        placeholder="Paste an article excerpt, social post, statement, or claim here for credibility analysis...",
        label_visibility="collapsed",
    )
    render_metrics(
        {
            "Characters": str(len(manual_text)),
            "Words": str(len(re.findall(r"\b\w+\b", manual_text))),
            "Mode": "Direct Text Input",
        }
    )

analyse_btn = st.button("Run Advanced Analysis", use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)


if analyse_btn:
    if mode == "Upload File":
        if uploaded_file is None:
            render_error("Please upload a file before running analysis.")
        else:
            file_ext = uploaded_file.name.rsplit(".", 1)[-1].lower()
            file_bytes = uploaded_file.read()

            if file_ext in ("jpg", "jpeg", "png"):
                try:
                    with st.spinner("Loading vision detector and analyzing image..."):
                        pil_img = Image.open(io.BytesIO(file_bytes)).convert("RGB")
                        st.image(pil_img, caption=uploaded_file.name, use_container_width=True)
                        label, conf, trust, expl, findings, metadata = analyse_image(pil_img)
                    metadata["File Size"] = format_bytes(len(file_bytes))
                    render_result(label, conf, trust, expl, findings, metadata)
                except Exception:
                    render_error(
                        "Error during image analysis:<br><pre>"
                        + traceback.format_exc()
                        + "</pre>"
                    )
            elif file_ext == "txt":
                try:
                    raw_text = file_bytes.decode("utf-8", errors="replace")
                    with st.expander("Preview uploaded text", expanded=False):
                        st.text(raw_text[:2500] + ("..." if len(raw_text) > 2500 else ""))
                    with st.spinner("Loading language model and analyzing text..."):
                        label, conf, trust, expl, findings, metadata = analyse_text(raw_text)
                    metadata["File Size"] = format_bytes(len(file_bytes))
                    render_result(label, conf, trust, expl, findings, metadata)
                except ValueError as err:
                    render_error(str(err))
                except Exception:
                    render_error(
                        "Error during text analysis:<br><pre>"
                        + traceback.format_exc()
                        + "</pre>"
                    )
            else:
                render_error(
                    f"Unsupported file type <strong>.{file_ext}</strong>. Please upload a JPG, PNG, or TXT file."
                )
    else:
        try:
            with st.spinner("Running credibility analysis on pasted text..."):
                label, conf, trust, expl, findings, metadata = analyse_text(manual_text)
            render_result(label, conf, trust, expl, findings, metadata)
        except ValueError as err:
            render_error(str(err))
        except Exception:
            render_error(
                "Error during text analysis:<br><pre>"
                + traceback.format_exc()
                + "</pre>"
            )


st.markdown(
    """
<div style="text-align:center;padding:2.8rem 1rem 1.4rem;color:#44506f;
            font-family:'IBM Plex Mono',monospace;font-size:.72rem;letter-spacing:.06em;">
    DIGITAL TRUST VERIFIER · RESEARCH ASSIST MODE · RESULTS ARE PROBABILISTIC, NOT FACTUAL PROOF
</div>
""",
    unsafe_allow_html=True,
)
