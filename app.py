import streamlit as st
import random

st.title("Platskoll Campus Växjö📍")
st.write("Hitta lediga studieplatser i realtid.")

# --- 1. KONTROLLER OCH FILTER ---
st.button("🔄 Uppdatera data")

# Skapa ett sökfält och en kryssruta bredvid varandra
col_sök, col_filter = st.columns([3, 2])
with col_sök:
    sökord = st.text_input("🔍 Sök byggnad eller sal:", "").lower()
with col_filter:
    # Den här rutan låter användaren dölja alla röda/fulla salar
    visa_bara_ledigt = st.checkbox("✅ Visa bara platser med låg belastning")

st.divider()

# --- 2. DATABASEN ---
campus = {
    "M-huset (Teknik & Maskin)": {
        "Sal Södra (M1050)": 60, "Sal Norra (M1051)": 60, "Grupprum M1042": 15,
        "Grupprum M1083": 15, "Grupprum M1088": 15, "Datasal M1054": 30, "Studieyta Entréplanet": 40
    },
    "N-huset": {
        "IKEA-salen (N1008)": 300, "Sal N1040": 80, "Sal N1012": 60,
        "Grupprum N2022": 10, "Grupprum N2024": 10, "Ljusgården N-huset": 150
    },
    "K-huset": {
        "Sal Myrdal (K1082)": 120, "Sal Wicksell (K1083)": 120, "Sal K1043": 40,
        "Ljusgården (K-huset)": 80, "Grupprum K2055": 8, "Grupprum K2057": 8
    },
    "F-huset": {
        "Sal Homeros (F332)": 90, "Sal F135": 45, "Lammhultsrummet (F303)": 30,
        "Grupprum F211": 8, "Grupprum F212": 8
    },
    "H-huset & D-huset": {
        "Sal H1314": 90, "Sal H1212": 60, "Sal D1136A": 50,
        "Datasal D1170": 30, "Grupprum H1410": 10, "Grupprum D1140": 8
    },
    "Universitetsbiblioteket (UB)": {
        "Studieplatser Plan 1": 100, "Studieplatser Plan 2": 150, "Tysta Läsrummet Plan 3": 80,
        "Grupprum UB201": 6, "Grupprum UB202": 6, "Datorsal UB104": 25
    },
    "Studentliv & Kaféer": {
        "Kafé Tufvan": 45, "Kafé Astrakan (UB)": 50, "Kafé Kristina (N-huset)": 60
    }
}

# --- 3. UPPRITNING AV GRÄNSSNITTET ---
for byggnad, salar in campus.items():
    
    # Skapa en tillfällig lista för de salar i denna byggnad som ska visas
    salar_att_visa = {}
    
    for sal, max_platser in salar.items():
        nuvarande = random.randint(0, max_platser)
        belastning = nuvarande / max_platser
        
        # FILTER 1: Om användaren kryssat i "visa bara ledigt" och belastningen är hög, hoppa över salen
        if visa_bara_ledigt and belastning >= 0.5:
            continue
            
        # FILTER 2: Om användaren skrivit ett sökord, och ordet varken finns i salens eller byggnadens namn, hoppa över
        if sökord and sökord not in sal.lower() and sökord not in byggnad.lower():
            continue
            
        # Om salen klarade filtren, spara dess värden för att rita upp den
        salar_att_visa[sal] = {"max": max_platser, "nuvarande": nuvarande, "belastning": belastning}

    # Rita bara ut byggnadens kategori om det finns några salar i den som klarade filtren
    if salar_att_visa:
        
        # Gör så att kategorin fälls ut automatiskt om man har skrivit ett sökord
        with st.expander(f"🏢 {byggnad}", expanded=bool(sökord)):
            
            for sal, data in salar_att_visa.items():
                belastning = data["belastning"]
                nuvarande = data["nuvarande"]
                max_platser = data["max"]
                
                if belastning < 0.5:
                    färg, status = "🟢", "Gott om plats"
                elif belastning < 0.85:
                    färg, status = "🟡", "Börjar bli fullt"
                else:
                    färg, status = "🔴", "Nästan fullt"

                col1, col2 = st.columns([3, 1])
                with col1:
                    st.subheader(f"{färg} {sal}")
                    st.write(status)
                    st.progress(belastning)
                with col2:
                    st.metric(label="Enheter", value=f"{nuvarande}/{max_platser}")
                
                st.divider()