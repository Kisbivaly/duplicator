import streamlit as st
import requests

# Alkalmazás konfigurálása
st.set_page_config(
    page_title="Discord Webhook Sender", 
    page_icon=":robot:", 
    layout="centered", 
    initial_sidebar_state="auto"
)

# Egyéni CSS stílusok hozzáadása
st.markdown("""
    <style>
    :root {
        --background-dark: linear-gradient(to top left, #000000, #ff7f00);
        --background-light: linear-gradient(to bottom right, #ff7f00, #000000);
        --input-dark: #292b2f;
        --input-light: #777777;
        --text-dark: #ccd5e0;
        --text-light: #192e44;
        --button-bg: rgb(88, 101, 242);
        --button-hover-opacity: 0.8;
    }

    body {
        background: var(--background-dark);
        color: var(--text-dark);
    }

    body.light {
        background: var(--background-light);
        color: var(--text-light);
    }

    .stTextInput > div > div, .stTextArea > div > div {
        background-color: var(--input-dark);
        color: var(--text-dark);
    }

    body.light .stTextInput > div > div, body.light .stTextArea > div > div {
        background-color: var(--input-light);
        color: var(--text-light);
    }

    .stTextInput > div > div:focus, .stTextArea > div > div:focus {
        border-color: rgb(88, 101, 242);
    }

    .stButton > button {
        background: var(--button-bg);
        color: white;
    }

    .stButton > button:hover {
        opacity: var(--button-hover-opacity);
    }
    </style>
    """, unsafe_allow_html=True)

# JavaScript a téma váltásához
st.markdown("""
    <script>
    const currentTheme = localStorage.getItem('theme');
    if (!currentTheme || currentTheme === 'dark') {
        document.body.classList.add('dark');
        localStorage.setItem('theme', 'dark');
    } else {
        document.body.classList.add('light');
    }

    function switchTheme() {
        document.body.classList.toggle('light');
        const theme = document.body.classList.contains('light') ? 'light' : 'dark';
        localStorage.setItem('theme', theme);
    }
    </script>
    """, unsafe_allow_html=True)

# Streamlit app címe
st.title("Discord Webhook Sender")
st.write("A simple webhook sender for Discord")

# Bemeneti mezők
webhook_link = st.text_input("Webhook Link", type="password")
name = st.text_input("Name", value="Atmin")
avatar_url = st.text_input("Avatar URL")
message = st.text_area("Message", max_chars=2000)

# Üzenet küldés
if st.button("Send"):
    if not webhook_link or not webhook_link.startswith("https://discord.com/api/webhooks/"):
        st.error("Provide a valid webhook link")
    elif not message:
        st.error("Provide a webhook message")
    else:
        response = requests.post(webhook_link, json={"content": message, "username": name, "avatar_url": avatar_url})
        if response.status_code == 204:
            st.success("Successfully sent webhook")
        elif response.status_code == 429:
            retry_after = response.json().get("retry_after", "unknown")
            st.error(f"429 - Too many requests. Retry in {retry_after}ms")
        else:
            st.error(response.json().get("message", "Failed to send webhook"))

# Webhook mentése
if st.button("Save Webhook"):
    st.write("Webhook saved: ", webhook_link)
    st.write("Username: ", name)
    # További mentési logika itt

# Téma váltó gomb hozzáadása
st.button("Switch Theme", on_click=lambda: st.markdown("<script>switchTheme();</script>", unsafe_allow_html=True))
