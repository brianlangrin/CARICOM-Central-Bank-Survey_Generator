from config import CSV_PATH, CREDENTIALS_FILE

### Core Survey Generator

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class CentralBankGoogleFormGenerator:
    """
    Generates Central Bank survey using Google Forms REST API v1.
    Combines static question groups with dynamic CSV-based sections.
    """
    VALID_IMAGE_URL_1 = "https://upload.wikimedia.org/wikipedia/commons/4/47/PNG_transparency_demonstration_1.png"
    VALID_IMAGE_URL_2 = "https://upload.wikimedia.org/wikipedia/commons/6/6b/Picture_icon_BLACK.svg"

    def __init__(self, csv_path: str = None, credentials_path: str = None, token_path: str = None):
        import os
        from googleapiclient.discovery import build
    
        self.SCOPES = [
            'https://www.googleapis.com/auth/forms.body',
            'https://www.googleapis.com/auth/drive',
            'https://www.googleapis.com/auth/documents',
            'https://www.googleapis.com/auth/forms.responses.readonly',
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/gmail.send'
        ]
    
        self.current_index = 1
        self.csv_path = csv_path or CSV_PATH
        self.credentials_path = credentials_path or CREDENTIALS_FILE
        self.token_path = token_path or os.getenv("TOKEN_PATH")
    
        logger.info("Initializing CentralBankGoogleFormGenerator")
        try:
            logger.info("Loading credentials...")
            print("🔑 Loading credentials...")
            self.creds = self._get_credentials()
            if not self.creds:
                raise RuntimeError("Failed to obtain Google credentials.")
    
            print("🧱 Building Google API clients...")
            self.forms = build("forms", "v1", credentials=self.creds)
            self.docs = build("docs", "v1", credentials=self.creds)
            self.drive = build("drive", "v3", credentials=self.creds)
            self.gmail = build("gmail", "v1", credentials=self.creds)
    
            print("📚 Parsing section definitions...")
            self.section_definitions = self._get_section_definitions()
    
            self.response_sheet_id = None
            print("✅ CentralBankGoogleFormGenerator initialized successfully.")
    
        except Exception as e:
            logger.error("Initialization error", exc_info=True)
            print(f"❌ Initialization error in CentralBankGoogleFormGenerator: {e}")
            raise


    def _get_section_definitions(self) -> List[Dict[str, Any]]:
        def sanitize(text: str) -> str:
            import re
            text = text.replace("\n", " ")
            text = re.sub(r"font-family[:;]?.*?;", "", text, flags=re.IGNORECASE)
            text = re.sub(r"font-family", "", text, flags=re.IGNORECASE)
            text = re.sub(r"\s{2,}", " ", text)
            return text.strip()
    
        return [
            {
                "title": sanitize("Respondent Information for Survey Tracking"),
                "description": sanitize("Please provide your professional information."),
                "questions": [
                    {
                        "title": sanitize("Please enter the name of your institution"),
                        "questionItem": {
                            "question": {
                                "textQuestion": {"paragraph": False}
                            }
                        }
                    },
                    {
                        "title": sanitize("What is your current job title or position within your institution?"),
                        "questionItem": {
                            "question": {
                                "textQuestion": {"paragraph": False}
                            }
                        }
                    }
                ]
            },
            {
                "title": sanitize("Policy and Regulatory Assessment"),
                "description": sanitize("Evaluate alignment of your retail payments infrastructure with international compliance, financial integrity, and governance standards (FATF, BIS CPMI, ISO 20022)."),
                "questions": [
                    {
                        "title": sanitize("On a scale of 1 (Not Compliant) to 5 (Fully Compliant), how well does your retail payment infrastructure comply with FATF AML/CFT recommendations?"),
                        "questionItem": {
                            "question": {
                                "scaleQuestion": {
                                    "low": 1, "high": 5,
                                    "lowLabel": sanitize("Not Compliant"),
                                    "highLabel": sanitize("Fully Compliant")
                                }
                            }
                        }
                    },
                    {
                        "title": sanitize("On a scale of 1 (Not Compatible) to 5 (Fully Compatible), how capable is your retail payment system of adapting to evolving cross-border interoperability requirements?"),
                        "questionItem": {
                            "question": {
                                "scaleQuestion": {
                                    "low": 1, "high": 5,
                                    "lowLabel": sanitize("Not Compatible"),
                                    "highLabel": sanitize("Fully Compatible")
                                }
                            }
                        }
                    },
                    {
                        "title": sanitize("What are the main challenges your institution faces in aligning regulatory rulebooks with those of other countries?"),
                        "questionItem": {
                            "question": {
                                "textQuestion": {"paragraph": True}
                            }
                        }
                    },
                    {
                        "title": sanitize("On a scale of 1 (Low Transparency) to 5 (Full Accountability), how would you rate your policy oversight and transparency mechanisms in line with BIS Principles?"),
                        "questionItem": {
                            "question": {
                                "scaleQuestion": {
                                    "low": 1, "high": 5,
                                    "lowLabel": sanitize("Low Transparency"),
                                    "highLabel": sanitize("Full Accountability")
                                }
                            }
                        }
                    },
                    {
                        "title": sanitize("Please describe any existing safeguards or gaps in accountability and oversight within your institution."),
                        "questionItem": {
                            "question": {
                                "textQuestion": {"paragraph": True}
                            }
                        }
                    },
                    {
                        "title": sanitize("Describe any regulatory sandboxes or pilot programs your institution has participated in for cross-border payment innovations."),
                        "questionItem": {
                            "question": {
                                "textQuestion": {"paragraph": True}
                            }
                        }
                    },
                    {
                        "title": sanitize("How appropriate is a retail cross-border platform for your jurisdiction, considering cost, scalability, and governance?"),
                        "questionItem": {
                            "question": {
                                "scaleQuestion": {
                                    "low": 1, "high": 5,
                                    "lowLabel": sanitize("Very Low"),
                                    "highLabel": sanitize("Very High")
                                }
                            }
                        }
                    },
                    {
                        "title": sanitize("How operationally viable is a single common platform or hub-and-spoke model that handles both domestic and cross-border payments without reducing local efficiency?"),
                        "questionItem": {
                            "question": {
                                "scaleQuestion": {
                                    "low": 1, "high": 5,
                                    "lowLabel": sanitize("Very Low"),
                                    "highLabel": sanitize("Very High")
                                }
                            }
                        }
                    },
                    {
                        "title": sanitize("How well-developed is your framework for proportionate regulation of FinTechs offering payment services under cross-border arrangements?"),
                        "questionItem": {
                            "question": {
                                "scaleQuestion": {
                                    "low": 1, "high": 5,
                                    "lowLabel": sanitize("Very Low"),
                                    "highLabel": sanitize("Very High")
                                }
                            }
                        }
                    },
                    {
                        "title": sanitize("To what extent does your jurisdiction maintain a level playing field for infrastructure access, especially between traditional banks and FinTechs?"),
                        "questionItem": {
                            "question": {
                                "scaleQuestion": {
                                    "low": 1, "high": 5,
                                    "lowLabel": sanitize("Very Low"),
                                    "highLabel": sanitize("Very High")
                                }
                            }
                        }
                    },
                    {
                        "title": sanitize("How administratively burdensome would it be for your institution to set and enforce differentiated holding/transaction limits for residents vs. non-residents?"),
                        "questionItem": {
                            "question": {
                                "scaleQuestion": {
                                    "low": 1, "high": 5,
                                    "lowLabel": sanitize("Very Low"),
                                    "highLabel": sanitize("Very High")
                                }
                            }
                        }
                    },
                    {
                        "title": sanitize("How developed is your national approach to Digital Public Infrastructure (i.e. ID systems, data exchange, real-time payments) supporting retail payment transformation?"),
                        "questionItem": {
                            "question": {
                                "scaleQuestion": {
                                    "low": 1, "high": 5,
                                    "lowLabel": sanitize("Very Low"),
                                    "highLabel": sanitize("Very High")
                                }
                            }
                        }
                    },
                    {
                        "title": sanitize("How effective is your regulatory structure in accommodating new entrants and private-sector innovations in retail payment system design?"),
                        "questionItem": {
                            "question": {
                                "scaleQuestion": {
                                    "low": 1, "high": 5,
                                    "lowLabel": sanitize("Very Low"),
                                    "highLabel": sanitize("Very High")
                                }
                            }
                        }
                    },
                    {
                        "title": sanitize("How ready is your jurisdiction to support cross-border data exchange via APIs and standardized messaging protocols for retail payment systems?"),
                        "questionItem": {
                            "question": {
                                "scaleQuestion": {
                                    "low": 1, "high": 5,
                                    "lowLabel": sanitize("Very Low"),
                                    "highLabel": sanitize("Very High")
                                }
                            }
                        }
                    },
                    {
                        "title": sanitize("How adequately does the legal/regulatory framework permit PSPs or the central bank to exchange transaction-related data across borders?"),
                        "questionItem": {
                            "question": {
                                "scaleQuestion": {
                                    "low": 1, "high": 5,
                                    "lowLabel": sanitize("Very Low"),
                                    "highLabel": sanitize("Very High")
                                }
                            }
                        }
                    }
                ]
            },
            {
                "title": sanitize("Monetary Policy"),
                "description": sanitize("Evaluate how interlinking regional retail payment systems may affect key monetary policy channels, including transmission effectiveness, currency stability, and reliance on the US dollar."),
                "questions": [
                    {
                        "title": sanitize("To what extent could interlinking regional retail payment systems impact the effectiveness of monetary policy transmission in your country? (1 = No Impact, 5 = Major Impact)"),
                        "questionItem": {
                            "question": {
                                "scaleQuestion": {
                                    "low": 1, "high": 5
                                }
                            }
                        }
                    },
                    {
                        "title": sanitize("Please explain your rating regarding the impact on monetary policy transmission effectiveness."),
                        "questionItem": {
                            "question": {
                                "textQuestion": {"paragraph": True}
                            }
                        }
                    },
                    {
                        "title": sanitize("To what extent could interlinking regional retail payment systems reduce your country's dependency on the US dollar for transactions? (1 = No Impact, 5 = Major Reduction)"),
                        "questionItem": {
                            "question": {
                                "scaleQuestion": {
                                    "low": 1, "high": 5
                                }
                            }
                        }
                    },
                    {
                        "title": sanitize("Please provide context or examples of how interlinking regional retail payment systems might alter your country's reliance on the US dollar."),
                        "questionItem": {
                            "question": {
                                "textQuestion": {"paragraph": True}
                            }
                        }
                    },
                    {
                        "title": sanitize("How might interlinking regional retail payment systems affect the stability of your domestic currency? (1 = No Impact, 5 = Major Impact)"),
                        "questionItem": {
                            "question": {
                                "scaleQuestion": {
                                    "low": 1, "high": 5
                                }
                            }
                        }
                    },
                    {
                        "title": sanitize("Please comment on any expected changes in foreign exchange market volatility or policy tools that may be needed as a result of regional retail payment system interlinking."),
                        "questionItem": {
                            "question": {
                                "textQuestion": {"paragraph": True}
                            }
                        }
                    },
                    {
                        "title": sanitize("To what extent do you anticipate cross-border retail payments will influence domestic interest rate policy? (1 = No Influence, 5 = Major Influence)"),
                        "questionItem": {
                            "question": {
                                "scaleQuestion": {
                                    "low": 1, "high": 5
                                }
                            }
                        }
                    },
                    {
                        "title": sanitize("Please describe any anticipated challenges in coordinating monetary policy with other countries due to increased cross-border retail payment flows."),
                        "questionItem": {
                            "question": {
                                "textQuestion": {"paragraph": True}
                            }
                        }
                    }
                ]
            },
            {
                "title": sanitize("Financial Stability"),
                "description": sanitize("This section assesses how integrating regional retail payment systems may affect the stability of your country's financial sector, including banks, capital markets, and payment system integrity."),
                "questions": [
                    {
                        "title": sanitize("On a scale of 1 (Low Impact) to 5 (High Impact), how do you assess the impact of regional retail payment system integration on the stability of your domestic banking sector?"),
                        "questionItem": {
                            "question": {
                                "scaleQuestion": {
                                    "low": 1, "high": 5
                                }
                            }
                        }
                    },
                    {
                        "title": sanitize("Please explain your assessment regarding the impact on banking sector stability. Consider factors such as liquidity, credit risk, and operational resilience."),
                        "questionItem": {
                            "question": {
                                "textQuestion": {"paragraph": True}
                            }
                        }
                    },
                    {
                        "title": sanitize("On a scale of 1 (Low Impact) to 5 (High Impact), how do you assess the impact of regional retail payment system integration on the development of domestic capital markets?"),
                        "questionItem": {
                            "question": {
                                "scaleQuestion": {
                                    "low": 1, "high": 5
                                }
                            }
                        }
                    },
                    {
                        "title": sanitize("Describe how interlinking regional retail payment systems may support or hinder the depth and growth of your domestic capital markets."),
                        "questionItem": {
                            "question": {
                                "textQuestion": {"paragraph": True}
                            }
                        }
                    },
                    {
                        "title": sanitize("On a scale of 1 (Low Impact) to 5 (High Impact), how do you assess the impact of regional retail payment system integration on the integrity and security of your domestic payment system?"),
                        "questionItem": {
                            "question": {
                                "scaleQuestion": {
                                    "low": 1, "high": 5
                                }
                            }
                        }
                    },
                    {
                        "title": sanitize("Please comment on any cybersecurity, fraud, or trust-related concerns that may arise from regional retail payment system integration."),
                        "questionItem": {
                            "question": {
                                "textQuestion": {"paragraph": True}
                            }
                        }
                    },
                    {
                        "title": sanitize("How prepared is your institution to participate in a Distributed Ledger Technology (DLT)-based payment or securities settlement network, especially in terms of infrastructure, policy, and governance?"),
                        "questionItem": {
                            "question": {
                                "scaleQuestion": {
                                    "low": 1, "high": 5
                                }
                            }
                        }
                    },
                    {
                        "title": sanitize("To what extent does your institution believe that digital technologies like blockchain can reduce trade logistics, regulatory, and administrative costs?"),
                        "questionItem": {
                            "question": {
                                "scaleQuestion": {
                                    "low": 1, "high": 5
                                }
                            }
                        }
                    },
                    {
                        "title": sanitize("How concerned is your institution about risks posed by digital transformation, such as market concentration or privacy erosion?"),
                        "questionItem": {
                            "question": {
                                "scaleQuestion": {
                                    "low": 1, "high": 5
                                }
                            }
                        }
                    },
                    {
                        "title": sanitize("To what extent does your institution see potential in DLT for compliance cost reduction (KYC utilities, digital IDs, AML/CFT alignment)?"),
                        "questionItem": {
                            "question": {
                                "scaleQuestion": {
                                    "low": 1, "high": 5
                                }
                            }
                        }
                    },
                    {
                        "title": sanitize("How disruptive would a shift to DLT-based payment networks (e.g., hub-and-spoke, CBDCs) be to your current operational model?"),
                        "questionItem": {
                            "question": {
                                "scaleQuestion": {
                                    "low": 1, "high": 5
                                }
                            }
                        }
                    },
                    {
                        "title": sanitize("How beneficial would a blockchain-integrated Supply Chain Finance (SCF) platform be in improving working capital access for regional SMEs?"),
                        "questionItem": {
                            "question": {
                                "scaleQuestion": {
                                    "low": 1, "high": 5
                                }
                            }
                        }
                    },
                    {
                        "title": sanitize("How likely is your institution to support a multi-country Caribbean platform for payments, SCF, and trade settlement using DLT?"),
                        "questionItem": {
                            "question": {
                                "scaleQuestion": {
                                    "low": 1, "high": 5
                                }
                            }
                        }
                    }
                ]
            },
            {
                "title": sanitize("Technical Readiness"),
                "description": sanitize("This section evaluates your institution's preparedness for technical interoperability and integration with a regional retail payment system. Please answer each question as accurately as possible."),
                "questions": [
                    {
                        "title": sanitize("Please describe your institution's progress or any gaps in implementing ISO 20022 compliance."),
                        "questionItem": {
                            "question": {
                                "textQuestion": {"paragraph": True}
                            }
                        }
                    },
                    {
                        "title": sanitize("Please explain the current state of API deployment at your institution, including any challenges faced."),
                        "questionItem": {
                            "question": {
                                "textQuestion": {"paragraph": True}
                            }
                        }
                    },
                    {
                        "title": sanitize("Please comment on any scalability testing or stress test outcomes for your payment system."),
                        "questionItem": {
                            "question": {
                                "textQuestion": {"paragraph": True}
                            }
                        }
                    },
                    {
                        "title": sanitize("How would you rate your institution’s readiness to support real-time cross-border retail payment processing? (1 = Not Ready, 5 = Fully Ready)"),
                        "questionItem": {
                            "question": {
                                "scaleQuestion": {
                                    "low": 1, "high": 5,
                                    "lowLabel": sanitize("Not Ready"),
                                    "highLabel": sanitize("Fully Ready")
                                }
                            }
                        }
                    },
                    {
                        "title": sanitize("Please describe any interoperability testing performed with foreign payment systems."),
                        "questionItem": {
                            "question": {
                                "textQuestion": {"paragraph": True}
                            }
                        }
                    },
                    {
                        "title": sanitize("How advanced is your jurisdiction in enabling a Request to Pay (RtP) functionality across banks, e-wallets, and credit union platforms?"),
                        "questionItem": {
                            "question": {
                                "scaleQuestion": {
                                    "low": 1, "high": 5,
                                    "lowLabel": sanitize("Very Low"),
                                    "highLabel": sanitize("Very High")
                                }
                            }
                        }
                    },
                    {
                        "title": sanitize("How interoperable are the RtP workflows across different payment service providers, including ability to route notifications, links, and confirmations securely?"),
                        "questionItem": {
                            "question": {
                                "scaleQuestion": {
                                    "low": 1, "high": 5,
                                    "lowLabel": sanitize("Very Low"),
                                    "highLabel": sanitize("Very High")
                                }
                            }
                        }
                    },
                    {
                        "title": sanitize("How viable is upgrading the existing retail payment infrastructure as opposed to creating a separate IPS for cross-border instant payments?"),
                        "questionItem": {
                            "question": {
                                "scaleQuestion": {
                                    "low": 1, "high": 5,
                                    "lowLabel": sanitize("Very Low"),
                                    "highLabel": sanitize("Very High")
                                }
                            }
                        }
                    },
                    {
                        "title": sanitize("How aligned are key stakeholders (e.g. central bank, Bankers Association, government) in deciding on a public vs. private sector-run IPS model?"),
                        "questionItem": {
                            "question": {
                                "scaleQuestion": {
                                    "low": 1, "high": 5,
                                    "lowLabel": sanitize("Very Low"),
                                    "highLabel": sanitize("Very High")
                                }
                            }
                        }
                    },
                    {
                        "title": sanitize("To what extent would a centralized RtP and an API-based Instant Fund Transfer (IFT) framework improve financial inclusion for underserved populations?"),
                        "questionItem": {
                            "question": {
                                "scaleQuestion": {
                                    "low": 1, "high": 5,
                                    "lowLabel": sanitize("Very Low"),
                                    "highLabel": sanitize("Very High")
                                }
                            }
                        }
                    },
                    {
                        "title": sanitize("How feasible is leveraging domestic Fast Payment System (FPS) infrastructure for processing cross-border payments, considering API interfaces, scheme rules, and messaging formats?"),
                        "questionItem": {
                            "question": {
                                "scaleQuestion": {
                                    "low": 1, "high": 5,
                                    "lowLabel": sanitize("Very Low"),
                                    "highLabel": sanitize("Very High")
                                }
                            }
                        }
                    },
                    {
                        "title": sanitize("How well-equipped is your system to integrate with hub-and-spoke or common platform models using standardized gateways?"),
                        "questionItem": {
                            "question": {
                                "scaleQuestion": {
                                    "low": 1, "high": 5,
                                    "lowLabel": sanitize("Very Low"),
                                    "highLabel": sanitize("Very High")
                                }
                            }
                        }
                    },
                    {
                        "title": sanitize("To what extent does the current architecture support programmability and synchronous communication for smart contract execution in PvP or DVP transactions?"),
                        "questionItem": {
                            "question": {
                                "scaleQuestion": {
                                    "low": 1, "high": 5,
                                    "lowLabel": sanitize("Very Low"),
                                    "highLabel": sanitize("Very High")
                                }
                            }
                        }
                    }
                ]
            },
            {
                "title": sanitize("Cross-Border Readiness"),
                "description": sanitize("This section assesses your institution's ability to integrate with regional cross-border retail payment systems. Please answer each question based on your current capabilities and challenges."),
                "questions": [
                    {
                        "title": sanitize("How compatible is your institution with a regional governance framework for cross-border payments? (1 = Not Ready, 5 = Fully Ready)"),
                        "questionItem": {
                            "question": {
                                "scaleQuestion": {
                                    "low": 1, "high": 5,
                                    "lowLabel": sanitize("Not Ready"),
                                    "highLabel": sanitize("Fully Ready")
                                }
                            }
                        }
                    },
                    {
                        "title": sanitize("Please explain any legal or institutional challenges that affect your alignment with regional governance frameworks."),
                        "questionItem": {
                            "question": {
                                "textQuestion": {"paragraph": True}
                            }
                        }
                    },
                    {
                        "title": sanitize("How compatible is your institution with a common regional regulatory compliance rulebook? (1 = Not Ready, 5 = Fully Ready)"),
                        "questionItem": {
                            "question": {
                                "scaleQuestion": {
                                    "low": 1, "high": 5,
                                    "lowLabel": sanitize("Not Ready"),
                                    "highLabel": sanitize("Fully Ready")
                                }
                            }
                        }
                    },
                    {
                        "title": sanitize("Please describe any friction points or obstacles in aligning your compliance frameworks with those of other countries."),
                        "questionItem": {
                            "question": {
                                "textQuestion": {"paragraph": True}
                            }
                        }
                    },
                    {
                        "title": sanitize("How ready is your institution to settle cross-border retail transactions in central bank money? (1 = Not Ready, 5 = Fully Ready)"),
                        "questionItem": {
                            "question": {
                                "scaleQuestion": {
                                    "low": 1, "high": 5,
                                    "lowLabel": sanitize("Not Ready"),
                                    "highLabel": sanitize("Fully Ready")
                                }
                            }
                        }
                    },
                    {
                        "title": sanitize("Please comment on any messaging standards, liquidity bridges, or technical enablers required for cross-border retail payment settlement."),
                        "questionItem": {
                            "question": {
                                "textQuestion": {"paragraph": True}
                            }
                        }
                    },
                    {
                        "title": sanitize("How compatible are your current anti-money laundering (AML) and know-your-customer (KYC) processes with those of other regional institutions? (1 = Not Compatible, 5 = Fully Compatible)"),
                        "questionItem": {
                            "question": {
                                "scaleQuestion": {
                                    "low": 1, "high": 5,
                                    "lowLabel": sanitize("Not Compatible"),
                                    "highLabel": sanitize("Fully Compatible")
                                }
                            }
                        }
                    },
                    {
                        "title": sanitize("Describe any technical or operational barriers to achieving real-time settlement for cross-border retail payments."),
                        "questionItem": {
                            "question": {
                                "textQuestion": {"paragraph": True}
                            }
                        }
                    },
                    {
                        "title": sanitize("Does your country have a National Payment Switch? If yes, to what extent does it support real-time interoperability between bank accounts, e-wallets, and credit unions?"),
                        "questionItem": {
                            "question": {
                                "scaleQuestion": {
                                    "low": 1, "high": 5,
                                    "lowLabel": sanitize("Very Low"),
                                    "highLabel": sanitize("Very High")
                                }
                            }
                        }
                    }
                ]
            },
            {
                "title": sanitize("Risk Assessment"),
                "description": sanitize("This section uses ISO-aligned definitions to evaluate your institution's exposure to key financial and operational risks related to regional retail payment system implementation and securities settlement infrastructure."),
                "questions": [
                    {
                        "title": sanitize("How would you assess your institution's operational risk (e.g., inadequate or failed internal processes, people, or systems)? (1 = Negligible, 5 = Critical)"),
                        "questionItem": {
                            "question": {
                                "scaleQuestion": {
                                    "low": 1, "high": 5,
                                    "lowLabel": sanitize("Negligible"),
                                    "highLabel": sanitize("Critical")
                                }
                            }
                        }
                    },
                    {
                        "title": sanitize("Please explain your operational risk assessment, including any recent incidents or mitigation strategies."),
                        "questionItem": {
                            "question": {
                                "textQuestion": {"paragraph": True}
                            }
                        }
                    },
                    {
                        "title": sanitize("How would you assess your institution's foreign exchange (FX) risk (e.g., volatility in currency value impacting cross-border settlements)? (1 = Low Exposure, 5 = High Exposure)"),
                        "questionItem": {
                            "question": {
                                "scaleQuestion": {
                                    "low": 1, "high": 5,
                                    "lowLabel": sanitize("Low Exposure"),
                                    "highLabel": sanitize("High Exposure")
                                }
                            }
                        }
                    },
                    {
                        "title": sanitize("Please explain your FX risk exposure assessment, including any hedging strategies."),
                        "questionItem": {
                            "question": {
                                "textQuestion": {"paragraph": True}
                            }
                        }
                    },
                    {
                        "title": sanitize("How would you assess your institution's credit risk (e.g., risk of counterparty default across the settlement chain)? (1 = Insignificant, 5 = Severe)"),
                        "questionItem": {
                            "question": {
                                "scaleQuestion": {
                                    "low": 1, "high": 5,
                                    "lowLabel": sanitize("Insignificant"),
                                    "highLabel": sanitize("Severe")
                                }
                            }
                        }
                    },
                    {
                        "title": sanitize("Please explain your credit risk concerns, including any recent experiences or controls in place."),
                        "questionItem": {
                            "question": {
                                "textQuestion": {"paragraph": True}
                            }
                        }
                    },
                    {
                        "title": sanitize("How would you assess your institution's liquidity risk under stress scenarios (e.g., inability to fund obligations in CBDC and fiat simultaneously)? (1 = Very Liquid, 5 = Highly Illiquid)"),
                        "questionItem": {
                            "question": {
                                "scaleQuestion": {
                                    "low": 1, "high": 5,
                                    "lowLabel": sanitize("Very Liquid"),
                                    "highLabel": sanitize("Highly Illiquid")
                                }
                            }
                        }
                    },
                    {
                        "title": sanitize("Please describe any potential liquidity shortfalls or strategies your institution uses to mitigate liquidity risk."),
                        "questionItem": {
                            "question": {
                                "textQuestion": {"paragraph": True}
                            }
                        }
                    },
                    {
                        "title": sanitize("How would you assess the cyber risk exposure of your institution when participating in regional cross-border payment systems? (1 = Low, 5 = High)"),
                        "questionItem": {
                            "question": {
                                "scaleQuestion": {
                                    "low": 1, "high": 5,
                                    "lowLabel": sanitize("Low"),
                                    "highLabel": sanitize("High")
                                }
                            }
                        }
                    },
                    {
                        "title": sanitize("Please describe any cross-border fraud detection or prevention mechanisms currently in place."),
                        "questionItem": {
                            "question": {
                                "textQuestion": {"paragraph": True}
                            }
                        }
                    }
                ]
            },
            {
                "title": sanitize("Implementation Readiness"),
                "description": sanitize("This section evaluates your institution's overall readiness to roll out a regional retail payment system. Please provide honest and detailed responses."),
                "questions": [
                    {
                        "title": sanitize("How would you rate your institution's readiness to implement a regional retail payment system? (1 = Not Ready, 5 = Fully Ready)"),
                        "questionItem": {
                            "question": {
                                "scaleQuestion": {
                                    "low": 1, "high": 5,
                                    "lowLabel": sanitize("Not Ready"),
                                    "highLabel": sanitize("Fully Ready")
                                }
                            }
                        }
                    },
                    {
                        "title": sanitize("Please explain your implementation readiness rating, including any key enablers or barriers."),
                        "questionItem": {
                            "question": {
                                "textQuestion": {"paragraph": True}
                            }
                        }
                    },
                    {
                        "title": sanitize("How would you rate your institution’s capacity to allocate resources (staff, budget, technology) for cross-border payment system implementation? (1 = Not Ready, 5 = Fully Ready)"),
                        "questionItem": {
                            "question": {
                                "scaleQuestion": {
                                    "low": 1, "high": 5,
                                    "lowLabel": sanitize("Not Ready"),
                                    "highLabel": sanitize("Fully Ready")
                                }
                            }
                        }
                    },
                    {
                        "title": sanitize("Describe any change management strategies planned for the transition to a regional cross-border payment system."),
                        "questionItem": {
                            "question": {
                                "textQuestion": {"paragraph": True}
                            }
                        }
                    },
                    {
                        "title": sanitize("How effective is your institution’s strategy to provide low-cost digital payment acceptance solutions (QR codes, POS, proxy identifiers) to MSMEs and micro-merchants?"),
                        "questionItem": {
                            "question": {
                                "scaleQuestion": {
                                    "low": 1, "high": 5,
                                    "lowLabel": sanitize("Very Low"),
                                    "highLabel": sanitize("Very High")
                                }
                            }
                        }
                    }
                ]
            },
            {
                "title": sanitize("Regional Integration"),
                "description": sanitize("Assess regional integration aspects."),
                "questions": [
                    {
                        "title": sanitize("Describe key enablers or barriers to regional integration"),
                        "questionItem": {
                            "question": {
                                "textQuestion": {"paragraph": True}
                            }
                        }
                    },
                    {
                        "title": sanitize("How effective is current collaboration with regional partners on retail payment system integration projects? (1 = Not Effective, 5 = Highly Effective)"),
                        "questionItem": {
                            "question": {
                                "scaleQuestion": {
                                    "low": 1, "high": 5,
                                    "lowLabel": sanitize("Not Effective"),
                                    "highLabel": sanitize("Highly Effective")
                                }
                            }
                        }
                    },
                    {
                        "title": sanitize("Please identify any key technical standards or protocols that would facilitate smoother regional retail payment system integration."),
                        "questionItem": {
                            "question": {
                                "textQuestion": {"paragraph": True}
                            }
                        }
                    },
                    {
                        "title": sanitize("How exposed is your jurisdiction to correspondent banking de-risking, particularly among smaller institutions and high-risk sectors?"),
                        "questionItem": {
                            "question": {
                                "textQuestion": {"paragraph": True}
                            }
                        }
                    },
                    {
                        "title": sanitize("How effective are your current strategies to safeguard access to cross-border payment corridors without relying solely on global correspondent banks?"),
                        "questionItem": {
                            "question": {
                                "textQuestion": {"paragraph": True}
                            }
                        }
                    },
                    {
                        "title": sanitize("How successful has your jurisdiction been in enforcing proportionate financial integrity standards without excluding vulnerable customers?"),
                        "questionItem": {
                            "question": {
                                "textQuestion": {"paragraph": True}
                            }
                        }
                    },
                    {
                        "title": sanitize("How aligned are national efforts with the G20 cross-border payments roadmap?"),
                        "questionItem": {
                            "question": {
                                "textQuestion": {"paragraph": True}
                            }
                        }
                    },
                    {
                        "title": sanitize("How ready is your jurisdiction to participate in regional proof-of-concept pilots? such as multilateral arrangements (e.g. Africa–Caribbean corridor)?"),
                        "questionItem": {
                            "question": {
                                "textQuestion": {"paragraph": True}
                            }
                        }
                    }
                ]
            },
            {
                "title": sanitize("Cost-Benefit Analysis"),
                "description": sanitize("Assessment of the costs and benefits of participating in a regional retail payment system."),
                "questions": [
                    {
                        "title": sanitize("How would you rate the cost-benefit ratio of participating in a regional retail payment system? (1 = Low Benefit, 5 = High Benefit)"),
                        "questionItem": {
                            "question": {
                                "scaleQuestion": {
                                    "low": 1, "high": 5,
                                    "lowLabel": sanitize("Low Benefit"),
                                    "highLabel": sanitize("High Benefit")
                                }
                            }
                        }
                    },
                    {
                        "title": sanitize("Please justify your cost-benefit assessment, providing supporting rationale and examples where possible."),
                        "questionItem": {
                            "question": {
                                "textQuestion": {"paragraph": True}
                            }
                        }
                    },
                    {
                        "title": sanitize("How do you assess the expected operational cost savings from participating in a regional cross-border retail payment system? (1 = No Savings, 5 = Significant Savings)"),
                        "questionItem": {
                            "question": {
                                "scaleQuestion": {
                                    "low": 1, "high": 5,
                                    "lowLabel": sanitize("No Savings"),
                                    "highLabel": sanitize("Significant Savings")
                                }
                            }
                        }
                    },
                    {
                        "title": sanitize("Please provide examples of anticipated efficiency gains or cost reductions from cross-border retail payment integration."),
                        "questionItem": {
                            "question": {
                                "textQuestion": {"paragraph": True}
                            }
                        }
                    }
                ]
            },
            {
                "title": sanitize("Governance Framework"),
                "description": sanitize("This section evaluates your institution's internal oversight structures and governance readiness for implementing regional retail payment systems."),
                "questions": [
                    {
                        "title": sanitize("How clear are the roles and responsibilities for cross-border retail payment oversight within your institution? (1 = Not Clear, 5 = Very Clear)"),
                        "questionItem": {
                            "question": {
                                "scaleQuestion": {
                                    "low": 1, "high": 5,
                                    "lowLabel": sanitize("Not Clear"),
                                    "highLabel": sanitize("Very Clear")
                                }
                            }
                        }
                    },
                    {
                        "title": sanitize("Describe any governance structures established for managing cross-border retail payment risks."),
                        "questionItem": {
                            "question": {
                                "textQuestion": {"paragraph": True}
                            }
                        }
                    }
                ]
            },
            {
                "title": sanitize("Stakeholder Impact"),
                "description": sanitize("This section assesses the expected impact of a regional retail payment system on your institution and other stakeholders, including the public."),
                "questions": [
                    {
                        "title": sanitize("How significant do you expect the impact of a regional retail payment system to be on your institution and stakeholders? (1 = Low Impact, 5 = High Impact)"),
                        "questionItem": {
                            "question": {
                                "scaleQuestion": {
                                    "low": 1, "high": 5,
                                    "lowLabel": sanitize("Low Impact"),
                                    "highLabel": sanitize("High Impact")
                                }
                            }
                        }
                    },
                    {
                        "title": sanitize("Please explain how stakeholders will be affected and what measures will be taken to mitigate any risks."),
                        "questionItem": {
                            "question": {
                                "textQuestion": {"paragraph": True}
                            }
                        }
                    },
                    {
                        "title": sanitize("How do you expect cross-border retail payment integration to affect your customers’ experience? (1 = No Change, 5 = Major Improvement)"),
                        "questionItem": {
                            "question": {
                                "scaleQuestion": {
                                    "low": 1, "high": 5,
                                    "lowLabel": sanitize("No Change"),
                                    "highLabel": sanitize("Major Improvement")
                                }
                            }
                        }
                    },
                    {
                        "title": sanitize("Please describe any stakeholder engagement or communication strategies planned for the rollout of cross-border retail payment services."),
                        "questionItem": {
                            "question": {
                                "textQuestion": {"paragraph": True}
                            }
                        }
                    }
                ]
            }
        ]


        
    def _get_credentials(self):
        try:
            if not os.path.exists(self.token_path):
                print(f"⚠️ Token path not found: {self.token_path}")
            if not os.path.exists(self.credentials_path):
                print(f"⚠️ Credentials path not found: {self.credentials_path}")
    
            from google.auth.transport.requests import Request
            from google.oauth2.credentials import Credentials
            from google_auth_oauthlib.flow import InstalledAppFlow
            import pickle
    
            creds = None
            if os.path.exists(self.token_path):
                with open(self.token_path, 'rb') as token:
                    creds = pickle.load(token)
    
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(self.credentials_path, self.SCOPES)
                    creds = flow.run_local_server(port=0)
    
                with open(self.token_path, 'wb') as token:
                    pickle.dump(creds, token)
    
            return creds

        except Exception as e:
            print(f"❌ Credential setup failed: {e}")
            return None


    
    def _wrap_text_pixels(self, text, font, max_width, draw):
        lines, line = [], ""
        for word in text.split():
            test_line = f"{line} {word}".strip()
            if draw.textlength(test_line, font=font) <= max_width:
                line = test_line
            else:
                if line:
                    lines.append(line)
                line = word
        if line:
            lines.append(line)
        return lines
   

    def _wrap_text(self, text, font, max_width, draw):
        lines, line = [], ""
        for word in text.split():
            test_line = f"{line} {word}".strip()
            if draw.textlength(test_line, font=font) <= max_width:
                line = test_line
            else:
                if line:
                    lines.append(line)
                line = word
        if line:
            lines.append(line)
        return lines
    
    def _create_and_upload_header_image(self, title: str, desc: str) -> str:
        # Settings: 4:1 aspect ratio for Google Forms header
        img_width = 800
        img_height = 200
        padding = 24
        spacing = 12
        bg_color = "#f8fafc"
        title_color = "#1a202c"
        desc_color = "#4a5568"
        border_color = "#cbd5e0"
    
        # Fonts with fallback
        def get_font(size, bold=False):
            try:
                if bold:
                    return ImageFont.truetype("arialbd.ttf", size)
                return ImageFont.truetype("arial.ttf", size)
            except IOError:
                return ImageFont.load_default()
    
        font_title = get_font(36, bold=True)
        font_desc = get_font(18)
    
        # Prepare for pixel-based wrapping
        dummy_img = Image.new("RGB", (1, 1))
        draw_dummy = ImageDraw.Draw(dummy_img)
        max_text_width = img_width - 2 * padding
        title_lines = self._wrap_text(title, font_title, max_text_width, draw_dummy)
        desc_lines = self._wrap_text(desc, font_desc, max_text_width, draw_dummy)

    
        # Calculate vertical placement
        title_heights = [draw_dummy.textbbox((0, 0), line, font=font_title)[3] for line in title_lines]
        desc_heights = [draw_dummy.textbbox((0, 0), line, font=font_desc)[3] for line in desc_lines]
        total_title_height = sum(title_heights) + (len(title_lines)-1)*spacing
        total_desc_height = sum(desc_heights) + (len(desc_lines)-1)*spacing
        total_text_height = total_title_height + spacing + total_desc_height
    
        # Center text block vertically
        y = (img_height - total_text_height) // 2
    
        # Create image
        img = Image.new("RGB", (img_width, img_height), bg_color)
        draw = ImageDraw.Draw(img)
    
        # Draw title (centered)
        for i, line in enumerate(title_lines):
            w = draw.textlength(line, font=font_title)
            x = (img_width - w) // 2
            draw.text((x, y), line, font=font_title, fill=title_color)
            y += title_heights[i] + spacing
    
        # Draw description (centered)
        for i, line in enumerate(desc_lines):
            w = draw.textlength(line, font=font_desc)
            x = (img_width - w) // 2
            draw.text((x, y), line, font=font_desc, fill=desc_color)
            y += desc_heights[i] + spacing
    
        # Optional: Add a subtle border
        draw.rectangle([0, 0, img_width-1, img_height-1], outline=border_color, width=2)
    
        # Save to temp file
        tmp_path = os.path.join(tempfile.gettempdir(), f"hdr_{hash(title)}.png")
        img.save(tmp_path, format="PNG")
    
        # Upload to Drive and set public
        try:
            media = MediaFileUpload(tmp_path, mimetype="image/png")
            meta = {"name": os.path.basename(tmp_path)}
            uploaded = self.drive.files().create(body=meta, media_body=media, fields="id").execute()
            file_id = uploaded["id"]
    
            # Make the file public
            self.drive.permissions().create(
                fileId=file_id,
                body={"role": "reader", "type": "anyone"}
            ).execute()
        finally:
            try:
                os.remove(tmp_path)
            except OSError:
                pass
    
        return file_id
    
    def _inject_section_with_image(self, form_id: str, section_title: str, section_desc: str, questions: List[Dict[str, Any]]):
        """
        Inserts a section header (as a pageBreakItem), a styled header image, and its questions into the form.
        """
        start = self.current_index
    
        # 1) Render & upload header PNG, get fileId
        title_clean = self._clean_form_text(section_title)
        desc_clean = self._clean_form_text(section_desc)
        file_id = self._create_and_upload_header_image(title_clean, desc_clean)
        public_url = f"https://drive.google.com/uc?export=view&id={file_id}"
    
        # 2) Prepare the requests
        requests = [
            # A) New section
            {"createItem": {
                "location": {"index": start},
                "item": {"pageBreakItem": {}}
            }},
            # B) Header image via sourceUri (with altText)
            {"createItem": {
                "location": {"index": start + 1},
                "item": {
                    "imageItem": {
                        "image": {
                            "sourceUri": public_url,
                            "altText": title_clean
                        }
                    }
                }
            }}
        ]
    
        # 3) Sanitize and append your questionItem blocks
        for offset, q in enumerate(questions, start=2):
            if "title" in q:
                q["title"] = self._clean_form_text(q["title"])
            if "helpText" in q:
                q["helpText"] = self._clean_form_text(q["helpText"])
            requests.append({
                "createItem": {
                    "location": {"index": start + offset},
                    "item": q
                }
            })
    
        # 4) Send each request one-by-one (as per your batch update logic)
        self._send_batch_update(form_id, {"requests": requests})
        self.current_index = start + len(requests)
        print(f"✅ Injected '{section_title}' at index {start}; next index = {self.current_index}")
    
    def _send_batch_update(self, form_id: str, body: Dict[str, Any]) -> None:
        try:
            for req in body.get("requests", []):
                info = self.forms.forms().get(formId=form_id).execute()
                item_count = len(info.get("items", []))
                loc = req["createItem"]["location"]
                idx = loc.get("index", 0)
                if isinstance(idx, int):
                    loc["index"] = min(max(0, idx), item_count)
                self.forms.forms().batchUpdate(
                    formId=form_id,
                    body={"requests": [req]}
                ).execute()
                self.current_index += 1
        except HttpError as e:
            logger.error(f"Google API error updating form {form_id}: {e}", exc_info=True)
        except Exception as e:
            logger.error(f"Unexpected error updating form {form_id}: {e}", exc_info=True)


    def create_centralbank_survey(self) -> str:
        # 🔁 Clean section definitions
        for sec in self.section_definitions:
            sec["title"] = self._clean_form_text(sec["title"])
            sec["description"] = self._clean_form_text(sec["description"])
            for q in sec.get("questions", []):
                if "title" in q:
                    q["title"] = self._clean_form_text(q["title"])
                if "helpText" in q:
                    q["helpText"] = self._clean_form_text(q["helpText"])
    
        # 🧾 Create Form
        form_body = {
            "info": {
                "title": "CARICOM Regional Financial Market Infrastructure Survey",
                "documentTitle": "Central Bank Survey Form"
            }
        }
        created = self.forms.forms().create(body=form_body).execute()
        form_id = created["formId"]
        self.current_index = 1
    
        # 📤 Inject sanitized content
        for sec in self.section_definitions:
            self._inject_section_with_image(
                form_id,
                sec["title"],
                sec["description"],
                sec["questions"]
            )
    
        # 🗂️ Create linked response sheet
        sheets_service = build("sheets", "v4", credentials=self.creds)
        sheet = sheets_service.spreadsheets().create(body={
            "properties": {"title": f"{form_body['info']['title']} Responses"}
        }).execute()
        self.response_sheet_id = sheet["spreadsheetId"]
        print(f"📄 Google Sheet created: {self.response_sheet_id}")
        print("⚠️ Note: Link this sheet via Forms UI → Responses → Select destination")
    
        return form_id

    def _clean_form_text(self, text: str) -> str:
        import re
        text = text.replace("\n", " ")
        text = re.sub(r"font-family[:;]?.*?;", "", text, flags=re.IGNORECASE)
        text = re.sub(r"font-family", "", text, flags=re.IGNORECASE)
        text = re.sub(r"\s{2,}", " ", text)
        return text.strip()