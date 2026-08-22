"""
Test-coverage map of the whole system, layer by layer.

WHY THIS EXISTS
    The prototype testing report covers the complete device, not one subsystem.
    Every layer was tested, but not with the same kind of evidence: some carry a
    recorded number that can be re-derived from the data, others rest on direct
    observation repeated across 18 wearing sessions. That distinction matters when
    an examiner asks "how did you measure this?", so the map states it rather than
    painting every layer the same colour.

OUTPUT
    paper/figures/system_test_coverage.png      (Vietnamese)
    paper/figures_en/system_test_coverage.png   (English)

USAGE
    python plot_system_coverage.py
"""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

C_INK = "#1F3B63"
C_FULL, C_PART, C_NONE = "#2E7D45", "#2E6F95", "#8B96A5"
C_FULL_BG, C_PART_BG, C_NONE_BG = "#E8F3EC", "#E7F0F6", "#EDEFF2"

plt.rcParams.update({"figure.dpi": 130, "font.size": 10.5})

FULL, PART, NONE = "full", "part", "none"

# bottom of the stack first: physical foundation -> abstract
LAYERS = {
    "vi": [
        ("Cơ khí, vỏ và dây đeo", "Vỏ, độ vừa vặn, độ bám khi vận động, thử rơi", PART,
         "Quan sát"),
        ("Mạch in và nguồn điện", "Mạch in riêng, thời lượng pin, chất lượng tín hiệu I2C", PART,
         "Quan sát"),
        ("Cảm biến và tiếp xúc da", "Hai cảm biến quang học, cảm biến chuyển động, phát hiện áp da", FULL,
         "Có số liệu"),
        ("Firmware và lưu trữ", "Đa tác vụ, ghi flash, phân vùng bộ nhớ, giao thức phiên đo", FULL,
         "Có số liệu"),
        ("Truyền dữ liệu", "Bluetooth theo dõi trực tiếp, quy trình rút dữ liệu về máy", FULL,
         "Có số liệu"),
        ("Mô hình AI trên thiết bị", "Nhận diện hoạt động, ước lượng nhịp tim", FULL,
         "Có số liệu"),
    ],
    "en": [
        ("Mechanics, case and strap", "Enclosure, fit, stability during movement, drop test", PART,
         "Observed"),
        ("Circuit board and power", "Custom board, battery life, I2C signal quality", PART,
         "Observed"),
        ("Sensors and skin contact", "Two optical sensors, motion sensor, contact detection", FULL,
         "Logged"),
        ("Firmware and storage", "Multitasking, flash logging, partitioning, session protocol", FULL,
         "Logged"),
        ("Data transport", "Bluetooth live monitoring, pulling data back to the laptop", FULL,
         "Logged"),
        ("On-device AI model", "Activity recognition, heart rate estimation", FULL,
         "Logged"),
    ],
}

TITLE = {
    "vi": "Sáu tầng của hệ thống — tầng nào có số liệu, tầng nào căn cứ quan sát",
    "en": "The six layers — which carry logged numbers, which rest on observation",
}
FOOT = {
    "vi": "Cả sáu tầng đều đã kiểm thử. Màu phân biệt loại bằng chứng, không phải đạt hay không đạt.",
    "en": "All six layers were tested. Colour distinguishes the kind of evidence, not pass or fail.",
}

STYLE = {FULL: (C_FULL, C_FULL_BG), PART: (C_PART, C_PART_BG), NONE: (C_NONE, C_NONE_BG)}


def draw(lang, out_dir):
    layers = LAYERS[lang]
    fig, ax = plt.subplots(figsize=(11.4, 5.6))
    ax.set_xlim(0, 10); ax.set_ylim(0, 10); ax.axis("off")

    h, gap = 1.28, 0.20
    y0 = 0.85
    for i, (name, detail, state, label) in enumerate(layers):
        y = y0 + i * (h + gap)
        edge, face = STYLE[state]
        ax.add_patch(FancyBboxPatch((0.35, y), 7.15, h,
                                    boxstyle="round,pad=0.012,rounding_size=0.02",
                                    facecolor=face, edgecolor=edge, linewidth=1.9))
        ax.text(0.72, y + h * 0.63, name, ha="left", va="center",
                fontsize=11.5, color=C_INK, fontweight="bold")
        ax.text(0.72, y + h * 0.26, detail, ha="left", va="center",
                fontsize=9.3, color="#4A5A70")

        ax.add_patch(FancyBboxPatch((7.72, y + h * 0.22), 1.95, h * 0.56,
                                    boxstyle="round,pad=0.012,rounding_size=0.03",
                                    facecolor=edge, edgecolor=edge, linewidth=1.4))
        ax.text(8.70, y + h * 0.50, label, ha="center", va="center",
                fontsize=10, color="white", fontweight="bold")

    ax.text(5.0, y0 + 6 * (h + gap) + 0.30, TITLE[lang], ha="center", va="center",
            fontsize=13, color=C_INK, fontweight="bold")
    ax.text(0.35, 0.30, FOOT[lang], ha="left", va="center",
            fontsize=9.3, color="#6B7787", style="italic")

    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "system_test_coverage.png")
    fig.savefig(path, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("wrote", path)


if __name__ == "__main__":
    draw("vi", "paper/figures")
    draw("en", "paper/figures_en")
