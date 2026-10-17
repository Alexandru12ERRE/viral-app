import streamlit as st, yt_dlp
from datetime import date

st.set_page_config(page_title="Viral Analyzer", page_icon="🔥")

if "count" not in st.session_state:
    st.session_state.count = 0
    st.session_state.last_date = str(date.today())
    st.session_state.is_premium = False

if st.session_state.last_date != str(date.today()):
    st.session_state.count = 0
    st.session_state.last_date = str(date.today())

# --- SIDEBAR ---
with st.sidebar:
    if not st.session_state.is_premium:
        st.metric("Analyses gratuites aujourd'hui", f"{st.session_state.count}/5")
        if st.session_state.count >= 5:
            st.error("Limite du jour atteinte. Reviens demain ou passe Premium.")
        st.divider()
        st.subheader("🔓 Débloquer tout")
        st.write("Passe Premium pour : Script + Titres + Sans Pub")
        code = st.text_input("Code Premium")
        if st.button("Activer"):
            if code == "PREMIUM2026":
                st.session_state.is_premium = True
                st.rerun()
        st.link_button("Devenir Premium - 9,90€", "https://buy.stripe.com/...")
    else:
        st.success("PREMIUM ACTIF - Illimité")

st.title("🔥 Viral Analyzer")

url = st.text_input("Lien YouTube :")
if st.button("Analyser"):
    if not st.session_state.is_premium and st.session_state.count >= 5:
        st.stop()

    try:
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            info = ydl.extract_info(url, download=False)
        st.session_state.count += 1
        
        # TOUT LE MONDE A CA - GRATUIT
        st.image(info.get('thumbnail'))
        st.subheader(info.get('title'))
        c1,c2,c3 = st.columns(3)
        c1.metric("Vues", f"{info.get('view_count',0):,}")
        c2.metric("Likes", f"{info.get('like_count',0):,}")
        c3.metric("Coms", f"{info.get('comment_count',0):,}")
        st.success("✅ Pourquoi c'est viral : Chiffre choc + Sujet Argent + IA")

        # PUB - QUE POUR LES GRATUITS
        if not st.session_state.is_premium:
            st.info("📢 PUB : Formation IA Offerte -> [Clique ici]")

        # CA C'EST PAYANT - ON TEASE
        st.divider()
        st.subheader("💰 Comment REFAIRE cette vidéo et gagner")
        if st.session_state.is_premium:
            st.write("**SCRIPT PRET :** 'Les 3 outils IA que j'utilise pour faire 300€/jour...'")
            st.write("**TITRES VIRAUX :** 1. J'ai copié cette vidéo et j'ai fait 10k vues en 24h")
            st.write("**ARGENT :** Cette vidéo a rapporté ~ 4.4k€ en pub")
        else:
            st.write("🔒 **SCRIPT COMPLET :** ████████ █████ pour faire la même vidéo...")
            st.write("🔒 **3 TITRES VIRAUX PRÊTS À POSTER**")
            st.write("🔒 **ESTIMATION EXACTE DES REVENUS**")
            st.button("🔓 Débloquer tout pour 9,90€")
            
    except Exception as e:
        st.error(str(e))