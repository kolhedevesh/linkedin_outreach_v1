def build_prompt(user_background, target_role, industry, location):

    return f"""
You are helping generate REALISTIC example LinkedIn profiles.

Create 5 profiles in this exact format:

PROFILE 1
Name:
Current Role:
Company:
LinkedIn URL:
Message:

Each profile must include a personalized LinkedIn connection message.

User background:
{user_background}

Target role:
{target_role}

Industry:
{industry}

Location:
{location}

Important:
These are example/simulated profiles, not scraped real people.
"""
