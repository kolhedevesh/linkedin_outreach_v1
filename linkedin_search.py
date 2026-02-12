from prompt_builder import build_prompt
from llm_client import query_llama

def get_profiles(user_profile, target_role, industry, location):
    prompt = build_prompt(
        user_profile,
        target_role,
        industry,
        location
    )

    return query_llama(prompt)
