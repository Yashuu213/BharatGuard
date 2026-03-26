import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.units import inch

class CompliancePDFGenerator:
    """
    Generates professional, auditor-ready Compliance Certificates.
    """
    
    def __init__(self, output_dir: str = "output"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()

    def _setup_custom_styles(self):
        self.styles.add(ParagraphStyle(
            name='CenterTitle',
            parent=self.styles['Title'],
            alignment=1,
            fontSize=24,
            spaceAfter=20,
            textColor=colors.HexColor("#1A237E")
        ))
        self.styles.add(ParagraphStyle(
            name='ComplianceScore',
            parent=self.styles['Normal'],
            alignment=1,
            fontSize=48,
            leading=56,
            spaceBefore=20,
            spaceAfter=20
        ))
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=14,
            spaceBefore=12,
            spaceAfter=6,
            textColor=colors.HexColor("#303F9F"),
            borderPadding=5,
            borderWidth=0,
            backColor=colors.HexColor("#E8EAF6")
        ))

    def generate_report(self, state: dict) -> str:
        """
        Creates the PDF report and returns the absolute path.
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"BharatGuard_Compliance_Report_{timestamp}.pdf"
        file_path = os.path.abspath(os.path.join(self.output_dir, filename))
        
        doc = SimpleDocTemplate(file_path, pagesize=A4)
        elements = []

        # --- Header ---
        elements.append(Paragraph("BharatGuard Compliance Certificate", self.styles['CenterTitle']))
        elements.append(Paragraph(f"Generated on: {datetime.now().strftime('%B %d, %Y | %I:%M %p')}", self.styles['Normal']))
        elements.append(Spacer(1, 0.2*inch))

        # --- Task Summary ---
        elements.append(Paragraph("Project Audit Summary", self.styles['SectionHeader']))
        elements.append(Paragraph(f"<b>Target Task:</b> {state.get('user_task', 'N/A')}", self.styles['Normal']))
        elements.append(Paragraph(f"<b>Tech Stack:</b> {state.get('plan', {}).get('tech_stack', 'FastAPI + React')}", self.styles['Normal']))
        elements.append(Spacer(1, 0.1*inch))

        # --- Score Section ---
        score = state.get('compliance_score', 0)
        score_color = colors.green if score >= 80 else (colors.orange if score >= 60 else colors.red)
        
        score_style = self.styles['ComplianceScore'].clone('DynamicScore')
        score_style.textColor = score_color
        
        elements.append(Paragraph(f"{score}%", score_style))
        elements.append(Paragraph("Overall Compliance Health Score", self.styles['Normal']))
        elements.append(Spacer(1, 0.3*inch))

        # --- Breakdown Table ---
        elements.append(Paragraph("Detailed Compliance Breakdown", self.styles['SectionHeader']))
        
        data = [["Rule ID", "Category", "Requirement", "Status", "Severity"]]
        for detail in state.get('compliance_details', []):
            status_icon = "PASS" if detail['status'] == 'passed' else "FAIL"
            data.append([
                detail['rule_id'],
                detail['category'],
                detail['description'][:40] + "...",
                status_icon,
                detail['severity'].upper()
            ])

        table = Table(data, colWidths=[0.8*inch, 0.8*inch, 2.5*inch, 0.7*inch, 0.7*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#3F51B5")),
            ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,-1), 8),
            ('BOTTOMPADDING', (0,0), (-1,0), 12),
            ('BACKGROUND', (0,1), (-1,-1), colors.whitesmoke),
            ('GRID', (0,0), (-1,-1), 0.5, colors.grey)
        ]))
        elements.append(table)
        elements.append(Spacer(1, 0.3*inch))

        # --- Fix Suggestions ---
        if state.get('fix_suggestions'):
            elements.append(Paragraph("Required Remediation Actions", self.styles['SectionHeader']))
            for suggestion in state.get('fix_suggestions', []):
                elements.append(Paragraph(f"• {suggestion}", self.styles['Normal']))
            elements.append(Spacer(1, 0.3*inch))

        # --- Footer ---
        elements.append(Spacer(1, 1*inch))
        elements.append(Paragraph("-" * 80, self.styles['Normal']))
        elements.append(Paragraph("<b>Disclaimer:</b> This is an AI-generated demo prototype. Not for production legal use.", self.styles['Italic']))
        elements.append(Paragraph("Demo Prototype of MetaForge | Fully Local Deployment | March 2026", self.styles['Normal']))

        doc.build(elements)
        return file_path
