import  streamlit as st
from langchain_google_genai import  ChatGoogleGenerativeAI

st.title("🦜🔗 Quickstart App")



#gemini_api_key ="AIzaSyDxZ2mkVGlxuE_Mt0WQkSkZT5KOcvSAVjQ"
def generate_response(input_text,gemini_api_key):
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", verbose="True",
                                 temperature=0.7, google_api_key=gemini_api_key)
    response = llm.invoke(input_text)

    main_content = clean_and_extract_main_content(response)
    return  main_content

def clean_and_extract_main_content(response):
    # Assuming response is an AIMessage object
    content = response.content
    if content:
        lines = content.split('\n')
        main_text = []

        for line in lines:
            if line.startswith('response_metadata='):
                break
            else:
                line = line.strip()
                if line:  # Skip empty lines
                    main_text.append(line)

        cleaned_text = ' '.join(main_text)
        return cleaned_text
    else:
        return "No content available"
# Main Streamlit form for text input and response display
with st.form('text_form'):
    text = st.text_area('Enter text:')
    submitted_text = st.form_submit_button('Submit Text')

# Sidebar form for API key input
with st.sidebar.form('api_key_form'):
    gemini_api_key = st.text_input('Enter API Key', type='password')
    submitted_api_key = st.form_submit_button('Submit API Key')

# Handle API key submission and display response
if submitted_api_key:
    if gemini_api_key and gemini_api_key.startswith('AIz'):
        st.success('API Key submitted successfully!')
    else:
        st.warning('Please enter a valid API Key!')

if submitted_text:
    if gemini_api_key and gemini_api_key.startswith('AIz'):
        response = generate_response(text, gemini_api_key)
        if response:
            st.write(response)
    else:
        st.warning('Please enter a valid API Key before submitting text.')