import openai, os, json, streamlit as st
from utils.parser import read_docx

openai.api_key = os.getenv("OPENAI_API_KEY")

def run_earnings_tool(files):
    combined_text = ""
    for f in files:
        combined_text += read_docx(f) + "\n"

    prompt = f"""
    You are an internal financial research extraction system.

    RULES:
    - No inference
    - No assumptions
    - If unclear, return "Not Disclosed"
    - Output STRICT JSON only

    {{
      "tone": "",
      "confidence_level": "",
      "positives": [],
      "concerns": [],
      "forward_guidance": "",
      "growth_initiatives": [],
      "confidence_score_0_100": ""
    }}

    Text:
    {combined_text}
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You extract structured financial research data."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.1
    )

    data = json.loads(response.choices[0].message.content)

    st.subheader("📊 Management Analysis")
    st.json(data)

    st.download_button(
        "Download JSON",
        json.dumps(data, indent=4),
        "earnings_analysis.json"
    )
