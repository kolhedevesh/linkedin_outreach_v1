# 🔗 LinkedIn Outreach Assistant

A powerful Streamlit-based tool that helps you find LinkedIn profiles and generate personalized outreach messages using AI. Perfect for founders, job seekers, recruiters, and anyone looking to build meaningful professional connections on LinkedIn.

## ✨ Features

- **Smart LinkedIn Search**: Find relevant profiles by role, industry, and location
- **AI-Powered Messages**: Generate personalized outreach messages using LLM
- **Multiple Presets**: Quick-start templates for Founders and Job Seekers
- **Customizable Tone**: Choose from professional, friendly, or casual tones
- **Real-time & Demo Modes**: Test with demo profiles or perform real LinkedIn searches
- **Multiple CTA Options**: Coffee chats, demos, meetings, or quick questions
- **Editable Messages**: Fine-tune generated messages before sending

## 🚀 Getting Started

### Prerequisites

- Python 3.7+
- API Keys (at least one):
  - Google Custom Search API credentials
  - OR Bing Search API credentials
  - Optional: LLM API key (for AI-generated messages)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/kolhedevesh/linkedin_outreach_v1.git
   cd linkedin_outreach_v1
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   
   Copy the `.env.template` to `.env`:
   ```bash
   cp .env.template .env
   ```
   
   Edit `.env` and add your API credentials:
   ```env
   # Google Custom Search API (Recommended)
   GOOGLE_API_KEY=your_google_api_key_here
   GOOGLE_SEARCH_ENGINE_ID=your_search_engine_id_here
   
   # OR Bing Search API (Alternative)
   BING_SEARCH_KEY=your_bing_search_key_here
   
   # Optional: LLM API for AI-generated messages
   # LLAMA_API_KEY=your_llama_key_here
   ```

### Getting API Keys

#### Google Custom Search API
1. Visit [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable "Custom Search API"
4. Create credentials (API key)
5. Create a Custom Search Engine at [Google CSE](https://cse.google.com/cse/)
6. Get your Search Engine ID

#### Bing Search API (Alternative)
1. Visit [Azure Portal](https://portal.azure.com/)
2. Create a "Bing Search v7" resource
3. Copy your API key from the resource

## 📖 Usage

1. **Start the application**
   ```bash
   streamlit run app.py
   ```

2. **Configure your search** (Tab 1: Search & Filters)
   - Select a preset (Founder/Job Seeker) or customize
   - Enter your background
   - Specify target role(s) and industry
   - Set location preferences

3. **Customize your message** (Tab 2: Outreach Settings)
   - Define your primary goal
   - Describe your value proposition
   - Choose message tone and call-to-action

4. **Generate profiles**
   - Choose between Real LinkedIn Search or Demo Mode
   - Click "Generate Profiles"
   - Review and edit generated messages
   - Copy messages to send on LinkedIn

## 🏗️ Project Structure

```
linkedin_outreach_v1/
├── app.py                  # Main Streamlit application
├── search_client.py        # LinkedIn profile search interface
├── search_api.py          # Search API client implementation
├── profile_generator.py   # Profile metadata parsing and message generation
├── llm_client.py          # LLM integration for AI-powered messages
├── requirements.txt       # Python dependencies
├── .env.template         # Environment variables template
└── README.md             # This file
```

## 🔧 Configuration

### Search Providers

The app supports multiple search providers. Configure in `.env`:
- **Google Custom Search**: Best for comprehensive results
- **Bing Search**: Alternative option

### Message Personalization

Customize message generation by adjusting:
- **Tone**: Professional & Formal, Professional & Friendly, Casual & Direct
- **Goal**: Networking, B2B Sales, Recruiting, Investor Outreach
- **CTA Type**: Coffee chat, demo request, meeting, quick question

## 💡 Tips for Best Results

1. **Be Specific**: Use specific roles and industries for better targeting
2. **Localize**: Specify city names rather than broad regions for faster searches
3. **Test First**: Use Demo Mode to test your messaging before real searches
4. **Personalize**: Always review and customize generated messages
5. **Follow Up**: Track your outreach and follow up appropriately

## 🛠️ Development

### Running Tests

```bash
# Run integration tests
python test_integration.py

# Run search API tests
python test_search_api.py

# Run LLM tests
python test_llama.py
```

## 📝 Example Workflows

### For Founders
1. Select "Founder" preset
2. Describe your product/service
3. Target relevant roles (VPs, Product Managers)
4. Choose B2B Sales/Partnership goal
5. Generate and personalize messages

### For Job Seekers
1. Select "Job Seeker" preset
2. Describe your experience
3. Target hiring managers/recruiters
4. Choose networking or recruiting goal
5. Generate conversation starters

## ⚠️ Important Notes

- **Rate Limits**: Be mindful of API rate limits for search providers
- **LinkedIn ToS**: This tool generates messages for manual sending. Always follow LinkedIn's terms of service
- **Privacy**: Never share sensitive information in outreach messages
- **Quality**: Always review and personalize AI-generated messages

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is provided as-is for personal and commercial use.

## 🐛 Troubleshooting

### Search Timeouts
- Use more specific location (city vs country)
- Try fewer industries at once
- Use Demo Mode to test message generation first

### API Errors
- Verify API keys are correctly set in `.env`
- Check API quota/limits haven't been exceeded
- Ensure the search engine is configured for LinkedIn search

### No Results Found
- Broaden your search criteria
- Try alternative role titles
- Check if location format is correct

## 📬 Support

For issues, questions, or suggestions, please open an issue on GitHub.

---

Made with ❤️ to help you build meaningful professional connections
