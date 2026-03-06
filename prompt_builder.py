def build_prompt(
    user_background,
    target_role,
    industry,
    location,
    name="",
    role="",
    company="",
    about="",
    user_goal="",
    value_proposition="",
):

    resolved_role = role or target_role or ""
    resolved_company = company or industry or ""
    resolved_about = about or location or ""

    return f"""
You are helping a professional write a LinkedIn outreach message.

Target Profile:
NAME: {name or 'Professional'}
ROLE: {resolved_role}
COMPANY: {resolved_company}
ABOUT: {resolved_about}

Sender Background:
USER_BACKGROUND: {user_background}

Goal:
USER_GOAL: {user_goal}

Value Proposition:
VALUE_PROPOSITION: {value_proposition}

Write a concise LinkedIn connection request under 280 characters.

Guidelines:
- Keep the tone natural and conversational.
- Reference one specific aspect of the person's work, role, or experience.
- Avoid generic praise such as "I'm impressed".
- Avoid repeating the same opening structure across messages.
- Use varied openings such as:
    - "I noticed your work on..."
    - "Your experience in..."
    - "Came across your work on..."
    - "Saw that you're working on..."
    - "Your background in..."

Additional constraints:
- Keep the message under ~280 characters.
- Do not sound overly formal or robotic.
- Avoid long sentences.
- End with a light connection request such as:
    - "Would love to connect."
    - "Open to connecting?"
    - "Would enjoy exchanging ideas."

Do NOT use placeholders.
Do NOT repeat the same phrasing across outputs.
Return ONLY the message text.
"""
