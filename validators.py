def non_empty(msg):
    while True:
        v = input(msg).strip()
        if v:
            return v
        print("⚠ No puede estar vacío.")