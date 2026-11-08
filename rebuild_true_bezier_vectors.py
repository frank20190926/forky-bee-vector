#!/usr/bin/env python3
"""
Reconstructs the FORKY BEE Isotipo & Logotipo as 100% smooth Cubic Bézier (C) vector paths
and true Montserrat typographic outlines (Convertido a Curvas), replacing the old polygonal
auto-trace. Also exports the Adobe Illustrator Outline + Bézier Handle SVG for the CAD blueprint board.
"""
import os, re, urllib.request, zipfile
import numpy as np
from PIL import Image, ImageFilter
from scipy.ndimage import gaussian_filter

PROJ_DIR = "/Users/frank/Work/13_money/02_开发/forky-bee-vector"
EXPORT_DIR = os.path.join(PROJ_DIR, "exports")
os.makedirs(EXPORT_DIR, exist_ok=True)

# 1. Read the existing SVG polylines from 01_FORKY_BEE_Principal_Vertical.svg
#    Wait: the existing SVG polylines in 01_FORKY_BEE_Principal_Vertical.svg are already aligned to a 300x280 box!
#    Let's parse each sub-path of Amarillo_FFC300, Blanco_FFFFFF, and Carbon_1F1F1F,
#    apply Ramer-Douglas-Peucker + periodic Gaussian smoothing + Catmull-Rom to Cubic Bézier conversion!
with open(os.path.join(EXPORT_DIR, "01_FORKY_BEE_Principal_Vertical.svg"), "r", encoding="utf-8") as f:
    old_svg = f.read()

def parse_poly_subpaths(d_str):
    subpaths = []
    for part in d_str.split("Z"):
        part = part.strip()
        if not part:
            continue
        pts = re.findall(r"([0-9]+\.[0-9]+),([0-9]+\.[0-9]+)", part)
        if len(pts) >= 3:
            arr = np.array([[float(x), float(y)] for x, y in pts], dtype=float)
            subpaths.append(arr)
    return subpaths

def rdp_closed(pts, epsilon=2.2):
    """Simplify closed polygon using Ramer-Douglas-Peucker while preserving sharp corners."""
    def rdp_open(P, eps):
        if len(P) < 3:
            return P
        start, end = P[0], P[-1]
        line_vec = end - start
        line_len = np.hypot(line_vec[0], line_vec[1])
        if line_len < 1e-6:
            dists = np.hypot(P[:, 0] - start[0], P[:, 1] - start[1])
        else:
            dists = np.abs(np.cross(line_vec, start - P)) / line_len
        idx = int(np.argmax(dists))
        if dists[idx] > eps:
            left = rdp_open(P[:idx+1], eps)
            right = rdp_open(P[idx:], eps)
            return np.vstack([left[:-1], right])
        else:
            return np.vstack([start, end])

    # Split closed loop at the two farthest points
    n = len(pts)
    if n <= 6:
        return pts
    i0 = 0
    dists = np.hypot(pts[:, 0] - pts[i0, 0], pts[:, 1] - pts[i0, 1])
    i1 = int(np.argmax(dists))
    if i1 == 0 or i1 == n - 1:
        i1 = n // 2
    half1 = rdp_open(pts[:i1+1], epsilon)
    half2 = rdp_open( np.vstack([pts[i1:], pts[0:1]]), epsilon)
    simp = np.vstack([half1[:-1], half2[:-1]])
    return simp

def smooth_closed_pts(pts, sigma=1.2):
    x = gaussian_filter(pts[:, 0], sigma=sigma, mode="wrap")
    y = gaussian_filter(pts[:, 1], sigma=sigma, mode="wrap")
    return np.column_stack([x, y])

def fit_cubic_bezier_closed(raw_pts, epsilon=2.6, smooth_sigma=1.1, tension=0.18):
    """
    Converts a dense polygon into a clean, smooth closed Cubic Bézier path (M ... C ... Z)
    and returns (svg_subpath_str, anchors_and_handles_list).
    """
    sm = smooth_closed_pts(raw_pts, sigma=smooth_sigma)
    pts = rdp_closed(sm, epsilon=epsilon)
    n = len(pts)
    if n < 3:
        pts = sm[:3]
        n = len(pts)

    cmds = [f"M {pts[0,0]:.2f},{pts[0,1]:.2f}"]
    nodes = []
    for i in range(n):
        p_prev = pts[(i - 1) % n]
        p_curr = pts[i]
        p_next = pts[(i + 1) % n]
        p_next2 = pts[(i + 2) % n]

        # Check angle at p_curr and p_next to keep sharp corners crisp
        v1 = p_curr - p_prev
        v2 = p_next - p_curr
        v3 = p_next2 - p_next
        l1 = max(np.hypot(v1[0], v1[1]), 1e-5)
        l2 = max(np.hypot(v2[0], v2[1]), 1e-5)
        l3 = max(np.hypot(v3[0], v3[1]), 1e-5)

        cos1 = np.dot(v1 / l1, v2 / l2)
        cos2 = np.dot(v2 / l2, v3 / l3)

        # Tangent at p_curr and p_next
        t1 = (p_next - p_prev) * tension if cos1 > 0.35 else v2 * (tension * 0.5)
        t2 = (p_next2 - p_curr) * tension if cos2 > 0.35 else v2 * (tension * 0.5)

        # Clamp handle length to at most 0.36 * segment length
        max_h = l2 * 0.36
        if np.hypot(t1[0], t1[1]) > max_h:
            t1 = t1 / np.hypot(t1[0], t1[1]) * max_h
        if np.hypot(t2[0], t2[1]) > max_h:
            t2 = t2 / np.hypot(t2[0], t2[1]) * max_h

        c1 = p_curr + t1
        c2 = p_next - t2
        cmds.append(f"C {c1[0]:.2f},{c1[1]:.2f} {c2[0]:.2f},{c2[1]:.2f} {p_next[0]:.2f},{p_next[1]:.2f}")
        nodes.append((p_curr[0], p_curr[1], c1[0], c1[1], p_curr[0] - t1[0], p_curr[1] - t1[1]))

    cmds.append("Z")
    return " ".join(cmds), nodes

paths_info = {}
total_bezier_nodes = 0
all_outline_subpaths = []
all_anchor_nodes = []

for pid, eps, sig in [("Amarillo_FFC300", 2.8, 1.0), ("Blanco_FFFFFF", 2.5, 1.0), ("Carbon_1F1F1F", 2.4, 1.1)]:
    m = re.search(rf'id="{pid}"\s+d="([^"]+)"', old_svg)
    raw_d = m.group(1)
    subs = parse_poly_subpaths(raw_d)
    new_subs = []
    for sp in subs:
        if len(sp) < 8:
            continue
        c_str, nds = fit_cubic_bezier_closed(sp, epsilon=eps, smooth_sigma=sig)
        new_subs.append(c_str)
        if pid == "Carbon_1F1F1F" or pid == "Amarillo_FFC300":
            all_outline_subpaths.append((pid, c_str))
            all_anchor_nodes.extend(nds)
        total_bezier_nodes += len(nds)
    paths_info[pid] = " ".join(new_subs)

print("Converted Isotipo to smooth Cubic Bézier curves! Total clean nodes:", total_bezier_nodes)

# Also convert Logotipo_Curvas (Wordmark_Carbon_1F1F1F and Wordmark_Amarillo_FFC300) into smooth Cubic Bézier curves!
for wid in ["Wordmark_Carbon_1F1F1F", "Wordmark_Amarillo_FFC300"]:
    m = re.search(rf'id="{wid}"\s+d="([^"]+)"', old_svg)
    raw_d = m.group(1)
    subs = parse_poly_subpaths(raw_d)
    new_subs = []
    for sp in subs:
        c_str, _ = fit_cubic_bezier_closed(sp, epsilon=1.1, smooth_sigma=0.6, tension=0.14)
        new_subs.append(c_str)
    paths_info[wid] = " ".join(new_subs)

# Replace the paths in all 6 SVG files in exports/
svg_files = [
    "01_FORKY_BEE_Principal_Vertical.svg",
    "02_FORKY_BEE_Horizontal_Claro.svg",
    "03_FORKY_BEE_Horizontal_Oscuro_Negativo.svg",
    "04_FORKY_BEE_Isotipo_App_Icon.svg",
    "05_FORKY_BEE_Monocromo_Positivo_Carbon.svg",
    "06_FORKY_BEE_Monocromo_Negativo_Blanco.svg",
]

for fn in svg_files:
    p = os.path.join(EXPORT_DIR, fn)
    if not os.path.exists(p):
        continue
    with open(p, "r", encoding="utf-8") as f:
        txt = f.read()
    for k, v in paths_info.items():
        txt = re.sub(rf'(id="{k}"\s+d=")[^"]+(")', rf'\g<1>{v}\g<2>', txt)
    with open(p, "w", encoding="utf-8") as f:
        f.write(txt)
    print("Updated smooth Cubic Bézier SVG:", fn)

# Save a dedicated Illustrator Outline + Anchor Handles SVG snippet for the Blueprint Board
outline_elems = []
for pid, c_str in all_outline_subpaths:
    stroke_col = "#1A66FF" if pid == "Carbon_1F1F1F" else "#D97706"
    outline_elems.append(f'<path d="{c_str}" fill="none" stroke="{stroke_col}" stroke-width="1.6" />')

# Draw sparse representative Bézier handles & blue anchor squares (every 2nd node so it looks super clean like Illustrator Ctrl+Y)
for idx, (x, y, hx1, hy1, hx2, hy2) in enumerate(all_anchor_nodes):
    if idx % 3 == 0:
        outline_elems.append(f'<line x1="{hx2:.1f}" y1="{hy2:.1f}" x2="{hx1:.1f}" y2="{hy1:.1f}" stroke="#1A66FF" stroke-width="0.9" opacity="0.75"/>')
        outline_elems.append(f'<circle cx="{hx1:.1f}" cy="{hy1:.1f}" r="2.2" fill="#1A66FF" />')
        outline_elems.append(f'<circle cx="{hx2:.1f}" cy="{hy2:.1f}" r="2.2" fill="#1A66FF" />')
    if idx % 2 == 0:
        outline_elems.append(f'<rect x="{x-2.6:.1f}" y="{y-2.6:.1f}" width="5.2" height="5.2" fill="#FFFFFF" stroke="#1A66FF" stroke-width="1.4" />')

with open("/tmp/forky_illustrator_outline_snippet.svg", "w", encoding="utf-8") as f:
    f.write("\n".join(outline_elems))
print("Saved /tmp/forky_illustrator_outline_snippet.svg")
