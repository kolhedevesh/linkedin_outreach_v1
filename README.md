🚀 LinkedIn Outreach Assistant (V1)

AI-powered LinkedIn outreach tool that helps you:

    🔍 Find relevant LinkedIn profiles
    
    ✍️ Generate personalized connection messages
    
    🎯 Target by role, industry, location, seniority
    
    🤖 Use LLMs for intelligent personalization
    
    🧪 Switch between Demo Mode and Real LinkedIn Search

Built as an MVP to enable high-quality networking for professionals exploring career opportunities.

🎯 Problem This Solves

Cold LinkedIn outreach is:

    Time consuming
    
    Hard to personalize at scale
    
    Often generic and spammy

This tool helps generate:

    Context-aware
    
    Role-relevant
    
    Industry-specific
    
    Career-focused outreach messages

Designed especially for:

    Job seekers
    
    Career switchers
    
    AI PM aspirants
    
    Founders exploring connections

🖥 Demo UI (Streamlit)

The app includes:


1️⃣ Search & Filters Tab

Your Background

Target Role

Industry

Location

Advanced Filters

Company size

Seniority

Experience range

Mode:

✅ Real LinkedIn Search (via SerpAPI)

🧪 Demo Mode (Simulated profiles)


2️⃣ Outreach Settings Tab

Primary goal

Unique value proposition

Message tone

Call-to-action type

Interests

Problems solved

Key achievements

Personalization slider


🧠 How It Works
1. Profile Discovery

Two modes:

🔹 Demo Mode

Uses LLM to generate realistic example profiles.

Prompt builder (prompt_builder.py) creates structured simulated outputs:

PROFILE 1
Name:
Current Role:
Company:
LinkedIn URL:
Message:


These are explicitly marked as simulated.

🔹 Real LinkedIn Search Mode

Uses SerpAPI

Performs LinkedIn search queries

Scrapes profile snippets from search results

Feeds extracted data into LLM

Generates personalized outreach messages

⚠️ Note: This project does NOT use LinkedIn’s official API.

2. Message Generation

LLM receives:

User background

Target role

Industry

Location

Profile data (real or simulated)

It generates a tailored message such as:

"Hi Ankit, I came across your profile as a fellow FinTech enthusiast and was impressed by your work in creating financial experiences that empower consumers..."

Users can:

Edit message

Copy directly into LinkedIn

Regenerate

🗂 Project Structure
linkedin_outreach_v1/
│
├── app.py                  # Streamlit UI
├── linkedin_search.py      # LinkedIn search logic
├── llm_client.py           # LLM abstraction layer
├── profile_generator.py    # Message + profile generator
├── prompt_builder.py       # Prompt templates
├── search_api.py           # Search interface
├── requirements.txt
├── .env.template
└── README.md

⚙️ Setup Instructions
1️⃣ Clone Repo
git clone https://github.com/kolhedevesh/linkedin_outreach_v1.git
cd linkedin_outreach_v1

2️⃣ Create Virtual Environment
python -m venv .venv
source .venv/bin/activate

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Add Environment Variables

Create .env file:

SERPAPI_API_KEY=your_serpapi_key
GOOGLE_API_KEY=your_google_llm_key


(Or whichever LLM provider you are using.)

5️⃣ Run Streamlit App
streamlit run app.py


App will open in browser.

🛑 Important Disclaimer

This project:

    Uses SerpAPI to retrieve LinkedIn search results
    
    Does NOT use LinkedIn’s official API
    
    Does NOT automate message sending
    
    Does NOT auto-connect or auto-DM
    
    Users must manually copy and send messages.
    
    Ensure compliance with:
    
    LinkedIn Terms of Service
    
    Local data regulations

This project is for educational and personal productivity use only.

🧪 Example Output

Input:

Industry: FinTech

Target Role: Product Manager

User background: Growth-focused PM

Generated message:

Hi Ankit, I came across your profile as a fellow FinTech enthusiast and was impressed by your work in creating financial experiences that empower consumers. As someone who designs features to drive user growth and engagement, I'm always looking for opportunities to learn from others in the space. Would love to connect and discuss some of the innovative approaches you're taking at FinTech.

🧱 MVP Status

Current Version: V1

Features:

    Search filtering
    
    Message generation
    
    Real & Demo mode
    
    Editable outputs
    
Not yet implemented:

    CRM tracking
    
    Follow-up automation
    
    Message variants
    
    Rate limiting
    
    Multi-account support
    
    Deployment pipeline

🚀 Future Roadmap

    Message A/B variants
    
    Follow-up generator
    
    Better prompt conditioning
    
    Structured output parsing
    
    Live message preview panel
    
    Deployment (Render / Railway / Vercel)
    
    CI/CD with GitHub Actions
    
    Analytics on response rate

💡 Why This Project Exists

Built as:
    
    A product thinking exercise
    
    A real-world AI application
    
    A career networking accelerator
    
    Designed with modular architecture to evolve beyond MVP.

🧠 Author

Devesh Kolhe
Product Manager → Transitioning into AI Product Management

Focused on:

AI-native product experiences

User engagement & lifecycle optimization

Structured problem solving

