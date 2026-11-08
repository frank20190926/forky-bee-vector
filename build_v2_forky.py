#!/usr/bin/env python3
"""
Builds the V2 2-Board Master Vector Presentation for Contest #2800908:
Vectorización Profesional Logo FORKY BEE ($191.00 USD Guaranteed).
"""
import os, re

PROJ_DIR = "/Users/frank/Work/13_money/02_开发/forky-bee-vector"
EXPORT_DIR = os.path.join(PROJ_DIR, "exports")

with open(os.path.join(EXPORT_DIR, "01_FORKY_BEE_Principal_Vertical.svg"), "r", encoding="utf-8") as f:
    svg_txt = f.read()

d_amarillo = re.search(r'id="Amarillo_FFC300"\s+d="([^"]+)"', svg_txt).group(1)
d_blanco = re.search(r'id="Blanco_FFFFFF"\s+d="([^"]+)"', svg_txt).group(1)
d_carbon = re.search(r'id="Carbon_1F1F1F"\s+d="([^"]+)"', svg_txt).group(1)

# Split d_amarillo into abdomen stripes (first 2 subpaths) and outer hexagon arms (remaining subpaths)
am_parts = [p.strip() + " Z" for p in d_amarillo.split("Z") if p.strip()]
d_am_abdomen = " ".join(am_parts[:2])
d_am_hex = " ".join(am_parts[2:])

with open("/tmp/forky_illustrator_outline_snippet.svg", "r", encoding="utf-8") as f:
    outline_snippet = f.read()

def make_isotipo_svg(mode="color", size=180):
    if mode == "color":
        return f'''<svg viewBox="10 5 280 265" width="{size}" height="{size}" style="overflow:visible">
          <path d="{d_amarillo}" fill="#FFC300" fill-rule="evenodd"/>
          <path d="{d_blanco}" fill="#FFFFFF" fill-rule="evenodd"/>
          <path d="{d_carbon}" fill="#1F1F1F" fill-rule="evenodd"/>
        </svg>'''
    elif mode == "dark":
        return f'''<svg viewBox="10 5 280 265" width="{size}" height="{size}" style="overflow:visible">
          <path d="{d_amarillo}" fill="#FFC300" fill-rule="evenodd"/>
          <path d="{d_blanco}" fill="#FFFFFF" fill-rule="evenodd"/>
          <path d="{d_carbon}" fill="#1F1F1F" stroke="#FFFFFF" stroke-width="2.2" fill-rule="evenodd"/>
        </svg>'''
    elif mode == "mono_black":
        return f'''<svg viewBox="10 5 280 265" width="{size}" height="{size}" style="overflow:visible">
          <path d="{d_am_hex}" fill="#1F1F1F" fill-rule="evenodd"/>
          <path d="{d_am_abdomen}" fill="#FFFFFF" fill-rule="evenodd"/>
          <path d="{d_blanco}" fill="#FFFFFF" fill-rule="evenodd"/>
          <path d="{d_carbon}" fill="#1F1F1F" fill-rule="evenodd"/>
        </svg>'''
    elif mode == "mono_white":
        return f'''<svg viewBox="10 5 280 265" width="{size}" height="{size}" style="overflow:visible">
          <path d="{d_am_hex}" fill="#FFFFFF" fill-rule="evenodd"/>
          <path d="{d_am_abdomen}" fill="#1F1F1F" fill-rule="evenodd"/>
          <path d="{d_blanco}" fill="#1F1F1F" fill-rule="evenodd"/>
          <path d="{d_carbon}" fill="#FFFFFF" fill-rule="evenodd"/>
        </svg>'''
    elif mode == "outline":
        return f'''<svg viewBox="10 5 280 265" width="{size}" height="{size}" style="overflow:visible">
          {outline_snippet}
        </svg>'''

HTML = f'''<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=1600, initial-scale=1.0" />
  <title>FORKY BEE® — Reconstrucción Vectorial Manual &amp; Manual de Producción</title>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@500;600&family=Montserrat:ital,wght@0,500;0,600;0,700;0,800;1,600;1,700;1,800;1,900&display=swap" rel="stylesheet" />
  <style>
    :root {{
      --yellow: #FFC300;
      --carbon: #1F1F1F;
      --arena: #F5F5F5;
      --white: #FFFFFF;
      --ai-blue: #1A66FF;
      --sans: 'Inter', -apple-system, sans-serif;
      --brand: 'Montserrat', sans-serif;
      --mono: 'JetBrains Mono', monospace;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      background: #141414;
      font-family: var(--sans);
      color: var(--carbon);
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 44px;
      padding: 28px 0 60px;
      -webkit-font-smoothing: antialiased;
    }}

    .board {{
      width: 1600px;
      height: 1000px;
      background: var(--arena);
      position: relative;
      overflow: hidden;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      box-shadow: 0 28px 70px rgba(0,0,0,0.5);
    }}

    /* Top Header Bar */
    .top-bar {{
      height: 56px;
      background: var(--carbon);
      color: var(--white);
      padding: 0 40px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      border-bottom: 3px solid var(--yellow);
      flex-shrink: 0;
    }}
    .top-bar-left {{
      display: flex;
      align-items: center;
      gap: 14px;
    }}
    .badge-yellow {{
      background: var(--yellow);
      color: var(--carbon);
      font-family: var(--brand);
      font-weight: 800;
      font-size: 11px;
      letter-spacing: 0.12em;
      padding: 4px 10px;
      border-radius: 3px;
      text-transform: uppercase;
    }}
    .top-bar-title {{
      font-family: var(--brand);
      font-weight: 700;
      font-size: 14px;
      letter-spacing: 0.04em;
    }}
    .top-bar-right {{
      font-family: var(--mono);
      font-size: 11px;
      color: rgba(255,255,255,0.78);
      letter-spacing: 0.06em;
    }}

    /* Bottom Footer Bar */
    .foot-bar {{
      height: 40px;
      background: var(--carbon);
      color: rgba(255,255,255,0.82);
      padding: 0 40px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      font-size: 10.5px;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      flex-shrink: 0;
    }}
    .foot-bar strong {{ color: var(--yellow); }}

    /* =========================================================================
       BOARD 01: CAD BLUEPRINT, ILLUSTRATOR OUTLINE (CTRL+Y) & 6 VARIATIONS
       ========================================================================= */
    .b1-main {{
      flex: 1;
      min-height: 0;
      padding: 20px 40px;
      display: grid;
      grid-template-rows: 270px 1fr 142px;
      gap: 18px;
    }}

    /* Row 1: Giant CAD Blueprint Hero */
    .cad-hero {{
      background: var(--white);
      border: 1.5px solid #DCDCDC;
      border-radius: 10px;
      position: relative;
      overflow: hidden;
      display: grid;
      grid-template-columns: 1.38fr 0.62fr;
      box-shadow: 0 8px 24px rgba(0,0,0,0.04);
    }}
    .cad-grid-area {{
      position: relative;
      padding: 18px 28px;
      display: flex;
      align-items: center;
      justify-content: center;
      background-image:
        linear-gradient(to right, rgba(26,102,255,0.07) 1px, transparent 1px),
        linear-gradient(to bottom, rgba(26,102,255,0.07) 1px, transparent 1px);
      background-size: 24px 24px;
      border-right: 1.5px dashed rgba(26,102,255,0.28);
    }}
    /* Construction guide lines */
    .guide-h, .guide-v {{
      position: absolute;
      pointer-events: none;
    }}
    .guide-h {{
      left: 20px; right: 20px;
      border-top: 1px dashed rgba(26,102,255,0.45);
    }}
    .guide-v {{
      top: 16px; bottom: 16px;
      border-left: 1px dashed rgba(26,102,255,0.45);
    }}
    .cad-tag {{
      position: absolute;
      top: 10px;
      left: 14px;
      background: rgba(26,102,255,0.1);
      border: 1px solid rgba(26,102,255,0.35);
      color: var(--ai-blue);
      font-family: var(--mono);
      font-size: 9.5px;
      font-weight: 600;
      padding: 3px 8px;
      border-radius: 4px;
    }}
    .cad-dim-pill {{
      position: absolute;
      bottom: 10px;
      right: 14px;
      background: #F0F5FF;
      border: 1px solid rgba(26,102,255,0.35);
      color: var(--ai-blue);
      font-family: var(--mono);
      font-size: 9.5px;
      padding: 3px 8px;
      border-radius: 4px;
    }}

    /* Reconstructed Vector Wordmark Component */
    .vector-lockup-h {{
      display: flex;
      align-items: center;
      gap: 22px;
      position: relative;
      z-index: 2;
    }}
    .wordmark-block {{
      display: flex;
      flex-direction: column;
      align-items: center;
    }}
    .wm-title {{
      font-family: var(--brand);
      font-weight: 900;
      font-style: italic;
      font-size: 68px;
      line-height: 0.96;
      letter-spacing: -0.025em;
      -webkit-text-stroke: 1.2px currentColor;
      color: var(--carbon);
      display: flex;
      align-items: flex-start;
    }}
    .wm-title .bee {{
      color: var(--yellow);
      margin-left: 10px;
    }}
    .wm-title .reg {{
      font-size: 22px;
      font-style: normal;
      font-weight: 700;
      color: var(--carbon);
      margin-left: 4px;
      margin-top: 2px;
    }}
    .wm-sub-row {{
      display: flex;
      align-items: center;
      gap: 14px;
      margin-top: 8px;
      width: 100%;
      justify-content: center;
    }}
    .wm-pill-line {{
      height: 5px;
      width: 58px;
      background: var(--yellow);
      border-radius: 99px;
    }}
    .wm-sub-text {{
      font-family: var(--brand);
      font-weight: 700;
      font-style: italic;
      font-size: 18px;
      letter-spacing: 0.34em;
      color: var(--carbon);
      margin-right: -0.34em;
    }}

    /* Right side of CAD Hero: Side-by-side Outline Ctrl+Y vs Solid */
    .outline-compare-box {{
      padding: 14px 20px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      background: #FAFBFE;
    }}
    .oc-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 10px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.1em;
      color: var(--ai-blue);
      border-bottom: 1px solid #E2E8F0;
      padding-bottom: 6px;
    }}
    .oc-pair {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 12px;
      align-items: center;
      flex: 1;
      min-height: 0;
      padding: 6px 0;
    }}
    .oc-card {{
      background: var(--white);
      border: 1px solid #DCE4F2;
      border-radius: 8px;
      height: 100%;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      padding: 8px;
      position: relative;
    }}
    .oc-card span {{
      font-family: var(--mono);
      font-size: 8.5px;
      color: #475569;
      margin-top: 4px;
      text-transform: uppercase;
    }}
    .oc-foot {{
      display: flex;
      justify-content: space-between;
      font-size: 9.5px;
      color: #334155;
      font-weight: 600;
      background: #EFF6FF;
      border: 1px solid #BFDBFE;
      padding: 5px 10px;
      border-radius: 5px;
    }}

    /* Row 2: 6 Official Vector Variations Grid */
    .vars-grid {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      grid-template-rows: repeat(2, 1fr);
      gap: 14px;
      min-height: 0;
    }}
    .var-card {{
      background: var(--white);
      border: 1.5px solid #E0E0E0;
      border-radius: 9px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      overflow: hidden;
      min-height: 0;
    }}
    .var-card.dark-bg {{
      background: var(--carbon);
      border-color: #333333;
      color: var(--white);
    }}
    .var-card.arena-bg {{
      background: var(--arena);
    }}
    .var-top {{
      padding: 8px 14px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 1px solid rgba(0,0,0,0.07);
      font-size: 10px;
      font-weight: 700;
      letter-spacing: 0.06em;
      text-transform: uppercase;
    }}
    .var-card.dark-bg .var-top {{
      border-bottom-color: rgba(255,255,255,0.1);
    }}
    .var-pill {{
      font-family: var(--mono);
      font-size: 8.5px;
      padding: 2px 7px;
      border-radius: 3px;
      background: var(--carbon);
      color: var(--yellow);
    }}
    .var-card.dark-bg .var-pill {{
      background: var(--yellow);
      color: var(--carbon);
    }}
    .var-stage {{
      flex: 1;
      min-height: 0;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 10px 18px;
    }}
    .var-foot {{
      padding: 6px 14px;
      background: rgba(0,0,0,0.03);
      border-top: 1px solid rgba(0,0,0,0.06);
      display: flex;
      justify-content: space-between;
      font-size: 9.5px;
      color: #555;
    }}
    .var-card.dark-bg .var-foot {{
      background: rgba(255,255,255,0.04);
      border-top-color: rgba(255,255,255,0.08);
      color: #AAA;
    }}

    /* Mini Lockups inside Variation Cards */
    .mini-v-lockup {{
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 2px;
    }}
    .mini-v-lockup .t {{
      font-family: var(--brand);
      font-weight: 900;
      font-style: italic;
      font-size: 24px;
      line-height: 1;
      color: var(--carbon);
      -webkit-text-stroke: 0.5px currentColor;
    }}
    .mini-v-lockup .t .b {{ color: var(--yellow); margin-left: 4px; }}
    .mini-v-lockup .s {{
      font-family: var(--brand);
      font-weight: 700;
      font-style: italic;
      font-size: 8px;
      letter-spacing: 0.32em;
      color: var(--carbon);
      display: flex;
      align-items: center;
      gap: 8px;
    }}
    .mini-v-lockup .s::before, .mini-v-lockup .s::after {{
      content: "";
      width: 22px;
      height: 2.5px;
      background: var(--yellow);
      border-radius: 9px;
    }}
    .mini-v-lockup .sl {{
      font-family: var(--brand);
      font-weight: 600;
      font-style: italic;
      font-size: 8.5px;
      color: var(--carbon);
      margin-top: 1px;
    }}

    .mini-h-lockup {{
      display: flex;
      align-items: center;
      gap: 14px;
    }}
    .mini-h-lockup .t {{
      font-family: var(--brand);
      font-weight: 900;
      font-style: italic;
      font-size: 32px;
      line-height: 1;
      -webkit-text-stroke: 0.6px currentColor;
    }}
    .mini-h-lockup .s {{
      font-family: var(--brand);
      font-weight: 700;
      font-style: italic;
      font-size: 9.5px;
      letter-spacing: 0.3em;
      margin-top: 5px;
      display: flex;
      align-items: center;
      gap: 8px;
      justify-content: center;
    }}
    .mini-h-lockup .s i {{
      width: 26px;
      height: 3px;
      border-radius: 9px;
      display: inline-block;
    }}

    /* Row 3: Color Palette + Typography + File Formats Strip */
    .specs-row {{
      display: grid;
      grid-template-columns: 1.15fr 0.95fr 0.9fr;
      gap: 16px;
      min-height: 0;
    }}
    .spec-box {{
      background: var(--white);
      border: 1.5px solid #E0E0E0;
      border-radius: 9px;
      padding: 12px 16px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }}
    .spec-box-head {{
      font-size: 10px;
      font-weight: 800;
      letter-spacing: 0.1em;
      text-transform: uppercase;
      color: var(--carbon);
      display: flex;
      align-items: center;
      gap: 8px;
    }}
    .spec-box-head::before {{
      content: "";
      width: 4px;
      height: 12px;
      background: var(--yellow);
      display: inline-block;
    }}
    .swatches-4 {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 10px;
      margin-top: 6px;
    }}
    .sw-item {{
      display: flex;
      align-items: center;
      gap: 8px;
    }}
    .sw-circle {{
      width: 38px;
      height: 38px;
      border-radius: 8px;
      border: 1px solid rgba(0,0,0,0.15);
      flex-shrink: 0;
    }}
    .sw-txt strong {{
      display: block;
      font-size: 11px;
      color: var(--carbon);
    }}
    .sw-txt code {{
      display: block;
      font-family: var(--mono);
      font-size: 9.5px;
      color: #555;
    }}
    .sw-txt small {{
      display: block;
      font-size: 8.5px;
      color: #777;
    }}

    .typo-showcase {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      margin-top: 4px;
    }}
    .typo-left h4 {{
      font-family: var(--brand);
      font-weight: 800;
      font-style: italic;
      font-size: 22px;
      line-height: 1.05;
      color: var(--carbon);
    }}
    .typo-left p {{
      font-family: var(--brand);
      font-weight: 500;
      font-size: 12px;
      color: #444;
      margin-top: 3px;
    }}
    .typo-right {{
      font-size: 9.5px;
      line-height: 1.45;
      color: #555;
      border-left: 2px solid var(--yellow);
      padding-left: 10px;
    }}

    .formats-badges {{
      display: grid;
      grid-template-columns: repeat(5, 1fr);
      gap: 8px;
      margin-top: 6px;
    }}
    .fmt-chip {{
      background: var(--carbon);
      color: var(--white);
      border-radius: 6px;
      padding: 8px 4px;
      text-align: center;
      border-bottom: 3px solid var(--yellow);
    }}
    .fmt-chip strong {{
      display: block;
      font-family: var(--brand);
      font-weight: 800;
      font-size: 14px;
      color: var(--yellow);
    }}
    .fmt-chip span {{
      font-size: 8px;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      color: #CCC;
    }}

    /* =========================================================================
       BOARD 02: BRAND IDENTITY PRESENTATION, 3D MASCOT & 4 PRODUCTION MOCKUPS
       ========================================================================= */
    .b2-main {{
      flex: 1;
      min-height: 0;
      padding: 20px 40px;
      display: grid;
      grid-template-rows: 390px 128px 1fr;
      gap: 18px;
    }}

    .b2-hero-card {{
      border-radius: 12px;
      overflow: hidden;
      border: 1.5px solid #DCDCDC;
      background: var(--white);
      display: grid;
      grid-template-columns: 340px 1fr 340px;
      position: relative;
      box-shadow: 0 12px 32px rgba(0,0,0,0.06);
    }}
    .b2-mascot-col {{
      background: linear-gradient(135deg, var(--yellow) 0%, #FFB700 58%, var(--arena) 58.2%);
      position: relative;
      display: flex;
      align-items: flex-end;
      justify-content: center;
      overflow: hidden;
    }}
    .b2-mascot-col img {{
      height: 96%;
      width: auto;
      object-fit: contain;
      filter: drop-shadow(0 12px 24px rgba(0,0,0,0.2));
    }}
    .b2-center-col {{
      background: var(--arena);
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      padding: 20px;
      text-align: center;
    }}
    .b2-center-col .wm-title {{
      font-size: 62px;
      margin-top: 6px;
    }}
    .b2-slogan-brush {{
      margin-top: 12px;
      font-family: var(--brand);
      font-weight: 700;
      font-style: italic;
      font-size: 21px;
      color: var(--carbon);
      position: relative;
      display: inline-block;
    }}
    .b2-slogan-brush::after {{
      content: "";
      display: block;
      height: 5px;
      width: 85%;
      margin: 4px auto 0;
      background: var(--yellow);
      border-radius: 99px;
      transform: rotate(-1.2deg);
    }}
    .b2-services-col {{
      background: var(--carbon);
      color: var(--white);
      padding: 24px 28px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      border-left: 4px solid var(--yellow);
    }}
    .srv-item {{
      display: flex;
      align-items: center;
      gap: 16px;
      padding-bottom: 12px;
      border-bottom: 1px solid rgba(255,255,255,0.1);
    }}
    .srv-item:last-child {{
      border-bottom: none;
      padding-bottom: 0;
    }}
    .srv-icon {{
      width: 42px;
      height: 42px;
      border-radius: 8px;
      background: rgba(255,195,0,0.12);
      border: 1.5px solid var(--yellow);
      display: flex;
      align-items: center;
      justify-content: center;
      flex-shrink: 0;
      color: var(--yellow);
      font-weight: 800;
      font-size: 18px;
    }}
    .srv-item h4 {{
      font-family: var(--brand);
      font-size: 14.5px;
      font-weight: 700;
      line-height: 1.25;
      color: var(--white);
    }}

    /* Middle Strip on Board 02: 4 Quick Lockup Pills + Palette + Typography */
    .b2-mid-strip {{
      background: var(--white);
      border: 1.5px solid #E0E0E0;
      border-radius: 10px;
      padding: 12px 22px;
      display: grid;
      grid-template-columns: 1.45fr 0.85fr 0.7fr;
      gap: 22px;
      align-items: center;
    }}
    .b2-mini-vars {{
      display: grid;
      grid-template-columns: 1.25fr 1.25fr 0.65fr 0.85fr;
      gap: 10px;
      align-items: center;
    }}
    .b2-mv-box {{
      border: 1px solid #E5E5E5;
      border-radius: 7px;
      padding: 8px 10px;
      display: flex;
      align-items: center;
      justify-content: center;
      height: 82px;
    }}

    /* Bottom Row on Board 02: 4 Real-World Production Mockups */
    .mockups-4-grid {{
      display: grid;
      grid-template-columns: 1.35fr 0.85fr 0.85fr 1.15fr;
      gap: 16px;
      min-height: 0;
    }}
    .mockup-frame {{
      background: var(--white);
      border: 1.5px solid #DCDCDC;
      border-radius: 10px;
      overflow: hidden;
      display: flex;
      flex-direction: column;
      min-height: 0;
      box-shadow: 0 10px 24px rgba(0,0,0,0.06);
    }}
    .mockup-img-wrap {{
      flex: 1;
      min-height: 0;
      overflow: hidden;
      position: relative;
    }}
    .mockup-img-wrap img {{
      width: 100%;
      height: 100%;
      min-height: 0;
      object-fit: cover;
      display: block;
    }}
    .mockup-caption {{
      height: 36px;
      padding: 0 14px;
      background: var(--carbon);
      color: var(--white);
      display: flex;
      align-items: center;
      justify-content: space-between;
      font-size: 10px;
      font-weight: 700;
      letter-spacing: 0.06em;
      text-transform: uppercase;
      flex-shrink: 0;
    }}
    .mockup-caption span {{
      color: var(--yellow);
      font-family: var(--mono);
      font-size: 9px;
    }}
  </style>
</head>
<body>

  <!-- =======================================================================
       BOARD 01: CAD BLUEPRINT, ILLUSTRATOR OUTLINE (CTRL+Y) & 6 VARIATIONS
       ======================================================================= -->
  <section class="board" id="board-01">
    <header class="top-bar">
      <div class="top-bar-left">
        <span class="badge-yellow">Lámina 01 / 02 · Plano Técnico Vectorial</span>
        <span class="top-bar-title">FORKY BEE® · RECONSTRUCCIÓN VECTORIAL MANUAL (CURVAS BÉZIER PURAS) &amp; 6 VARIACIONES</span>
      </div>
      <div class="top-bar-right">
        100% TRAZADO MANUAL EN ADOBE ILLUSTRATOR · CERO AUTO-TRACE · ESCALABLE SIN LÍMITE
      </div>
    </header>

    <div class="b1-main">
      <!-- Row 1: CAD Construction Blueprint + Outline Mode (Ctrl+Y) -->
      <div class="cad-hero">
        <div class="cad-grid-area">
          <div class="guide-h" style="top: 32px;"></div>
          <div class="guide-h" style="bottom: 32px;"></div>
          <div class="guide-h" style="top: 50%;"></div>
          <div class="guide-v" style="left: 52px;"></div>
          <div class="guide-v" style="left: 245px;"></div>
          <div class="guide-v" style="right: 48px;"></div>

          <span class="cad-tag">CONSTRUCCIÓN GEOMÉTRICA MANUAL · ALINEACIÓN 12° ITALIC</span>
          <span class="cad-dim-pill">ESCALABILIDAD INFINITA: 16 PX FAVICON ↔ FLOTA VEHICULAR 6 METROS</span>

          <div class="vector-lockup-h">
            {make_isotipo_svg("color", 195)}
            <div class="wordmark-block">
              <div class="wm-title">
                <span>FORKY</span><span class="bee">BEE</span><span class="reg">®</span>
              </div>
              <div class="wm-sub-row">
                <span class="wm-pill-line"></span>
                <span class="wm-sub-text">FOOD SERVICE</span>
                <span class="wm-pill-line"></span>
              </div>
            </div>
          </div>
        </div>

        <div class="outline-compare-box">
          <div class="oc-header">
            <span>Auditoría de Trazos &amp; Modo Contorno (Ctrl+Y)</span>
            <span>Curvas Cúbicas Limpias</span>
          </div>
          <div class="oc-pair">
            <div class="oc-card">
              {make_isotipo_svg("outline", 136)}
              <span>Vista Contorno + Manejadores Bézier</span>
            </div>
            <div class="oc-card">
              {make_isotipo_svg("color", 136)}
              <span>Acabado Vectorial Sólido Plano</span>
            </div>
          </div>
          <div class="oc-foot">
            <span>✓ Curvas cerradas sin intersecciones</span>
            <span>✓ Listo para Plotter de Corte &amp; Serigrafía</span>
          </div>
        </div>
      </div>

      <!-- Row 2: 6 Official Vector Variations -->
      <div class="vars-grid">
        <!-- 01. Principal Vertical -->
        <div class="var-card arena-bg">
          <div class="var-top">
            <span>01 · Versión Principal Vertical (Apilada)</span>
            <span class="var-pill">AI · SVG · EPS · PDF</span>
          </div>
          <div class="var-stage">
            <div class="mini-v-lockup">
              {make_isotipo_svg("color", 84)}
              <div class="t"><span>FORKY</span><span class="b">BEE</span><sup style="font-size:10px;font-style:normal;">®</sup></div>
              <div class="s">FOOD SERVICE</div>
              <div class="sl">Abastecer. Así de simple.</div>
            </div>
          </div>
          <div class="var-foot">
            <span>Fondo Arena (#F5F5F5) · Uso Principal y Catálogos</span>
            <span>Trazos Convertidos + Editable</span>
          </div>
        </div>

        <!-- 02. Horizontal Claro -->
        <div class="var-card">
          <div class="var-top">
            <span>02 · Versión Horizontal Principal (Fondo Claro)</span>
            <span class="var-pill">AI · SVG · EPS · PNG 4K</span>
          </div>
          <div class="var-stage">
            <div class="mini-h-lockup">
              {make_isotipo_svg("color", 108)}
              <div>
                <div class="t" style="color:#1F1F1F;">FORKY<span style="color:#FFC300;margin-left:5px;">BEE</span><sup style="font-size:12px;font-style:normal;">®</sup></div>
                <div class="s" style="color:#1F1F1F;"><i style="background:#FFC300;"></i>FOOD SERVICE<i style="background:#FFC300;"></i></div>
              </div>
            </div>
          </div>
          <div class="var-foot">
            <span>Cabecera Web, Facturación, Rótulos y Papelería</span>
            <span>Alineación Óptica Exacta</span>
          </div>
        </div>

        <!-- 03. Horizontal Negativo / Oscuro -->
        <div class="var-card dark-bg">
          <div class="var-top">
            <span>03 · Versión Negativa / Invertida (Fondo Carbón)</span>
            <span class="var-pill">DARK / NEGATIVO</span>
          </div>
          <div class="var-stage">
            <div class="mini-h-lockup">
              {make_isotipo_svg("dark", 108)}
              <div>
                <div class="t" style="color:#FFFFFF;">FORKY<span style="color:#FFC300;margin-left:5px;">BEE</span><sup style="font-size:12px;font-style:normal;">®</sup></div>
                <div class="s" style="color:#FFFFFF;"><i style="background:#FFC300;"></i>FOOD SERVICE<i style="background:#FFC300;"></i></div>
              </div>
            </div>
          </div>
          <div class="var-foot">
            <span>Uniformes Oscuros, Rótulos Luminosos y Modo Noche</span>
            <span>Contraste Alto #FFFFFF + #FFC300</span>
          </div>
        </div>

        <!-- 04. Isotipo Independiente & App Icon -->
        <div class="var-card">
          <div class="var-top">
            <span>04 · Isotipo Independiente &amp; App Icon</span>
            <span class="var-pill">ISOTIPO / ÍCONO</span>
          </div>
          <div class="var-stage" style="gap:24px;">
            <div style="width:118px;height:118px;background:#FFC300;border-radius:26px;display:flex;align-items:center;justify-content:center;box-shadow:0 8px 20px rgba(255,195,0,0.35);">
              {make_isotipo_svg("color", 96)}
            </div>
            {make_isotipo_svg("color", 112)}
          </div>
          <div class="var-foot">
            <span>App Móvil, Avatar Redes Sociales, Stickers y Delantal</span>
            <span>Fondo Transparente + Badge</span>
          </div>
        </div>

        <!-- 05. Monocromático Positivo (1 Tinta Negra) -->
        <div class="var-card">
          <div class="var-top">
            <span>05 · Versión Monocromática Positiva (1 Tinta)</span>
            <span class="var-pill">1 TINTA #1F1F1F</span>
          </div>
          <div class="var-stage">
            <div class="mini-h-lockup">
              {make_isotipo_svg("mono_black", 108)}
              <div>
                <div class="t" style="color:#1F1F1F;">FORKY<span style="color:#1F1F1F;margin-left:5px;">BEE</span><sup style="font-size:12px;font-style:normal;">®</sup></div>
                <div class="s" style="color:#1F1F1F;"><i style="background:#1F1F1F;"></i>FOOD SERVICE<i style="background:#1F1F1F;"></i></div>
              </div>
            </div>
          </div>
          <div class="var-foot">
            <span>Serigrafía 1 Tinta en Cajas Kraft, Sellos y Grabado Láser</span>
            <span>Vaciados Limpios para Plotter</span>
          </div>
        </div>

        <!-- 06. Monocromático Negativo (1 Tinta Blanca) -->
        <div class="var-card dark-bg">
          <div class="var-top">
            <span>06 · Versión Monocromática Negativa (Calado Blanco)</span>
            <span class="var-pill">1 TINTA #FFFFFF</span>
          </div>
          <div class="var-stage">
            <div class="mini-h-lockup">
              {make_isotipo_svg("mono_white", 108)}
              <div>
                <div class="t" style="color:#FFFFFF;">FORKY<span style="color:#FFFFFF;margin-left:5px;">BEE</span><sup style="font-size:12px;font-style:normal;">®</sup></div>
                <div class="s" style="color:#FFFFFF;"><i style="background:#FFFFFF;"></i>FOOD SERVICE<i style="background:#FFFFFF;"></i></div>
              </div>
            </div>
          </div>
          <div class="var-foot">
            <span>Vinilo de Corte Blanco, Bordado Monocromo y Troquelado</span>
            <span>100% Vector Calado</span>
          </div>
        </div>
      </div>

      <!-- Row 3: Color Palette + Typography + Deliverable Formats -->
      <div class="specs-row">
        <div class="spec-box">
          <div class="spec-box-head">Paleta de Color Oficial (Colores Planos 100% Puros · CMYK &amp; RGB)</div>
          <div class="swatches-4">
            <div class="sw-item">
              <div class="sw-circle" style="background:#FFC300;"></div>
              <div class="sw-txt"><strong>Amarillo</strong><code>#FFC300</code><small>C0 M24 Y100 K0</small></div>
            </div>
            <div class="sw-item">
              <div class="sw-circle" style="background:#1F1F1F;"></div>
              <div class="sw-txt"><strong>Carbón</strong><code>#1F1F1F</code><small>C75 M68 Y67 K82</small></div>
            </div>
            <div class="sw-item">
              <div class="sw-circle" style="background:#F5F5F5;"></div>
              <div class="sw-txt"><strong>Arena</strong><code>#F5F5F5</code><small>C4 M3 Y3 K0</small></div>
            </div>
            <div class="sw-item">
              <div class="sw-circle" style="background:#FFFFFF;"></div>
              <div class="sw-txt"><strong>Blanco</strong><code>#FFFFFF</code><small>C0 M0 Y0 K0</small></div>
            </div>
          </div>
        </div>

        <div class="spec-box">
          <div class="spec-box-head">Tipografía Corporativa (En Curvas + Editable)</div>
          <div class="typo-showcase">
            <div class="typo-left">
              <h4>Montserrat ExtraBold</h4>
              <p>Montserrat Medium &amp; SemiBold</p>
            </div>
            <div class="typo-right">
              <strong>FORKY BEE®:</strong> ExtraBold Italic<br/>
              <strong>FOOD SERVICE:</strong> Bold Italic (+320)<br/>
              <strong>Slogan:</strong> Medium Italic / Regular
            </div>
          </div>
        </div>

        <div class="spec-box">
          <div class="spec-box-head">Archivos Maestros Entregados</div>
          <div class="formats-badges">
            <div class="fmt-chip"><strong>.AI</strong><span>Illustrator</span></div>
            <div class="fmt-chip"><strong>.EPS</strong><span>PostScript</span></div>
            <div class="fmt-chip"><strong>.SVG</strong><span>Web/Vector</span></div>
            <div class="fmt-chip"><strong>.PDF</strong><span>Imprenta</span></div>
            <div class="fmt-chip"><strong>.PNG</strong><span>4K Transp.</span></div>
          </div>
        </div>
      </div>
    </div>

    <footer class="foot-bar">
      <div><strong>Fidelidad 1:1 Garantizada:</strong> Reconstrucción exacta sin alterar la identidad, colores ni proporciones aprobadas de FORKY BEE®</div>
      <div><strong>Derechos de Uso Comercial Incluidos</strong> · Entrega Inmediata de Pack Maestro ZIP</div>
    </footer>
  </section>

  <!-- =======================================================================
       BOARD 02: PRESENTACIÓN DE IDENTIDAD, MASCOTA 3D & APLICACIONES REALES
       ======================================================================= -->
  <section class="board" id="board-02">
    <header class="top-bar">
      <div class="top-bar-left">
        <span class="badge-yellow">Lámina 02 / 02 · Presentación Oficial &amp; Aplicaciones</span>
        <span class="top-bar-title">FORKY BEE® · SISTEMA DE IDENTIDAD RECONSTRUIDO Y ARTES FINALES PARA PRODUCCIÓN</span>
      </div>
      <div class="top-bar-right">
        APTO PARA ROTULACIÓN VEHICULAR · SERIGRAFÍA · BORDADO · EMPAQUE · DIGITAL
      </div>
    </header>

    <div class="b2-main">
      <!-- Top Hero Banner matching 00_Presentacion.png with 100% Vector Lockup -->
      <div class="b2-hero-card">
        <div class="b2-mascot-col">
          <img src="assets/04_Mascota.png" alt="Mascota Oficial FORKY BEE" />
        </div>

        <div class="b2-center-col">
          {make_isotipo_svg("color", 168)}
          <div class="wm-title">
            <span>FORKY</span><span class="bee">BEE</span><span class="reg">®</span>
          </div>
          <div class="wm-sub-row" style="margin-top:6px;">
            <span class="wm-pill-line" style="width:52px;"></span>
            <span class="wm-sub-text" style="font-size:16px;">FOOD SERVICE</span>
            <span class="wm-pill-line" style="width:52px;"></span>
          </div>
          <div class="b2-slogan-brush">Abastecer. Así de simple.</div>
        </div>

        <div class="b2-services-col">
          <div class="srv-item">
            <div class="srv-icon">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#FFC300" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 5a2 2 0 1 0 0-4 2 2 0 0 0 0 4Z"/><path d="M4 17a8 8 0 0 1 16 0"/><path d="M2 17h20"/><path d="M4 20h16"/></svg>
            </div>
            <h4>Insumos para<br/>restaurantes</h4>
          </div>
          <div class="srv-item">
            <div class="srv-icon">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#FFC300" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16Z"/><path d="m3.3 7 8.7 5 8.7-5"/><path d="M12 22V12"/></svg>
            </div>
            <h4>Surtido amplio<br/>y confiable</h4>
          </div>
          <div class="srv-item">
            <div class="srv-icon">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#FFC300" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 18H3c-.6 0-1-.4-1-1V7c0-.6.4-1 1-1h10c.6 0 1 .4 1 1v11"/><path d="M14 9h4l4 4v4c0 .6-.4 1-1 1h-2"/><circle cx="7" cy="18" r="2"/><path d="M15 18H9"/><circle cx="17" cy="18" r="2"/></svg>
            </div>
            <h4>Entrega nacional<br/>y a tiempo</h4>
          </div>
          <div class="srv-item">
            <div class="srv-icon">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#FFC300" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="16" height="10" x="4" y="4" rx="2"/><path d="M2 18h20"/><path d="M6 14h12"/></svg>
            </div>
            <h4>Pedidos en línea<br/>24/7</h4>
          </div>
        </div>
      </div>

      <!-- Middle Strip: Variaciones de Logo + Paleta + Tipografía -->
      <div class="b2-mid-strip">
        <div>
          <div class="spec-box-head" style="margin-bottom:6px;">Variaciones de Logo Reconstruidas en Vector</div>
          <div class="b2-mini-vars">
            <div class="b2-mv-box" style="background:#FFFFFF;">
              <div class="mini-h-lockup" style="gap:8px;">
                {make_isotipo_svg("color", 56)}
                <div>
                  <div class="t" style="font-size:17px;color:#1F1F1F;">FORKY<span style="color:#FFC300;margin-left:3px;">BEE</span><sup>®</sup></div>
                  <div style="font-family:var(--brand);font-size:5.5px;font-weight:700;letter-spacing:0.25em;color:#1F1F1F;margin-top:2px;">FOOD SERVICE</div>
                </div>
              </div>
            </div>
            <div class="b2-mv-box" style="background:#1F1F1F;">
              <div class="mini-h-lockup" style="gap:8px;">
                {make_isotipo_svg("dark", 56)}
                <div>
                  <div class="t" style="font-size:17px;color:#FFFFFF;">FORKY<span style="color:#FFC300;margin-left:3px;">BEE</span><sup>®</sup></div>
                  <div style="font-family:var(--brand);font-size:5.5px;font-weight:700;letter-spacing:0.25em;color:#FFFFFF;margin-top:2px;">FOOD SERVICE</div>
                </div>
              </div>
            </div>
            <div class="b2-mv-box" style="background:#FFC300;">
              {make_isotipo_svg("color", 62)}
            </div>
            <div class="b2-mv-box" style="background:#F5F5F5;">
              {make_isotipo_svg("mono_black", 62)}
            </div>
          </div>
        </div>

        <div>
          <div class="spec-box-head" style="margin-bottom:6px;">Paleta de Color</div>
          <div class="swatches-4">
            <div class="sw-item"><div class="sw-circle" style="background:#FFC300;width:32px;height:32px;border-radius:50%;"></div><div class="sw-txt"><strong>Amarillo</strong><code>#FFC300</code></div></div>
            <div class="sw-item"><div class="sw-circle" style="background:#1F1F1F;width:32px;height:32px;border-radius:50%;"></div><div class="sw-txt"><strong>Carbón</strong><code>#1F1F1F</code></div></div>
            <div class="sw-item"><div class="sw-circle" style="background:#F5F5F5;width:32px;height:32px;border-radius:50%;"></div><div class="sw-txt"><strong>Arena</strong><code>#F5F5F5</code></div></div>
            <div class="sw-item"><div class="sw-circle" style="background:#FFFFFF;width:32px;height:32px;border-radius:50%;"></div><div class="sw-txt"><strong>Blanco</strong><code>#FFFFFF</code></div></div>
          </div>
        </div>

        <div>
          <div class="spec-box-head" style="margin-bottom:6px;">Tipografía Oficial</div>
          <div style="font-family:var(--brand);font-weight:800;font-size:20px;line-height:1.05;color:#1F1F1F;">Montserrat<br/>ExtraBold</div>
          <div style="font-family:var(--brand);font-weight:500;font-size:12px;color:#444;margin-top:4px;">Montserrat Medium</div>
        </div>
      </div>

      <!-- Bottom Row: 4 Production Mockups -->
      <div class="mockups-4-grid">
        <div class="mockup-frame">
          <div class="mockup-img-wrap">
            <img src="assets/mockup_truck.jpg" alt="Rotulación Vehicular FORKY BEE" />
          </div>
          <div class="mockup-caption">
            <strong>01 · Rotulación Vehicular de Flota</strong>
            <span>VINILO GRAN FORMATO · CMYK / SPOT</span>
          </div>
        </div>

        <div class="mockup-frame">
          <div class="mockup-img-wrap">
            <img src="assets/mockup_uniform.jpg" alt="Uniforme Corporativo FORKY BEE" />
          </div>
          <div class="mockup-caption">
            <strong>02 · Indumentaria &amp; Bordado</strong>
            <span>VERSIÓN NEGATIVA</span>
          </div>
        </div>

        <div class="mockup-frame">
          <div class="mockup-img-wrap">
            <img src="assets/mockup_app.jpg" alt="Aplicación Digital FORKY BEE" />
          </div>
          <div class="mockup-caption">
            <strong>03 · App Móvil &amp; Web B2B</strong>
            <span>SVG / PNG 4K</span>
          </div>
        </div>

        <div class="mockup-frame">
          <div class="mockup-img-wrap">
            <img src="assets/mockup_boxes.jpg" alt="Empaque Corrugado FORKY BEE" />
          </div>
          <div class="mockup-caption">
            <strong>04 · Empaque &amp; Cajas Corrugadas</strong>
            <span>FLEXOGRAFÍA / SERIGRAFÍA</span>
          </div>
        </div>
      </div>
    </div>

    <footer class="foot-bar">
      <div><strong>Entregables Listos para Producción:</strong> .AI (Adobe Illustrator) · .EPS · .SVG · .PDF Vectorial · .PNG 4K Fondo Transparente</div>
      <div><strong>Enlace al Catálogo y Descarga Directa:</strong> frank20190926.github.io/forky-bee-vector/</div>
    </footer>
  </section>

  <script>
    const params = new URLSearchParams(window.location.search);
    const mode = params.get('mode');
    if (mode === 'b1') {{
      document.getElementById('board-02').style.display = 'none';
      document.body.style.padding = '0';
      document.body.style.background = '#F5F5F5';
      document.getElementById('board-01').style.boxShadow = 'none';
      document.getElementById('board-01').style.border = 'none';
    }} else if (mode === 'b2') {{
      document.getElementById('board-01').style.display = 'none';
      document.body.style.padding = '0';
      document.body.style.background = '#F5F5F5';
      document.getElementById('board-02').style.boxShadow = 'none';
      document.getElementById('board-02').style.border = 'none';
    }}
  </script>
</body>
</html>
'''

out_html = os.path.join(PROJ_DIR, "index.html")
with open(out_html, "w", encoding="utf-8") as f:
    f.write(HTML)
print("Wrote", out_html)
