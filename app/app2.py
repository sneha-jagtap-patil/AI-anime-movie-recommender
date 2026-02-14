import streamlit as st
from pipeline.pipeline import AnimeRecommendationPipeline
from dotenv import load_dotenv
import time

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Anime Recommender | Premium",
    page_icon="🎌",
    layout="wide",
    initial_sidebar_state="expanded"
)
load_dotenv()

# Initialize session state for theme
if 'theme' not in st.session_state:
    st.session_state.theme = 'dark'

# ---------------- ULTIMATE PREMIUM CSS ----------------
st.markdown(f"""
    <style>
    /* Import Premium Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Clash+Display:wght@400;600;700&family=Cabinet+Grotesk:wght@400;500;700;800&family=Azeret+Mono:wght@400;600&family=JetBrains+Mono:wght@400;600&display=swap');
    
    /* Theme Variables */
    :root {{
        /* Dark Theme */
        --primary: {'#FF2D55' if st.session_state.theme == 'dark' else '#E63946'};
        --secondary: {'#5E5CE6' if st.session_state.theme == 'dark' else '#457B9D'};
        --accent: {'#FFD60A' if st.session_state.theme == 'dark' else '#F77F00'};
        --bg-main: {'#0A0E27' if st.session_state.theme == 'dark' else '#F8F9FA'};
        --bg-secondary: {'#1A1F3A' if st.session_state.theme == 'dark' else '#FFFFFF'};
        --bg-card: {'rgba(26, 31, 58, 0.8)' if st.session_state.theme == 'dark' else 'rgba(255, 255, 255, 0.9)'};
        --text-primary: {'#E5E7EB' if st.session_state.theme == 'dark' else '#1A1A1A'};
        --text-secondary: {'#9CA3AF' if st.session_state.theme == 'dark' else '#6B7280'};
        --border-color: {'rgba(255, 255, 255, 0.1)' if st.session_state.theme == 'dark' else 'rgba(0, 0, 0, 0.1)'};
        --shadow-color: {'rgba(0, 0, 0, 0.4)' if st.session_state.theme == 'dark' else 'rgba(0, 0, 0, 0.1)'};
    }}
    
    /* Hide Streamlit Elements */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
    
    /* Animated Background */
    .stApp {{
        background: {'linear-gradient(135deg, #0A0E27 0%, #1A1F3A 25%, #2D1B3D 50%, #1A1F3A 75%, #0A0E27 100%)' if st.session_state.theme == 'dark' else 'linear-gradient(135deg, #F8F9FA 0%, #E9ECEF 50%, #F8F9FA 100%)'};
        background-size: 400% 400%;
        animation: gradientShift 20s ease infinite;
        font-family: 'Cabinet Grotesk', sans-serif;
        color: var(--text-primary);
        transition: all 0.5s ease;
    }}
    
    @keyframes gradientShift {{
        0%, 100% {{ background-position: 0% 50%; }}
        50% {{ background-position: 100% 50%; }}
    }}
    
    /* Particle Effect Layer */
    .stApp::before {{
        content: '';
        position: fixed;
        top: 0; left: 0;
        width: 100%; height: 100%;
        background-image: 
            radial-gradient(circle at 20% 30%, {'rgba(255, 45, 85, 0.15)' if st.session_state.theme == 'dark' else 'rgba(230, 57, 70, 0.08)'} 0%, transparent 50%),
            radial-gradient(circle at 80% 70%, {'rgba(94, 92, 230, 0.15)' if st.session_state.theme == 'dark' else 'rgba(69, 123, 157, 0.08)'} 0%, transparent 50%),
            radial-gradient(circle at 50% 50%, {'rgba(255, 214, 10, 0.08)' if st.session_state.theme == 'dark' else 'rgba(247, 127, 0, 0.05)'} 0%, transparent 50%);
        pointer-events: none;
        z-index: 0;
        animation: pulse 10s ease-in-out infinite;
    }}
    
    @keyframes pulse {{
        0%, 100% {{ opacity: 0.4; }}
        50% {{ opacity: 0.7; }}
    }}
    
    /* Container */
    .block-container {{
        max-width: 1600px;
        padding: 4rem 3rem;
        position: relative;
        z-index: 1;
    }}
    
    /* Hero Section */
    .hero-section {{
        text-align: center;
        margin-bottom: 5rem;
        animation: fadeInDown 1s cubic-bezier(0.4, 0, 0.2, 1);
    }}
    
    @keyframes fadeInDown {{
        from {{ opacity: 0; transform: translateY(-40px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    
    .badge {{
        display: inline-block;
        background: linear-gradient(135deg, var(--primary), var(--secondary));
        color: white;
        padding: 0.5rem 1.5rem;
        border-radius: 50px;
        font-family: 'Azeret Mono', monospace;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.15em;
        font-weight: 600;
        margin-bottom: 1.5rem;
        box-shadow: 0 8px 24px rgba(255, 45, 85, 0.3);
        animation: float 3s ease-in-out infinite;
    }}
    
    @keyframes float {{
        0%, 100% {{ transform: translateY(0px); }}
        50% {{ transform: translateY(-12px); }}
    }}
    
    .main-title {{
        font-family: 'Clash Display', sans-serif;
        font-size: clamp(3.5rem, 10vw, 7rem);
        font-weight: 700;
        background: linear-gradient(135deg, 
            var(--primary) 0%, 
            var(--accent) 50%, 
            var(--secondary) 100%
        );
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        letter-spacing: -0.03em;
        line-height: 1;
        margin: 1rem 0 1.5rem;
        position: relative;
        display: inline-block;
        animation: titleGlow 4s ease-in-out infinite;
    }}
    
    @keyframes titleGlow {{
        0%, 100% {{ 
            filter: drop-shadow(0 0 30px {'rgba(255, 45, 85, 0.5)' if st.session_state.theme == 'dark' else 'rgba(230, 57, 70, 0.3)'}); 
        }}
        50% {{ 
            filter: drop-shadow(0 0 60px {'rgba(255, 45, 85, 0.8)' if st.session_state.theme == 'dark' else 'rgba(230, 57, 70, 0.5)'}); 
        }}
    }}
    
    .tagline {{
        font-size: clamp(1.2rem, 3vw, 1.8rem);
        color: var(--text-secondary);
        font-weight: 400;
        max-width: 700px;
        margin: 0 auto;
        line-height: 1.6;
        opacity: 0.95;
        animation: fadeIn 1.2s ease 0.5s both;
    }}
    
    @keyframes fadeIn {{
        from {{ opacity: 0; }}
        to {{ opacity: 1; }}
    }}
    
    /* Premium Glass Card */
    .glass-card {{
        background: var(--bg-card);
        backdrop-filter: blur(30px);
        -webkit-backdrop-filter: blur(30px);
        border: 1px solid var(--border-color);
        border-radius: 32px;
        padding: 3rem;
        box-shadow: 
            0 20px 60px var(--shadow-color),
            inset 0 1px 0 {'rgba(255, 255, 255, 0.1)' if st.session_state.theme == 'dark' else 'rgba(255, 255, 255, 0.8)'};
        transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }}
    
    .glass-card::before {{
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg,
            transparent 30%,
            {'rgba(255, 255, 255, 0.1)' if st.session_state.theme == 'dark' else 'rgba(255, 255, 255, 0.5)'} 50%,
            transparent 70%
        );
        transform: rotate(45deg);
        transition: all 0.6s;
        opacity: 0;
    }}
    
    .glass-card:hover::before {{
        left: 100%;
        opacity: 1;
    }}
    
    .glass-card:hover {{
        transform: translateY(-12px) scale(1.01);
        box-shadow: 
            0 30px 80px {'rgba(255, 45, 85, 0.4)' if st.session_state.theme == 'dark' else 'rgba(230, 57, 70, 0.2)'},
            inset 0 1px 0 {'rgba(255, 255, 255, 0.2)' if st.session_state.theme == 'dark' else 'rgba(255, 255, 255, 1)'};
        border-color: {'rgba(255, 45, 85, 0.4)' if st.session_state.theme == 'dark' else 'rgba(230, 57, 70, 0.3)'};
    }}
    
    /* Enhanced Input */
    .stTextInput > div > div > input {{
        background: var(--bg-card) !important;
        border: 2px solid var(--border-color) !important;
        border-radius: 20px !important;
        color: var(--text-primary) !important;
        font-size: 1.2rem !important;
        padding: 1.8rem 2rem !important;
        font-family: 'Cabinet Grotesk', sans-serif !important;
        font-weight: 500 !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 8px 24px var(--shadow-color) !important;
    }}
    
    .stTextInput > div > div > input:focus {{
        border-color: var(--primary) !important;
        box-shadow: 
            0 0 0 4px {'rgba(255, 45, 85, 0.2)' if st.session_state.theme == 'dark' else 'rgba(230, 57, 70, 0.15)'} !important,
            0 12px 32px var(--shadow-color) !important;
        transform: translateY(-2px) !important;
    }}
    
    .stTextInput > div > div > input::placeholder {{
        color: var(--text-secondary) !important;
        font-style: italic !important;
        opacity: 0.7 !important;
    }}
    
    /* Anime Recommendation Card */
    .anime-card {{
        background: linear-gradient(135deg,
            {'rgba(255, 45, 85, 0.12)' if st.session_state.theme == 'dark' else 'rgba(230, 57, 70, 0.08)'} 0%,
            {'rgba(94, 92, 230, 0.12)' if st.session_state.theme == 'dark' else 'rgba(69, 123, 157, 0.08)'} 100%
        );
        backdrop-filter: blur(20px);
        border: 2px solid {'rgba(255, 45, 85, 0.2)' if st.session_state.theme == 'dark' else 'rgba(230, 57, 70, 0.15)'};
        border-radius: 28px;
        padding: 3rem;
        margin: 2.5rem 0;
        box-shadow: 
            0 20px 60px var(--shadow-color),
            inset 0 1px 0 {'rgba(255, 255, 255, 0.15)' if st.session_state.theme == 'dark' else 'rgba(255, 255, 255, 0.8)'};
        animation: slideInScale 0.8s cubic-bezier(0.34, 1.56, 0.64, 1);
        position: relative;
        overflow: hidden;
        font-size: 1.05rem;
        line-height: 1.8;
    }}
    
    @keyframes slideInScale {{
        from {{
            opacity: 0;
            transform: translateY(40px) scale(0.95);
        }}
        to {{
            opacity: 1;
            transform: translateY(0) scale(1);
        }}
    }}
    
    .anime-card::after {{
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, 
            {'rgba(255, 45, 85, 0.15)' if st.session_state.theme == 'dark' else 'rgba(230, 57, 70, 0.08)'}, 
            transparent 70%
        );
        animation: rotate 15s linear infinite;
        pointer-events: none;
    }}
    
    @keyframes rotate {{
        from {{ transform: rotate(0deg); }}
        to {{ transform: rotate(360deg); }}
    }}
    
    /* Sidebar Premium Styling */
    section[data-testid="stSidebar"] {{
        background: var(--bg-secondary);
        backdrop-filter: blur(30px);
        border-right: 1px solid var(--border-color);
        box-shadow: 4px 0 24px var(--shadow-color);
    }}
    
    section[data-testid="stSidebar"] > div {{
        padding: 2.5rem 2rem;
    }}
    
    section[data-testid="stSidebar"] h2 {{
        font-family: 'Clash Display', sans-serif !important;
        font-size: 2rem !important;
        background: linear-gradient(135deg, var(--primary), var(--secondary));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 700 !important;
        margin-bottom: 2rem !important;
        letter-spacing: -0.02em !important;
    }}
    
    /* Enhanced Selectbox */
    .stSelectbox > div > div {{
        background: var(--bg-card) !important;
        border: 1.5px solid var(--border-color) !important;
        border-radius: 16px !important;
        color: var(--text-primary) !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 12px var(--shadow-color) !important;
    }}
    
    .stSelectbox > div > div:hover {{
        border-color: var(--primary) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 20px var(--shadow-color) !important;
    }}
    
    /* Labels */
    label {{
        font-family: 'Azeret Mono', monospace !important;
        text-transform: uppercase !important;
        letter-spacing: 0.12em !important;
        font-size: 0.8rem !important;
        color: var(--text-secondary) !important;
        font-weight: 600 !important;
        margin-bottom: 0.8rem !important;
        display: block !important;
    }}
    
    /* Info/Success Boxes */
    .stInfo {{
        background: linear-gradient(135deg,
            {'rgba(94, 92, 230, 0.2)' if st.session_state.theme == 'dark' else 'rgba(69, 123, 157, 0.1)'} 0%,
            {'rgba(255, 45, 85, 0.2)' if st.session_state.theme == 'dark' else 'rgba(230, 57, 70, 0.1)'} 100%
        ) !important;
        border-left: 4px solid var(--primary) !important;
        border-radius: 16px !important;
        backdrop-filter: blur(10px) !important;
        padding: 1.5rem !important;
        box-shadow: 0 8px 20px var(--shadow-color) !important;
    }}
    
    .stSuccess {{
        background: linear-gradient(135deg,
            rgba(52, 211, 153, 0.2) 0%,
            rgba(16, 185, 129, 0.2) 100%
        ) !important;
        border-left: 4px solid #10B981 !important;
        border-radius: 16px !important;
        color: {'#D1FAE5' if st.session_state.theme == 'dark' else '#065F46'} !important;
        font-weight: 500 !important;
        padding: 1.5rem !important;
        box-shadow: 0 8px 20px var(--shadow-color) !important;
    }}
    
    /* Section Headers */
    h2 {{
        font-family: 'Clash Display', sans-serif !important;
        font-size: 3rem !important;
        color: var(--text-primary) !important;
        margin: 4rem 0 2rem !important;
        font-weight: 700 !important;
        letter-spacing: -0.02em !important;
        position: relative !important;
        display: inline-block !important;
    }}
    
    h2::after {{
        content: '';
        position: absolute;
        bottom: -12px;
        left: 0;
        width: 80px;
        height: 5px;
        background: linear-gradient(90deg, var(--primary), var(--accent));
        border-radius: 3px;
        box-shadow: 0 2px 8px var(--primary);
    }}
    
    /* Spinner */
    .stSpinner > div {{
        border-top-color: var(--primary) !important;
        border-right-color: var(--secondary) !important;
    }}
    
    /* Divider */
    hr {{
        border: none !important;
        height: 2px !important;
        background: linear-gradient(90deg,
            transparent,
            var(--border-color),
            transparent
        ) !important;
        margin: 4rem 0 !important;
    }}
    
    /* Scrollbar */
    ::-webkit-scrollbar {{
        width: 12px;
    }}
    
    ::-webkit-scrollbar-track {{
        background: var(--bg-main);
    }}
    
    ::-webkit-scrollbar-thumb {{
        background: linear-gradient(180deg, var(--primary), var(--secondary));
        border-radius: 6px;
        border: 2px solid var(--bg-main);
    }}
    
    ::-webkit-scrollbar-thumb:hover {{
        background: linear-gradient(180deg, var(--secondary), var(--accent));
    }}
    
    /* Responsive */
    @media (max-width: 768px) {{
        .block-container {{ padding: 2rem 1.5rem; }}
        .glass-card {{ padding: 2rem; }}
        .main-title {{ font-size: 3rem; }}
        h2 {{ font-size: 2rem !important; }}
    }}
    </style>
""", unsafe_allow_html=True)

# ---------------- PIPELINE INIT ----------------
@st.cache_resource
def init_pipeline():
    return AnimeRecommendationPipeline()

pipeline = init_pipeline()

# ---------------- HERO SECTION ----------------
st.markdown("""
    <div class="hero-section">
        <div class="badge">✨ AI-Powered Premium Experience</div>
        <h1 class="main-title">
            ANIME ORACLE
        </h1>
        <p class="tagline">
            Discover your perfect anime match with intelligent, personalized recommendations
        </p>
    </div>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.markdown('<h2>🎯 Preferences</h2>', unsafe_allow_html=True)
    
    # Genre Selection
    genre = st.selectbox(
        "Genre",
        ["Any", "Action", "Adventure", "Romance", "Comedy", "Drama", 
         "Fantasy", "Horror", "Mystery", "Sci-Fi", "Slice of Life", 
         "Thriller", "Supernatural", "Sports"],
        help="Choose your preferred anime genre"
    )
    
    # Mood Selection
    mood = st.selectbox(
        "Mood",
        ["Any", "Light Hearted", "Emotional", "Dark", "Thrilling", 
         "Inspiring", "Chill", "Intense", "Wholesome"],
        help="What's your current vibe?"
    )
    
    # Additional Filters
    with st.expander("🎨 Advanced Filters"):
        era = st.selectbox(
            "Era",
            ["Any", "Classic (Pre-2000)", "Modern (2000-2015)", "Recent (2015+)"],
            help="Prefer a specific time period?"
        )
        
        length = st.selectbox(
            "Series Length",
            ["Any", "Short (1-12 episodes)", "Medium (13-26 episodes)", 
             "Long (27+ episodes)", "Movies"],
            help="How much time do you have?"
        )
    
    st.markdown("---")
    
    # Stats
    st.info("""
        🚀 **Powered By**
        
        • LangChain RAG
        • Groq LLM (70B)
        • ChromaDB Vector Store
        • 1000+ Anime Database
        
        Made with 💜 for otakus
    """)
    
    # Credits
    st.markdown("""
        <div style="text-align: center; margin-top: 2rem; opacity: 0.6;">
            <p style="font-size: 0.75rem; font-family: 'Azeret Mono', monospace;">
                v2.0 Premium Edition
            </p>
        </div>
    """, unsafe_allow_html=True)

# ---------------- MAIN INPUT ----------------
st.markdown('<div class="glass-card" style="animation: fadeInUp 0.8s ease 0.3s both;">', unsafe_allow_html=True)

query = st.text_input(
    "Describe your ideal anime:",
    placeholder="E.g., A thought-provoking psychological thriller with mind-bending plot twists...",
    help="Be specific! Mention themes, art style, pacing, or anything that matters to you.",
    label_visibility="collapsed"
)

st.markdown('</div>', unsafe_allow_html=True)

# ---------------- RECOMMENDATION ENGINE ----------------
if query:
    # Build comprehensive query
    full_query = query
    
    filters = []
    if genre != "Any":
        filters.append(f"Genre: {genre}")
    if mood != "Any":
        filters.append(f"Mood: {mood}")
    if 'era' in locals() and era != "Any":
        filters.append(f"Era: {era}")
    if 'length' in locals() and length != "Any":
        filters.append(f"Length: {length}")
    
    if filters:
        full_query += f". Preferences: {', '.join(filters)}."
    
    # Animated Loading
    with st.spinner("🔮 Analyzing your preferences across thousands of anime..."):
        progress_text = st.empty()
        
        # Simulated progress for UX
        progress_text.markdown("⚡ Searching database...")
        time.sleep(0.5)
        progress_text.markdown("🧠 AI analyzing your taste...")
        time.sleep(0.7)
        progress_text.markdown("🎯 Finding perfect matches...")
        time.sleep(0.5)
        
        # Get actual recommendation
        response = pipeline.recommend(full_query)
        
        progress_text.empty()
    
    # Display Results
    st.markdown('<h2>🎬 Your Perfect Matches</h2>', unsafe_allow_html=True)
    
    st.markdown(
        f"""
        <div class="anime-card">
            {response}
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Success message
    st.success("🍿 Enjoy your anime adventure! Come back anytime for more recommendations 🌟")
    
    # Quick Actions
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🔄 New Recommendation", use_container_width=True):
            st.rerun()
    with col2:
        if st.button("💾 Save to List", use_container_width=True):
            st.info("Feature coming soon!")
    with col3:
        if st.button("📤 Share", use_container_width=True):
            st.info("Share feature coming soon!")

else:
    # Empty state with examples
    st.markdown("""
        <div class="glass-card" style="text-align: center; padding: 4rem 2rem; animation: fadeIn 1s ease 0.8s both;">
            <h3 style="font-size: 1.8rem; margin-bottom: 1.5rem; color: var(--text-primary);">
                🎯 Not sure what to watch?
            </h3>
            <p style="color: var(--text-secondary); margin-bottom: 2rem; font-size: 1.1rem;">
                Try these example searches:
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("💭 Deep philosophical anime", use_container_width=True):
            st.session_state.example_query = "Deep philosophical anime that makes you question reality"
            st.rerun()
    
    with col2:
        if st.button("😂 Comedy to brighten my day", use_container_width=True):
            st.session_state.example_query = "Hilarious comedy anime with great character dynamics"
            st.rerun()
    
    with col3:
        if st.button("⚔️ Epic fantasy adventure", use_container_width=True):
            st.session_state.example_query = "Epic fantasy adventure with world-building and magic"
            st.rerun()

# ---------------- FOOTER ----------------
st.markdown("---")
st.markdown("""
    <div style="text-align: center; padding: 3rem 0;">
        <p style="font-family: 'Clash Display', sans-serif; font-size: 1.2rem; margin-bottom: 0.5rem;">
            🎌 Built by anime lovers, for anime lovers
        </p>
        <p style="font-family: 'Azeret Mono', monospace; font-size: 0.85rem; color: var(--text-secondary); opacity: 0.7;">
            Discover • Watch • Repeat
        </p>
    </div>
""", unsafe_allow_html=True)