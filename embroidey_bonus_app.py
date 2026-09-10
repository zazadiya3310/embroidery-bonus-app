import streamlit as st
import pandas as pd

st.set_page_config(page_title="Embroidery Machine Bonus / एम्ब्रॉयडरी मशीन बोनस", layout="centered")

st.title("🧵 Embroidery Machine Production & Bonus System\nएम्ब्रॉयडरी मशीन प्रोडक्शन और बोनस सिस्टम")

if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=[
        'तारीख / Date', 'कारीगर का नाम / Worker Name', 'मशीन नंबर / Machine No.', 
        'डिजाइन नंबर / Design No.', 'कुल टांके / Total Stitches', 'ब्रेकेज / Breakage', 
        'स्टॉप टाइम / Stop Time', 'फ्रेम टाइम / Frame Time', 'बोनस (₹) / Bonus'
    ])

# 1. इनपुट मोड और कैमरा को फॉर्म के बाहर रखा गया है
input_mode = st.radio("डेटा इनपुट का तरीका चुनें / Choose Data Input Method:", ["मैन्युअल टाइप करें / Type Manually", "मॉनिटर फोटो खींचें / Capture Monitor Photo"])

monitor_photo = None
if input_mode == "मॉनिटर फोटो खींचें / Capture Monitor Photo":
    monitor_photo = st.camera_input("मशीन के मॉनिटर का फोटो खींचें / Take Monitor Photo")
    st.info("💡 फोटो खींचने के बाद नीचे दी गई डिटेल्स भरें।")

with st.form("production_form"):
    st.subheader("दैनिक प्रोडक्शन एंट्री / Daily Production Entry")
    
    date = st.date_input("तारीख / Date")
    worker_name = st.text_input("कारीगर का नाम / Worker Name")
    machine_no = st.selectbox("मशीन नंबर / Machine No.", ["मशीन - १ / Machine - 1", "मशीन - २ / Machine - 2", "मशीन - ३ / Machine - 3", "मशीन - ४ / Machine - 4", "मशीन - ५ / Machine - 5"])
    
    design_no = st.text_input("डिजाइन नंबर / Design No.")
    production = st.number_input("कुल टांके / Total Stitches", min_value=0, step=1000)
    breakage = st.number_input("टोटल ब्रेकेज / Total Breakage", min_value=0, step=1)
    stop_time = st.text_input("स्टॉप टाइम / Stop Time (जैसे 15 mins)")
    frame_time = st.text_input("फ्रेम एंड टाइम / Frame End Time")
    
    submit_button = st.form_submit_button(label="सेव करो और बोनस गनो / Save and Calculate Bonus")

if submit_button:
    if worker_name.strip() == "":
        st.warning("कृपया कारीगर का नाम दाखिल करें। / Please enter the worker name.")
    else:
        bonus = 0
        if production > 250000:
            bonus = ((production - 250000) / 1000) * 2
        else:
            bonus = 0
            
        new_row = pd.DataFrame({
            'तारीख / Date': [str(date)],
            'कारीगर का नाम / Worker Name': [worker_name],
            'मशीन नंबर / Machine No.': [machine_no],
            'डिजाइन नंबर / Design No.': [design_no],
            'कुल टांके / Total Stitches': [production],
            'ब्रेकेज / Breakage': [breakage],
            'स्टॉप टाइम / Stop Time': [stop_time],
            'फ्रेम टाइम / Frame Time': [frame_time],
            'बोनस (₹) / Bonus': [round(bonus, 2)]
        })
        
        st.session_state.data = pd.concat([st.session_state.data, new_row], ignore_index=True)
        st.success(f"डेटा सफलतापूर्वक सेव हो गया! कुल बोनस: ₹ {round(bonus, 2)} / Saved successfully! Total Bonus: ₹ {round(bonus, 2)}")

st.markdown("---")
st.subheader("📊 कुल प्रोडक्शन और रिपोर्ट / Production and Detailed Report")

if not st.session_state.data.empty:
    st.dataframe(st.session_state.data, use_container_width=True)
    
    csv = st.session_state.data.to_csv(index=False).encode('utf-8')
