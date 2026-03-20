# 📧 Cold Email Generator

Job hunting is time-consuming. Writing personalised cold emails for every application is even more so. This tool solves that.

Paste a company's careers page URL, upload your resume, and the app uses AI to read the job listing, match it to your actual experience and projects, and generate a tailored cold email ready to send — in seconds.

---

## The Problem It Solves

Most cold emails fail because they're generic. Hiring managers can tell when someone has copy-pasted the same email to 50 companies. This tool reads the actual job requirements and your real experience to write an email that speaks directly to what that specific company needs.

---

## How It Works

<img width="1000" alt="Main Interface" src="https://github.com/user-attachments/assets/0e440c5f-47ee-4c0f-adf3-64dae1c7c144" />


1. **Upload your resume** — the AI reads your actual skills, experience, and achievements
2. **Paste a careers page URL** — the app scrapes the job listing and extracts the role requirements
3. **Choose a tone** — Professional, Friendly, Confident, or Concise
4. **Generate** — the AI matches your experience to their needs and writes the email

<img width="1000" alt="Generated Email" src="https://github.com/user-attachments/assets/1cc701c2-e0f4-4e49-8328-956a5a720e92" />


Your last 5 generated emails are saved in the sidebar so you can always refer back to a previous version.

<img width="400"  alt="Email History" src="https://github.com/user-attachments/assets/f951bce5-6dac-461e-8a1c-c8b7c203dcd7" />


---

## Architecture Diagram
<img width="1400"  alt="image" src="https://github.com/user-attachments/assets/9b12dc09-766b-4a44-991e-5d3a48293014" />


## Features

- 📄 **Resume upload** — AI reads your actual experience to personalise every email
- 🎯 **Smart job scraping** — extracts role, skills and requirements from careers pages
- 💼 **Portfolio matching** — links your most relevant projects to the job requirements
- 🎨 **Tone selector** — choose between Professional, Friendly, Confident, or Concise
- 📋 **Email history** — last 5 generated emails saved in session for easy reference
- 🗑️ **Portfolio cache reset** — update your portfolio and refresh with one click

---

## Tech Stack

| Tool | What it does |
|---|---|
| **LLaMA 3.3 70B via Groq** | The AI model that reads the job listing and writes the email |
| **LangChain** | Connects the AI model to the app and structures the prompts |
| **ChromaDB** | Stores your portfolio projects and matches them to job requirements |
| **Streamlit** | The web interface you interact with |
| **pdfplumber** | Extracts text from your uploaded resume PDF |
| **Python** | The programming language everything is built in |

---

## Setup

1. Clone the repo
2. Install dependencies:
```bash
pip install langchain langchain-community langchain-groq chromadb streamlit python-dotenv pdfplumber
```
3. Create a `.env` file in the root folder:
```
GROQ_API_KEY=your_groq_api_key_here
```
4. Update `app/resource/my_portfolio.csv` with your own projects and GitHub links
5. Run the app:
```bash
streamlit run app/main.py
```

---

## Usage

1. Upload your resume as a PDF
2. Paste a direct company careers page URL
3. Select your preferred email tone
4. Click **Generate Email**
5. Copy and send!

---

## Important Notes

- Use direct company careers page URLs only (e.g. `careers.google.com`)
- Job boards like LinkedIn, Seek, or Ashby are not supported
- Your `.env` file is gitignored — never share your API key publicly
