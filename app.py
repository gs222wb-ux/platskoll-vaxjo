import streamlit as st
import random

st.title("Platskoll Campus 📍")
st.write("Hitta lediga studieplatser i realtid.")

st.button("🔄 Uppdatera data")

col_sök, col_filter = st.columns([3, 2])
with col_sök:
    sökord = st.text_input("🔍 Sök byggnad eller sal:", "").lower()
with col_filter:
    visa_bara_ledigt = st.checkbox("✅ Visa bara platser med låg belastning")

st.divider()

campus = {
    "M-huset (Teknik & Maskin)": {
        "Sal Södra (M1050)": 60, "Sal Norra (M1051)": 60, "Grupprum M1042": 15,
        "Grupprum M1083": 15, "Datasal M1054": 30
    },
    "Universitetsbiblioteket (UB)": {
        "Studieplatser Plan 2": 150, "Tysta Läsrummet Plan 3": 80, "Grupprum UB201": 6
    },
    "Studentliv & Kaféer": {
        "Kafé Tufvan": 45, "Kafé Kristina (N-huset)": 60
    }
}

for byggnad, salar in campus.items():
    salar_att_visa = {}
    
    for sal, max_platser in salar.items():
        nuvarande = random.randint(0, max_platser)
        belastning = nuvarande / max_platser
        
        if visa_bara_ledigt and belastning >= 0.5:
            continue
        if sökord and sökord not in sal.lower() and sökord not in byggnad.lower():
            continue
            
        salar_att_visa[sal] = {"max": max_platser, "nuvarande": nuvarande, "belastning": belastning}

    if salar_att_visa:
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
                
                # NYTT: Lägg till en graf som visar fiktiv data från kl 08 till 17
                st.write("📊 **Beläggning under dagen (uppskattning)**")
                
                # Skapar påhittad data för varje timme
                timmar = ["08", "09", "10", "11", "12", "13", "14", "15", "16", "17"]
                graf_data = {timme: random.randint(0, max_platser) for timme in timmar}
                
                # Ritar ut grafen
                st.bar_chart(graf_data)
                
                st.divider()