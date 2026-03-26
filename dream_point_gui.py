import tkinter as tk
from tkinter import ttk, messagebox

# ราคาแพ็ก Dream Point
PACKS = [290, 890, 1490, 2990, 9990, 49990]


def find_best_combo(points, packs):
    """
    หา combo ที่ใช้ point ได้มากที่สุดโดยไม่เกิน points
    ถ้าใช้ได้เท่ากัน จะเลือกจำนวนชิ้นน้อยกว่า
    """
    dp = [None] * (points + 1)
    dp[0] = [0] * len(packs)  # base

    for current in range(points + 1):
        if dp[current] is None:
            continue

        for i, price in enumerate(packs):
            nxt = current + price
            if nxt <= points:
                new_combo = dp[current].copy()
                new_combo[i] += 1

                if dp[nxt] is None:
                    dp[nxt] = new_combo
                else:
                    old_count = sum(dp[nxt])
                    new_count = sum(new_combo)
                    if new_count < old_count:
                        dp[nxt] = new_combo

    best_used = -1
    best_combo = None

    for used in range(points, -1, -1):
        if dp[used] is not None:
            best_used = used
            best_combo = dp[used]
            break

    remain = points - best_used
    return best_used, remain, best_combo


def calculate():
    raw = entry_points.get().replace(",", "").strip()

    if not raw.isdigit():
        messagebox.showerror("Error", "กรุณากรอก Dream Point เป็นตัวเลขจำนวนเต็ม")
        return

    points = int(raw)
    used, remain, combo = find_best_combo(points, PACKS)

    result_lines = []
    result_lines.append(f"Dream Point ทั้งหมด: {points:,}")
    result_lines.append(f"ใช้ไป: {used:,}")
    result_lines.append(f"เหลือ: {remain:,}")
    result_lines.append("-" * 30)

    total_items = 0
    for price, count in zip(PACKS, combo):
        if count > 0:
            result_lines.append(f"{price:>6,} x {count}")
            total_items += count

    if total_items == 0:
        result_lines.append("ยังซื้ออะไรไม่ได้")

    result_lines.append("-" * 30)
    result_lines.append(f"จำนวนทั้งหมด: {total_items} ชิ้น")

    text_result.config(state="normal")
    text_result.delete("1.0", tk.END)
    text_result.insert(tk.END, "\n".join(result_lines))
    text_result.config(state="disabled")


def clear_all():
    entry_points.delete(0, tk.END)
    text_result.config(state="normal")
    text_result.delete("1.0", tk.END)
    text_result.config(state="disabled")


def fill_example(value):
    entry_points.delete(0, tk.END)
    entry_points.insert(0, str(value))
    calculate()


root = tk.Tk()
root.title("Dream Point Calculator")
root.iconbitmap("app.ico")
root.geometry("520x520")
root.resizable(False, False)

main = ttk.Frame(root, padding=16)
main.pack(fill="both", expand=True)

title_label = ttk.Label(main, text="คำนวณซื้อแพ็กให้เหลือ Point น้อยที่สุด", font=("Tahoma", 14, "bold"))
title_label.pack(pady=(0, 12))

pack_label = ttk.Label(
    main,
    text="แพ็กที่มี: 290, 890, 1,490, 2,990, 9,990, 49,990",
    font=("Tahoma", 10)
)
pack_label.pack(pady=(0, 12))

input_frame = ttk.Frame(main)
input_frame.pack(fill="x", pady=(0, 10))

ttk.Label(input_frame, text="Dream Point:").pack(side="left")

entry_points = ttk.Entry(input_frame, width=25)
entry_points.pack(side="left", padx=8)
entry_points.focus()

btn_frame = ttk.Frame(main)
btn_frame.pack(fill="x", pady=(0, 10))

ttk.Button(btn_frame, text="คำนวณ", command=calculate).pack(side="left", padx=(0, 8))
ttk.Button(btn_frame, text="ล้างค่า", command=clear_all).pack(side="left")

example_frame = ttk.LabelFrame(main, text="ตัวอย่าง")
example_frame.pack(fill="x", pady=(0, 12))

examples = [10580, 14420, 31600, 7010]
for val in examples:
    ttk.Button(
        example_frame,
        text=f"{val:,}",
        command=lambda v=val: fill_example(v)
    ).pack(side="left", padx=5, pady=8)

result_label = ttk.Label(main, text="ผลลัพธ์")
result_label.pack(anchor="w")

text_result = tk.Text(main, height=18, width=58, font=("Consolas", 11))
text_result.pack(fill="both", expand=True)
text_result.config(state="disabled")

root.mainloop()