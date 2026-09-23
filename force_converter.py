import tkinter as tk
from tkinter import ttk, scrolledtext

def convert_force():
    """입력된 힘 값을 변환하여 결과 영역에 누적 기록합니다."""
    value_str = entry_value.get().strip()
    unit = combo_unit.get()
    
    if not value_str:
        append_to_history("⚠️ 입력 오류", "값을 입력해주세요.", is_error=True)
        return
        
    try:
        val = float(value_str)
        if val < 0:
            append_to_history("⚠️ 입력 오류", "힘의 크기는 0 이상이어야 합니다.", is_error=True)
            return

        # 기준 단위(kN) 환산
        if unit == "kN":
            kn = val
        elif unit == "N":
            kn = val / 1000.0
        elif unit == "kgf":
            kn = val / 101.971621

        n = kn * 1000.0
        kgf = kn * 101.971621

        # 결과 텍스트 구성
        result_msg = (
            f"입력: {val:g} {unit}\n"
            f"  • N   : {n:,.2f} N\n"
            f"  • kN  : {kn:,.4f} kN\n"
            f"  • kgf : {kgf:,.2f} kgf"
        )
        append_to_history("RESULT", result_msg, is_error=False)
        
    except ValueError:
        append_to_history("⚠️ 입력 오류", "숫자만 입력해 주세요.", is_error=True)

def append_to_history(title, content, is_error=False):
    """스크롤 영역에 기록을 추가합니다."""
    txt_history.config(state=tk.NORMAL)
    
    # 처음 입력 시 기본 안내 문구 제거
    first_char = txt_history.get("1.0", tk.END).strip()
    if first_char.startswith("값을 입력하고"):
        txt_history.delete("1.0", tk.END)

    divider = "─" * 32 + "\n"
    txt_history.insert(tk.END, divider, "divider")
    
    if is_error:
        txt_history.insert(tk.END, f"{title}\n", "error_title")
        txt_history.insert(tk.END, f"{content}\n\n", "error_body")
    else:
        txt_history.insert(tk.END, f"📌 {title}\n", "result_title")
        txt_history.insert(tk.END, f"{content}\n\n", "result_body")
        
    txt_history.see(tk.END)  # 자동 스크롤 하단 이동
    txt_history.config(state=tk.DISABLED)

def reset_fields():
    """입력 및 히스토리 초기화"""
    entry_value.delete(0, tk.END)
    combo_unit.current(0)
    
    txt_history.config(state=tk.NORMAL)
    txt_history.delete("1.0", tk.END)
    txt_history.insert(tk.END, "값을 입력하고 변환 버튼을 누르시면\n이곳에 변환 기록이 누적됩니다.", "placeholder")
    txt_history.config(state=tk.DISABLED)

# ----------------------------------------------------
# UI 구성 (Flat Modern UI Design)
# ----------------------------------------------------
root = tk.Tk()
root.title("Force Converter Pro")
root.geometry("420x580")
root.configure(bg="#F5F7FA")  # 연한 회색 배경

# ttk 스타일 설정
style = ttk.Style()
style.theme_use("clam")
style.configure("TCombobox", fieldbackground="#FFFFFF", background="#E2E8F0", borderwidth=0)

# 1. 헤더 타이틀
lbl_header = tk.Label(
    root, text="힘 단위 변환기", font=("Pretendard", 16, "bold"),
    bg="#F5F7FA", fg="#1E293B", pady=15
)
lbl_header.pack()

# 2. 입력 카드 프레임
card_frame = tk.Frame(root, bg="#FFFFFF", bd=0, highlightthickness=1, highlightbackground="#E2E8F0")
card_frame.pack(padx=20, pady=5, fill=tk.X)

lbl_input_title = tk.Label(card_frame, text="값 입력", font=("Pretendard", 9, "bold"), bg="#FFFFFF", fg="#64748B")
lbl_input_title.pack(anchor="w", padx=15, pady=(12, 5))

input_inner_frame = tk.Frame(card_frame, bg="#FFFFFF")
input_inner_frame.pack(padx=15, pady=(0, 15), fill=tk.X)

entry_value = tk.Entry(
    input_inner_frame, font=("Pretendard", 11), bg="#F8FAFC", fg="#0F172A",
    bd=1, relief="solid", highlightthickness=0
)
entry_value.pack(side=tk.LEFT, expand=True, fill=tk.X, ipady=6, padx=(0, 8))
entry_value.focus()

combo_unit = ttk.Combobox(
    input_inner_frame, values=["kN", "N", "kgf"], width=6,
    state="readonly", font=("Pretendard", 10)
)
combo_unit.current(0)
combo_unit.pack(side=tk.LEFT, ipady=4)

# 3. 버튼 영역
btn_frame = tk.Frame(root, bg="#F5F7FA")
btn_frame.pack(padx=20, pady=12, fill=tk.X)

btn_convert = tk.Button(
    btn_frame, text="변환하기", font=("Pretendard", 10, "bold"),
    bg="#2563EB", fg="white", activebackground="#1D4ED8", activeforeground="white",
    bd=0, relief="flat", cursor="hand2", command=convert_force
)
btn_convert.pack(side=tk.LEFT, expand=True, fill=tk.X, ipady=8, padx=(0, 5))

btn_reset = tk.Button(
    btn_frame, text="초기화", font=("Pretendard", 10),
    bg="#E2E8F0", fg="#475569", activebackground="#CBD5E1",
    bd=0, relief="flat", cursor="hand2", command=reset_fields
)
btn_reset.pack(side=tk.LEFT, width=80, ipady=8, padx=(5, 0))

root.bind('<Return>', lambda event: convert_force())

# 4. 히스토리 출력 영역 (ScrolledText)
history_frame = tk.Frame(root, bg="#F5F7FA")
history_frame.pack(padx=20, pady=(5, 20), fill=tk.BOTH, expand=True)

lbl_history_title = tk.Label(history_frame, text="변환 기록", font=("Pretendard", 9, "bold"), bg="#F5F7FA", fg="#64748B")
lbl_history_title.pack(anchor="w", pady=(0, 5))

txt_history = scrolledtext.ScrolledText(
    history_frame, font=("Consolas", 10), bg="#FFFFFF", fg="#1E293B",
    bd=1, relief="solid", highlightthickness=0, wrap=tk.WORD
)
txt_history.pack(fill=tk.BOTH, expand=True)

# ScrolledText 태그 (스타일 지정)
txt_history.tag_config("placeholder", foreground="#94A3B8", justify="center")
txt_history.tag_config("divider", foreground="#E2E8F0")
txt_history.tag_config("result_title", foreground="#2563EB", font=("Consolas", 10, "bold"))
txt_history.tag_config("result_body", foreground="#334155")
txt_history.tag_config("error_title", foreground="#DC2626", font=("Consolas", 10, "bold"))
txt_history.tag_config("error_body", foreground="#EF4444")

# 초기 안내 문구 설정
reset_fields()

# 실행
root.mainloop()
