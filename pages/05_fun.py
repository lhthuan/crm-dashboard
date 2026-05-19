"""
Joke Generator page - Random jokes for fun!
"""

import streamlit as st
import requests
import json
from datetime import datetime

st.set_page_config(page_title="Fun Zone", page_icon="😂", layout="wide")

st.title("😂 Fun Zone - Random Joke Generator")
st.markdown("Take a break and enjoy some laughs!")

st.markdown("---")

# Joke APIs
JOKE_APIS = {
    "Official Joke API": "https://official-joke-api.appspot.com/random_joke",
    "JokeAPI (Single)": "https://jokeapi.dev/random?type=single",
    "Random Useless Facts": "https://uselessfacts.jsoup.com/random.json",
}

# Sidebar settings
st.sidebar.markdown("### ⚙️ Settings")
selected_api = st.sidebar.selectbox("Select Joke Source", list(JOKE_APIS.keys()))

# Initialize session state
if 'joke_history' not in st.session_state:
    st.session_state.joke_history = []

if 'last_joke' not in st.session_state:
    st.session_state.last_joke = None

# Function to fetch joke
def fetch_joke(api_name):
    """Fetch a random joke from selected API"""
    url = JOKE_APIS[api_name]
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        return data, None
    except requests.exceptions.RequestException as e:
        return None, f"Error fetching joke: {str(e)}"

# Function to format joke
def format_joke(data, api_name):
    """Format joke data based on source"""
    if api_name == "Official Joke API":
        setup = data.get('setup', '')
        punchline = data.get('punchline', '')
        return f"**{setup}**\n\n*{punchline}*"
    
    elif api_name == "JokeAPI (Single)":
        joke = data.get('joke', '')
        return f"*{joke}*"
    
    elif api_name == "Random Useless Facts":
        fact = data.get('text', '')
        return f"**Fun Fact:** {fact}"
    
    return "No joke available"

# Main joke display area
st.markdown("### 🎭 Today's Joke")

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    if st.button("🎲 Get Random Joke", use_container_width=True, key="joke_button"):
        data, error = fetch_joke(selected_api)
        
        if error:
            st.error(error)
        else:
            joke_text = format_joke(data, selected_api)
            st.session_state.last_joke = {
                'text': joke_text,
                'source': selected_api,
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            st.session_state.joke_history.append(st.session_state.last_joke)

# Display last joke
if st.session_state.last_joke:
    st.markdown("---")
    
    # Joke card
    st.markdown(f"""
        <div style="background-color: #f0f2f6; padding: 2rem; border-radius: 0.5rem; text-align: center;">
            {st.session_state.last_joke['text']}
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"*Source: {st.session_state.last_joke['source']} | {st.session_state.last_joke['timestamp']}*")
    
    # Action buttons
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("👍 Funny", use_container_width=True):
            st.success("Glad you enjoyed it! 😄")
    with col2:
        if st.button("😐 Not Funny", use_container_width=True):
            st.info("Let's try another one!")
    with col3:
        if st.button("📋 Copy", use_container_width=True):
            st.code(st.session_state.last_joke['text'], language="text")

st.markdown("---")

# Joke history
if st.session_state.joke_history:
    st.markdown("### 📜 Joke History")
    
    if st.button("Clear History", use_container_width=False):
        st.session_state.joke_history = []
        st.rerun()
    
    # Display history in reverse order (newest first)
    for i, joke in enumerate(reversed(st.session_state.joke_history)):
        with st.expander(f"Joke #{len(st.session_state.joke_history) - i}"):
            st.markdown(joke['text'])
            st.caption(f"Source: {joke['source']} | {joke['timestamp']}")

st.markdown("---")

# Info section
with st.expander("ℹ️ About"):
    st.markdown("""
        ### Random Joke Generator
        
        This fun tool fetches random jokes from multiple APIs:
        
        - **Official Joke API**: Classic jokes with setup and punchline
        - **JokeAPI**: Single-line jokes with various categories
        - **Random Useless Facts**: Interesting but useless facts
        
        ### How to Use
        
        1. Select a joke source from the sidebar
        2. Click "Get Random Joke" button
        3. Enjoy the laugh!
        4. View your joke history
        
        ### Features
        
        - ✅ Multiple joke sources
        - ✅ Joke history tracking
        - ✅ Copy jokes to clipboard
        - ✅ Rate jokes (funny/not funny)
        - ✅ Clear history
    """)

# Footer
st.markdown("""
    <div style='text-align: center; color: #888; margin-top: 2rem;'>
        <p>😄 Remember: Laughter is the best medicine!</p>
    </div>
""", unsafe_allow_html=True)
