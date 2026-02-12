import streamlit as st
from dotenv import load_dotenv
from search_client import search_linkedin_profiles
import pyperclip

load_dotenv()

st.set_page_config(page_title="LinkedIn Outreach Assistant", layout="wide")
st.title("🔗 LinkedIn Outreach Assistant")
st.write("Find LinkedIn profiles and generate personalized outreach messages")

# Minimal presets
PRESETS = {
    "Founder": {
        "user_background": "I'm building B2B SaaS to help teams move faster.",
        "value_prop": "We help product teams launch faster with better analytics.",
    },
    "Job Seeker": {
        "user_background": "I'm a Product Manager with 5+ years of experience.",
        "value_prop": "I design features that drive user growth and engagement.",
    },
}

def apply_preset(preset_name):
    preset = PRESETS.get(preset_name, {})
    for k, v in preset.items():
        st.session_state[k] = v
    st.rerun()

def validate_inputs(target_role_value: str = None, industry_value: str = None):
    tab1_required = {
        "Your Background": (st.session_state.get("user_background", "") or "").strip(),
        "Target Role": ((target_role_value if target_role_value is not None else st.session_state.get("target_role", "")) or "").strip(),
        "Industry": ((industry_value if industry_value is not None else st.session_state.get("industry", "")) or "").strip(),
        "Location": (st.session_state.get("location", "") or "").strip()
    }
    tab2_required = {
        "Primary Goal": (st.session_state.get("relationship_goal", "") or "").strip(),
        "Value Proposition": (st.session_state.get("value_prop", "") or "").strip(),
        "Tone": (st.session_state.get("tone", "") or "").strip(),
    }
    missing_tab1 = [k for k, v in tab1_required.items() if not v]
    missing_tab2 = [k for k, v in tab2_required.items() if not v]
    return {"tab1": missing_tab1, "tab2": missing_tab2, "total": len(missing_tab1) + len(missing_tab2)}

# --- TABS ---
tab1, tab2 = st.tabs(["🔍 Search & Filters", "💬 Outreach Settings"])

with tab1:
    st.subheader("Profile Search Criteria")
    
    # Initialize preset state if not exists
    if 'selected_preset' not in st.session_state:
        st.session_state['selected_preset'] = None
    
    # Presets with visual feedback
    st.write("**Quick Start Presets:**")
    col_preset1, col_preset2, col_spacer = st.columns([1, 1, 2])
    
    # Determine button labels with checkmarks
    founder_active = st.session_state.get('selected_preset') == "Founder"
    seeker_active = st.session_state.get('selected_preset') == "Job Seeker"
    
    founder_label = "📌 Founder ✓" if founder_active else "📌 Founder"
    seeker_label = "📌 Job Seeker ✓" if seeker_active else "📌 Job Seeker"
    
    with col_preset1:
        if st.button(founder_label, use_container_width=True, key="btn_founder"):
            apply_preset("Founder")
            st.session_state['selected_preset'] = "Founder"
            st.rerun()
    
    with col_preset2:
        if st.button(seeker_label, use_container_width=True, key="btn_job_seeker"):
            apply_preset("Job Seeker")
            st.session_state['selected_preset'] = "Job Seeker"
            st.rerun()
    
    # Show active preset with strong visual indicator
    if founder_active:
        st.markdown("""
        <div style='background-color: #1f77b4; border: 3px solid #0056b3; border-radius: 8px; padding: 12px; margin: 12px 0; text-align: center;'>
            <span style='color: white; font-weight: bold; font-size: 16px;'>✓ Founder Preset Active</span>
        </div>
        """, unsafe_allow_html=True)
    elif seeker_active:
        st.markdown("""
        <div style='background-color: #20a39e; border: 3px solid #0d6b5b; border-radius: 8px; padding: 12px; margin: 12px 0; text-align: center;'>
            <span style='color: white; font-weight: bold; font-size: 16px;'>✓ Job Seeker Preset Active</span>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style='background-color: #e9ecef; border: 2px dashed #6c757d; border-radius: 8px; padding: 12px; margin: 12px 0; text-align: center;'>
            <span style='color: #6c757d; font-weight: bold; font-size: 14px;'>← Click a preset to fill in defaults</span>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # Background
    st.markdown("**Your Background** <span style='color:red'>*</span>", unsafe_allow_html=True)
    user_background = st.text_area(
        "Your Background",
        placeholder="e.g., I'm a founder with 10 years in B2B SaaS...",
        height=80,
        key="user_background",
        label_visibility="collapsed"
    )

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Target Role** <span style='color:red'>*</span>", unsafe_allow_html=True)
        role_options = ["Product Manager", "VP of Product", "Engineering Manager", "VP of Engineering", "Founder", "CTO", "Other"]
        target_role_choice = st.multiselect("Target Role", role_options, key="target_role_choice", label_visibility="collapsed")
        target_role_custom = ""
        if "Other" in target_role_choice:
            target_role_custom = st.text_input("Specify other roles (comma-separated)", key="target_role_custom", label_visibility="collapsed")

    with col2:
        st.markdown("**Industry** <span style='color:red'>*</span>", unsafe_allow_html=True)
        industry_options = ["SaaS", "FinTech", "AI/ML", "Healthcare", "B2B", "EdTech", "Other"]
        industry_choice = st.multiselect("Industry", industry_options, key="industry_choice", label_visibility="collapsed")
        industry_custom = ""
        if "Other" in industry_choice:
            industry_custom = st.text_input("Specify other industries (comma-separated)", key="industry_custom", label_visibility="collapsed")

    # Resolve final values - combine selected + custom
    target_role_final = target_role_choice.copy() if target_role_choice else []
    if target_role_custom:
        target_role_final.extend([r.strip() for r in target_role_custom.split(",") if r.strip()])
    if "Other" in target_role_final:
        target_role_final.remove("Other")
    target_role_final = ", ".join(target_role_final) if target_role_final else ""
    
    industry_final = industry_choice.copy() if industry_choice else []
    if industry_custom:
        industry_final.extend([ind.strip() for ind in industry_custom.split(",") if ind.strip()])
    if "Other" in industry_final:
        industry_final.remove("Other")
    industry_final = ", ".join(industry_final) if industry_final else ""
    
    st.session_state['target_role'] = target_role_final
    st.session_state['industry'] = industry_final

    st.markdown("**Location** <span style='color:red'>*</span>", unsafe_allow_html=True)
    location = st.text_input(
        "Location",
        placeholder="e.g., San Francisco, Remote, India",
        key="location",
        label_visibility="collapsed"
    )

    # Show selections
    if target_role_final:
        st.caption(f"✓ Role: **{target_role_final}**")
    if industry_final:
        st.caption(f"✓ Industry: **{industry_final}**")
    if location:
        st.caption(f"✓ Location: **{location}**")

    # Tab1 validation
    v = validate_inputs(target_role_value=target_role_final, industry_value=industry_final)
    if v["tab1"]:
        st.error(f"❌ Missing: {', '.join(v['tab1'])}")
    else:
        st.success("✅ Search & Filters ready")

with tab2:
    st.subheader("Outreach Message Settings")

    st.markdown("**Primary Goal** <span style='color:red'>*</span>", unsafe_allow_html=True)
    relationship_goal = st.selectbox(
        "Goal",
        ["Network & Build Relationship", "B2B Sales/Partnership", "Hire/Recruit", "Investor Outreach", "General Connection"],
        key="relationship_goal",
        label_visibility="collapsed"
    )

    st.markdown("**Value Proposition** <span style='color:red'>*</span>", unsafe_allow_html=True)
    value_prop = st.text_area(
        "Value Prop",
        placeholder="e.g., We help SaaS companies increase conversion by 40%...",
        height=80,
        key="value_prop",
        label_visibility="collapsed"
    )

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Message Tone** <span style='color:red'>*</span>", unsafe_allow_html=True)
        tone = st.selectbox(
            "Tone",
            ["Professional & Formal", "Professional & Friendly", "Casual & Direct"],
            key="tone",
            label_visibility="collapsed"
        )
    with col2:
        cta_type = st.selectbox(
            "Call-to-Action",
            ["Coffee/Chat Request", "Demo Request", "Meeting Proposal", "Quick Question"],
            key="cta_type"
        )

    # Tab2 validation
    target_role_final_tab2 = target_role_final if 'target_role_final' in locals() else st.session_state.get('target_role', '')
    industry_final_tab2 = industry_final if 'industry_final' in locals() else st.session_state.get('industry', '')
    v2 = validate_inputs(target_role_value=target_role_final_tab2, industry_value=industry_final_tab2)
    if v2["tab2"]:
        st.error(f"❌ Missing: {', '.join(v2['tab2'])}")
    else:
        st.success("✅ Outreach Settings ready")

# --- RESULT MODE ---
st.divider()
result_mode = st.radio(
    "Mode",
    ["🔗 Real LinkedIn Search", "🧪 Demo Mode"],
    horizontal=True,
    key="result_mode"
)

# --- GENERATE SECTION ---
st.divider()

def generate_profiles():
    """Generate and display profiles."""
    user_background = (st.session_state.get("user_background", "") or "").strip()
    target_role = (st.session_state.get("target_role", "") or "").strip()
    industry = (st.session_state.get("industry", "") or "").strip()
    location = (st.session_state.get("location", "") or "").strip()
    value_prop = (st.session_state.get("value_prop", "") or "").strip()

    if not all([user_background, target_role, industry, location, value_prop]):
        st.error("⚠️ Please fill all required fields above")
        return

    if "🔗" in result_mode:
        # Real LinkedIn search
        with st.spinner("Searching LinkedIn profiles..."):
            try:
                search_results = search_linkedin_profiles(target_role, industry, location)
                if search_results:
                    st.success(f"✅ Found {len(search_results)} profiles")
                    
                    from profile_generator import parse_profile_metadata, generate_outreach_variants

                    # Show all results but display nicely
                    for i, result in enumerate(search_results, 1):
                        metadata = parse_profile_metadata(result.get('title',''), result.get('snippet',''))
                        profile_name = metadata.get('name', f"Profile {i}")
                        profile_url = result.get('link', '')
                        
                        with st.expander(f"Profile {i}: {profile_name}", expanded=False):
                            col1, col2 = st.columns([3, 1])
                            with col1:
                                st.write(f"**Role:** {metadata.get('current_role', 'N/A')}")
                                st.write(f"**Company:** {metadata.get('company', 'N/A')}")
                                st.write(f"**About:** {result.get('snippet','')}")
                            with col2:
                                if profile_url:
                                    st.markdown(f"[🔗 View Profile]({profile_url})")
                            
                            st.divider()
                            
                            # Generate message
                            try:
                                variants = generate_outreach_variants(
                                    user_background=user_background,
                                    profile={**metadata, 'snippet': result.get('snippet','')},
                                    relationship_goal=st.session_state.get("relationship_goal", ""),
                                    value_prop=value_prop,
                                    tone=st.session_state.get("tone", "Professional & Friendly"),
                                    cta_type=st.session_state.get("cta_type", "Coffee/Chat Request"),
                                    interests="",
                                    problem_solving="",
                                    achievements="",
                                    personalization_level=3,
                                    mention_mutual=True
                                )
                                message = variants.get("medium", "")
                            except Exception as e:
                                message = f"Hi {profile_name.split()[0]},\n\nI noticed your work in {industry}. {value_prop}\n\nWould love to connect.\n\nThanks!"
                            
                            # Editable message area
                            edited_message = st.text_area(
                                "Message (edit as needed)",
                                value=message,
                                height=150,
                                key=f"msg_{i}_{profile_url}",
                                help="Edit as needed before sending"
                            )
                            
                            st.caption("💡 Copy and paste this message directly into LinkedIn DMs")
                else:
                    st.warning("No profiles found. Try different search criteria.")
            except Exception as e:
                error_msg = str(e)
                if "timeout" in error_msg.lower() or "read timed out" in error_msg.lower():
                    st.warning("⏱️ Search took too long (network timeout). Please try:")
                    st.info("• Use a more specific location (e.g., 'San Francisco' instead of 'India')\n• Try fewer industries\n• Use Demo Mode to test messages first")
                else:
                    st.error(f"Search error: {error_msg}")
    
    else:
        # Demo mode
        st.subheader("🧪 Demo Profiles")
        demo_profiles = [
            {"name": "Jane Doe", "role": "Senior PM", "company": "TechCorp"},
            {"name": "John Smith", "role": "VP Engineering", "company": "StartupXYZ"},
            {"name": "Sarah Chen", "role": "Product Lead", "company": "DataCo"},
        ]
        
        for i, profile in enumerate(demo_profiles, 1):
            with st.expander(f"Demo {i}: {profile['name']}", expanded=False):
                st.write(f"**Role:** {profile['role']}")
                st.write(f"**Company:** {profile['company']}")
                
                message = f"Hi {profile['name'].split()[0]},\n\nI noticed your work at {profile['company']}. {st.session_state.get('value_prop', '')}\n\nWould love to connect and explore potential synergies.\n\nThanks!"
                
                st.divider()
                
                edited_message = st.text_area(
                    "Message (edit as needed)",
                    value=message,
                    height=150,
                    key=f"demo_msg_{i}",
                    help="Edit as needed before sending"
                )
                
                st.caption("💡 Copy and paste this message directly into LinkedIn DMs")

# --- GENERATE BUTTON ---
target_role_final_btn = target_role_final if 'target_role_final' in locals() else st.session_state.get('target_role', '')
industry_final_btn = industry_final if 'industry_final' in locals() else st.session_state.get('industry', '')
v_final = validate_inputs(target_role_value=target_role_final_btn, industry_value=industry_final_btn)

if v_final["total"] == 0:
    if st.button("🚀 Generate Profiles", use_container_width=True, type="primary"):
        generate_profiles()
else:
    st.warning(f"⚠️ {v_final['total']} required field(s) missing. Fill all fields in the tabs above to proceed.")
