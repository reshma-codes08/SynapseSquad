import streamlit as st
import sqlite3
import numpy as np
from PIL import Image

# -------------------- DATABASE SETUP --------------------
def create_users_table():
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(
        username TEXT,
        password TEXT
    )
    """)
    conn.commit()
    conn.close()

def add_default_user():
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM users")
    if not cur.fetchone():
        cur.execute("INSERT INTO users VALUES (?,?)", ("farmer", "1234"))
    conn.commit()
    conn.close()

def login(username, password):
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    result = cur.fetchone()
    conn.close()
    return result

create_users_table()
add_default_user()

# -------------------- DISEASE DATA --------------------
disease_data = {
    0: {
        "name": "Tomato Leaf Mold",
        "cure": "Reduce humidity, use fungicide, ensure proper air circulation."
    },
    1: {
        "name": "Tomato Late Blight",
        "cure": "Remove infected leaves, apply copper-based fungicide."
    },
    2: {
        "name": "Potato Early Blight",
        "cure": "Use certified seeds, rotate crops, apply fungicide."
    },
    3: {
        "name": "Potato Late Blight",
        "cure": "Destroy infected plants, avoid overhead irrigation."
    },
    4: {
        "name": "Pepper Bell Bacterial Spot",
        "cure": "Use disease-free seeds, apply copper sprays."
    },
    5: {
        "name": "Healthy Plant",
        "cure": "No disease detected. Continue proper care."
    }
}

# -------------------- FAKE AI PREDICTION --------------------
# (Hackathon acceptable demo logic)
def predict_disease(image):
    img = Image.open(image)
    img = img.resize((224, 224))
    img = np.array(img)
    prediction = np.random.randint(0, len(disease_data))
    return prediction

# -------------------- STREAMLIT UI --------------------
st.set_page_config(page_title="AgroDetect AI", layout="centered")
st.title("🌱 AgroDetect AI")
st.subheader("Plant Disease Identifier Engine")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# -------------------- LOGIN PAGE --------------------
if not st.session_state.logged_in:
    st.markdown("### 👨‍🌾 Farmer Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if login(username, password):
            st.session_state.logged_in = True
            st.success("Login Successful ✅")
        else:
            st.error("Invalid Username or Password ❌")

# -------------------- MAIN APP --------------------
else:
    st.success("Welcome Farmer 👨‍🌾")
    st.markdown("### 📷 Upload Plant Leaf Image")

    uploaded_file = st.file_uploader("Choose an image", type=["jpg", "png", "jpeg"])

    if uploaded_file:
        st.image(uploaded_file, caption="Uploaded Leaf Image", use_column_width=True)

        if st.button("Detect Disease"):
            result = predict_disease(uploaded_file)

            st.markdown("## 🦠 Disease Detected")
            st.write(disease_data[result]["name"])

            st.markdown("## 💊 Cure / Treatment")
            st.write(disease_data[result]["cure"])

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.experimental_rerun()