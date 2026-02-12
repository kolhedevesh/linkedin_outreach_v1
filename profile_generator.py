"""Generate personalized outreach messages and extract profile metadata"""

import re
from typing import Dict
from llm_client import query_llama


def parse_profile_metadata(title: str, snippet: str) -> Dict[str, str]:
    metadata = {
        "name": "",
        "current_role": "",
        "company": "",
        "experience_level": "Unknown",
        "key_skills": []
    }

    name_match = re.match(r"^([^-|•]+?)(?:\s*[-|•]\s*|$)", title)
    if name_match:
        metadata["name"] = name_match.group(1).strip()

    role_parts = title.split(" - ")
    if len(role_parts) > 1:
        metadata["current_role"] = role_parts[0].strip()

    company_match = re.search(r"@\s*([^\s|•-]+)", title + " " + snippet)
    if company_match:
        metadata["company"] = company_match.group(1).strip()
    else:
        parts = re.split(r'\s*[-|•]\s*', title)
        if len(parts) > 1:
            metadata["company"] = parts[-1].strip()

    snippet_lower = (snippet + title).lower()
    if any(word in snippet_lower for word in ["principal", "director", "vp", "head of", "chief", "c-level"]):
        metadata["experience_level"] = "Executive"
    elif any(word in snippet_lower for word in ["senior", "lead", "staff", "principal", "manager"]):
        metadata["experience_level"] = "Senior"
    elif any(word in snippet_lower for word in ["mid-level", "3-5 years", "4+ years", "5+ years"]):
        metadata["experience_level"] = "Mid-Level"
    elif any(word in snippet_lower for word in ["junior", "1-2 years", "2-3 years", "entry", "graduate"]):
        metadata["experience_level"] = "Junior"

    skill_keywords = [
        "product management", "growth", "b2b", "b2c", "saas", "enterprise",
        "strategy", "analytics", "data", "customer", "market", "launch",
        "monetization", "pricing", "fundraising", "leadership", "innovation"
    ]

    combined_text = (snippet + title).lower()
    found_skills = [skill for skill in skill_keywords if skill in combined_text]
    metadata["key_skills"] = list(set(found_skills))[:5]

    return metadata


def _base_prompt(
    user_background: str,
    profile: Dict,
    relationship_goal: str,
    value_prop: str,
    tone: str,
    cta_type: str,
    interests: str,
    problem_solving: str,
    achievements: str,
    personalization_level: int,
    mention_mutual: bool,
):
    personalization_hint = {
        1: "Keep very brief and generic",
        2: "Basic personalization",
        3: "Good balance of personal and concise",
        4: "Deep personalization with multiple references",
        5: "Highly personalized, detailed, reference their specific achievements"
    }

    prompt = f"""Generate a LinkedIn outreach message based on the context below.

CONTEXT:
Your Background: {user_background or 'Not specified'}
Value Proposition: {value_prop or 'Not specified'}
Problem You Solve: {problem_solving or 'Not specified'}
Achievements: {achievements or 'Not specified'}
Interests: {interests or 'Not specified'}

TARGET:
- Name: {profile.get('name', 'Professional')}
- Role: {profile.get('current_role', 'Unknown')}
- Company: {profile.get('company', 'Unknown')}
- Experience Level: {profile.get('experience_level', 'Unknown')}
- Key Skills: {', '.join(profile.get('key_skills', []))}
- Profile Summary: {profile.get('snippet', '')}

OUTREACH PARAMETERS:
- Goal: {relationship_goal}
- Tone: {tone}
- Call-to-Action: {cta_type}
- Personalization Depth: {personalization_hint.get(personalization_level, 'Standard')}
- Mention Mutual Connections: {'Yes' if mention_mutual else 'No'}

GUIDELINES:
- Write a concise, professional LinkedIn message (2-4 sentences max).
- Reference something SPECIFIC from the profile or their role.
- Lead with value/relevance, NOT with what you want.
- Include a clear but soft CTA at the end (e.g., "Would love to connect" or "Let's chat sometime").
- Match the requested tone and personalization depth.
- Output ONLY the message itself, no preamble, meta-text, or explanations.
- Do NOT include phrases like "Here's a message", "Let me know if...", or meta commentary.
- Make it ready to copy-paste directly into LinkedIn DMs without editing.
- Be authentic and conversational, not robotic.
"""
    return prompt


def _variant_instructions(variant: str) -> str:
    if variant == "short":
        return "Output a very short message (1-2 sentences). Keep it concise and direct."
    if variant == "medium":
        return "Output a medium-length message (2-4 sentences). Balanced personalization."
    if variant == "ultra":
        return "Output an ultra-personalized message (3-6 sentences). Include multiple profile-specific references and a clear but gentle CTA."
    return ""


def generate_outreach_variants(
    user_background: str,
    profile: Dict,
    relationship_goal: str = "Network & Build Relationship",
    value_prop: str = "",
    tone: str = "Professional & Friendly",
    cta_type: str = "Coffee/Chat Request",
    interests: str = "",
    problem_solving: str = "",
    achievements: str = "",
    personalization_level: int = 3,
    mention_mutual: bool = True,
):
    """
    Return 3 variants: short, medium, ultra.
    Falls back to simple templates if LLM fails.
    """
    base = _base_prompt(
        user_background,
        profile,
        relationship_goal,
        value_prop,
        tone,
        cta_type,
        interests,
        problem_solving,
        achievements,
        personalization_level,
        mention_mutual,
    )

    variants = {}
    for key in ("short", "medium", "ultra"):
        prompt = base + "\n" + _variant_instructions(key) + "\n\nRespond with ONLY the message text."
        try:
            text = query_llama(prompt)
            if not text or text.strip() == "":
                raise RuntimeError("Empty response")
            text = text.strip()
            # Clean up any unwanted preamble
            if "Here is the generated LinkedIn outreach message:" in text:
                text = text.split("Here is the generated LinkedIn outreach message:", 1)[1].strip()
            variants[key] = text
        except Exception:
            # fallback template generation
            name = profile.get("name", "there")
            role = profile.get("current_role", "")
            comp = profile.get("company", "")
            if key == "short":
                variants[key] = f"Hi {name},\n\nI liked your work as {role}. {value_prop or ''} Would you be open to a quick {cta_type.lower()}?\n\nThanks!"
            elif key == "medium":
                variants[key] = f"Hi {name},\n\nI noticed your work as {role} at {comp}. {value_prop or ''} I’d love to {cta_type.lower()} to learn about your experience and share a quick idea.\n\nBest,\n[Your Name]"
            else:
                variants[key] = (
                    f"Hi {name},\n\nYour leadership as {role} stood out to me—especially your experience with "
                    f"{', '.join(profile.get('key_skills', [])[:3])}. {value_prop or ''} Would you be open to a brief {cta_type.lower()} to explore fit?\n\nThanks,\n[Your Name]"
                )
    return variants


def generate_outreach_message(
    user_background: str,
    profile: Dict,
    relationship_goal: str = "Network & Build Relationship",
    value_prop: str = "",
    tone: str = "Professional & Friendly",
    cta_type: str = "Coffee/Chat Request",
    interests: str = "",
    problem_solving: str = "",
    achievements: str = "",
    personalization_level: int = 3,
    mention_mutual: bool = True,
):
    """
    Backwards-compatible: returns the medium variant by default.
    """
    variants = generate_outreach_variants(
        user_background=user_background,
        profile=profile,
        relationship_goal=relationship_goal,
        value_prop=value_prop,
        tone=tone,
        cta_type=cta_type,
        interests=interests,
        problem_solving=problem_solving,
        achievements=achievements,
        personalization_level=personalization_level,
        mention_mutual=mention_mutual,
    )
    return variants.get("medium", next(iter(variants.values())))
