# AI Clinical Assistant 🤖 

**AI-powered clinical assistant offering intelligent ✨ medical insights and decision support for healthcare professionals.**

---

## 🚀 Overview
**AI-Clinical-Assistant** is a comprehensive platform integrating AI-driven medical intelligence for:

- Symptom analysis & personalized health plans
- Diagnosis support and risk prediction
- Treatment planning & drug interaction checking
- OCR for prescriptions, lab reports, and X-rays
- Multi-modal input: PDFs, images, voice notes
- Full health report generation for patients

This platform leverages advanced language models to provide actionable insights while ensuring clarity, usability, and professional-grade output.

---

## 💡 Features
- **Interactive AI Chat:** Discuss symptoms and clinical cases with an AI assistant.
- **Diagnosis & Risk Prediction:** Get possible diagnoses, red flags, and risk assessments.
- **Treatment Planning:** Generate treatment options, lifestyle advice, and follow-ups.
- **Drug Interaction Checker:** Evaluate drug interactions and safety guidelines.
- **Medical OCR & Analysis:** Extract and analyze data from prescriptions, lab reports, and scans.
- **X-Ray Interpretation:** Preliminary AI insights for uploaded imaging.
- **Full Health Report Generator:** Aggregate multiple documents into a cohesive patient report.
- **Multi-user Login:** Secure session management with verification.

---

## 🛠️ Tech Stack
- **Frontend:** [Streamlit](https://streamlit.io)
- **AI Model:** [GROQ](https://www.groq.ai) (`llama-3.3-70b-versatile`)
- **OCR:** [pytesseract](https://pypi.org/project/pytesseract/), PyMuPDF, pdf2image
- **File Handling:** PDFs, images (PNG, JPG, JPEG)
- **Environment Management:** `.env` + Python `dotenv`

---

## ⚡ Quick Start
1. **Clone the repository**
```bash
git clone https://github.com/hemant467/AI-Clinical-Assistant.git
cd AI-Clinical-Assistant
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Setup environment**
```
cp .env.example .env
# Add your GROQ_API_KEY in .env
```

4. Run the app
```
streamlit run ai_clinical_assist.py
```

## 🔒 Security Note
- User passwords in this prototype are stored in session state (for demo purposes only).

- ⚠️ Do NOT use this setup in production for sensitive patient data 🗃️. Always hash passwords 🔒 and use secure authentication 🔐 methods.

## 📂 Folder Structure

```
AI-Clinical-Assistant/
├─ app.py
├─ requirements.txt
├─ .env.example
├─ utils/
│  ├─ ocr.py
│  ├─ ai_helper.py
│  └─ document_analysis.py
└─ README.md
```

## ⚠️ Disclaimer

This tool is for educational purposes only. It does NOT replace a qualified medical professional. Use responsibly.

## 💖 Author

Hemant Katta

---

## 🖼️ Output

<img width="1303" height="569" alt="1" src="https://github.com/user-attachments/assets/e3bd6564-8fc2-4665-9194-75cc210dafe2" />

<img width="1307" height="621" alt="3" src="https://github.com/user-attachments/assets/a397aed9-de95-4f11-918e-a22c64db2074" />

<img width="1331" height="618" alt="6" src="https://github.com/user-attachments/assets/5dea26cc-47da-4d34-93f8-182adff6eea3" />

<img width="1330" height="621" alt="10" src="https://github.com/user-attachments/assets/f953e3e7-8df0-4736-b8f0-5a2d6530bfd9" />

<img width="1333" height="610" alt="17" src="https://github.com/user-attachments/assets/1d1d5585-8373-4ce3-b7b6-c97dc51d184f" />

---

## ⭐ Support

If you like this project, please ⭐ the repository and share it!

---

<img src="https://readme-typing-svg.herokuapp.com/?lines=🩺+AI+Clinical+Assistant+🤖;Smart+Healthcare+Insights;Analyze+%7C+Diagnose+%7C+Advise;Built+with+Streamlit+%26+Python&font=Fira%20Code&color=%23FFD700&center=true&width=900&height=130&size=26&pause=1000">

<p align="center"><a href="https://github.com/hemant467/AI-Clinical-Assistant">AI Clinical Assistant 🤖</a></p>
