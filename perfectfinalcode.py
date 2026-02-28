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
0: {"name": "Healthy Plant", "cure": "No disease detected. Maintain proper irrigation and nutrition."},
1: {"name": "Tomato Leaf Mold", "cure": "Reduce humidity and apply fungicide."},
2: {"name": "Tomato Late Blight", "cure": "Remove infected leaves and spray copper fungicide."},
3: {"name": "Tomato Early Blight", "cure": "Crop rotation and fungicide application."},
4: {"name": "Tomato Septoria Leaf Spot", "cure": "Remove infected leaves and use fungicide."},
5: {"name": "Tomato Bacterial Spot", "cure": "Use disease-free seeds and copper sprays."},
6: {"name": "Tomato Mosaic Virus", "cure": "Remove infected plants and disinfect tools."},
7: {"name": "Potato Late Blight", "cure": "Destroy infected plants and apply fungicide."},
8: {"name": "Potato Early Blight", "cure": "Crop rotation and fungicide spraying."},
9: {"name": "Potato Black Scab", "cure": "Use certified seed potatoes and maintain soil pH."},
10: {"name": "Potato Leaf Roll Virus", "cure": "Control aphids and remove infected plants."},

11: {"name": "Rice Blast", "cure": "Use resistant varieties and balanced fertilization."},
12: {"name": "Rice Bacterial Blight", "cure": "Avoid excess nitrogen and use resistant seeds."},
13: {"name": "Rice Brown Spot", "cure": "Apply fungicides and improve soil nutrients."},
14: {"name": "Rice Sheath Blight", "cure": "Reduce plant density and apply fungicide."},
15: {"name": "Rice Tungro Virus", "cure": "Control leafhoppers and remove infected plants."},

16: {"name": "Wheat Rust", "cure": "Grow resistant varieties and spray fungicide."},
17: {"name": "Wheat Powdery Mildew", "cure": "Improve air circulation and apply fungicide."},
18: {"name": "Wheat Smut", "cure": "Use treated seeds and crop rotation."},
19: {"name": "Wheat Leaf Blight", "cure": "Use disease-free seeds and fungicide."},
20: {"name": "Wheat Mosaic Virus", "cure": "Remove infected plants and control vectors."},

21: {"name": "Corn Leaf Rust", "cure": "Plant resistant hybrids and apply fungicide."},
22: {"name": "Corn Gray Leaf Spot", "cure": "Crop rotation and fungicide application."},
23: {"name": "Corn Smut", "cure": "Remove infected galls and destroy them."},
24: {"name": "Corn Leaf Blight", "cure": "Use resistant varieties and balanced fertilizer."},
25: {"name": "Corn Mosaic Virus", "cure": "Control insect vectors and remove infected plants."},

26: {"name": "Cotton Leaf Curl Virus", "cure": "Control whiteflies and use resistant varieties."},
27: {"name": "Cotton Wilt", "cure": "Crop rotation and soil treatment."},
28: {"name": "Cotton Boll Rot", "cure": "Improve drainage and apply fungicide."},
29: {"name": "Cotton Root Rot", "cure": "Improve soil aeration and rotate crops."},
30: {"name": "Cotton Bacterial Blight", "cure": "Use resistant seeds and copper sprays."},

31: {"name": "Apple Scab", "cure": "Remove infected leaves and apply fungicide."},
32: {"name": "Apple Powdery Mildew", "cure": "Prune infected branches and spray fungicide."},
33: {"name": "Apple Fire Blight", "cure": "Prune affected areas and disinfect tools."},
34: {"name": "Apple Rust", "cure": "Apply fungicide and remove alternate hosts."},
35: {"name": "Apple Black Rot", "cure": "Remove infected fruit and branches."},

36: {"name": "Grape Downy Mildew", "cure": "Improve air flow and apply fungicide."},
37: {"name": "Grape Powdery Mildew", "cure": "Use sulfur-based fungicide."},
38: {"name": "Grape Black Rot", "cure": "Remove infected fruit and apply fungicide."},
39: {"name": "Grape Leaf Blight", "cure": "Prune infected leaves and spray fungicide."},
40: {"name": "Grape Anthracnose", "cure": "Apply copper fungicide and prune vines."},

41: {"name": "Mango Anthracnose", "cure": "Apply fungicide and prune affected branches."},
42: {"name": "Mango Powdery Mildew", "cure": "Spray sulfur fungicide."},
43: {"name": "Mango Bacterial Canker", "cure": "Remove infected parts and use copper spray."},
44: {"name": "Mango Leaf Spot", "cure": "Improve air circulation and apply fungicide."},
45: {"name": "Mango Wilt", "cure": "Remove infected plants and improve drainage."},

46: {"name": "Banana Panama Disease", "cure": "Use resistant varieties and destroy infected plants."},
47: {"name": "Banana Leaf Spot", "cure": "Apply fungicide and remove infected leaves."},
48: {"name": "Banana Bunchy Top Virus", "cure": "Control aphids and remove infected plants."},
49: {"name": "Banana Anthracnose", "cure": "Apply fungicide after harvesting."},
50: {"name": "Banana Root Rot", "cure": "Improve drainage and soil aeration."},

51: {"name": "Pepper Bell Bacterial Spot", "cure": "Use disease-free seeds and copper sprays."},
52: {"name": "Pepper Anthracnose", "cure": "Apply fungicide and remove infected fruit."},
53: {"name": "Pepper Powdery Mildew", "cure": "Improve airflow and apply fungicide."},
54: {"name": "Pepper Mosaic Virus", "cure": "Remove infected plants and control aphids."},
55: {"name": "Pepper Leaf Curl Virus", "cure": "Control whiteflies and remove infected plants."},

56: {"name": "Soybean Rust", "cure": "Apply fungicide and grow resistant varieties."},
57: {"name": "Soybean Leaf Blight", "cure": "Crop rotation and fungicide use."},
58: {"name": "Soybean Mosaic Virus", "cure": "Control aphids and remove infected plants."},
59: {"name": "Soybean Root Rot", "cure": "Improve drainage and use resistant seeds."},
60: {"name": "Soybean Bacterial Blight", "cure": "Use disease-free seeds."},

61: {"name": "Groundnut Leaf Spot", "cure": "Apply fungicide and rotate crops."},
62: {"name": "Groundnut Rust", "cure": "Use resistant varieties and fungicide."},
63: {"name": "Groundnut Rosette Virus", "cure": "Control aphids and remove infected plants."},
64: {"name": "Groundnut Stem Rot", "cure": "Improve drainage and apply fungicide."},
65: {"name": "Groundnut Root Rot", "cure": "Crop rotation and soil treatment."},

66: {"name": "Sugarcane Red Rot", "cure": "Use resistant varieties and destroy infected canes."},
67: {"name": "Sugarcane Smut", "cure": "Remove infected plants and hot-water seed treatment."},
68: {"name": "Sugarcane Wilt", "cure": "Improve drainage and rotate crops."},
69: {"name": "Sugarcane Leaf Scald", "cure": "Use disease-free planting material."},
70: {"name": "Sugarcane Mosaic Virus", "cure": "Remove infected plants and control vectors."},

71: {"name": "Chili Leaf Curl Virus", "cure": "Control whiteflies and remove infected plants."},
72: {"name": "Chili Anthracnose", "cure": "Apply fungicide and remove infected fruits."},
73: {"name": "Chili Powdery Mildew", "cure": "Spray sulfur fungicide."},
74: {"name": "Chili Wilt", "cure": "Improve drainage and use resistant varieties."},
75: {"name": "Chili Mosaic Virus", "cure": "Control aphids and remove infected plants."},

76: {"name": "Citrus Canker", "cure": "Prune infected branches and apply copper spray."},
77: {"name": "Citrus Greening", "cure": "Control psyllids and remove infected trees."},
78: {"name": "Citrus Leaf Miner", "cure": "Use neem oil or insecticide."},
79: {"name": "Citrus Black Spot", "cure": "Apply fungicide and remove fallen fruits."},
80: {"name": "Citrus Root Rot", "cure": "Improve drainage and avoid overwatering."},

81: {"name": "Okra Yellow Vein Virus", "cure": "Control whiteflies and remove infected plants."},
82: {"name": "Okra Leaf Spot", "cure": "Apply fungicide and remove infected leaves."},
83: {"name": "Okra Powdery Mildew", "cure": "Spray fungicide and improve airflow."},
84: {"name": "Okra Root Rot", "cure": "Improve soil drainage."},
85: {"name": "Okra Wilt", "cure": "Crop rotation and soil treatment."},

86: {"name": "Brinjal Wilt", "cure": "Use resistant varieties and crop rotation."},
87: {"name": "Brinjal Leaf Spot", "cure": "Apply fungicide and remove infected leaves."},
88: {"name": "Brinjal Mosaic Virus", "cure": "Control aphids and remove infected plants."},
89: {"name": "Brinjal Root Rot", "cure": "Improve drainage and soil health."},
90: {"name": "Brinjal Little Leaf Disease", "cure": "Remove infected plants and control insects."},

91: {"name": "Papaya Ring Spot Virus", "cure": "Remove infected plants and control aphids."},
92: {"name": "Papaya Anthracnose", "cure": "Apply fungicide and avoid fruit injury."},
93: {"name": "Papaya Leaf Curl", "cure": "Control whiteflies."},
94: {"name": "Papaya Root Rot", "cure": "Improve drainage."},
95: {"name": "Papaya Powdery Mildew", "cure": "Spray fungicide."},

96: {"name": "Cabbage Black Rot", "cure": "Use disease-free seeds and crop rotation."},
97: {"name": "Cabbage Downy Mildew", "cure": "Apply fungicide and avoid overcrowding."},
98: {"name": "Cauliflower Leaf Spot", "cure": "Apply fungicide and remove infected leaves."},
99: {"name": "Carrot Leaf Blight", "cure": "Crop rotation and fungicide application."}
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