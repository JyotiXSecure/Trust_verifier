# Digital Trust Verifier

Digital Trust Verifier is a Streamlit app that analyzes images and text for possible manipulation or misinformation using Hugging Face transformer models.

## What It Does

- Detects whether an uploaded image looks more like a real photo or AI-generated / manipulated content
- Analyzes text for fake-news style patterns
- Shows model confidence, trust score, and risk level
- Supports both file upload and direct pasted text
- Adds extra diagnostics such as image quality signals and text-tone signals

## Tech Stack

- Python
- Streamlit
- Hugging Face `transformers`
- PyTorch
- Pillow
- NumPy

## Models Used

- Image detection: `prithivMLmods/Deep-Fake-Detector-v2-Model`
- Text detection: `mrm8488/bert-tiny-finetuned-fake-news-detection`

## Project Files

- [app.py](/Users/niteshv1520/Trust_verifier_seniour/app.py) - main Streamlit application
- [requirements.txt](/Users/niteshv1520/Trust_verifier_seniour/requirements.txt) - Python dependencies

## Setup

Create a virtual environment:

```bash
python3 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

## Run The App

```bash
streamlit run app.py
```

If you prefer not to activate the environment, you can run:

```bash
.venv/bin/streamlit run app.py
```

## Supported Inputs

- `.jpg`
- `.jpeg`
- `.png`
- `.txt`
- pasted text inside the app

## Notes

- Results are probabilistic, not proof
- Model confidence does not guarantee truth
- Text and image analysis should be treated as decision support, not final verification
- The first run may take longer because models may need to download

## Troubleshooting

If `pip install` fails in the system Python environment, use a virtual environment as shown above.

If model downloads fail, check your internet connection and rerun the app after dependencies are installed.
