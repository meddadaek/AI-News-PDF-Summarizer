import ssl
import nltk
from newspaper import Article, Config
from textblob import TextBlob
from PyPDF2 import PdfReader

ssl._create_default_https_context = ssl._create_unverified_context
nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)

def summarize_url(url: str):
    config = Config()
    config.browser_user_agent = (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/120.0.0.0 Safari/537.36'
    )

    article = Article(url, config=config)
    article.download()
    article.parse()
    article.nlp()

    analysis = TextBlob(article.summary)
    sentiment = "Positive" if analysis.polarity > 0 else "Negative" if analysis.polarity < 0 else "Neutral"

    return {
        "title": article.title,
        "summary": article.summary,
        "authors": article.authors,
        "sentiment": sentiment,
        "polarity": analysis.polarity,
        "subjectivity": analysis.subjectivity
    }

def summarize_pdf(file):
    pdf = PdfReader(file)
    text = " ".join(page.extract_text() for page in pdf.pages if page.extract_text())
    blob = TextBlob(text)
    summary = " ".join(blob.sentences[:5])  # crude short summary

    sentiment = "Positive" if blob.polarity > 0 else "Negative" if blob.polarity < 0 else "Neutral"
    return {
        "summary": summary,
        "sentiment": sentiment,
        "polarity": blob.polarity,
        "subjectivity": blob.subjectivity
    }
