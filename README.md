# LinkedIn Outreach Assistant

An AI-powered tool that helps generate **personalized LinkedIn outreach messages** by analyzing target profiles and combining them with your professional background and outreach goals.

The application allows users to search for relevant LinkedIn profiles and generate tailored networking messages using an LLM-based prompt generation pipeline.

### Live App
https://ai-linkedin-outreach.streamlit.app

---

# Overview

Networking on LinkedIn often requires writing personalized messages that reference the recipient’s background and align with your own goals.

This tool automates that process by combining:

- Profile information of the target user
- Your professional background
- Outreach objective
- Value proposition
- Desired tone and call-to-action

The system then generates a **context-aware outreach message** suitable for LinkedIn.

---

# Features

- LinkedIn profile discovery using SerpAPI
- AI-generated personalized outreach messages
- Configurable outreach settings:
  - Primary goal
  - Value proposition
  - Tone of message
  - Call-to-action
- Debug logs for prompt inspection
- Streamlit-based interactive UI
- Deployed as a public web application

---

# Live Demo

Access the deployed application:

https://ai-linkedin-outreach.streamlit.app

---

# Tech Stack

### Frontend
- Streamlit

### Backend
- Python

### AI / LLM
- Groq API (LLM inference)

### Data Source
- SerpAPI (LinkedIn search results)

### Key Libraries
- requests  
- pandas  
- python-dotenv  

---

# Project Structure

```
linkedin_outreach_v1
│
├── app.py                # Streamlit application
├── linkedin_search.py    # LinkedIn profile search via SerpAPI
├── search_api.py         # API interaction layer
├── search_client.py      # Search result handling
│
├── prompt_builder.py     # Prompt construction for LLM
├── profile_generator.py  # Profile summarization logic
├── llm_client.py         # Groq API integration
│
├── requirements.txt
├── README.md
```

---

# How It Works

1. User enters search filters (role, industry, location).
2. The system retrieves LinkedIn profile results via SerpAPI.
3. Profile data is processed and summarized.
4. A prompt is dynamically constructed using:
   - Target profile information
   - User background
   - Outreach goal
5. The LLM generates a personalized LinkedIn outreach message.

---

# Example Workflow

### Input

User Background  
"I am a Product Manager focused on building growth-oriented features."

Target Profile  
Engineering Manager in a SaaS company

Goal  
Networking and relationship building

### Output

A personalized outreach message referencing the target profile’s experience and aligning it with the sender’s interests.

---

# Local Setup

Clone the repository

```
git clone https://github.com/kolhedevesh/linkedin_outreach_v1.git
cd linkedin_outreach_v1
```

Create a virtual environment

```
python -m venv venv
source venv/bin/activate
```

Install dependencies

```
pip install -r requirements.txt
```

Add API keys

Create `.streamlit/secrets.toml`

```
SERPAPI_API_KEY="your_key"
GROQ_API_KEY="your_key"
```

Run the application

```
streamlit run app.py
```

---

# Deployment

The application is deployed using **Streamlit Community Cloud**.

Deployment steps:

1. Push code to GitHub  
2. Connect repository to Streamlit Cloud  
3. Configure secrets  
4. Deploy the app  

---

# Future Improvements

- Multi-message generation variants
- CSV upload for bulk outreach
- Automatic LinkedIn lead extraction
- Message A/B testing
- CRM integrations
- Outreach analytics dashboard

---

# Author

Devesh Kolhe  

GitHub  
https://github.com/kolhedevesh

---

# License

MIT License
