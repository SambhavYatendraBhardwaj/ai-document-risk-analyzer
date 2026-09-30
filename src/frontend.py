import streamlit as st
import requests
import requests

st.set_page_config(page_title="AI Document Risk Analyzer", layout="wide")

st.title("🛡️ AI Document Risk Analyzer")
st.caption("Upload contracts, NDAs, or agreements to detect operational, financial, and legal risks.")

uploaded_file = st.file_uploader("Upload a PDF document", type=["pdf"])

if uploaded_file is not None:
    if st.button("Analyze Document", type="primary"):
        with st.spinner("Analyzing document clauses and verifying groundedness..."):
            # FastAPI endpoint par file bhejna
            files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
            try:
                response = requests.post("http://127.0.0.1:8000/analyze-risk", files=files)
                
                if response.status_code == 200:
                    data = response.json()
                    report = data["risk_report"]
                    eval_data = data["evaluation"]

                    st.success("Analysis Complete!")

                    # Top Metrics
                    col1, col2, col3 = st.columns(3)
                    col1.metric("Overall Risk Score", report["overall_risk_score"])
                    col2.metric("Groundedness Score", f"{eval_data['groundedness_score'] * 100}%")
                    col3.metric("Verified Citations", f"{eval_data['verified_evidences']}/{eval_data['total_evidences']}")

                    st.subheader("Executive Summary")
                    st.info(report["summary"])

                    st.subheader("Detected Risks & Mitigations")
                    if not report["risks_detected"]:
                        st.write("✅ No critical hazards or high risks detected in this document.")
                    else:
                        for risk in report["risks_detected"]:
                            color = "🔴" if risk["level"] in ["HIGH", "CRITICAL"] else "🟡" if risk["level"] == "MEDIUM" else "🟢"
                            with st.expander(f"{color} {risk['clause_title']} ({risk['category']} - {risk['level']})"):
                                st.markdown(f"**Issue Description:** {risk['issue_description']}")
                                st.markdown(f"**Verbatim Evidence:** > *\"{risk['verbatim_evidence']}\"*")
                                st.markdown(f"**Recommended Mitigation:** {risk['recommended_mitigation']}")
                else:
                    st.error(f"Error: {response.json().get('detail', 'Unknown error')}")
            except Exception as e:
                st.error(f"Backend connection failed: {e}")