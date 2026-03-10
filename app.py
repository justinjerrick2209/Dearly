import streamlit as st
import random
import json
import google.generativeai as genai
from PIL import Image, ImageDraw, ImageFont
import io

st.set_page_config(page_title='Dearly', page_icon='💖', layout="centered")

genai.configure(api_key="AIzaSyBqNJh4mjbFQnKDn9mBDbdnaITMwHWhpRo")

st.markdown("""
<style>
    .poem-card {
        background-color: #ffffff;
        padding: 25px;
        border-radius: 12px;
        border-left: 8px solid #ff4b4b;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        font-family: 'Georgia', serif;
        color: #333333;
        line-height: 1.6;
        margin-bottom: 20px;
        white-space: pre-wrap;
    }
    .poem-header { color: #ff4b4b; font-style: italic; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

def generatePoem(name, gender):
    with open('poem.json', 'r') as file:
        data = json.load(file)
        opener = random.sample(data['openers'][gender], 4)
        middle = random.sample(data['middles'], 4)
        closers = random.sample(data['closers'], 4)
        
        s1 = [line.format(name=name).strip() for line in opener]
        s2 = [line.strip() for line in middle]
        s3 = [line.strip() for line in closers]
        
        return "\n".join(s1) + "\n\n" + "\n".join(s2) + "\n\n" + "\n".join(s3)

def generate_ai_poem(name, gender):
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = f"""
    Write a deeply meaningful, exact 12-line romantic/complimentary poem for {name} ({gender}).
    Focus on unique metaphors (nature, stars, time). 
    Use the name '{name}' ONLY ONCE in the whole poem.
    Do not repeat it. Focus on 'you' and 'your'.
    Keep it as plain text. No emojis.
    """
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return generatePoem(name, gender)

if 'poem' not in st.session_state:
    st.session_state.poem = ""
    st.session_state.user_name = ""
    st.session_state.user_gender = ""

st.title('Dearly 💖')

if not st.session_state.poem:
    st.header('A meaningful poem for you')
    name = st.text_input('Enter name:')
    gender = st.selectbox('Select gender:', ['Male', 'Female'])
    
    if st.button('Generate Poem'):
        if name:
            with st.spinner('Crafting...'):
                st.session_state.user_name = name
                st.session_state.user_gender = gender
                st.session_state.poem = generate_ai_poem(name, gender)
                st.rerun()
        else:
            st.warning('Please enter a name!')

else:
    st.divider()
    
    fmt_poem = st.session_state.poem.replace('\n', '<br>')
    st.markdown(f"""
    <div class="poem-card">
        <div class="poem-header">For {st.session_state.user_name}...</div>
        {fmt_poem}
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button('Generate Again'):
            st.session_state.poem = generate_ai_poem(st.session_state.user_name, st.session_state.user_gender)
            st.rerun()
    with col2:
        if st.button('Create New'):
            st.session_state.poem = ""
            st.rerun()