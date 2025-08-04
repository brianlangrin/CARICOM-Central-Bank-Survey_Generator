class EmailTemplateManager:
    """
    Manages templated email messages for survey invitations and reminders.
    """

    def __init__(self):
        self.templates = {
            "survey_invite": """<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <style>
    body {{ font-family: Arial, sans-serif; color: #333; line-height: 1.6; }}
    .container {{ max-width: 680px; margin: auto; padding: 20px; background-color: #fdfdfd; }}
    h1, h2 {{ color: #005a8b; }}
    ul {{ padding-left: 20px; }}
    .section {{ margin-bottom: 20px; }}
    .cta {{ display: block; margin-top: 20px; padding: 10px 20px; background-color: #005a8b;
          color: white; text-decoration: none; border-radius: 5px; text-align: center;
          font-weight: bold; }}
    .note {{ font-size: 0.9em; background-color: #eef7ff; padding: 10px;
            border-left: 4px solid #005a8b; }}
  </style>
</head>
<body>
  <div class="container">
    <h1>📢 You're Invited to Shape the Future of CARICOM Finance 📢</h1>
    <p>Dear {name},</p>
    <p>The CARICOM Secretariat is pleased to invite you to participate in the
    <strong>{survey_title}</strong>. This initiative supports the modernization of our regional
    financial market infrastructure to strengthen integration across Member States.</p>
    <div class="section">
      <h2>🌐 Why This Survey Matters</h2>
      <ul>
        <li>Free movement of people</li>
        <li>Free movement of goods and capital</li>
        <li>Right of establishment</li>
        <li>Provision of services</li>
      </ul>
    </div>
    <div class="section">
      <h2>💡 Current Challenges</h2>
      <ul>
        <li>Limited success in cross-border securities settlement and stock exchange integration</li>
        <li>Low liquidity and fragmentation across capital markets</li>
        <li>Continued reliance on cash and cheques</li>
        <li>Limited interoperability among regional retail payment systems</li>
        <li>Limited digitalization of commerce</li>
        <li>Poor access to finance</li>
      </ul>
    </div>
    <div class="section">
      <h2>📋 Survey Sections</h2>
      <ul>
        <li><strong>Respondent Information for Survey Tracking</strong> – 2 questions</li>
        <li><strong>Policy and Regulatory Assessment</strong> – 15 questions</li>
        <li><strong>Monetary Policy</strong> – 8 questions</li>
        <li><strong>Financial Stability</strong> – 13 questions</li>
        <li><strong>Technical Readiness</strong> – 13 questions</li>
        <li><strong>Cross-Border Readiness</strong> – 9 questions</li>
        <li><strong>Risk Assessment</strong> – 10 questions</li>
        <li><strong>Implementation Readiness</strong> – 5 questions</li>
        <li><strong>Regional Integration</strong> – 8 questions</li>
        <li><strong>Cost-Benefit Analysis</strong> – 4 questions</li>
        <li><strong>Governance Framework</strong> – 2 questions</li>
        <li><strong>Stakeholder Impact</strong> – 4 questions</li>
      </ul>
    </div>
    <div class="note">
      <strong>Instructions for Completing the Survey:</strong>
      <ul>
        <li>You may attach supporting documents (Excel, PDF) where requested using the file upload option.</li>
        <li>If you wish to reference external resources, please paste the URL in your response.</li>
        <li>For tabular data, please attach a file or format your answer as a list.</li>
        <li>Answer all questions as completely as possible to help us understand your institution's operations and needs.</li>
      </ul>
    </div>
    <p>Your insights will directly inform regional technical recommendations and policy alignment.
    Thank you for contributing to a more efficient, inclusive, and future-ready financial services framework.</p>
    <a class="cta" href="{form_url}" target="_blank">👉 Access the Survey</a>
    <p>Sincerely,<br><strong>On behalf of: CARICOM Secretariat</strong></p>
  </div>
</body>
</html>"""
        }

    def render(self, template_name: str, **kwargs) -> str:
        """
        Render a named email template using keyword substitutions.

        Args:
            template_name (str): The key in self.templates (e.g., 'survey_invite')
            **kwargs: Named substitutions like name=, survey_title=, form_url=

        Returns:
            str: Formatted email body
        """
        if template_name not in self.templates:
            raise ValueError(f"Template '{template_name}' not found.")
        return self.templates[template_name].format(**kwargs)