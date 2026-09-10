[11-09-2026 00:12] Ganga traders: import streamlit as st
import pandas as pd

st.set_page_config(page_title="Embroidery Machine Bonus / एम्ब्रॉयडरी मशीन बोनस", layout="centered")

st.title("🧵 Embroidery Machine Production & Bonus System\nएम्ब्रॉयडरी मशीन प्रोडक्शन और बोनस सिस्टम")

if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=['तारीख / Date', 'कारीगर का नाम / Worker Name', 'मशीन नंबर / Machine No.', 'कुल प्रोडक्शन (टाका अथवा पीस) / Production', 'बोनस (₹) / Bonus'])

with st.form("production_form"):
    st.subheader("दैनिक प्रोडक्शन एंट्री / Daily Production Entry")
    
    date = st.date_input("तारीख / Date")
    worker_name = st.text_input("कारीगर का नाम / Worker Name")
    machine_no = st.selectbox("मशीन नंबर / Machine No.", ["मशीन - १ / Machine - 1", "मशीन - २ / Machine - 2", "मशीन - ३ / Machine - 3", "मशीन - ४ / Machine - 4", "मशीन - ५ / Machine - 5"])
    production = st.number_input("कुल प्रोडक्शन (टाका अथवा पीस) / Total Production", min_value=0, step=1000)
    
    submit_button = st.form_submit_button(label="सेव करो और बोनस गनो / Save and Calculate Bonus")

if submit_button:
    if worker_name.strip() == "":
        st.warning("कृपया कारीगर का नाम दाखिल करें। / Please enter the worker name.")
    else:
        bonus = 0
        if production > 250000:
            # 2,50,000 से ऊपर के हर 1000 टांके पर 2 रुपये की गणना
            bonus = ((production - 250000) / 1000) * 2
        else:
            bonus = 0
            
        new_row = pd.DataFrame({
            'तारीख / Date': [str(date)],
            'कारीगर का नाम / Worker Name': [worker_name],
            'मशीन नंबर / Machine No.': [machine_no],
            'कुल प्रोडक्शन (टाका अथवा पीस) / Production': [production],
            'बोनस (₹) / Bonus': [round(bonus, 2)]
        })
        
        st.session_state.data = pd.concat([st.session_state.data, new_row], ignore_index=True)
        st.success(f"बोनस सफलतापूर्वक जोड़ दिया गया है! कुल बोनस: ₹ {round(bonus, 2)} / Bonus calculated successfully! Total Bonus: ₹ {round(bonus, 2)}")

st.markdown("---")
st.subheader("📊 कुल प्रोडक्शन और बोनस रिपोर्ट / Production and Bonus Report")

if not st.session_state.data.empty:
    st.dataframe(st.session_state.data, use_container_width=True)
    
    csv = st.session_state.data.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="रिपोर्ट डाउनलोड करें (CSV) / Download Report (CSV)",
        data=csv,
        file_name='embroidery_bonus_report.csv',
        mime='text/csv',
    )
else:
    st.info("अभी तक कोई एंट्री की गई नहीं है। / No entries recorded yet.")
[11-09-2026 00:21] Ganga traders: import streamlit as st
import pandas as pd

st.set_page_config(page_title="Embroidery Machine Bonus / एम्ब्रॉयडरी मशीन बोनस", layout="centered")

st.title("🧵 Embroidery Machine Production & Bonus System\nएम्ब्रॉयडरी मशीन प्रोडक्शन और बोनस सिस्टम")

if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=[
        'तारीख / Date', 'कारीगर का नाम / Worker Name', 'मशीन नंबर / Machine No.', 
        'डिजाइन नंबर / Design No.', 'कुल टांके / Total Stitches', 'ब्रेकेज / Breakage', 
        'स्टॉप टाइम / Stop Time', 'फ्रेम टाइम / Frame Time', 'बोनस (₹) / Bonus'
    ])

with st.form("production_form"):
    st.subheader("दैनिक प्रोडक्शन एंट्री (फोटो या मैन्युअल) / Daily Production Entry")
    
    date = st.date_input("तारीख / Date")
    worker_name = st.text_input("कारीगर का नाम / Worker Name")
    machine_no = st.selectbox("मशीन नंबर / Machine No.", ["मशीन - १ / Machine - 1", "मशीन - २ / Machine - 2", "मशीन - ३ / Machine - 3", "मशीन - ४ / Machine - 4", "मशीन - ५ / Machine - 5"])
    
    # ऑप्शन: फोटो अपलोड या मैन्युअल टाइपिंग
    input_mode = st.radio("डेटा इनपुट का तरीका चुनें / Choose Data Input Method:", ["मैन्युअल टाइप करें / Type Manually", "मॉनिटर फोटो अपलोड करें / Upload Monitor Photo"])
    
    design_no = ""
    production = 0
    breakage = 0
    stop_time = "0"
    frame_time = "0"
    
    if input_mode == "मॉनिटर फोटो अपलोड करें / Upload Monitor Photo":
        monitor_photo = st.file_uploader("मशीन के मॉनिटर का फोटो चुनें / Choose Monitor Photo", type=["jpg", "png", "jpeg"])
        st.info("💡 फोटो अपलोड करने पर OCR द्वारा डेटा रीड किया जाएगा (फिलहाल आप नीचे मैन्युअल वैल्यू भी भर सकते हैं)।")
        # यहाँ भविष्य में OCR कोडिंग जोड़ी जा सकती है, अभी सुरक्षा के लिए मैन्युअल फील्ड्स साथ में रखे हैं
        design_no = st.text_input("डिजाइन नंबर (फोटो से / Manual) / Design No.")
        production = st.number_input("कुल टांके / Total Stitches", min_value=0, step=1000)
        breakage = st.number_input("टोटल ब्रेकेज / Total Breakage", min_value=0, step=1)
        stop_time = st.text_input("स्टॉप टाइम / Stop Time (जैसे 15 mins)")
        frame_time = st.text_input("फ्रेम एंड टाइम / Frame End Time")
    else:
        design_no = st.text_input("डिजाइन नंबर / Design No.")
        production = st.number_input("कुल टांके / Total Stitches", min_value=0, step=1000)
        breakage = st.number_input("टोटल ब्रेकेज / Total Breakage", min_value=0, step=1)
        stop_time = st.text_input("स्टॉप टाइम / Stop Time")
        frame_time = st.text_input("फ्रेम एंड टाइम / Frame End Time")
    
    submit_button = st.form_submit_button(label="सेव करो और बोनस गनो / Save and Calculate Bonus")

if submit_button:
    if worker_name.strip() == "":
        st.warning("कृपया कारीगर का नाम दाखिल करें। / Please enter the worker name.")
    else:
        bonus = 0
        if production > 250000:
            # 2,50,000 से ऊपर के हर 1000 टांके पर 2 रुपये की गणना
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
