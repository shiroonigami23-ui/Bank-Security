from fpdf import FPDF
import base64

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'FinGuard Forensic Report', 0, 1, 'C')
        self.ln(10)

def create_download_link(transaction_id, risk_score, amount, status):
    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    pdf.cell(200, 10, txt=f"Transaction ID: {transaction_id}", ln=1)
    pdf.cell(200, 10, txt=f"Timestamp: 2025-12-12 14:30:05 UTC", ln=1)
    pdf.cell(200, 10, txt="------------------------------------------------", ln=1)
    pdf.cell(200, 10, txt=f"Transaction Amount: EUR {amount}", ln=1)
    pdf.cell(200, 10, txt=f"AI Risk Score: {risk_score}%", ln=1)
    pdf.cell(200, 10, txt=f"Final Classification: {status}", ln=1)
    
    pdf_output = pdf.output(dest="S").encode("latin-1")
    b64 = base64.b64encode(pdf_output).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="Fraud_Report_{transaction_id}.pdf" style="background-color: #e74c3c; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">📥 Download Official PDF Report</a>'
    return href