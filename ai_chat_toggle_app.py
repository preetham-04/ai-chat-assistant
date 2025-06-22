import streamlit as st
import openai
import ollama
import google.generativeai as genai

# Page configuration
st.set_page_config(page_title="🔀 Multi-LLM Chat App", layout="centered")
st.title("🤖 Multi-LLM Chat Assistant")

# Model selection
mode = st.selectbox("Choose LLM Provider", ["OpenAI", "Ollama", "Gemini"])

# Prompt input
prompt = st.text_area("📝 Enter your prompt here:")

# Sidebar: model-specific settings
if mode == "OpenAI":
    st.sidebar.header("🔐 OpenAI Settings")
    openai_api_key = st.sidebar.text_input("Enter OpenAI API Key", type="password")
    openai_model = st.sidebar.selectbox("Choose OpenAI Model", ["gpt-3.5-turbo", "gpt-4"])

elif mode == "Ollama":
    st.sidebar.header("🧩 Ollama Settings")
    ollama_model = st.sidebar.selectbox("Choose Ollama Model", ["llama3", "mistral", "gemma"])

elif mode == "Gemini":
    st.sidebar.header("🔐 Gemini Settings")
    gemini_api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")
    gemini_model = st.sidebar.selectbox("Choose Gemini Model", ["gemini-pro"])

# Action button
if st.button("🚀 Generate Response"):
    if not prompt.strip():
        st.warning("⚠️ Please enter a prompt.")
    
    # OpenAI response
    elif mode == "OpenAI":
        if not openai_api_key:
            st.warning("⚠️ OpenAI API Key required.")
        else:
            try:
                client = openai.OpenAI(api_key=openai_api_key)
                with st.spinner("🔄 Contacting OpenAI..."):
                    response = client.chat.completions.create(
                        model=openai_model,
                        messages=[{"role": "user", "content": prompt}],
                        temperature=0.7,
                        max_tokens=500,
                    )
                output = response.choices[0].message.content
                st.success(f"✅ Response from OpenAI ({openai_model})")
                st.markdown(output)
            except Exception as e:
                st.error(f"❌ OpenAI Error: {e}")

    # Ollama response
    elif mode == "Ollama":
        try:
            with st.spinner(f"🔄 Running {ollama_model} via Ollama..."):
                response = ollama.chat(
                    model=ollama_model,
                    messages=[{"role": "user", "content": prompt}],
                )
            output = response["message"]["content"]
            st.success(f"✅ Response from Ollama ({ollama_model})")
            st.markdown(output)
        except Exception as e:
            st.error(f"❌ Ollama Error: {e}")

    # Gemini response
    elif mode == "Gemini":
        if not gemini_api_key:
            st.warning("⚠️ Gemini API Key required.")
        else:
            try:
                genai.configure(api_key=gemini_api_key)
                model = genai.GenerativeModel(gemini_model)
                with st.spinner("🔄 Contacting Gemini..."):
                    response = model.generate_content(prompt)
                output = response.text
                st.success(f"✅ Response from Gemini ({gemini_model})")
                st.markdown(output)
            except Exception as e:
                st.error(f"❌ Gemini Error: {e}")
