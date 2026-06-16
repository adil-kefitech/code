from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.lib.colors import HexColor

# --- Color constants matching the letterhead ---
TEAL = HexColor('#1A7A8A')       # Header teal/blue
DARK_TEAL = HexColor('#145F6E')
BLACK = colors.black
LIGHT_GRAY = HexColor('#F5F5F5')
MED_GRAY = HexColor('#CCCCCC')

PAGE_W, PAGE_H = A4
MARGIN_L = 20 * mm
MARGIN_R = 20 * mm
MARGIN_T = 18 * mm
MARGIN_B = 20 * mm
USABLE_W = PAGE_W - MARGIN_L - MARGIN_R

# OUTPUT = "/mnt/user-data/outputs/MayFlower_Invoice_MFWH_30052026_001.pdf"
OUTPUT = "MayFlower_Invoice.pdf"

def draw_invoice(c, doc=None):
    y = PAGE_H - MARGIN_T  # start from top

    # ── HEADER ──────────────────────────────────────────────────
    # Hostel name
    c.setFont("Helvetica-Bold", 20)
    c.setFillColor(TEAL)
    hostel_name = "MAY FLOWER WOMEN'S HOSTEL"
    name_w = c.stringWidth(hostel_name, "Helvetica-Bold", 20)
    c.drawString((PAGE_W - name_w) / 2, y, hostel_name)
    y -= 7 * mm

    # Address
    c.setFont("Helvetica", 9.5)
    addr1 = "Charachira Road, Plamoodu, Kowdiar P.O."
    addr1_w = c.stringWidth(addr1, "Helvetica", 9.5)
    c.drawString((PAGE_W - addr1_w) / 2, y, addr1)
    y -= 5.5 * mm

    addr2 = "Mob. 8848877399, 6282485282"
    addr2_w = c.stringWidth(addr2, "Helvetica", 9.5)
    c.drawString((PAGE_W - addr2_w) / 2, y, addr2)
    y -= 6 * mm

    # Double separator line
    c.setStrokeColor(TEAL)
    c.setLineWidth(1.8)
    c.line(MARGIN_L, y, PAGE_W - MARGIN_R, y)
    y -= 1.5 * mm
    c.setLineWidth(0.6)
    c.line(MARGIN_L, y, PAGE_W - MARGIN_R, y)
    y -= 8 * mm

    # ── DATE (right-aligned) ─────────────────────────────────────
    c.setFillColor(BLACK)
    c.setFont("Helvetica", 10)
    date_text = "Date: 30/05/2026"
    date_w = c.stringWidth(date_text, "Helvetica", 10)
    c.drawString(PAGE_W - MARGIN_R - date_w, y, date_text)
    y -= 10 * mm

    # ── SALUTATION ───────────────────────────────────────────────
    c.setFont("Helvetica-Bold", 10.5)
    c.drawString(MARGIN_L, y, "To Whom It May Concern,")
    y -= 9 * mm

    # ── BODY PARAGRAPH ──────────────────────────────────────────
    body = (
        "I, Mizna Siraj, the proprietor of May Flower Women's Hostel, hereby certify that the "
        "individual, Niji K A, residing at Kolladiparambil House, has been a resident of this "
        "hostel from 5th March 2026 to 05/05/2026. The total amount received for this stay is "
        "Rupees 10,770 (Ten thousand seven hundred and seventy only)."
    )
    c.setFont("Helvetica", 10)
    # Word-wrap manually
    from reportlab.lib.utils import simpleSplit
    lines = simpleSplit(body, "Helvetica", 10, USABLE_W)
    line_h = 5.5 * mm
    for line in lines:
        c.drawString(MARGIN_L, y, line)
        y -= line_h
    y -= 8 * mm

    # ── INVOICE BOX ─────────────────────────────────────────────
    box_x = MARGIN_L
    box_w = USABLE_W

    # Title bar
    c.setFillColor(TEAL)
    c.setStrokeColor(TEAL)
    c.roundRect(box_x, y - 8*mm, box_w, 8*mm, 2*mm, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 11)
    title_txt = "PAYMENT RECEIPT / INVOICE"
    title_w = c.stringWidth(title_txt, "Helvetica-Bold", 11)
    c.drawString((PAGE_W - title_w) / 2, y - 5.5*mm, title_txt)
    y -= 10 * mm

    # Invoice details table
    inv_data = [
        ["Invoice No.", "MFWH/30052026/001"],
        ["Guest Name",  "Niji K A"],
        ["Address",     "Kolladiparambil House"],
        ["Stay Period",  "05/03/2026  –  05/05/2026"],
        ["Amount",       "Rs. 10,770  (Ten thousand seven hundred and seventy only)"],
        ["Mode of Payment", "UPI"],
        ["Received By",   "May Flower Women's Hostel"],
    ]

    col_w = [60*mm, USABLE_W - 60*mm]
    row_h = 8.5 * mm
    c.setStrokeColor(MED_GRAY)
    c.setLineWidth(0.5)

    for i, (label, value) in enumerate(inv_data):
        row_y = y - row_h
        bg = LIGHT_GRAY if i % 2 == 0 else colors.white
        c.setFillColor(bg)
        c.rect(box_x, row_y, col_w[0], row_h, fill=1, stroke=0)
        c.rect(box_x + col_w[0], row_y, col_w[1], row_h, fill=1, stroke=0)

        # grid lines
        c.setStrokeColor(MED_GRAY)
        c.setFillColor(BLACK)
        c.rect(box_x, row_y, box_w, row_h, fill=0, stroke=1)
        c.line(box_x + col_w[0], row_y, box_x + col_w[0], row_y + row_h)

        c.setFont("Helvetica-Bold", 9.5)
        c.setFillColor(DARK_TEAL)
        c.drawString(box_x + 3*mm, row_y + 2.8*mm, label)

        c.setFont("Helvetica", 9.5)
        c.setFillColor(BLACK)
        c.drawString(box_x + col_w[0] + 3*mm, row_y + 2.8*mm, value)

        y -= row_h

    y -= 10 * mm

    # ── SEAL & SIGNATURE ─────────────────────────────────────────
    # Two columns: left = "Seal & Signature", right = "Sincerely / Proprietor"
    left_x  = MARGIN_L
    right_x = PAGE_W - MARGIN_R - 65*mm
    sig_y   = y

    # Left box
    c.setStrokeColor(MED_GRAY)
    c.setFillColor(colors.white)
    c.setLineWidth(0.5)
    c.rect(left_x, sig_y - 22*mm, 70*mm, 22*mm, fill=0, stroke=1)
    c.setFont("Helvetica-Bold", 9)
    c.setFillColor(TEAL)
    c.drawString(left_x + 2*mm, sig_y - 6*mm, "Seal & Signature")
    c.setFont("Helvetica", 8.5)
    c.setFillColor(colors.gray)
    c.drawString(left_x + 2*mm, sig_y - 19*mm, "(Office Seal)")

    # Right block
    c.setFont("Helvetica", 10)
    c.setFillColor(BLACK)
    c.drawString(right_x, sig_y - 3*mm, "Sincerely,")
    c.setFont("Helvetica-Bold", 10)
    c.drawString(right_x, sig_y - 9*mm, "Mizna Siraj")
    # Signature underline
    c.setStrokeColor(BLACK)
    c.setLineWidth(0.5)
    c.line(right_x, sig_y - 15*mm, right_x + 55*mm, sig_y - 15*mm)
    c.setFont("Helvetica-Bold", 9)
    c.setFillColor(TEAL)
    c.drawString(right_x, sig_y - 19*mm, "MAY FLOWER WOMEN'S HOSTEL")
    c.setFont("Helvetica-Bold", 9)
    c.setFillColor(BLACK)
    c.drawString(right_x, sig_y - 24*mm, "Proprietor")

    # ── FOOTER LINE ──────────────────────────────────────────────
    footer_y = MARGIN_B + 8*mm
    c.setStrokeColor(TEAL)
    c.setLineWidth(0.8)
    c.line(MARGIN_L, footer_y, PAGE_W - MARGIN_R, footer_y)
    c.setFont("Helvetica", 7.5)
    c.setFillColor(colors.gray)
    footer_txt = "May Flower Women's Hostel  |  Charachira Road, Plamoodu, Kowdiar P.O.  |  Mob: 8848877399, 6282485282"
    ft_w = c.stringWidth(footer_txt, "Helvetica", 7.5)
    c.drawString((PAGE_W - ft_w) / 2, footer_y - 4*mm, footer_txt)


# ── MAIN ─────────────────────────────────────────────────────────
c = canvas.Canvas(OUTPUT, pagesize=A4)
draw_invoice(c)
c.save()
print(f"PDF saved to: {OUTPUT}")

