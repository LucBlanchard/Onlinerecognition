import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode
import av # Utilisé pour le traitement d'image si nécessaire

st.title("Webcam Control Panel")

# 1. État de la session (Optionnel ici car WebRTC gère son propre état)
if 'run' not in st.session_state:
    st.session_state['run'] = False

# 2. Interface de Statut
# Note : streamlit-webrtc possède son propre bouton START/STOP intégré
if st.session_state['run']:
    st.success("STATUS: **PRÊT / EN COURS**")
else:
    st.error("STATUS: **ARRÊTÉ**")

# 3. Logique Camera avec WebRTC
# webrtc_streamer remplace cv2.VideoCapture et la boucle while
# Configuration standard pour éviter les blocages réseaux on utilise 3 sous-domaines pour la redondance
rtc_configuration={
    "iceServers": [
        {"urls": ["stun:stun.l.google.com:19302"]},
        {"urls": ["stun:stun1.l.google.com:19302"]},
        {"urls": ["stun:stun2.l.google.com:19302"]}
    ]
}
ctx = webrtc_streamer(
    key="webcam-control",
    mode=WebRtcMode.SENDRECV, # Pour envoyer et recevoir de la vidéo
    # Configuration standard pour éviter les blocages réseaux
    rtc_configuration=rtc_configuration,
    media_stream_constraints={"video": True, "audio": False},
    async_processing=True
)

# Mise à jour du statut basée sur l'état du flux
if ctx.state.playing:
    st.session_state['run'] = True
else:
    st.session_state['run'] = False

# Information complémentaire
if not ctx.state.playing:
    st.info("Cliquez sur le bouton 'Start' ci-dessus pour activer la webcam.")

