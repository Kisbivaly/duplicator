import streamlit as st
import requests

# Egyedi CSS stílusok hozzáadása
st.markdown("""
    <style>
    .main {
        background: linear-gradient(to bottom right, #ff7f00, #000000);
        color: white;
    }
    .stTextInput, .stTextArea, .stButton {
        background-color: #292b2f;
        color: white;
    }
    .stTextInput > div, .stTextArea > div {
        border: 2px solid transparent;
        border-radius: 3px;
    }
    .stTextInput > div:focus, .stTextArea > div:focus {
        border-color: rgb(88, 101, 242);
    }
    </style>
    """, unsafe_allow_html=True)

# Streamlit app címe és ikonja
st.set_page_config(page_title="Dismeseg", page_icon=":robot_face:")

st.title("Dismeseg")
st.write("A simple Discord webhook sender with embed support")

# Bemeneti mezők
webhook_link = st.text_input("Webhook Link", type="password")
name = st.text_input("Name", value="Atmin")
avatar_url = st.text_input("Avatar URL")
message = st.text_area("Message", max_chars=2000)

# Embed mezők
st.write("Embed Options (Optional)")
embed_title = st.text_input("Embed Title")
embed_description = st.text_area("Embed Description")
embed_color = st.color_picker("Embed Color", "#3498db")

# Üzenet küldés
if st.button("Send"):
    if not webhook_link or not webhook_link.startswith("https://discord.com/api/webhooks/"):
        st.error("Provide a valid webhook link")
    elif not message and not embed_title and not embed_description:
        st.error("Provide a webhook message or embed content")
    else:
        data = {
            "content": message,
            "username": name,
            "avatar_url": avatar_url,
            "embeds": []
        }
        if embed_title or embed_description:
            embed = {
                "title": embed_title,
                "description": embed_description,
                "color": int(embed_color.lstrip('#'), 16)
            }
            data["embeds"].append(embed)
        
        response = requests.post(webhook_link, json=data)
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
