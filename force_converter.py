while True:
    user_input = input("힘(kN)을 입력하세요 (종료: q): ")
    if user_input.lower() == 'q':
        break
    try:
        kn = float(user_input)
        n = kn * 1000
        kgf = kn * 101.971621
        print(f"-> N: {n:,.2f} N | kgf: {kgf:,.2f} kgf\n")
    except ValueError:
        print("잘못된 입력입니다. 숫자를 입력해주세요.\n")

 