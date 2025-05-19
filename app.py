from flask import Flask, request, render_template
import requests
from bs4 import BeautifulSoup
import openai
import os
from dotenv import load_dotenv


load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

def get_pubmed_abstract(pmid):
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    params = {
        "db": "pubmed",
        "id": pmid,
        "retmode": "xml"
    }
    response = requests.get(url, params=params)
    soup = BeautifulSoup(response.content, "lxml")
    abstract_text = soup.find("abstracttext")
    if abstract_text:
        return abstract_text.get_text(strip=True)
    return "Geen abstract gevonden."


def ask_question_about_text(text, question):
    prompt = f"""
Je bent een Nederlands sprekende medisch expert. Beantwoord de vraag hieronder op basis van deze tekst uit PubMed.

Tekst:
{text}

Vraag:
{question}

Antwoord in het Nederlandse, inenvoudige en begrijpelijke taal:
"""
    response = openai.ChatCompletion.create(
        model="gpt-4",  # of "gpt-3.5-turbo"
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.5
    )
    return response.choices[0].message['content'].strip()

def translate_abstract_to_dutch(text):
    prompt = f"""
Vertaal de volgende medische abstract naar het Nederlands. Gebruik duidelijke en begrijpelijke taal:

{text}

Vertaling:
"""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )
    return response.choices[0].message['content'].strip()

@app.route("/", methods=["GET", "POST"])
def index():
    answer = ""
    abstract = ""
    pmid = ""
    question = ""
    if request.method == "POST":
        pmid = request.form["pmid"]
        question = request.form["question"]
        abstract = get_pubmed_abstract(pmid)
        answer = ask_question_about_text(abstract, question)
    return render_template("index.html", abstract=abstract, answer=answer, pmid=pmid, question=question)

@app.route("/vertaling", methods=["GET", "POST"])
def vertaling():
    translated = ""
    abstract = ""
    pmid = ""
    if request.method == "POST":
        pmid = request.form["pmid"]
        abstract = get_pubmed_abstract(pmid)
        translated = translate_abstract_to_dutch(abstract)
    return render_template("vertaling.html", pmid=pmid, abstract=abstract, translated=translated)



if __name__ == "__main__":
    app.run(debug=True)
