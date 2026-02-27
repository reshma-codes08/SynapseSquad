# SynapseSquad
🌿 AgroDetect AI – Plant Disease Classification Engine

AgroDetect AI is a deep learning–based plant disease classification system designed to help farmers, agronomists, and researchers quickly identify plant diseases using leaf images. The system leverages computer vision and convolutional neural networks (CNNs) to deliver accurate and fast predictions.

🚀 Features

🌱 Automated plant disease detection from leaf images

🧠 Deep Learning–based image classification

📊 High accuracy with optimized CNN architecture

🖼️ Image preprocessing & augmentation pipeline

📁 Easy-to-use dataset structure

🌍 Scalable and deployable (Web / Mobile ready)

📈 Model evaluation metrics (Accuracy, Precision, Recall, F1-Score)

🏗️ Project Architecture
AgroDetect-AI/
│
├── dataset/
│   ├── train/
│   ├── validation/
│   └── test/
│
├── models/
│   └── trained_model.h5
│
├── src/
│   ├── preprocessing.py
│   ├── train.py
│   ├── predict.py
│   └── utils.py
│
├── app.py
├── requirements.txt
└── README.md
🧠 Model Details

Framework: TensorFlow / Keras (or PyTorch if applicable)

Architecture: Convolutional Neural Network (CNN)

Input Shape: 224x224x3

Output: Multi-class classification (Plant disease categories)

Optimizer: Adam

Loss Function: Categorical Crossentropy

📂 Dataset

The dataset should be structured as:

dataset/
   train/
      Tomato___Late_blight/
      Potato___Early_blight/
      Corn___Common_rust/
   validation/
   test/

Each folder represents a disease class.

Recommended dataset: PlantVillage Dataset (or your custom dataset)

⚙️ Installation
1️⃣ Clone the repository
git clone https://github.com/yourusername/AgroDetect-AI.git
cd AgroDetect-AI
2️⃣ Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
3️⃣ Install dependencies
pip install -r requirements.txt
🏋️ Training the Model
python src/train.py

The trained model will be saved in the models/ directory.

🔍 Running Predictions
python src/predict.py --image path_to_image.jpg

Example Output:

Prediction: Tomato - Late Blight
Confidence: 96.42%
🌐 Running the Web App (Optional)

If using Flask or FastAPI:

python app.py

Open browser at:

http://127.0.0.1:5000/
📊 Evaluation Metrics

Accuracy

Precision

Recall

F1-Score

Confusion Matrix

🛠️ Tech Stack

Python 3.x

TensorFlow / Keras (or PyTorch)

OpenCV

NumPy

Matplotlib

Flask / FastAPI (for deployment)

🔮 Future Improvements

🌾 Support for more crop types

📱 Mobile app integration

☁️ Cloud deployment (AWS / Azure / GCP)

🔎 Real-time disease detection

🌡️ Integration with IoT field sensors

🤝 Contributing

Contributions are welcome!
