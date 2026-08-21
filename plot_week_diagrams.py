"""
Explanatory diagrams for the weekly reports.

WHY THESE EXIST
    The weekly reports are read by an advisor who does not work in signal processing.
    A list of bullet points describing architecture decisions is hard to picture on a
    first read, however carefully each bullet is worded. These diagrams carry the shape
    of each decision so the text only has to explain the reasoning.

    They deliberately contain no jargon, no axis numbers and no signal plots -- they are
    boxes and arrows showing where data goes and what happens when something fails.

OUTPUT
    paper/weekly_reports/figures/

USAGE
    python plot_week_diagrams.py
"""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

OUT = "paper/weekly_reports/figures"

C_ACTIVE, C_IDLE = "#2E6F95", "#C9D2DE"
C_GOOD, C_BAD, C_INK = "#2E7D45", "#B3261E", "#1F3B63"
C_WARN_BG, C_GOOD_BG = "#FBEAE8", "#E8F3EC"

plt.rcParams.update({"figure.dpi": 130, "font.size": 10.5})


def box(ax, x, y, w, h, text, face, edge=None, fontsize=10.5, weight="normal",
        textcolor="white"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.012,rounding_size=0.02",
                                facecolor=face, edgecolor=edge or face, linewidth=1.6))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fontsize,
            color=textcolor, fontweight=weight, linespacing=1.45)


def arrow(ax, x1, y1, x2, y2, color=C_INK, style="-|>", lw=1.8, ls="-"):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=style, color=color,
                                 linewidth=lw, linestyle=ls, mutation_scale=17,
                                 shrinkA=2, shrinkB=2))


def blank_ax(figsize):
    fig, ax = plt.subplots(figsize=figsize)
    ax.set_xlim(0, 10); ax.set_ylim(0, 10); ax.axis("off")
    return fig, ax


# ------------------------------------------------------------------ Figure 1
def fig_project_pipeline():
    """Where this week sits in the project as a whole."""
    fig, ax = blank_ax((11, 3.5))
    stages = [
        ("1. Thu thập\ndữ liệu", C_ACTIVE, "TUẦN 5–8"),
        ("2. Làm sạch\n& gán nhãn", C_IDLE, "Tuần 8–9"),
        ("3. Huấn luyện\nmô hình AI", C_IDLE, "Tuần 9, 12"),
        ("4. Phân tích\n& báo cáo", C_IDLE, "Tuần 10–13"),
    ]
    w, h, gap = 2.05, 2.1, 0.55
    x0 = 0.5
    for i, (label, colour, when) in enumerate(stages):
        x = x0 + i * (w + gap)
        box(ax, x, 4.6, w, h, label, colour,
            fontsize=11, weight="bold",
            textcolor="white" if colour == C_ACTIVE else "#41506B")
        ax.text(x + w / 2, 4.25, when, ha="center", va="top", fontsize=9,
                color=C_ACTIVE if colour == C_ACTIVE else "#8A98AB",
                fontweight="bold" if colour == C_ACTIVE else "normal")
        if i < len(stages) - 1:
            arrow(ax, x + w + 0.08, 5.65, x + w + gap - 0.08, 5.65, color="#8A98AB")

    ax.text(5.0, 8.6, "Tuần 5 nằm ở bước đầu tiên của toàn dự án",
            ha="center", fontsize=13, fontweight="bold", color=C_INK)
    ax.text(5.0, 7.85,
            "Chưa có dữ liệu đáng tin thì ba bước sau đều không thực hiện được",
            ha="center", fontsize=10.5, color="#55606D")

    ax.add_patch(FancyBboxPatch((0.5, 1.5), 9.05, 2.0,
                                boxstyle="round,pad=0.02,rounding_size=0.03",
                                facecolor="#F4F7FA", edgecolor="#D6DEE9", linewidth=1.2))
    ax.text(5.0, 2.5,
            "Mỗi người tham gia chỉ đến đo MỘT lần duy nhất.\n"
            "Một buổi đo hỏng là mất vĩnh viễn dữ liệu của người đó — không đo lại được.",
            ha="center", va="center", fontsize=10.5, color="#41506B", linespacing=1.6)

    fig.tight_layout()
    p = f"{OUT}/week05_project_pipeline.png"
    fig.savefig(p); plt.close(fig)
    return p


# ------------------------------------------------------------------ Figure 2
def fig_flash_vs_wireless():
    """Why the device writes to its own memory first."""
    fig, ax = blank_ax((11, 5.2))
    ax.text(5.0, 9.5, "Dữ liệu đi đâu sau khi cảm biến đọc được?",
            ha="center", fontsize=13, fontweight="bold", color=C_INK)

    box(ax, 0.35, 5.1, 1.9, 1.5, "Thiết bị\nđeo tay", C_INK, fontsize=10.5, weight="bold")

    # Đường bắt buộc
    ax.add_patch(FancyBboxPatch((2.9, 6.35), 6.75, 2.35,
                                boxstyle="round,pad=0.02,rounding_size=0.03",
                                facecolor=C_GOOD_BG, edgecolor=C_GOOD, linewidth=1.5))
    ax.text(3.15, 8.35, "ĐƯỜNG CHÍNH — luôn luôn chạy", fontsize=9.5,
            fontweight="bold", color=C_GOOD, va="center")
    box(ax, 3.15, 6.7, 2.5, 1.25, "Ghi vào bộ nhớ\ntrong thiết bị", C_GOOD, fontsize=10)
    box(ax, 6.9, 6.7, 2.5, 1.25, "Sau buổi đo,\ncắm dây lấy về", C_GOOD, fontsize=10)
    arrow(ax, 5.75, 7.32, 6.8, 7.32, color=C_GOOD)
    arrow(ax, 2.3, 6.1, 3.1, 7.0, color=C_GOOD)

    # Đường phụ
    ax.add_patch(FancyBboxPatch((2.9, 3.15), 6.75, 2.35,
                                boxstyle="round,pad=0.02,rounding_size=0.03",
                                facecolor="#F4F7FA", edgecolor="#B8C4D6", linewidth=1.5))
    ax.text(3.15, 5.15, "ĐƯỜNG PHỤ — có thì tốt, mất cũng không sao", fontsize=9.5,
            fontweight="bold", color="#6B7785", va="center")
    box(ax, 3.15, 3.5, 2.5, 1.25, "Gửi qua\nBluetooth", "#8A98AB", fontsize=10)
    box(ax, 6.9, 3.5, 2.5, 1.25, "Xem trực tiếp\ntrên máy tính", "#8A98AB", fontsize=10)
    arrow(ax, 5.75, 4.12, 6.8, 4.12, color="#8A98AB", ls=(0, (4, 2)))
    arrow(ax, 2.3, 5.6, 3.1, 4.4, color="#8A98AB", ls=(0, (4, 2)))
    ax.text(6.3, 2.72, "Bluetooth thỉnh thoảng mất sóng", ha="center", fontsize=9,
            color=C_BAD, style="italic")

    ax.add_patch(FancyBboxPatch((0.35, 0.35), 9.3, 1.75,
                                boxstyle="round,pad=0.02,rounding_size=0.03",
                                facecolor=C_WARN_BG, edgecolor=C_BAD, linewidth=1.3))
    ax.text(5.0, 1.22,
            "Nếu dựa hẳn vào Bluetooth để lưu: một lần mất sóng giữa buổi đo\n"
            "là mất trắng dữ liệu của người tham gia hôm đó.",
            ha="center", va="center", fontsize=10.5, color="#7A2E28", linespacing=1.6)

    fig.tight_layout()
    p = f"{OUT}/week05_flash_vs_wireless.png"
    fig.savefig(p); plt.close(fig)
    return p


# ------------------------------------------------------------------ Figure 3
def fig_transport_pivot():
    """The decision to drop the intermediate machine."""
    fig, ax = blank_ax((11, 4.2))
    ax.text(5.0, 9.4, "Quyết định đổi cách truyền dữ liệu",
            ha="center", fontsize=13, fontweight="bold", color=C_INK)

    # Trước
    ax.text(0.35, 7.9, "Kế hoạch ban đầu", fontsize=10.5, fontweight="bold",
            color="#8A98AB", va="center")
    for i, (lbl, x) in enumerate([("Thiết bị\nđeo tay", 0.35), ("Máy trung gian\n(Jetson)", 3.6),
                                  ("Máy tính", 7.0)]):
        box(ax, x, 5.9, 2.4, 1.35, lbl, C_IDLE, fontsize=10, textcolor="#41506B")
    arrow(ax, 2.85, 6.57, 3.5, 6.57, color="#8A98AB")
    arrow(ax, 6.1, 6.57, 6.9, 6.57, color="#8A98AB")
    ax.text(4.8, 5.35, "lỗi phần mềm mạng, sửa mãi không xong",
            ha="center", fontsize=9.5, color=C_BAD, style="italic")
    # Cắt ở đoạn nối phía sau máy trung gian, không vẽ đè lên tên hộp.
    ax.plot([6.28, 6.72], [6.35, 6.79], color=C_BAD, lw=2.8, zorder=6)
    ax.plot([6.28, 6.72], [6.79, 6.35], color=C_BAD, lw=2.8, zorder=6)

    # Sau
    ax.text(0.35, 3.9, "Đã đổi thành", fontsize=10.5, fontweight="bold",
            color=C_GOOD, va="center")
    box(ax, 0.35, 1.9, 2.4, 1.35, "Thiết bị\nđeo tay", C_INK, fontsize=10)
    box(ax, 7.0, 1.9, 2.4, 1.35, "Máy tính", C_ACTIVE, fontsize=10)
    arrow(ax, 2.85, 2.57, 6.9, 2.57, color=C_GOOD, lw=2.2)
    ax.text(4.9, 3.0, "Bluetooth — nối thẳng, bỏ máy trung gian",
            ha="center", fontsize=10, color=C_GOOD, fontweight="bold")
    ax.text(4.9, 1.45, "đã chứng minh chạy ổn định", ha="center", fontsize=9.5,
            color="#55606D", style="italic")

    fig.tight_layout()
    p = f"{OUT}/week05_transport_pivot.png"
    fig.savefig(p); plt.close(fig)
    return p


def main():
    os.makedirs(OUT, exist_ok=True)
    paths = [fig_project_pipeline(), fig_flash_vs_wireless(), fig_transport_pivot()]
    print("Đã lưu:")
    for p in paths:
        print(f"  {p}")


if __name__ == "__main__":
    main()
