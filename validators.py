def non_empty(msg):
    while True:
        v = input(msg).strip()
        if v:
            return v
        print("⚠ No puede estar vacío.")

def positive_int(msg):
    while True:
        v = input(msg).strip()
        if v.isdigit() and int(v) > 0:
            return int(v)
        print("⚠ Ingrese un entero positivo.")

def non_negative_float(msg):
    while True:
        try:
            v = float(input(msg).strip())
            if v >= 0:
                return v
        except:
            pass
        print("⚠ Ingrese un número válido.")

def email(msg):
    while True:
        v = input(msg).strip()
        if "@" in v and "." in v.split("@")[-1] and len(v) >= 6:
            return v
        print("⚠ Correo inválido.")

def phone(msg):
    while True:
        v = input(msg).strip()
        if v.isdigit() and len(v) >= 7:
            return v
        print("⚠ Ingrese solo números (mínimo 7 dígitos).")

def unique_code(code, items, key):
    return not any(i[key] == code for i in items)