#!/usr/bin/env python3
"""
Hermes Architect Audit -- Core PDF Generation Engine
=====================================================
Version: 5.1 (Environment-Agnostic)
License: MIT

Description:
    Generates landscape A4 PDF audit reports for multi-agent LLM routing.
    Pure Python FPDF2 -- no external chart dependencies.
    Stable vertical-block card layout with zero truncation.
    Fully environment-agnostic: works on Linux, Mac, and Windows.

Author: Hgteo (VEGO64)
Repository: https://github.com/VEGO64/Hermes-Architect-Audit
"""

from fpdf import FPDF
from datetime import datetime
import os, sys, json

DATE = datetime.now().strftime("%Y-%m-%d")

# ─── Output Directory (relative, auto-created) ───────────────────────────────
OUT = "./output"
os.makedirs(OUT, exist_ok=True)

# ─── Font Setup (cross-platform fallback) ────────────────────────────────────
FONT_DIR = "/usr/share/fonts/truetype/dejavu"
if os.path.isdir(FONT_DIR):
    FPDF_FONT_DIR = FONT_DIR
else:
    # Disable FPDF built-in font directory -- use default Arial/Helvetica
    FPDF_FONT_DIR = None

# ─── Layout Constants ────────────────────────────────────────────────────────
LM = 8        # Left/Right margin mm
RM = 8
TM = 8        # Top margin
HDR_H = 14    # Header bar height
FTR_H = 8     # Footer bar height
USABLE_H = 277 - LM - RM
INNER_W = 277 - LM - RM

# Card accent bar
ACCENT_W = 1.2  # mm

# Color palette
C = {
    'RED':    (180, 40, 40),
    'GREEN':  (30, 130, 60),
    'BLUE':   (40, 80, 180),
    'BLACK':  (0, 0, 0),
    'GREY':   (100, 100, 100),
    'WHITE':  (255, 255, 255),
    'LTGREY': (245, 245, 245),
    'DKGREY': (40, 40, 40),
}


class P(FPDF):
    def header(self):
        self.set_fill_color(*C['DKGREY'])
        self.rect(0, 0, 297, HDR_H, 'F')
        self.set_font('Helvetica', 'B', 13)
        self.set_text_color(*C['WHITE'])
        self.set_xy(0, 3)
        self.cell(277, 7, 'MODEL COST INTELLIGENCE', align='C')
        self.set_xy(0, 10)
        self.set_font('Helvetica', '', 7)
        self.cell(277, 4, f'Architect Audit v5 | {DATE} | Full Analysis', align='C')
        self.set_text_color(*C['BLACK'])

    def footer(self):
        h = self.page_h
        self.set_fill_color(*C['DKGREY'])
        self.rect(0, h - FTR_H, 297, FTR_H, 'F')
        self.set_font('Helvetica', '', 7)
        self.set_text_color(*C['WHITE'])
        self.set_xy(0, h - FTR_H + 2.5)
        txt = f'Model Cost Intelligence -- Audit v5 -- Page {self.page_no()}'
        self.cell(INNER_W, 4, txt, align='C')
        self.set_text_color(*C['BLACK'])


def section_title(pdf, text):
    pdf.ln(3)
    pdf.set_x(LM)
    pdf.set_font('Helvetica', 'B', 10)
    pdf.set_fill_color(*C['LTGREY'])
    pdf.cell(INNER_W, 6, text.upper(), fill=True)
    pdf.ln(7)


def kv(pdf, label, value, indent=0):
    pdf.set_x(LM + indent)
    pdf.set_font('Helvetica', 'B', 7.5)
    pdf.cell(22, 4, label, ln=0)
    pdf.set_font('Helvetica', '', 7.5)
    pdf.cell(0, 4, value)


def draw_card(pdf, card_h, content_y_start):
    """Draw accent bar and thin border around a task card."""
    pdf.set_draw_color(*C['GREY'])
    # Left accent bar
    pdf.set_fill_color(*C['BLUE'])
    pdf.rect(LM, content_y_start, ACCENT_W, card_h, 'F')
    # Card border
    pdf.rect(LM + ACCENT_W, content_y_start,
             INNER_W - ACCENT_W, card_h, 'D')


def task_card(pdf, t):
    # Estimate how many lines we need, then add 5 extra for safety margin
    current_len = max(len(t.get('current', '')), 30)
    opt_a_len = max(len(t.get('opt_a_name', '')), 30)
    opt_b_len = max(len(t.get('opt_b_name', '')), 30)
    rat_len = len(t.get('rationale', ''))
    est_lines = 17 + (rat_len // 55) + 2
    row_h = max(4.5, est_lines * 4.0)

    card_h = row_h + 10

    y = pdf.get_y()
    avail = 190 - y

    if avail < card_h + 8:
        pdf.add_page()
        y = pdf.get_y()

    start_y = y

    pdf.set_x(LM)
    pdf.set_font('Helvetica', 'B', 9)
    pdf.set_text_color(*C['RED'])
    pdf.cell(INNER_W, 5, f"TASK: {t['name'].upper()}", ln=1)

    pdf.set_x(LM)
    pdf.set_font('Helvetica', '', 7.5)
    pdf.set_text_color(*C['GREY'])
    cur_model = t.get('current', '')
    cur_in = t.get('cur_in', 'N/A')
    cur_out = t.get('cur_out', 'N/A')
    pdf.cell(0, 4, f"CURRENT: {cur_model}  |  In {cur_in} / 1M  |  Out {cur_out} / 1M", ln=1)

    pdf.ln(1.5)
    pdf.set_x(LM)
    pdf.set_font('Helvetica', 'B', 8)
    pdf.set_text_color(*C['GREEN'])
    pdf.cell(0, 4, f"OPTION A (Efficiency Leader): {t['opt_a_name']}", ln=1)
    pdf.set_x(LM)
    pdf.set_font('Helvetica', '', 7.5)
    pdf.set_text_color(*C['BLACK'])
    pdf.cell(0, 4, f"   In ${t.get('a_in','?')}/1M  |  Out ${t.get('a_out','?')}/1M  |  Context {t.get('a_ctx','?')}", ln=1)

    pdf.ln(1.5)
    pdf.set_x(LM)
    pdf.set_font('Helvetica', 'B', 8)
    pdf.set_text_color(*C['BLUE'])
    pdf.cell(0, 4, f"OPTION B (Performance Leader): {t['opt_b_name']}", ln=1)
    pdf.set_x(LM)
    pdf.set_font('Helvetica', '', 7.5)
    pdf.set_text_color(*C['BLACK'])
    pdf.cell(0, 4, f"   In ${t.get('b_in','?')}/1M  |  Out ${t.get('b_out','?')}/1M  |  Context {t.get('b_ctx','?')}", ln=1)

    pdf.ln(2)

    rec = t.get('rec_label', 'N/A')
    pdf.set_x(LM)
    pdf.set_font('Helvetica', 'B', 8)
    pdf.set_text_color(*C['BLACK'])
    pdf.cell(0, 4, f"FINAL RECOMMENDATION: {rec}", ln=1)

    pdf.set_x(LM)
    pdf.set_font('Helvetica', '', 7)
    pdf.set_text_color(*C['BLACK'])
    rat = t.get('rationale', '')
    pdf.multi_cell(INNER_W, 3.8, f"DEEP RATIONALE: {rat}")

    end_y = pdf.get_y()
    actual_h = end_y - start_y + 3

    draw_card(pdf, actual_h, start_y)

    pdf.set_y(end_y + 4)
    pdf.set_text_color(*C['BLACK'])


def build(d):
    pdf = P()
    pdf.set_margins(LM, TM, RM)
    pdf.set_auto_page_break(True, 15)
    pdf.add_page()

    # Page 1: User Behavior Profile
    section_title(pdf, 'User Behavior Profile')
    pdf.set_x(LM)
    pdf.set_font('Helvetica', '', 9)
    pdf.set_text_color(*C['BLACK'])
    profile_text = d.get('profile', 'High-intensity AI engineering workload.')
    pdf.multi_cell(INNER_W, 5, profile_text)
    pdf.ln(2)

    profile_detail = d.get('profile_detail', '')
    if profile_detail:
        pdf.set_x(LM)
        pdf.set_font('Helvetica', '', 8)
        pdf.multi_cell(INNER_W, 4.5, profile_detail)
        pdf.ln(3)

    section_title(pdf, 'Executive Summary & Strategic Roadmap')
    tasks = d.get('tasks', [])
    switch_count = sum(1 for t in tasks if 'KEEP' not in t.get('rec_label', '').upper())
    keep_count = len(tasks) - switch_count
    pdf.set_x(LM)
    pdf.set_font('Helvetica', '', 8.5)
    pdf.multi_cell(INNER_W, 5, f"Total Tasks: {len(tasks)} | SWITCH: {switch_count} | KEEP: {keep_count}")
    pdf.ln(4)

    # Page 2+: Task cards
    for t in tasks:
        task_card(pdf, t)
        pdf.ln(2)

    return pdf


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 generate_audit_pdf.py '<json_payload>'")
        sys.exit(1)

    try:
        data = json.loads(sys.argv[1])
    except json.JSONDecodeError as e:
        print(f"JSON parse error: {e}")
        sys.exit(1)

    pdf = build(data)
    out_path = os.path.join(OUT, f'Model_Cost_Intelligence_{DATE}_v5.pdf')
    pdf.output(out_path)
    print(f"PDF_PATH:{out_path}")