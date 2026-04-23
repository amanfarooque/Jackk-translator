"""
╔══════════════════════════════════════════════════════════════════╗
║         JACKK — Video to Hindi Subtitle Generator               ║
║         Senior Python Developer & AI Engineer Build             ║
╚══════════════════════════════════════════════════════════════════╝

Dependencies:
    pip install streamlit faster-whisper moviepy pydub

Run:
    streamlit run hindi_subtitle_generator.py
"""

import os
import time
import tempfile
import math
import streamlit as st
from pathlib import Path


# ──────────────────────────────────────────────
# PAGE CONFIG  (must be first Streamlit call)
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="Jackk · Hindi Subtitle Generator",
    page_icon="🎬",
    layout="centered",
    initial_sidebar_state="collapsed",
)


# ──────────────────────────────────────────────
# DARK THEME CSS  — Jackk Brand
# ──────────────────────────────────────────────
BRAND_CSS = """
<style>
/* ── Google Font ── */
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

/* ── Root Variables ── */
:root {
    --bg-0:    #0a0a0f;
    --bg-1:    #111118;
    --bg-2:    #1a1a24;
    --bg-3:    #22222f;
    --accent:  #ff4d6d;
    --accent2: #f97316;
    --gold:    #fbbf24;
    --text-1:  #f1f0ff;
    --text-2:  #a09ec0;
    --text-3:  #5c5a7a;
    --border:  #2a2a3d;
    --success: #22c55e;
    --mono:    'JetBrains Mono', monospace;
    --sans:    'Syne', sans-serif;
}

/* ── Global Reset ── */
html, body, [class*="css"] {
    background-color: var(--bg-0) !important;
    color: var(--text-1) !important;
    font-family: var(--sans) !important;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none !important; }

/* ── Block container ── */
.block-container {
    padding: 2.5rem 1.5rem 4rem !important;
    max-width: 860px !important;
}

/* ── Hero banner ── */
.jackk-hero {
    background: linear-gradient(135deg, #0f0f1a 0%, #1a0a1f 50%, #0f1020 100%);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 2.8rem 2.4rem 2.4rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.jackk-hero::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 220px; height: 220px;
    background: radial-gradient(circle, rgba(255,77,109,.18) 0%, transparent 70%);
    border-radius: 50%;
}
.jackk-hero::after {
    content: '';
    position: absolute;
    bottom: -40px; left: 10%;
    width: 160px; height: 160px;
    background: radial-gradient(circle, rgba(249,115,22,.12) 0%, transparent 70%);
    border-radius: 50%;
}
.jackk-wordmark {
    font-family: var(--sans);
    font-weight: 800;
    font-size: 2.6rem;
    letter-spacing: -0.04em;
    background: linear-gradient(90deg, var(--accent), var(--accent2));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1;
    margin-bottom: .3rem;
}
.jackk-tagline {
    color: var(--text-2);
    font-size: .9rem;
    font-weight: 400;
    letter-spacing: .06em;
    text-transform: uppercase;
}
.jackk-badge {
    display: inline-block;
    background: linear-gradient(90deg, var(--accent), var(--accent2));
    color: white;
    font-size: .65rem;
    font-weight: 700;
    letter-spacing: .1em;
    text-transform: uppercase;
    padding: .2rem .55rem;
    border-radius: 4px;
    margin-top: .8rem;
}

/* ── Section card ── */
.jackk-card {
    background: var(--bg-1);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.8rem 1.8rem 1.4rem;
    margin-bottom: 1.4rem;
}
.jackk-card-title {
    font-size: .75rem;
    font-weight: 700;
    letter-spacing: .12em;
    text-transform: uppercase;
    color: var(--text-3);
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: .5rem;
}
.jackk-card-title span.dot {
    width: 6px; height: 6px;
    background: var(--accent);
    border-radius: 50%;
    display: inline-block;
}

/* ── Uploader override ── */
[data-testid="stFileUploader"] {
    background: var(--bg-2) !important;
    border: 1.5px dashed var(--border) !important;
    border-radius: 10px !important;
    padding: 1rem !important;
    transition: border-color .2s;
}
[data-testid="stFileUploader"]:hover {
    border-color: var(--accent) !important;
}
[data-testid="stFileUploaderDropzoneInstructions"] {
    color: var(--text-2) !important;
}

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(90deg, var(--accent) 0%, var(--accent2) 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    padding: .65rem 1.8rem !important;
    font-family: var(--sans) !important;
    font-weight: 700 !important;
    font-size: .9rem !important;
    letter-spacing: .03em !important;
    transition: opacity .2s, transform .15s !important;
    box-shadow: 0 4px 20px rgba(255,77,109,.25) !important;
}
.stButton > button:hover {
    opacity: .88 !important;
    transform: translateY(-1px) !important;
}

/* ── Download buttons ── */
[data-testid="stDownloadButton"] > button {
    background: var(--bg-3) !important;
    color: var(--text-1) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    padding: .55rem 1.4rem !important;
    font-family: var(--sans) !important;
    font-weight: 600 !important;
    font-size: .85rem !important;
    transition: border-color .2s, background .2s !important;
}
[data-testid="stDownloadButton"] > button:hover {
    border-color: var(--accent) !important;
    background: var(--bg-2) !important;
}

/* ── Progress bar ── */
[data-testid="stProgress"] > div > div {
    background: linear-gradient(90deg, var(--accent), var(--accent2)) !important;
    border-radius: 999px !important;
}
[data-testid="stProgress"] {
    background: var(--bg-3) !important;
    border-radius: 999px !important;
}

/* ── Text area (preview) ── */
.stTextArea textarea {
    background: var(--bg-2) !important;
    border: 1px solid var(--border) !important;
    color: var(--text-1) !important;
    font-family: var(--mono) !important;
    font-size: .82rem !important;
    border-radius: 8px !important;
    line-height: 1.7 !important;
}

/* ── Info / success boxes ── */
[data-testid="stAlert"] {
    background: var(--bg-2) !important;
    border-radius: 10px !important;
    border-left-color: var(--success) !important;
}

/* ── Step indicator ── */
.step-row {
    display: flex;
    gap: 1rem;
    margin-bottom: 1.8rem;
    flex-wrap: wrap;
}
.step-item {
    flex: 1;
    min-width: 140px;
    background: var(--bg-2);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: .9rem 1rem;
    text-align: center;
}
.step-num {
    font-size: 1.5rem;
    font-weight: 800;
    background: linear-gradient(90deg, var(--accent), var(--gold));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1;
    margin-bottom: .25rem;
}
.step-label {
    font-size: .72rem;
    color: var(--text-2);
    letter-spacing: .06em;
    text-transform: uppercase;
}

/* ── Log / mono text ── */
.log-box {
    background: var(--bg-2);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 1.2rem;
    font-family: var(--mono);
    font-size: .78rem;
    color: var(--text-2);
    line-height: 1.8;
    max-height: 240px;
    overflow-y: auto;
}
.log-box .ok   { color: var(--success); }
.log-box .warn { color: var(--gold);    }
.log-box .err  { color: var(--accent);  }

/* ── Divider ── */
hr { border-color: var(--border) !important; margin: 1.4rem 0 !important; }

/* ── Selectbox / number input ── */
[data-testid="stSelectbox"] > div,
[data-testid="stNumberInput"] > div {
    background: var(--bg-2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text-1) !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: var(--bg-1); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 999px; }
</style>
"""
st.markdown(BRAND_CSS, unsafe_allow_html=True)


# ──────────────────────────────────────────────
# HELPER: Format seconds → SRT timestamp
# ──────────────────────────────────────────────
def seconds_to_srt_time(seconds: float) -> str:
    """Convert float seconds to SRT timestamp HH:MM:SS,mmm"""
    hours   = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs    = int(seconds % 60)
    millis  = int(round((seconds - int(seconds)) * 1000))
    return f"{hours:02}:{minutes:02}:{secs:02},{millis:03}"


# ──────────────────────────────────────────────
# HELPER: Build .srt content from segments
# ──────────────────────────────────────────────
def build_srt(segments) -> str:
    lines = []
    for i, seg in enumerate(segments, 1):
        start = seconds_to_srt_time(seg.start)
        end   = seconds_to_srt_time(seg.end)
        text  = seg.text.strip()
        lines.append(f"{i}\n{start} --> {end}\n{text}\n")
    return "\n".join(lines)


# ──────────────────────────────────────────────
# HELPER: Extract audio with moviepy
# ──────────────────────────────────────────────
def extract_audio(video_path: str, audio_path: str) -> float:
    """Extract audio to WAV, returns duration in seconds."""
    from moviepy import VideoFileClip
    clip = VideoFileClip(video_path)
    duration = clip.duration
    clip.audio.write_audiofile(audio_path, fps=16000, nbytes=2, codec="pcm_s16le", logger=None)
    clip.close()
    return duration


# ──────────────────────────────────────────────
# HELPER: Chunk audio file into segments
# ──────────────────────────────────────────────
def chunk_audio(audio_path: str, chunk_seconds: int, tmp_dir: str) -> list[str]:
    """Split audio WAV into fixed-length chunks. Returns list of chunk paths."""
    from pydub import AudioSegment
    audio = AudioSegment.from_wav(audio_path)
    total_ms    = len(audio)
    chunk_ms    = chunk_seconds * 1000
    num_chunks  = math.ceil(total_ms / chunk_ms)
    paths       = []
    for i in range(num_chunks):
        start  = i * chunk_ms
        end    = min((i + 1) * chunk_ms, total_ms)
        chunk  = audio[start:end]
        cpath  = os.path.join(tmp_dir, f"chunk_{i:04d}.wav")
        chunk.export(cpath, format="wav")
        paths.append(cpath)
    return paths


# ──────────────────────────────────────────────
# CORE: Transcribe  (chunked or single-pass)
# ──────────────────────────────────────────────
def transcribe(
    audio_path: str,
    duration: float,
    model_size: str,
    progress_bar,
    status_text,
    chunk_threshold_secs: int = 120,
    chunk_size_secs: int      = 60,
) -> list:
    """
    Returns a flat list of Segment-like objects (namedtuples with .start/.end/.text).
    Uses chunking for videos > chunk_threshold_secs.
    """
    from faster_whisper import WhisperModel
    from collections import namedtuple

    FakeSegment = namedtuple("Segment", ["start", "end", "text"])

    status_text.markdown(
        '<p style="color:#a09ec0;font-size:.85rem;">⚙️ Loading Whisper model — first run downloads weights…</p>',
        unsafe_allow_html=True,
    )
    model = WhisperModel(model_size, compute_type="int8", device="cpu")

    all_segments = []

    if duration <= chunk_threshold_secs:
        # ── Single-pass ──────────────────────────────
        status_text.markdown(
            '<p style="color:#a09ec0;font-size:.85rem;">🎙️ Transcribing in single pass…</p>',
            unsafe_allow_html=True,
        )
        segments, _ = model.transcribe(audio_path, language="hi", beam_size=5)
        for seg in segments:
            all_segments.append(FakeSegment(seg.start, seg.end, seg.text))
        progress_bar.progress(1.0)

    else:
        # ── Chunked pass ─────────────────────────────
        with tempfile.TemporaryDirectory() as tmp_chunk_dir:
            status_text.markdown(
                '<p style="color:#a09ec0;font-size:.85rem;">✂️ Splitting audio into 60-second chunks…</p>',
                unsafe_allow_html=True,
            )
            chunk_paths = chunk_audio(audio_path, chunk_size_secs, tmp_chunk_dir)
            total_chunks = len(chunk_paths)

            for idx, cpath in enumerate(chunk_paths):
                time_offset = idx * chunk_size_secs
                frac = idx / total_chunks
                progress_bar.progress(frac)
                status_text.markdown(
                    f'<p style="color:#a09ec0;font-size:.85rem;">'
                    f'🎙️ Transcribing chunk {idx + 1} / {total_chunks}…</p>',
                    unsafe_allow_html=True,
                )
                segments, _ = model.transcribe(cpath, language="hi", beam_size=5)
                for seg in segments:
                    all_segments.append(
                        FakeSegment(
                            seg.start + time_offset,
                            seg.end   + time_offset,
                            seg.text,
                        )
                    )
                # chunk cleaned up when TemporaryDirectory exits

        progress_bar.progress(1.0)

    return all_segments


# ──────────────────────────────────────────────
# UI: Hero Header
# ──────────────────────────────────────────────
st.markdown("""
<div class="jackk-hero">
    <div class="jackk-wordmark">JACKK</div>
    <div class="jackk-tagline">AI-Powered Video Intelligence Suite</div>
    <div class="jackk-badge">🇮🇳 Hindi Subtitle Generator · v2.0</div>
</div>
""", unsafe_allow_html=True)

# ── How-it-works steps ──
st.markdown("""
<div class="step-row">
    <div class="step-item"><div class="step-num">01</div><div class="step-label">Upload Video</div></div>
    <div class="step-item"><div class="step-num">02</div><div class="step-label">Extract Audio</div></div>
    <div class="step-item"><div class="step-num">03</div><div class="step-label">AI Transcription</div></div>
    <div class="step-item"><div class="step-num">04</div><div class="step-label">Export Subtitles</div></div>
</div>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────────
# UI: Settings Card
# ──────────────────────────────────────────────
st.markdown("""
<div class="jackk-card">
    <div class="jackk-card-title"><span class="dot"></span> Model Configuration</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    model_size = st.selectbox(
        "Whisper Model",
        options=["base", "small", "medium"],
        index=0,
        help="base = fastest / lowest RAM | small = better accuracy | medium = best (needs 4 GB+ RAM)",
    )
with col2:
    chunk_minutes = st.number_input(
        "Chunk threshold (minutes)",
        min_value=1, max_value=10, value=2,
        help="Videos longer than this will be split into 60-second segments to save RAM.",
    )

st.markdown("</div>", unsafe_allow_html=True)  # close jackk-card


# ──────────────────────────────────────────────
# UI: Upload Card
# ──────────────────────────────────────────────
st.markdown("""
<div class="jackk-card">
    <div class="jackk-card-title"><span class="dot"></span> Upload Video</div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Drag & drop your video, or click to browse",
    type=["mp4", "mkv", "mov"],
    label_visibility="collapsed",
)

st.markdown("</div>", unsafe_allow_html=True)


# ──────────────────────────────────────────────
# UI: Action Button + Processing Pipeline
# ──────────────────────────────────────────────
if uploaded_file is not None:
    file_size_mb = uploaded_file.size / (1024 * 1024)
    st.markdown(
        f'<p style="color:#5c5a7a;font-size:.78rem;margin-bottom:1rem;">'
        f'📁 {uploaded_file.name} &nbsp;·&nbsp; {file_size_mb:.1f} MB &nbsp;·&nbsp; '
        f'{uploaded_file.type}</p>',
        unsafe_allow_html=True,
    )

    col_btn, _ = st.columns([1, 3])
    with col_btn:
        run_btn = st.button("🚀 Generate Hindi Subtitles", use_container_width=True)

    if run_btn:
        # ── Spinner / log placeholder ──
        log_placeholder     = st.empty()
        progress_bar        = st.progress(0)
        status_text         = st.empty()
        log_lines: list[str] = []

        def log(msg: str, cls: str = ""):
            tag = f'<span class="{cls}">{msg}</span>' if cls else msg
            log_lines.append(tag)
            log_placeholder.markdown(
                '<div class="log-box">' + "<br>".join(log_lines[-12:]) + "</div>",
                unsafe_allow_html=True,
            )

        log("▶ Pipeline started…")

        # ── Write uploaded file to temp path ──
        with tempfile.TemporaryDirectory() as tmp_dir:
            video_path = os.path.join(tmp_dir, uploaded_file.name)
            audio_path = os.path.join(tmp_dir, "audio_16k.wav")

            with open(video_path, "wb") as f:
                f.write(uploaded_file.read())
            log(f"✔ Saved video → {Path(video_path).name}", "ok")

            # ── Extract audio ──
            try:
                progress_bar.progress(0.05)
                status_text.markdown(
                    '<p style="color:#a09ec0;font-size:.85rem;">🎞️ Extracting audio from video…</p>',
                    unsafe_allow_html=True,
                )
                duration = extract_audio(video_path, audio_path)
                log(f"✔ Audio extracted — duration: {duration:.1f}s ({duration/60:.1f} min)", "ok")
                progress_bar.progress(0.15)
            except Exception as exc:
                st.error(f"❌ Audio extraction failed: {exc}")
                log(f"✘ {exc}", "err")
                st.stop()

            # ── Transcribe ──
            try:
                segments = transcribe(
                    audio_path       = audio_path,
                    duration         = duration,
                    model_size       = model_size,
                    progress_bar     = progress_bar,
                    status_text      = status_text,
                    chunk_threshold_secs = chunk_minutes * 60,
                )
                log(f"✔ Transcription complete — {len(segments)} segments", "ok")
            except Exception as exc:
                st.error(f"❌ Transcription failed: {exc}")
                log(f"✘ {exc}", "err")
                st.stop()

            # Temp dir auto-deleted here ────────────────────
            log("✔ Temporary files cleaned up", "ok")

        # ── Build SRT ──
        progress_bar.progress(0.98)
        srt_content   = build_srt(segments)
        plain_text    = "\n".join(seg.text.strip() for seg in segments)

        log(f"✔ SRT file built — {len(srt_content)} chars", "ok")
        progress_bar.progress(1.0)
        status_text.empty()

        # ── SUCCESS BANNER ──────────────────────────────
        st.markdown("<br>", unsafe_allow_html=True)
        st.success(
            f"✅ **Subtitles generated successfully!**  \n"
            f"`{len(segments)}` subtitle blocks · `{duration/60:.1f}` minutes of video  \n"
            f"Model: `{model_size}` · Language: `Hindi (hi)` · Compute: `int8`"
        )

        # ── Preview first 10 lines ──
        preview_lines = plain_text.split("\n")[:10]
        preview_text  = "\n".join(preview_lines)

        st.markdown("""
<div class="jackk-card">
    <div class="jackk-card-title"><span class="dot"></span> Preview · First 10 lines (Hindi)</div>
""", unsafe_allow_html=True)
        st.text_area(
            label       = "Hindi Transcript Preview",
            value       = preview_text,
            height      = 220,
            label_visibility = "collapsed",
        )
        st.markdown("</div>", unsafe_allow_html=True)

        # ── Download Buttons ─────────────────────────────
        base_name = Path(uploaded_file.name)
