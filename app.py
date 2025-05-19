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
Je bent een Nederlands sprekende medisch expert. Analyseer de volgende teksten uit PubMed en beantwoord de vraag.
Belangrijke instructies:
1. Verwijs naar de specifieke artikelen (PMID) waar je je antwoord op baseert
2. Als er tegenstrijdige informatie is tussen artikelen, markeer dit met [TEGENSTRIJDIG] en leg uit waarom
3. Geef aan welke artikelen elkaar bevestigen en welke elkaar tegenspreken
4. Als het antwoord niet direct in de gegeven teksten staat, markeer dit met [NIET IN TEKST] en geef dan een betrouwbaar antwoord gebaseerd op je medische expertise
5. Gebruik alleen informatie die direct uit de gegeven teksten komt, tenzij je [NIET IN TEKST] gebruikt

Teksten:
{text}

Vraag:
{question}

Antwoord in het Nederlands, in eenvoudige en begrijpelijke taal:
"""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.5
    )
    answer = response.choices[0].message['content'].strip()
    
    # Mark contradictions and non-text answers in blue
    answer = answer.replace("[TEGENSTRIJDIG]", '<span class="contradiction">[TEGENSTRIJDIG]</span>')
    answer = answer.replace("[NIET IN TEKST]", '<span class="contradiction">[NIET IN TEKST]</span>')
    return answer

def translate_abstract_to_dutch(text):
    # Split the text into individual abstracts
    abstracts = text.split('\n\n')
    translated_abstracts = []
    
    for abstract in abstracts:
        if not abstract.strip():
            continue
            
        # Extract PMID if present
        pmid = ""
        if "(PMID:" in abstract:
            pmid_start = abstract.find("(PMID:")
            pmid_end = abstract.find(")", pmid_start)
            if pmid_end != -1:
                pmid = abstract[pmid_start:pmid_end + 1]
                abstract = abstract[pmid_end + 1:].strip()
        
        prompt = f"""
Vertaal de volgende medische abstract naar het Nederlands. Gebruik duidelijke en begrijpelijke taal.
Behoud de PMID referentie en vertaal alleen de abstract tekst.

{abstract}

Vertaling:
"""
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=2000  # Limit response length
            )
            translated = response.choices[0].message['content'].strip()
            if pmid:
                translated = f"{pmid} {translated}"
            translated_abstracts.append(translated)
        except Exception as e:
            print(f"Error translating abstract: {e}")
            translated_abstracts.append(f"Fout bij vertalen: {abstract}")
    
    return '\n\n'.join(translated_abstracts)

@app.route("/", methods=["GET", "POST"])
def index():
    answer = ""
    abstract = ""
    pmid = ""
    question = ""
    pmids_raw = ""
    combined_abstracts = ""
    if request.method == "POST":
        pmids_raw = request.form["pmids"]
        question = request.form["question"]
        pmid_list = pmids_raw.split(",")
        combined_abstracts = get_multiple_abstracts(pmid_list)
        answer = ask_question_about_text(combined_abstracts, question)
    return render_template("index.html", abstract=combined_abstracts, pmids=pmids_raw, answer=answer, pmid=pmid, question=question)

@app.route("/vertaling", methods=["GET", "POST"])
def vertaling():
    translated = ""
    abstracts = ""
    pmids_raw = ""
    combined_abstracts = ""
    if request.method == "POST":
        pmids_raw = request.form["pmids"]
        pmid_list = pmids_raw.split(",")
        combined_abstracts = get_multiple_abstracts(pmid_list)
        translated = translate_abstract_to_dutch(combined_abstracts)
    return render_template("vertaling.html", pmids=pmids_raw, abstracts=combined_abstracts, translated=translated)

def get_multiple_abstracts(pmids):
    abstracts = []
    for pmid in pmids:
        abs_text = get_pubmed_abstract(pmid.strip())
        if abs_text and abs_text != "Geen abstract gevonden.":
            abstracts.append(f"(PMID: {pmid.strip()}) {abs_text}")
    return "\n\n".join(abstracts)

if __name__ == "__main__":
    app.run(debug=True)
