# PubMed QA Application

Een Nederlandse applicatie voor het analyseren en vertalen van PubMed abstracts met behulp van AI.

## Functionaliteiten

1. **Abstract Ophalen**

   - Zoek PubMed artikelen op basis van PMID
   - Automatische caching van opgehaalde abstracts
   - Ondersteuning voor meerdere PMID's tegelijk

2. **AI Vraag & Antwoord**

   - Stel vragen over de abstracts in het Nederlands
   - Krijg gedetailleerde antwoorden met referenties naar specifieke artikelen
   - Markering van informatie die niet direct uit de tekst komt [NIET IN TEKST]
   - Markering van tegenstrijdige informatie [TEGENSTRIJDIG]
   - Intelligente caching van antwoorden

3. **Vertalingen**
   - Vertaal PubMed abstracts naar het Nederlands
   - Behoud van PMID referenties
   - Caching van vertalingen voor snelle toegang

## Installatie

1. Clone de repository:

```bash
git clone [repository-url]
cd pubmed_qa
```

2. Maak een virtuele omgeving aan en activeer deze:

```bash
python -m venv venv
source venv/bin/activate  # Voor Linux/Mac
# OF
venv\Scripts\activate  # Voor Windows
```

3. Installeer de vereiste packages:

```bash
pip install -r requirements.txt
```

4. Maak een `.env` bestand aan met je OpenAI API key:

```
OPENAI_API_KEY=jouw-api-key-hier
```

## Gebruik

1. Start de applicatie:

```bash
python app.py
```

2. Open een webbrowser en ga naar:

```
http://localhost:5000
```

3. De applicatie heeft twee hoofdpagina's:
   - `/` - Vraag & Antwoord interface
   - `/vertaling` - Vertaalinterface

### Vraag & Antwoord

1. Voer één of meerdere PMID's in (gescheiden door komma's)
2. Stel je vraag in het Nederlands
3. Het antwoord zal:
   - Verwijzen naar specifieke artikelen (PMID)
   - Tegenstrijdigheden markeren
   - Aangeven wanneer informatie niet direct uit de tekst komt

### Vertalingen

1. Voer één of meerdere PMID's in
2. De abstracts worden automatisch vertaald naar het Nederlands
3. Zowel originele als vertaalde tekst wordt getoond

## Caching

De applicatie gebruikt een slim caching systeem voor:

- PubMed abstracts
- AI antwoorden
- Vertalingen

Dit zorgt voor:

- Snellere responstijden
- Minder API-calls
- Consistente antwoorden

## Technische Details

- Flask web framework
- OpenAI GPT-4 voor AI functionaliteit
- PubMed E-utilities voor abstract ophalen
- JSON-gebaseerd caching systeem
- Normalisatie van vragen voor effectievere caching

## Licentie

[Voeg licentie informatie toe]
