import streamlit as st
import requests

# Streamlit app címe
st.markdown("""
    <style>
    .main {
        background: linear-gradient(to top left, #000000, #ff7f00);
    }
    </style>
    """, unsafe_allow_html=True)

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
import streamlit as st
import requests

# Streamlit app címe
st.markdown("""
    <style>
    .main {
        background: linear-gradient(to top left, #000000, #ff7f00);
    }
    </style>
    """, unsafe_allow_html=True)

st.title("Dismeseg")
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
