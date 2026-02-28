import streamlit as st
import tensorflow as tf
from PIL import Image
import numpy as np

# --- 1. SETTING UP THE PAGE ---
st.set_page_config(page_title="AgroDetect AI", page_icon="🌿")
st.title("🌿 AgroDetect AI: Plant Disease Classifier")
st.markdown("Upload a leaf image to detect diseases instantly.")

# --- 2. LOAD THE TRAINED MODEL ---
# Replace 'plant_model.h5' with your actual model file path
@st.cache_resource
def load_model():
    # In a real hackathon, you'd load your model here:
    # return tf.keras.models.load_model('plant_model.h5')
    return None 

model = load_model()

# --- 3. HELPER FUNCTION: PREDICT ---
def model_prediction(test_image):
    # Load and resize image to 224x224 as required by most CNNs (MobileNet/ResNet)
    image = Image.open(test_image)
    image = image.resize((224, 224))
    input_arr = tf.keras.preprocessing.image.img_to_array(image)
    input_arr = np.array([input_arr]) # Convert single image to a batch
    
    # Preprocessing (Scaling pixels 0-1)
    input_arr = input_arr / 255.0
    
    # Dummy result for demonstration if model isn't loaded
    if model is None:
        return 0, 0.95 
        
    predictions = model.predict(input_arr)
    result_index = np.argmax(predictions)
    confidence = np.max(predictions)
    return result_index, confidence

# --- 4. UI SIDEBAR & UPLOAD ---
st.sidebar.title("Dashboard")
app_mode = st.sidebar.selectbox("Select Page", ["Home", "Disease Recognition"])

if app_mode == "Home":
    st.image("https://images.unsplash.com/photo-1523348837708-15d4a09cfac2?auto=format&fit=crop&q=80&w=1000", use_column_width=True)
    st.markdown("""
    ### About the Project
    AgroDetect AI uses Deep Learning to help farmers identify crop health issues.
    * **High Accuracy:** Powered by CNN architectures.
    * **Fast Results:** Instant classification within seconds.
    """)
elif app_mode== "Disease Recognition":
    st.header("Upload Image")
    test_image = st.file_uploader("Choose a leaf image...", type=["jpg", "jpeg", "png"])
    
    if test_image is not None:
        st.image(test_image, width=300, caption="Uploaded Image")
        
        if st.button("Analyze Image"):
            with st.spinner("Processing..."):
                # Complete PlantVillage Class List (38 Classes)
                classes = [
                    'Apple___Apple_scab', 'Apple___Black_rot', 'Apple___Cedar_apple_rust', 'Apple___healthy',
                    'Blueberry___healthy', 'Cherry_(including_sour)___Powdery_mildew', 'Cherry_(including_sour)___healthy',
                    'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot', 'Corn_(maize)___Common_rust_', 
                    'Corn_(maize)___Northern_Leaf_Blight', 'Corn_(maize)___healthy', 'Grape___Black_rot', 
                    'Grape___Esca_(Black_Measles)', 'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)', 'Grape___healthy',
                    'Orange___Haunglongbing_(Citrus_greening)', 'Peach___Bacterial_spot', 'Peach___healthy',
                    'Pepper,_bell___Bacterial_spot', 'Pepper,_bell___healthy', 'Potato___Early_blight', 
                    'Potato___Late_blight', 'Potato___healthy', 'Raspberry___healthy', 'Soybean___healthy', 
                    'Squash___Powdery_mildew', 'Strawberry___Leaf_scorch', 'Strawberry___healthy', 
                    'Tomato___Bacterial_spot', 'Tomato___Early_blight', 'Tomato___Late_blight', 'Tomato___Leaf_Mold', 
                    'Tomato___Septoria_leaf_spot', 'Tomato___Spider_mites Two-spotted_spider_mite', 
                    'Tomato___Target_Spot', 'Tomato___Tomato_Yellow_Leaf_Curl_Virus', 'Tomato___Tomato_mosaic_virus',
                    'Tomato___healthy'
                ]

                # Treatment Database
                recommendations = {
                    "scab": "Apply fungicides containing captan or sulfur. Rake and destroy fallen leaves.",
                    "rot": "Prune out infected branches. Apply copper-based fungicides during the dormant season.",
                    "rust": "Remove nearby cedar trees if possible. Use fungicides like Myclobutanil.",
                    "mildew": "Improve air circulation. Use neem oil or potassium bicarbonate sprays.",
                    "blight": "Apply copper fungicides. Avoid overhead watering to keep leaves dry.",
                    "spot": "Remove infected leaves. Use copper-based bactericides.",
                    "rust_": "Use resistant varieties. Apply fungicides if infection is severe early in the season.",
                    "greening": "No cure. Remove infected trees immediately to prevent spread via psyllids.",
                    "scorch": "Plant resistant varieties. Ensure proper spacing for airflow.",
                    "virus": "Control whitefly/aphid populations. Remove and burn infected plants.",
                    "mites": "Increase humidity. Use insecticidal soap or Neem oil.",
                    "mold": "Reduce humidity in greenhouses. Use calcium-based sprays.",
                    "healthy": "Your plant looks great! Maintain regular watering and nutrient cycles."
                }

                idx, conf = model_prediction(test_image)
                prediction_name = classes[idx]
                
                # --- Display Results ---
                st.success(f"**Prediction:** {prediction_name.replace('___', ' - ').replace('_', ' ')}")
                st.info(f"**Confidence:** {conf*100:.2f}%")

                # --- Logic to find treatment ---
                found_treatment = False
                for key in recommendations:
                    if key in prediction_name.lower():
                        st.warning(f"💊 **Treatment Recommendation:** {recommendations[key]}")
                        found_treatment = True
                        break
                
                if not found_treatment:
                    st.write("Treatment data for this specific strain is being updated. Consult a local agronomist.")