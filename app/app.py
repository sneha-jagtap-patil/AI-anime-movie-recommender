import streamlit as st
from pipeline.pipeline import AnimeRecommendationPipeline
from dotenv import load_dotenv
import time

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Anime Recommender",
    page_icon="🎌",
    layout="wide",
)
load_dotenv()

# ---------------- NEXT-LEVEL CUSTOM CSS ----------------
st.markdown("""
    <style>
    /* Import gorgeous fonts */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=Space+Mono:wght@400;700&family=Kanit:wght@300;500;700&display=swap');
    
    /* Global Reset & Base Styles */
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    /* Custom CSS Variables */
    :root {
        --primary: #FF2D55;
        --secondary: #5E5CE6;
        --accent: #FFD60A;
        --bg-dark: #0A0E27;
        --bg-card: #1A1F3A;
        --text-light: #E5E7EB;
        --text-muted: #9CA3AF;
        --glass-bg: rgba(26, 31, 58, 0.7);
        --glow: rgba(255, 45, 85, 0.4);
    }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main Background with Animated Gradient */
    .stApp {
        background: linear-gradient(135deg, 
            #0A0E27 0%, 
            #1A1F3A 25%,
            #2D1B3D 50%,
            #1A1F3A 75%,
            #0A0E27 100%
        );
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
        font-family: 'Outfit', sans-serif;
        color: var(--text-light);
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Animated Particles Background */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            radial-gradient(circle at 20% 30%, rgba(255, 45, 85, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 80% 70%, rgba(94, 92, 230, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 50% 50%, rgba(255, 214, 10, 0.05) 0%, transparent 50%);
        pointer-events: none;
        z-index: 0;
        animation: pulse 8s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 0.3; }
        50% { opacity: 0.6; }
    }
    
    /* Main Container */
    .block-container {
        max-width: 1400px;
        padding: 3rem 2rem;
        position: relative;
        z-index: 1;
    }
    
    /* Hero Header Section */
    .hero-section {
        text-align: center;
        margin-bottom: 4rem;
        animation: fadeInDown 0.8s ease-out;
    }
    
    @keyframes fadeInDown {
        from {
            opacity: 0;
            transform: translateY(-30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .main-title {
        font-family: 'Kanit', sans-serif;
        font-size: clamp(3rem, 8vw, 5.5rem);
        font-weight: 800;
        background: linear-gradient(135deg, #FF2D55 0%, #FFD60A 50%, #5E5CE6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-shadow: 0 0 80px rgba(255, 45, 85, 0.3);
        letter-spacing: -0.02em;
        line-height: 1.1;
        margin-bottom: 1rem;
        animation: glow 3s ease-in-out infinite;
    }
    
    @keyframes glow {
        0%, 100% { filter: drop-shadow(0 0 20px rgba(255, 45, 85, 0.4)); }
        50% { filter: drop-shadow(0 0 40px rgba(255, 45, 85, 0.8)); }
    }
    
    .subtitle {
        font-family: 'Space Mono', monospace;
        font-size: clamp(1rem, 2vw, 1.3rem);
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 0.3em;
        margin-bottom: 0.5rem;
        animation: fadeIn 1s ease-out 0.3s both;
    }
    
    .tagline {
        font-size: clamp(1.1rem, 2.5vw, 1.5rem);
        color: var(--text-light);
        font-weight: 300;
        max-width: 600px;
        margin: 0 auto 3rem;
        opacity: 0.9;
        animation: fadeIn 1s ease-out 0.6s both;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    /* Glass Morphism Cards */
    .glass-card {
        background: var(--glass-bg);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 24px;
        padding: 2.5rem;
        box-shadow: 
            0 8px 32px rgba(0, 0, 0, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .glass-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, 
            transparent, 
            rgba(255, 255, 255, 0.1), 
            transparent
        );
        transition: left 0.5s;
    }
    
    .glass-card:hover::before {
        left: 100%;
    }
    
    .glass-card:hover {
        transform: translateY(-8px);
        box-shadow: 
            0 20px 60px rgba(255, 45, 85, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.2);
        border-color: rgba(255, 45, 85, 0.3);
    }
    
    /* Input Container */
    .input-section {
        margin: 3rem 0;
        animation: fadeInUp 0.8s ease-out 0.4s both;
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Style Streamlit Input */
    .stTextInput > div > div > input {
        background: rgba(26, 31, 58, 0.8) !important;
        border: 2px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 16px !important;
        color: var(--text-light) !important;
        font-size: 1.1rem !important;
        padding: 1.5rem 1.5rem !important;
        font-family: 'Outfit', sans-serif !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 3px rgba(255, 45, 85, 0.2) !important;
        background: rgba(26, 31, 58, 0.95) !important;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: var(--text-muted) !important;
        font-style: italic !important;
    }
    
    /* Recommendation Cards */
    .anime-card {
        background: linear-gradient(135deg, 
            rgba(255, 45, 85, 0.1) 0%, 
            rgba(94, 92, 230, 0.1) 100%
        );
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 20px;
        padding: 2.5rem;
        margin: 2rem 0;
        box-shadow: 
            0 10px 40px rgba(0, 0, 0, 0.4),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
        animation: slideIn 0.6s ease-out;
        position: relative;
        overflow: hidden;
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateX(-50px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    .anime-card::before {
        content: '';
        position: absolute;
        top: -2px;
        left: -2px;
        right: -2px;
        bottom: -2px;
        background: linear-gradient(45deg, 
            var(--primary), 
            var(--accent), 
            var(--secondary), 
            var(--primary)
        );
        background-size: 300% 300%;
        border-radius: 20px;
        z-index: -1;
        opacity: 0;
        animation: borderGlow 3s linear infinite;
        transition: opacity 0.3s;
    }
    
    .anime-card:hover::before {
        opacity: 0.6;
    }
    
    @keyframes borderGlow {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, 
            rgba(26, 31, 58, 0.95) 0%, 
            rgba(10, 14, 39, 0.95) 100%
        );
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    section[data-testid="stSidebar"] > div {
        padding: 2rem 1.5rem;
    }
    
    /* Sidebar Header */
    section[data-testid="stSidebar"] h2 {
        font-family: 'Kanit', sans-serif;
        font-size: 1.8rem;
        color: var(--primary);
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 2rem;
        text-shadow: 0 0 20px rgba(255, 45, 85, 0.5);
    }
    
    /* Selectbox Styling */
    .stSelectbox > div > div {
        background: rgba(26, 31, 58, 0.6) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        color: var(--text-light) !important;
        transition: all 0.3s ease !important;
    }
    
    .stSelectbox > div > div:hover {
        border-color: rgba(255, 45, 85, 0.5) !important;
        background: rgba(26, 31, 58, 0.8) !important;
    }
    
    /* Labels */
    label {
        font-family: 'Space Mono', monospace !important;
        text-transform: uppercase !important;
        letter-spacing: 0.1em !important;
        font-size: 0.85rem !important;
        color: var(--text-muted) !important;
        font-weight: 600 !important;
    }
    
    /* Info Box */
    .stInfo {
        background: linear-gradient(135deg, 
            rgba(94, 92, 230, 0.2) 0%, 
            rgba(255, 45, 85, 0.2) 100%
        ) !important;
        border-left: 4px solid var(--primary) !important;
        border-radius: 12px !important;
        padding: 1rem !important;
        backdrop-filter: blur(10px) !important;
    }
    
    /* Success Message */
    .stSuccess {
        background: linear-gradient(135deg, 
            rgba(52, 211, 153, 0.2) 0%, 
            rgba(16, 185, 129, 0.2) 100%
        ) !important;
        border-left: 4px solid #10B981 !important;
        border-radius: 12px !important;
        color: #D1FAE5 !important;
        font-weight: 500 !important;
    }
    
    /* Spinner */
    .stSpinner > div {
        border-top-color: var(--primary) !important;
    }
    
    /* Section Titles */
    h2 {
        font-family: 'Kanit', sans-serif !important;
        font-size: 2.5rem !important;
        color: var(--text-light) !important;
        margin: 3rem 0 1.5rem !important;
        letter-spacing: -0.02em !important;
        position: relative !important;
        display: inline-block !important;
    }
    
    h2::after {
        content: '';
        position: absolute;
        bottom: -8px;
        left: 0;
        width: 60px;
        height: 4px;
        background: linear-gradient(90deg, var(--primary), var(--accent));
        border-radius: 2px;
    }
    
    /* Floating Elements */
    .floating {
        animation: float 3s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    /* Emoji Styling */
    .emoji {
        display: inline-block;
        font-size: 1.5em;
        margin-right: 0.5rem;
        filter: drop-shadow(0 2px 8px rgba(255, 45, 85, 0.4));
    }
    
    /* Divider */
    hr {
        border: none !important;
        height: 1px !important;
        background: linear-gradient(90deg, 
            transparent, 
            rgba(255, 255, 255, 0.2), 
            transparent
        ) !important;
        margin: 3rem 0 !important;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(10, 14, 39, 0.5);
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, var(--primary), var(--secondary));
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(180deg, var(--secondary), var(--primary));
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .block-container {
            padding: 2rem 1rem;
        }
        
        .glass-card {
            padding: 1.5rem;
        }
        
        .main-title {
            font-size: 2.5rem;
        }
    }
    </style>
""", unsafe_allow_html=True)

# ---------------- PIPELINE INIT ----------------
@st.cache_resource
def init_pipeline():
    return AnimeRecommendationPipeline()

pipeline = init_pipeline()

# ---------------- HERO HEADER ----------------
st.markdown("""
    <div class="hero-section">
        <div class="subtitle">✨ Powered by AI ✨</div>
        <h1 class="main-title floating">
            <span class="emoji">🎌</span>
            ANIME FINDER
        </h1>
        <p class="tagline">
            Discover your next obsession with intelligent recommendations
        </p>
    </div>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.markdown('<h2><span class="emoji">⚙️</span>Filters</h2>', unsafe_allow_html=True)
    
    genre = st.selectbox(
        "Preferred Genre",
        ["Any", "Action", "Romance", "Comedy", "Fantasy", "Horror", "Slice of Life", "Thriller", "Mystery", "Sci-Fi"],
        help="Choose your favorite anime genre"
    )
    
    mood = st.selectbox(
        "Current Mood",
        ["Any", "Light Hearted", "Emotional", "Dark", "Thrilling", "Inspiring", "Chill"],
        help="What vibe are you feeling?"
    )
    
    st.markdown("---")
    
    st.info("""
        🤖 **Powered By**
        - LangChain
        - Groq LLM
        - ChromaDB
        
        Built with ❤️ for anime lovers
    """)

# ---------------- MAIN INPUT SECTION ----------------
st.markdown('<div class="input-section">', unsafe_allow_html=True)

query = st.text_input(
    "What kind of anime are you looking for?",
    placeholder="Example: Emotional romance anime with beautiful animation and character development...",
    help="Be as specific as you want! The AI understands nuance.",
    label_visibility="collapsed"
)

st.markdown('</div>', unsafe_allow_html=True)

# ---------------- RECOMMENDATION LOGIC ----------------
if query:
    # Build enhanced query
    full_query = f"{query}"
    if genre != "Any":
        full_query += f" Genre preference: {genre}."
    if mood != "Any":
        full_query += f" Mood: {mood}."
    
    # Loading animation
    with st.spinner("🔮 Analyzing thousands of anime to find your perfect match..."):
        time.sleep(1.5)  # Smooth loading experience
        response = pipeline.recommend(full_query)
    
    # Display recommendations
    st.markdown('<h2><span class="emoji">🎬</span>Your Perfect Picks</h2>', unsafe_allow_html=True)
    
    st.markdown(
        f"""
        <div class="anime-card">
            {response}
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.success("🍿 Enjoy your anime marathon! Don't forget to hydrate 💧")

# ---------------- FOOTER ----------------
st.markdown("---")
st.markdown("""
    <div style="text-align: center; opacity: 0.6; padding: 2rem 0;">
        <p style="font-family: 'Space Mono', monospace; font-size: 0.9rem;">
            Made with 💜 by anime enthusiasts, for anime enthusiasts
        </p>
    </div>
""", unsafe_allow_html=True)