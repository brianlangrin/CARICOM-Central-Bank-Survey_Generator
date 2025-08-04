# 📊 CARICOM Central Bank Survey Generator

This repository contains python code for generating and distributing a regional financial market infrastructure (FMI) survey to CARICOM central banks. The tool automates survey creation, email distribution, and recipient management to support policy harmonization and technical readiness assessments across Member States.

---

## 🧭 Purpose

The survey supports CARICOM’s strategic goals for regional integration, including:

- Free movement of people, goods, capital, and services  
- Enhanced interoperability of payment systems  
- Improved digitalization of commerce  
- Strengthened financial stability and risk management  

---

## 📋 Survey Sections

The survey includes structured questions across key domains:

| Section                     | Question Types               |
|----------------------------|------------------------------|
| Respondent Information     | Identification & tracking    |
| Policy & Regulatory        | AML/CFT posture, frameworks  |
| Monetary Policy            | Instruments, coordination    |
| Financial Stability        | Risk exposure, resilience    |
| Technical Readiness        | ISO 20022, API support       |
| Cross-Border Readiness     | Settlement & integration     |
| Risk Assessment            | Credit risk, key factors     |
| Implementation Readiness   | Timeline, budget, staffing   |
| Regional Integration       | Collaboration, alignment     |
| Cost-Benefit Analysis      | Expected impact, feasibility |
| Governance Framework       | Oversight, accountability    |

---

## ⚙️ Features

- **Automated Email Distribution** via Gmail API  
- **Recipient Management** from CSV files  
- **Templated HTML Emails** for survey invitations  
- **Google Forms Integration** for survey hosting  

---

## 📁 File Structure
caricom_survey/
│
├── caricom_central_bank_survey/
│   ├── __init__.py
│   ├── CentralBankGoogleFormsGenerator.py
│   ├── SurveyDistributor.py
│   ├── EmailTemplateManager.py
│   ├── ReminderSystem.py
│   └── ... (other modules)
│
├── main.py
├── config.py
├── auth.py
├── requirements.txt
├── setup.py
├── .env
├── .gitignore
└── README.md

# CARICOM Survey Automation

Automated survey distribution tool for CARICOM central banks.

## Setup

1. Clone the repository.
2. Create a virtual environment and activate it.
3. Install dependencies:
   pip install -r requirements.txt
4. Create a `.env` file with the required environment variables.

## Running

python main.py