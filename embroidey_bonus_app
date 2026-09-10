import streamlit as st
import pandas as pd

st.set_page_config(page_title="એમ્બ્રોડરી મશીન બોનસ કેલ્ક્યુલેટર", layout="centered")

st.title("🧵 એમ્બ્રોડરી મશીન પ્રોડક્શન અને બોનસ સિસ્ટમ")

if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=['તારીખ', 'કારીગરનું નામ', 'મશીન નંબર', 'પ્રોડક્શન (ટાકા/પીસ)', 'બોનસ (₹)'])

with st.form("production_form"):
    st.subheader("દૈનિક પ્રોડક્શન એન્ટ્રી")
    
    date = st.date_input("તારીખ")
    worker_name = st.text_input("કારીગરનું નામ")
    machine_no = st.selectbox("મશીન નંબર", ["મશીન - ૧", "મશીન - ૨", "મશીન - ૩", "મશીન - ૪", "મશીન - ૫"])
    production = st.number_input("કુલ પ્રોડક્શન (ટાકા અથવા પીસ)", min_value=0, step=1000)
    
    submit_button = st.form_submit_button(label="સેવ કરો અને બોનસ ગણો")

if submit_button:
    if worker_name.strip() == "":
        st.warning("કૃપા કરીને કારીગરનું નામ દાખલ કરો.")
    else:
        bonus = 0
        if production <= 250000:
            bonus = (production // 1000) * 50
        elif production <= 300000:
            bonus = (250000 // 1000) * 50 + ((production - 250000) // 1000) * 1
        else:
            bonus = (250000 // 1000) * 50 + (50000 // 1000) * 1 + ((production - 300000) // 1000) * 2
        
        new_row = {
            'તારીખ': str(date),
            'કારીગરનું નામ': worker_name,
            'મશીન નંબર': machine_no,
            'પ્રોડક્શન (ટાકા/પીસ)': production,
            'બોનસ (₹)': bonus
        }
        
        st.session_state.data = pd.concat([st.session_state.data, pd.DataFrame([new_row])], ignore_index=True)
        st.success(f"સફળતાપૂર્વક એન્ટ્રી થઈ ગઈ! આ કારીગરનું કુલ બોનસ: ₹ {bonus}")

st.divider()
st.subheader("📊 કુલ પ્રોડક્શન અને બોનસ રિપોર્ટ")

if not st.session_state.data.empty:
    st.dataframe(st.session_state.data, use_container_width=True)
    
    total_prod = st.session_state.data['પ્રોડક્શન (ટાકા/પીસ)'].sum()
    total_bonus = st.session_state.data['બોનસ (₹)'].sum()
    
    col1, col2 = st.columns(2)
    col1.metric("કુલ પ્રોડક્શન", f"{total_prod:,}")
    col2.metric("કુલ ચૂકવવાનું બોનસ", f"₹ {total_bonus:,}")
else:
    st.info("હજી સુધી કોઈ એન્ટ્રી કરવામાં આવી નથી.")
