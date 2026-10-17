import streamlit as st
import os
import json
import cv2
import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import transforms, models
from PIL import Image
import numpy as np

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Face / Body Analysis | NeuroMind",
    page_icon="👤",
    layout="wide"
)

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>
.block-container {
    padding-top: 2.5rem;
    padding-left: 4rem;
    padding-right: 4rem;
    padding-bottom: 3rem;
}
[data-testid="stSidebarNav"] { display: none; }
section[data-testid="stSidebar"] { background-color: #f3f5f9; }
section[data-testid="stSidebar"] .block-container {
    padding-top: 2rem;
    padding-left: 1.3rem;
    padding-right: 1.3rem;
}
.page-title { font-size: 42px; font-weight: 750; color: #292d3d; margin-bottom: 5px; }
.page-subtitle { font-size: 19px; color: #68748b; margin-bottom: 30px; }
.upload-heading { font-size: 26px; font-weight: 700; color: #292d3d; }
.upload-description { font-size: 17px; color: #68748b; margin-bottom: 15px; }
</style>
""", unsafe_allow_html=True)

# =========================================================
# SIDEBAR NAVIGATION
# =========================================================

with st.sidebar:
    st.markdown(
        '<div style="font-size:28px; font-weight:750; color:#292d3d; margin-bottom:35px;">'
        '🧠 NeuroMind'
        '</div>',
        unsafe_allow_html=True
    )
    st.markdown("### Navigation")
    st.page_link("app/main.py", label="Dashboard", icon="🏠")
    st.page_link("app/pages/behavioral_assessment.py", label="Behavioral Assessment", icon="📋")
    st.page_link("app/pages/mri_analysis.py", label="MRI Analysis", icon="🧠")
    st.page_link("app/pages/face_body_analysis.py", label="Face / Body Analysis", icon="👤")
    st.page_link("app/pages/results.py", label="Results", icon="📊")

# =========================================================
# MODEL DEFINITIONS & CACHED LOADER
# =========================================================

class FusionClassifier(nn.Module):
    def __init__(self, input_dim=518, hidden_dim=32, num_classes=2):
        super().__init__()
        self.fc1 = nn.Linear(input_dim, hidden_dim)
        self.bn1 = nn.BatchNorm1d(hidden_dim)
        self.relu = nn.ReLU()
        self.dropout1 = nn.Dropout(0.6)
        self.fc2 = nn.Linear(hidden_dim, num_classes)

    def forward(self, x):
        x = self.fc1(x)
        x = self.bn1(x)
        x = self.relu(x)
        x = self.dropout1(x)
        return self.fc2(x)

@st.cache_resource
def load_pipeline():
    model_dir = "models/facial"
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    config_path = os.path.join(model_dir, "facial_config.json")
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file missing at {config_path}")

    with open(config_path, "r") as f:
        config = json.load(f)

    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.Grayscale(num_output_channels=3),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

    ood_data = torch.load(os.path.join(model_dir, "ood_stats.pt"), map_location=device)
    train_mean = ood_data["mean"].to(device)
    train_std = ood_data["std"].to(device)

    # 1. Feature extractor (ResNet18)
    feat_extractor = models.resnet18(weights=None)
    feat_extractor.fc = nn.Identity()
    feat_extractor.load_state_dict(
        torch.load(os.path.join(model_dir, "best_autism_resnet18.pth"), map_location=device),
        strict=False
    )
    feat_extractor = feat_extractor.to(device).eval()

    # 2. Emotion classifier (ResNet18)
    emotion_model = models.resnet18(weights=None)
    emotion_model.fc = nn.Linear(emotion_model.fc.in_features, len(config["emotion_classes"]))
    emotion_model.load_state_dict(
        torch.load(os.path.join(model_dir, "best_emotion_resnet18_final.pth"), map_location=device)
    )
    emotion_model = emotion_model.to(device).eval()

    # 3. Fusion classifier
    fusion = FusionClassifier(
        input_dim=512 + len(config["emotion_classes"]),
        hidden_dim=config["hidden_dim"],
        num_classes=config["num_classes"]
    ).to(device)
    fusion.load_state_dict(
        torch.load(os.path.join(model_dir, "best_fusion_model_v2.pth"), map_location=device)
    )
    fusion.eval()

    cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    return {
        "device": device,
        "config": config,
        "transform": transform,
        "train_mean": train_mean,
        "train_std": train_std,
        "feat_extractor": feat_extractor,
        "emotion_model": emotion_model,
        "fusion": fusion,
        "cascade": cascade
    }

# =========================================================
# HEADER
# =========================================================

st.markdown('<div class="page-title">Face / Body Analysis</div>', unsafe_allow_html=True)
st.markdown('<div class="page-subtitle">Pediatric Facial Morphology and Affect Screening</div>', unsafe_allow_html=True)

try:
    pipe = load_pipeline()
except Exception as e:
    st.error(f"Failed to load facial model files from 'models/facial/': {e}")
    st.info("Make sure you copied your models into the 'models/facial/' directory.")
    st.stop()

# =========================================================
# INPUT SELECTION
# =========================================================

with st.container(border=True):
    st.markdown('<div class="upload-heading">Provide Facial Input</div>', unsafe_allow_html=True)
    st.markdown('<div class="upload-description">Select capture method and specify the individual\'s age.</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])
    with col1:
        mode = st.radio("Input Source:", ["📸 Live Camera Snapshot", "📁 Upload Image File"], horizontal=True)
    with col2:
        age = st.number_input("Age (Years):", min_value=1, max_value=99, value=7)

    target_img = None
    if mode == "📸 Live Camera Snapshot":
        cam_shot = st.camera_input("Look straight into the camera and take snapshot:")
        if cam_shot:
            target_img = Image.open(cam_shot).convert("RGB")
    else:
        uploaded_file = st.file_uploader("Upload portrait photo", type=["jpg", "jpeg", "png"])
        if uploaded_file:
            target_img = Image.open(uploaded_file).convert("RGB")

# =========================================================
# PREVIEW & ANALYSIS
# =========================================================

if target_img is not None:
    st.markdown("### Image Preview")
    st.image(target_img, caption="Screening Input Image", width=340)

    if st.button("👤 Analyze Face →", use_container_width=True):
        img_bgr = cv2.cvtColor(np.array(target_img), cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
        faces = pipe["cascade"].detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(80, 80))

        if len(faces) == 0:
            st.error("⚠️ No frontal face detected. Ensure the face is clearly lit and looking toward the camera.")
        else:
            x, y, w, h = max(faces, key=lambda f: f[2] * f[3])
            face_crop = Image.fromarray(cv2.cvtColor(img_bgr[y:y+h, x:x+w], cv2.COLOR_BGR2RGB))
            tensor = pipe["transform"](face_crop).unsqueeze(0).to(pipe["device"])

            with torch.no_grad():
                # 1. Expressions
                raw_emo = F.softmax(pipe["emotion_model"](tensor), dim=1).cpu().numpy()[0]
                ranked_emo = sorted(zip(pipe["config"]["emotion_classes"], raw_emo), key=lambda x: x[1], reverse=True)
                top_2_emo = [(e, float(p)) for e, p in ranked_emo[:2]]

                # 2. Adult / Out-of-Distribution Guard
                img_feats = pipe["feat_extractor"](tensor)
                z_diff = (img_feats[0] - pipe["train_mean"]) / pipe["train_std"]
                dist = torch.norm(z_diff).item()
                is_ood = dist > pipe["config"]["ood_threshold"]
                is_adult = (age > 16) or is_ood

                if is_adult:
                    reason = f"Age ({age} yrs) exceeds pediatric limits" if age > 16 else f"Facial proportions match adult morphology (Z: {dist:.1f})"
                    st.warning("⚠️ **Adult Facial Morphology Detected**")
                    st.info(f"**Scope Limitation**: {reason}. Pediatric facial ASD morphology screening is restricted to children (ages 2–16).")
                    
                    st.markdown("#### Dominant Facial Expressions:")
                    for rank, (emo, prob) in enumerate(top_2_emo, 1):
                        st.write(f"**{rank}. {emo.capitalize()}**: {prob * 100:.1f}%")

                    # Save to session_state so results.py can read it
                    st.session_state.face_result = {
                        "prediction": "Adult Advisory (Pediatric Screening Disabled)",
                        "probability": None,
                        "expressions": top_2_emo
                    }
                else:
                    # 3. Pediatric Fusion Prediction
                    emo_tensor = torch.tensor(raw_emo, device=pipe["device"]).unsqueeze(0)
                    fusion_input = torch.cat([img_feats, emo_tensor], dim=1)
                    logits = pipe["fusion"](fusion_input)
                    scaled_logits = logits / pipe["config"]["optimal_temperature"]
                    probs = F.softmax(scaled_logits, dim=1).cpu().numpy()[0]

                    prob_asd = float(probs[0])
                    threshold = pipe["config"]["optimal_threshold"]
                    pred_label = "YES (Features Resemble ASD Indicators)" if prob_asd >= threshold else "NO (Typical Developmental Markers)"

                    st.success("✅ **Pediatric Screening Analysis Completed**")
                    col_res1, col_res2 = st.columns(2)
                    with col_res1:
                        st.metric("Screening Assessment", pred_label)
                        st.metric("ASD Probability", f"{prob_asd * 100:.1f}%", help=f"Optimal calibrated threshold: {threshold:.2f}")
                    with col_res2:
                        st.markdown("**Dominant Facial Expressions:**")
                        for rank, (emo, prob) in enumerate(top_2_emo, 1):
                            st.write(f"**{rank}. {emo.capitalize()}**: {prob * 100:.1f}%")

                    # Save to session_state so results.py can read it
                    st.session_state.face_result = {
                        "prediction": pred_label,
                        "probability": f"{prob_asd * 100:.1f}%",
                        "expressions": top_2_emo
                    }