import openai, os, pandas as pd, streamlit as st
from utils.parser import read_docx

openai.api_key = os.getenv("OPENAI_API_KEY")

LINE_ITEMS = [
    "Revenue",
    "Cost of Goods Sold",
    "Gross Profit",
    "Operating Expenses",
    "Operating Income",
    "Net Income"
]

def run_financials_tool(files):
    text = ""
    for f in files:
        text += read_docx(f) + "\n"

    prompt = f"""
    Extract financial line items into structured table format.
    Only return values explicitly stated.

    Line Items: {LINE_ITEMS}

    Output JSON:
    {{
      "currency": "",
      "unit": "",
      "yearly_data": {{
        "2023": {{}},
        "2022": {{}}
      }}
    }}

    Text:
    {text}
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You extract financial statement data."},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    data = json.loads(response.choices[0].message.content)

    rows = []
    for year, items in data["yearly_data"].items():
        row = {"Year": year}
        row.update(items)
        rows.append(row)

    df = pd.DataFrame(rows)

    st.subheader("📈 Extracted Financials")
    st.dataframe(df)

    st.download_button(
        "Download Excel",
        df.to_csv(index=False),
        "financials.csv",
        "text/csv"
    )
