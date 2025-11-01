import streamlit as st
import requests
import io

API_URL = "http://127.0.0.1:8000"  # your FastAPI local endpoint

st.set_page_config(page_title="AI News & PDF Summarizer", page_icon="🧠", layout="centered")

st.title("📰 AI News & PDF Summarizer")
st.write("Enter a news URL or upload a PDF file to get an instant summary with sentiment analysis.")

option = st.radio("Choose an input type:", ["News URL", "PDF File"])

if option == "News URL":
    url = st.text_input("Enter the news article URL:")
    if st.button("Summarize Article") and url:
        with st.spinner("Summarizing..."):
            response = requests.post(f"{API_URL}/summarize-url/", data={"url": url})
            if response.status_code == 200:
                data = response.json()
                st.subheader(data['title'])
                st.write(data['summary'])
                st.info(f"Sentiment: **{data['sentiment']}** | Polarity: {data['polarity']:.2f}")
            else:
                st.error("Failed to summarize article.")
elif option == "PDF File":
    pdf_file = st.file_uploader("Upload a PDF file", type=["pdf"])
    if st.button("Summarize PDF") and pdf_file:
        with st.spinner("Analyzing PDF..."):
            files = {'file': (pdf_file.name, pdf_file.getvalue(), 'application/pdf')}
            response = requests.post(f"{API_URL}/summarize-pdf/", files=files)
            if response.status_code == 200:
                data = response.json()
                st.write(data['summary'])
                st.info(f"Sentiment: **{data['sentiment']}** | Polarity: {data['polarity']:.2f}")
            else:
                st.error("Failed to summarize PDF.")
