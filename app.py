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

elif app_mode == "Disease Recognition":
    st.header("Upload Image")
    test_image = st.file_uploader("Choose a leaf image...", type=["jpg", "jpeg", "png"])
    
    if test_image is not None:
        st.image(test_image, width=300, caption="Uploaded Image")
        
        if st.button("Analyze Image"):
            with st.spinner("Processing..."):
                # Class list (Example for Tomato/Potato)
                classes = ['Tomato_Late_blight', 'Tomato_Healthy', 'Potato_Early_blight']
                
                idx, conf = model_prediction(test_image)
                st.success(f"Prediction: **{classes[idx]}**")
                st.info(f"Confidence: **{conf*100:.2f}%**")
                
                # Dynamic Recommendation
                if "blight" in classes[idx].lower():
                    st.warning("Recommendation: Use Copper-based fungicides and improve air circulation.")