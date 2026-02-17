import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.parser import read_docx
from utils.earnings_tool import run_earnings_tool
from utils.financials_tool import run_financials_tool


st.set_page_config(page_title="Elite AI Research Portal", layout="wide")

st.title("🏦 Elite AI Research Portal")
st.caption("Internal-grade financial research tools powered by AI")

tool = st.selectbox(
    "Select Research Tool",
    [
        "Earnings Call / Management Commentary",
        "Financial Statement → Excel Extraction"
    ]
)

uploaded_files = st.file_uploader(
    "Upload Documents",
    type=["docx"],
    accept_multiple_files=True
)

if uploaded_files:
    if tool == "Earnings Call / Management Commentary":
        run_earnings_tool(uploaded_files)
    else:
        run_financials_tool(uploaded_files)
