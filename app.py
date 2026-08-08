import html
import streamlit as st
from transformers import pipeline


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Review Sentiment Analysis",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="collapsed",
)


# ============================================================
# MODERN GLASS & GRADIENT DARK THEME
# ============================================================

st.markdown(
    """
    <style>

    /* ========================================================
       IMPORT GOOGLE FONTS
       ======================================================== */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    /* ========================================================
       GLOBAL RESET & BASE STYLES
       ======================================================== */

    * {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    .stApp {
        background: radial-gradient(circle at 50% -20%, #1e1b4b 0%, #0f172a 45%, #020617 100%);
        background-attachment: fixed;
        color: #f8fafc;
    }

    .block-container {
        max-width: 820px;
        padding-top: 50px;
        padding-bottom: 60px;
    }

    header, #MainMenu, footer {
        visibility: hidden;
    }

    /* ========================================================
       TYPOGRAPHY & HEADERS
       ======================================================== */

    .app-title {
        text-align: center;
        font-size: 40px;
        font-weight: 800;
        letter-spacing: -1.2px;
        background: linear-gradient(135deg, #ffffff 0%, #cbd5e1 50%, #818cf8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 8px;
    }

    .app-subtitle {
        text-align: center;
        color: #94a3b8;
        font-size: 16px;
        font-weight: 500;
        margin-bottom: 40px;
    }

    .section-title {
        font-size: 16px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        color: #818cf8;
        margin-top: 36px;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    /* ========================================================
       TEXT AREA INPUT
       ======================================================== */

    .stTextArea textarea {
        background-color: rgba(15, 23, 42, 0.65) !important;
        color: #f8fafc !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        border-radius: 14px !important;
        font-size: 15px !important;
        line-height: 1.6 !important;
        padding: 16px !important;
        backdrop-filter: blur(12px);
        box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5);
        transition: all 0.25s ease-in-out !important;
    }

    .stTextArea textarea:focus {
        border-color: #6366f1 !important;
        box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.2) !important;
    }

    /* ========================================================
       BUTTON STYLING
       ======================================================== */

    /* Secondary Example Buttons */
    .stButton > button {
        border-radius: 12px;
        height: 48px;
        font-weight: 600;
        font-size: 14px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        background: rgba(30, 41, 59, 0.5);
        color: #e2e8f0;
        backdrop-filter: blur(8px);
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }

    .stButton > button:hover {
        background: rgba(51, 65, 85, 0.8);
        border-color: rgba(255, 255, 255, 0.25);
        color: #ffffff;
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.25);
    }

    /* Primary Analyze Button */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
        border: none;
        color: #ffffff;
        font-weight: 700;
        font-size: 16px;
        letter-spacing: 0.3px;
        box-shadow: 0 10px 25px -5px rgba(79, 70, 229, 0.5);
    }

    .stButton > button[kind="primary"]:hover {
        background: linear-gradient(135deg, #4338ca 0%, #6d28d9 100%);
        box-shadow: 0 15px 30px -5px rgba(79, 70, 229, 0.7);
        transform: translateY(-2px);
    }

    /* ========================================================
       PROGRESS BAR
       ======================================================== */

    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #6366f1 0%, #a855f7 100%);
        border-radius: 10px;
    }

    .stProgress > div > div {
        background-color: rgba(30, 41, 59, 0.8);
        border-radius: 10px;
        height: 10px;
    }

    /* ========================================================
       DYNAMIC CARDS (GLASSMORPHISM)
       ======================================================== */

    .glass-card {
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 24px;
        margin-top: 14px;
        backdrop-filter: blur(16px);
        box-shadow: 0 20px 40px -15px rgba(0, 0, 0, 0.5);
    }

    /* Main Result Card */
    .result-card-container {
        border-radius: 20px;
        padding: 36px 28px;
        margin-top: 28px;
        text-align: center;
        backdrop-filter: blur(16px);
        position: relative;
        overflow: hidden;
    }

    .result-card-positive {
        background: radial-gradient(circle at top, rgba(16, 185, 129, 0.15) 0%, rgba(15, 23, 42, 0.7) 100%);
        border: 1px solid rgba(16, 185, 129, 0.3);
        box-shadow: 0 20px 40px -15px rgba(16, 185, 129, 0.2);
    }

    .result-card-negative {
        background: radial-gradient(circle at top, rgba(244, 63, 94, 0.15) 0%, rgba(15, 23, 42, 0.7) 100%);
        border: 1px solid rgba(244, 63, 94, 0.3);
        box-shadow: 0 20px 40px -15px rgba(244, 63, 94, 0.2);
    }

    .prediction-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 8px 18px;
        border-radius: 30px;
        font-size: 13px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 16px;
    }

    .badge-positive {
        background: rgba(16, 185, 129, 0.15);
        color: #34d399;
        border: 1px solid rgba(16, 185, 129, 0.3);
    }

    .badge-negative {
        background: rgba(244, 63, 94, 0.15);
        color: #fb7185;
        border: 1px solid rgba(244, 63, 94, 0.3);
    }

    .result-label {
        font-size: 32px;
        font-weight: 800;
        letter-spacing: -0.5px;
        margin-bottom: 8px;
    }

    .result-label.positive {
        color: #10b981;
        text-shadow: 0 0 25px rgba(16, 185, 129, 0.4);
    }

    .result-label.negative {
        color: #f43f5e;
        text-shadow: 0 0 25px rgba(244, 63, 94, 0.4);
    }

    .interpretation {
        color: #cbd5e1;
        font-size: 15px;
        line-height: 1.6;
        max-width: 520px;
        margin: 0 auto;
    }

    .confidence-pill {
        display: inline-block;
        margin-top: 20px;
        padding: 6px 16px;
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        font-size: 13px;
        color: #94a3b8;
    }

    .confidence-pill strong {
        color: #f8fafc;
    }

    /* Highlight Key Value Labels */
    .summary-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 16px;
        margin-top: 8px;
    }

    .summary-item {
        background: rgba(30, 41, 59, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 16px;
    }

    .summary-item-title {
        font-size: 12px;
        color: #64748b;
        text-transform: uppercase;
        font-weight: 700;
        letter-spacing: 0.5px;
        margin-bottom: 6px;
    }

    .summary-item-value {
        font-size: 15px;
        color: #f1f5f9;
        font-weight: 600;
    }

    /* ========================================================
       FOOTER
       ======================================================== */

    .footer {
        text-align: center;
        color: #475569;
        font-size: 13px;
        font-weight: 500;
        margin-top: 60px;
        padding-top: 24px;
        border-top: 1px solid rgba(255, 255, 255, 0.05);
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# MODEL PATH & LOADING
# ============================================================

MODEL_PATH = "./imdb_distilbert_sst2"


@st.cache_resource
def load_model():
    return pipeline(
        "sentiment-analysis", model=MODEL_PATH, tokenizer=MODEL_PATH
    )


try:
    sentiment_pipe = load_model()
except Exception as e:
    st.error("Unable to load the sentiment model.")
    st.code(str(e))
    st.stop()


# ============================================================
# SESSION STATE MANAGEMENT
# ============================================================

if "review_text" not in st.session_state:
    st.session_state.review_text = ""

if "prediction" not in st.session_state:
    st.session_state.prediction = None

if "confidence" not in st.session_state:
    st.session_state.confidence = None


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="app-title">Review Sentiment Intelligence</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="app-subtitle">'
    "Analyze customer feedback, movie reviews, and product opinions instantly"
    "</div>",
    unsafe_allow_html=True,
)


# ============================================================
# REVIEW INPUT SECTION
# ============================================================

st.markdown(
    '<div class="section-title"><span>✍️</span> Write your review</div>',
    unsafe_allow_html=True,
)

review = st.text_area(
    "Review Input",
    value=st.session_state.review_text,
    height=170,
    placeholder="Enter a review or select one of the quick test cases below...",
    label_visibility="collapsed",
)

# Keep session state synced with user input
st.session_state.review_text = review


# ============================================================
# EXAMPLE PRESETS
# ============================================================

st.markdown(
    '<div class="section-title"><span>💡</span> Try an example</div>',
    unsafe_allow_html=True,
)

col1, col2 = st.columns(2)

with col1:
    if st.button("👍 Positive Example", use_container_width=True):
        st.session_state.review_text = (
            "I really enjoyed this movie. "
            "The story was engaging, the acting was excellent, "
            "and the ending was extremely satisfying."
        )
        st.session_state.prediction = None
        st.rerun()

with col2:
    if st.button("👎 Negative Example", use_container_width=True):
        st.session_state.review_text = (
            "This movie was deeply disappointing. "
            "The plot was uninspired, the acting felt flat, "
            "and the pacing was completely off throughout."
        )
        st.session_state.prediction = None
        st.rerun()


# ============================================================
# ACTION BUTTON
# ============================================================

st.write("")

analyze = st.button(
    "Analyze Sentiment", type="primary", use_container_width=True
)


# ============================================================
# RUN INFERENCE
# ============================================================

if analyze:
    current_review = st.session_state.review_text.strip()

    if not current_review:
        st.warning("Please enter a review before running analysis.")
    else:
        with st.spinner("Analyzing text patterns..."):
            result = sentiment_pipe(current_review, truncation=True)[0]

        st.session_state.prediction = result["label"]
        st.session_state.confidence = result["score"]


# ============================================================
# DISPLAY PREDICTION RESULTS
# ============================================================

if st.session_state.prediction is not None:
    label = st.session_state.prediction
    confidence = st.session_state.confidence

    if label == "POSITIVE":
        prediction_text = "Positive Sentiment"
        interpretation = "The model evaluated the text and determined it carries an overall favorable and positive tone."
        result_class = "positive"
        card_class = "result-card-positive"
        badge_class = "badge-positive"
        badge_icon = "🟢"
    else:
        prediction_text = "Negative Sentiment"
        interpretation = "The model evaluated the text and determined it carries an overall unfavorable or critical tone."
        result_class = "negative"
        card_class = "result-card-negative"
        badge_class = "badge-negative"
        badge_icon = "🔴"

    # Main Visual Result Card
    st.markdown(
        f"""
        <div class="result-card-container {card_class}">
            <div class="prediction-badge {badge_class}">
                <span>{badge_icon}</span> Classification Result
            </div>
            <div class="result-label {result_class}">
                {prediction_text}
            </div>
            <div class="interpretation">
                {interpretation}
            </div>
            <div class="confidence-pill">
                Confidence Score: <strong>{confidence:.2%}</strong>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Progress Meter
    st.markdown(
        '<div class="section-title"><span>📊</span> Confidence Score Meter</div>',
        unsafe_allow_html=True,
    )
    st.progress(confidence)

    # Analyzed Content Display
    st.markdown(
        '<div class="section-title"><span>📝</span> Review Analyzed</div>',
        unsafe_allow_html=True,
    )

    safe_review = html.escape(st.session_state.review_text)

    st.markdown(
        f"""
        <div class="glass-card" style="font-size: 15px; line-height: 1.7; color: #cbd5e1;">
            "{safe_review}"
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Key Summary Grid
    st.markdown(
        '<div class="section-title"><span>📋</span> Result Summary</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="summary-grid">
            <div class="summary-item">
                <div class="summary-item-title">Predicted Sentiment</div>
                <div class="summary-item-value">{prediction_text}</div>
            </div>
            <div class="summary-item">
                <div class="summary-item-title">Certainty</div>
                <div class="summary-item-value">{confidence:.2%}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# MODEL EXPLANATION CARD
# ============================================================

st.markdown(
    '<div class="section-title"><span>ℹ️</span> About Sentiment Prediction</div>',
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="glass-card" style="font-size: 14px; line-height: 1.7; color: #94a3b8;">
        <p style="margin-bottom: 12px;">
            This NLP system evaluates structural syntax, context, and word choice within reviews to determine whether the expressed opinion is <b style="color: #34d399;">Positive</b> or <b style="color: #fb7185;">Negative</b>.
        </p>
        <p style="margin-bottom: 12px;">
            <strong>Best Practices:</strong> Provide complete sentences expressing clear opinions. Highly ambiguous, sarcastic, or multi-faceted reviews may impact prediction accuracy.
        </p>
        <p style="margin-bottom: 0;">
            <strong>Note on Confidence:</strong> The percentage represents how strongly the transformer model supports its classification decision.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        Review Sentiment Intelligence &nbsp;•&nbsp; Powered by Hugging Face & Streamlit
    </div>
    """,
    unsafe_allow_html=True,
)