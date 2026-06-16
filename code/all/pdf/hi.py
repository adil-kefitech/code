import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.lib.colors import HexColor

# --- Design Configuration ---
PRIMARY = HexColor('#1A7A8A')    # Corporate Deep Teal
SECONDARY = HexColor('#145F6E')  # Accent Dark Teal
TEXT_COLOR = HexColor('#222222') # Professional Charcoal Text
LIGHT_BG = HexColor('#F4F7F8')   # Light Slate Alternating Tint
BORDER_COLOR = HexColor('#CCCCCC') # Muted Grid Grey

class NumberedCanvas(canvas.Canvas):
    """ Two-pass canvas to dynamically compute and render real page totals """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        
        # Suppress running header/footer elements on the Title Cover Page
        if self._pageNumber == 1:
            self.restoreState()
            return
            
        # Draw Running Header
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(SECONDARY)
        self.drawString(20 * mm, A4[1] - 12 * mm, "MAYFLOWER SYSTEMS — MULTI-PAGE REFERENCE & SPECIFICATION DOCUMENT")
        
        self.setStrokeColor(PRIMARY)
        self.setLineWidth(0.5)
        self.line(20 * mm, A4[1] - 14 * mm, A4[0] - 20 * mm, A4[1] - 14 * mm)
        
        # Draw Running Footer
        self.setStrokeColor(BORDER_COLOR)
        self.setLineWidth(0.5)
        self.line(20 * mm, 15 * mm, A4[0] - 20 * mm, 15 * mm)
        
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.gray)
        self.drawString(20 * mm, 10 * mm, "Confidential — Internal Business Distribution Only")
        
        # Dynamic page numbers string output
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(A4[0] - 20 * mm, 10 * mm, page_str)
        
        self.restoreState()

def create_multi_page_pdf(filename):
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        leftMargin=20*mm,
        rightMargin=20*mm,
        topMargin=22*mm, 
        bottomMargin=22*mm
    )
    
    styles = getSampleStyleSheet()
    
    # Custom Typography Styles Configuration
    title_style = ParagraphStyle(
        'CoverTitle', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=28, leading=34, textColor=PRIMARY, spaceAfter=15
    )
    subtitle_style = ParagraphStyle(
        'CoverSubtitle', parent=styles['Normal'],
        fontName='Helvetica', fontSize=14, leading=18, textColor=colors.gray, spaceAfter=40
    )
    h1_style = ParagraphStyle(
        'SectionH1', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=18, leading=22, textColor=PRIMARY,
        spaceBefore=15, spaceAfter=10, keepWithNext=True
    )
    h2_style = ParagraphStyle(
        'SectionH2', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=13, leading=16, textColor=SECONDARY,
        spaceBefore=12, spaceAfter=6, keepWithNext=True
    )
    body_style = ParagraphStyle(
        'CustomBody', parent=styles['Normal'],
        fontName='Helvetica', fontSize=10.5, leading=15, textColor=TEXT_COLOR,
        spaceAfter=10, alignment=TA_JUSTIFY
    )
    bullet_style = ParagraphStyle(
        'CustomBullet', parent=body_style,
        leftIndent=15, bulletIndent=5, spaceAfter=5, alignment=TA_LEFT
    )
    table_cell_bold = ParagraphStyle(
        'TableCellBold', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=9, leading=12, textColor=SECONDARY
    )
    table_cell_text = ParagraphStyle(
        'TableCellText', parent=styles['Normal'], fontName='Helvetica', fontSize=9, leading=12, textColor=TEXT_COLOR
    )

    story = []
    usable_width = A4[0] - 40*mm

    # ---------------- PAGE 1: COVER ----------------
    story.append(Spacer(1, 40*mm))
    d_table = Table([[""]], colWidths=[usable_width], rowHeights=[6*mm])
    d_table.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,-1), PRIMARY)]))
    story.append(d_table)
    story.append(Spacer(1, 10*mm))
    story.append(Paragraph("MAYFLOWER SYSTEMS &amp; OPERATIONS", title_style))
    story.append(Paragraph("Comprehensive Framework, Business Intelligence Metrics, and Structural Guidelines", subtitle_style))
    story.append(Spacer(1, 50*mm))
    meta_text = """
    <b>Document Control ID:</b> MSO-2026-X10<br/>
    <b>Version:</b> 4.2.1<br/>
    <b>Release Date:</b> June 01, 2026<br/>
    <b>Author:</b> Operations &amp; Strategy Architecture Division
    """
    story.append(Paragraph(meta_text, body_style))
    story.append(PageBreak())

    # ---------------- PAGE 2: TABLE OF CONTENTS & SUMMARY ----------------
    story.append(Paragraph("Document Structure &amp; Overview", h1_style))
    story.append(Spacer(1, 5*mm))
    toc_data = [
        ["Section 1", "Executive Summary &amp; Structural Architecture", "Page 2"],
        ["Section 2", "Operational Workflow &amp; Process Automation", "Page 3"],
        ["Section 3", "Financial Forecasts &amp; Analytical Ledger", "Page 4"],
        ["Section 4", "Regulatory Compliance Framework &amp; Audits", "Page 5"],
        ["Section 5", "Technical Stack Architecture &amp; Scalability", "Page 6"],
        ["Section 6", "Risk Matrix Assessment &amp; Contingency Maps", "Page 7"],
        ["Section 7", "Human Resource Optimization &amp; Capital Retention", "Page 8"],
        ["Section 8", "Marketing Benchmarks &amp; Acquisition Funnels", "Page 9"],
        ["Section 9", "Appendix: Historical Data Ledger (2020-2026)", "Page 10"],
    ]
    toc_table_data = []
    for sec, title, pg in toc_data:
        toc_table_data.append([Paragraph(f"<b>{sec}</b>", table_cell_bold), Paragraph(title, table_cell_text), Paragraph(pg, table_cell_bold)])
    toc_table = Table(toc_table_data, colWidths=[25*mm, usable_width - 45*mm, 20*mm])
    toc_table.setStyle(TableStyle([('LINEBELOW', (0,0), (-1,-1), 0.5, BORDER_COLOR), ('PADDING', (0,0), (-1,-1), 6)]))
    story.append(toc_table)
    story.append(Spacer(1, 12*mm))
    story.append(Paragraph("Executive Core Summary", h2_style))
    story.append(Paragraph("This architectural directive maps out the strategic posture and operational paradigms guiding Mayflower Systems across the 2026–2030 fiscal timeline.", body_style))
    story.append(PageBreak())

    # ---------------- PAGE 3: OPERATIONAL WORKFLOW ----------------
    story.append(Paragraph("Section 2: Operational Workflow &amp; Process Automation", h1_style))
    story.append(Paragraph("Modern scaling limits dictate that continuous data evaluation workflows remain modular.", body_style))
    story.append(Paragraph("• <b>1. Ingestion Phase:</b> Sanitization of multi-tenant analytical inputs via schema validations.", bullet_style))
    story.append(Paragraph("• <b>2. Processing Engine:</b> Low-latency asynchronous compilation leveraging dynamic threads.", bullet_style))
    story.append(Paragraph("• <b>3. Final Serialization:</b> Distributing structured ledgers directly to replicas.", bullet_style))
    story.append(Spacer(1, 5*mm))
    pipeline_data = [
        [Paragraph("<b>Pipeline Stage</b>", table_cell_bold), Paragraph("<b>Target Latency</b>", table_cell_bold), Paragraph("<b>Failure Recovery Vector</b>", table_cell_bold)],
        [Paragraph("Data Ingestion", table_cell_text), Paragraph("&lt; 45ms", table_cell_text), Paragraph("Automatic dead-letter queue routing", table_cell_text)],
        [Paragraph("State Computation", table_cell_text), Paragraph("&lt; 120ms", table_cell_text), Paragraph("Asynchronous snapshot rollback", table_cell_text)],
        [Paragraph("Ledger Commit", table_cell_text), Paragraph("&lt; 15ms", table_cell_text), Paragraph("Dual-region consensus fallback", table_cell_text)]
    ]
    p_table = Table(pipeline_data, colWidths=[40*mm, 35*mm, usable_width - 75*mm])
    p_table.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,0), LIGHT_BG), ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR), ('PADDING', (0,0), (-1,-1), 8)]))
    story.append(p_table)
    story.append(PageBreak())

    # ---------------- PAGE 4: FINANCIAL FORECASTS ----------------
    story.append(Paragraph("Section 3: Financial Forecasts &amp; Analytical Ledger", h1_style))
    fin_data = [
        [Paragraph("<b>Quarter</b>", table_cell_bold), Paragraph("<b>Gross ARR ($M)</b>", table_cell_bold), Paragraph("<b>OpEx Allocation</b>", table_cell_bold), Paragraph("<b>Net Yield Margin</b>", table_cell_bold)],
        [Paragraph("Q1 2026", table_cell_text), Paragraph("$14.2M", table_cell_text), Paragraph("$4.1M", table_cell_text), Paragraph("+ 22.4%", table_cell_text)],
        [Paragraph("Q2 2026", table_cell_text), Paragraph("$16.8M", table_cell_text), Paragraph("$4.2M", table_cell_text), Paragraph("+ 24.8%", table_cell_text)],
        [Paragraph("Q3 2026 (Est)", table_cell_text), Paragraph("$19.5M", table_cell_text), Paragraph("$5.8M", table_cell_text), Paragraph("+ 21.1%", table_cell_text)],
        [Paragraph("Q4 2026 (Est)", table_cell_text), Paragraph("$23.1M", table_cell_text), Paragraph("$6.0M", table_cell_text), Paragraph("+ 26.5%", table_cell_text)],
    ]
    f_table = Table(fin_data, colWidths=[35*mm, 40*mm, 40*mm, usable_width - 115*mm])
    f_table.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,0), PRIMARY), ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR), ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LIGHT_BG]), ('PADDING', (0,0), (-1,-1), 8)]))
    for i in range(4): fin_data[0][i].style.textColor = colors.white
    story.append(f_table)
    story.append(PageBreak())

    # ---------------- PAGE 5: REGULATORY COMPLIANCE ----------------
    story.append(Paragraph("Section 4: Regulatory Compliance Framework &amp; Audits", h1_style))
    comp_data = [
        [Paragraph("<b>Standard</b>", table_cell_bold), Paragraph("<b>Scope Requirements</b>", table_cell_bold), Paragraph("<b>Audit Cycle</b>", table_cell_bold)],
        [Paragraph("SOC 2 Type II", table_cell_text), Paragraph("Continuous validation of encryption-at-rest, strict multi-factor IAM controls.", table_cell_text), Paragraph("Annual", table_cell_text)],
        [Paragraph("ISO 27001", table_cell_text), Paragraph("Systemic organizational asset mapping, threat-vulnerability evaluation matrices.", table_cell_text), Paragraph("Bi-Annual", table_cell_text)],
    ]
    c_table = Table(comp_data, colWidths=[35*mm, usable_width - 70*mm, 35*mm])
    c_table.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,0), LIGHT_BG), ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR), ('PADDING', (0,0), (-1,-1), 10)]))
    story.append(c_table)
    story.append(PageBreak())

    # ---------------- PAGE 6: TECHNICAL STACK ----------------
    story.append(Paragraph("Section 5: Technical Stack Architecture &amp; Scalability", h1_style))
    tech_data = [
        [Paragraph("<b>Layer</b>", table_cell_bold), Paragraph("<b>Technology Stack Components</b>", table_cell_bold)],
        [Paragraph("Presentation", table_cell_text), Paragraph("Next.js 15, WebAssembly Engine, Tailwind CSS Compiler Core", table_cell_text)],
        [Paragraph("Application Logic", table_cell_text), Paragraph("Go (Golang 1.26), Rust System Callbacks, Python AI Pipelines", table_cell_text)],
        [Paragraph("Persistence", table_cell_text), Paragraph("Distributed PostgreSQL clusters, Redis Enterprise Cache, Apache Kafka", table_cell_text)],
    ]
    t_style_table = Table(tech_data, colWidths=[45*mm, usable_width - 45*mm])
    t_style_table.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,0), SECONDARY), ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR), ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LIGHT_BG]), ('PADDING', (0,0), (-1,-1), 10)]))
    for i in range(2): tech_data[0][i].style.textColor = colors.white
    story.append(t_style_table)
    story.append(PageBreak())

    # ---------------- PAGE 7: RISK MATRIX ASSESSMENT ----------------
    story.append(Paragraph("Section 6: Risk Matrix Assessment &amp; Contingency Maps", h1_style))
    risk_data = [
        [Paragraph("<b>Identified Threat Vector</b>", table_cell_bold), Paragraph("<b>Severity</b>", table_cell_bold), Paragraph("<b>Mitigation Vector Protocols</b>", table_cell_bold)],
        [Paragraph("Dependency Disruption", table_cell_text), Paragraph("Medium", table_cell_text), Paragraph("Maintain isolated fallback dependency mirrors.", table_cell_text)],
        [Paragraph("Regional Grid Offline Fault", table_cell_text), Paragraph("Critical", table_cell_text), Paragraph("Multi-cloud hot-standby infrastructure replication.", table_cell_text)],
    ]
    r_table = Table(risk_data, colWidths=[50*mm, 25*mm, usable_width - 75*mm])
    r_table.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,0), LIGHT_BG), ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR), ('PADDING', (0,0), (-1,-1), 10)]))
    story.append(r_table)
    story.append(PageBreak())

    # ---------------- PAGE 8: HUMAN RESOURCE OPTIMIZATION ----------------
    story.append(Paragraph("Section 7: Human Resource Optimization &amp; Capital Retention", h1_style))
    story.append(Paragraph("To sustain operational output, workforce models prioritize asynchronous communication.", body_style))
    story.append(Paragraph("• <b>Continuous Technical Upskilling:</b> Standardized corporate educational stipends.", bullet_style))
    story.append(Paragraph("• <b>Distributed Autonomy Framework:</b> Core working blocks normalized over 4 timezones.", bullet_style))
    story.append(PageBreak())

    # ---------------- PAGE 9: MARKETING BENCHMARKS ----------------
    story.append(Paragraph("Section 8: Marketing Benchmarks &amp; Acquisition Funnels", h1_style))
    mkt_data = [
        [Paragraph("<b>Channel Group</b>", table_cell_bold), Paragraph("<b>Conversion %</b>", table_cell_bold), Paragraph("<b>LTV:CAC Ratio</b>", table_cell_bold)],
        [Paragraph("Organic Inbound", table_cell_text), Paragraph("4.8%", table_cell_text), Paragraph("6.2 : 1", table_cell_text)],
        [Paragraph("Developer Evangelism", table_cell_text), Paragraph("3.1%", table_cell_text), Paragraph("4.8 : 1", table_cell_text)],
    ]
    m_table = Table(mkt_data, colWidths=[60*mm, 40*mm, usable_width - 100*mm])
    m_table.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,0), PRIMARY), ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR), ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LIGHT_BG]), ('PADDING', (0,0), (-1,-1), 10)]))
    for i in range(3): mkt_data[0][i].style.textColor = colors.white
    story.append(m_table)
    story.append(PageBreak())

    # ---------------- PAGE 10: APPENDIX HISTORICAL DATA ----------------
    story.append(Paragraph("Section 9: Appendix: Historical Data Ledger (2020-2026)", h1_style))
    app_data = [
        [Paragraph("<b>Fiscal Year</b>", table_cell_bold), Paragraph("<b>Processed Requests (Trillion)</b>", table_cell_bold), Paragraph("<b>System Uptime %</b>", table_cell_bold)],
        [Paragraph("FY 2023", table_cell_text), Paragraph("19.1 Tx", table_cell_text), Paragraph("99.98%", table_cell_text)],
        [Paragraph("FY 2024", table_cell_text), Paragraph("44.0 Tx", table_cell_text), Paragraph("99.99%", table_cell_text)],
        [Paragraph("FY 2025", table_cell_text), Paragraph("102.5 Tx", table_cell_text), Paragraph("99.995%", table_cell_text)],
        [Paragraph("FY 2026 (YTD)", table_cell_text), Paragraph("158.2 Tx", table_cell_text), Paragraph("99.999%", table_cell_text)],
    ]
    a_table = Table(app_data, colWidths=[40*mm, 60*mm, usable_width - 100*mm])
    a_table.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,0), LIGHT_BG), ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR), ('PADDING', (0,0), (-1,-1), 8)]))
    story.append(a_table)
    
    doc.build(story, canvasmaker=NumberedCanvas)

if __name__ == "__main__":
    create_multi_page_pdf("Mayflower_Systems_Operational_Document.pdf")