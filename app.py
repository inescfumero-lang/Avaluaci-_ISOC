import random

# Fixem una llavor (seed) per generar codis completament aleatoris de 4 xifres pero deterministes si cal
random.seed(42)

alumnes = [
    ("Kelly", "A"), ("Valeria", "A"), ("Alejandro", "A"), ("Nora", "A"),
    ("Lucia", "B"), ("Carla", "B"), ("Alexia", "B"), ("Emelie", "B"),
    ("Víctor", "B"), ("Isabella", "B"), ("Helena", "C"), ("Alba", "C"),
    ("Vega", "C"), ("Dylan", "C"), ("Carla R", "C"), ("Aleix Q", "D"),
    ("Carla P", "D"), ("Lucia P", "D"), ("Mar", "D"), ("Maials", "D"),
    ("Valery", "E"), ("Ashley", "E"), ("Angelo", "E"), ("Aleix M", "E"),
    ("Sara", "E"), ("Carla Z", "E")
]

pins_usats = set()
raw_alumnos = []

for nom, grup in alumnes:
    while True:
        pin = f"{random.randint(1000, 9999)}"
        if pin not in pins_usats:
            pins_usats.add(pin)
            break
    raw_alumnos.append((nom, grup, pin))

print("raw_alumnos = [")
for nom, grup, pin in raw_alumnos:
    print(f'    ("{nom}", "{grup}", "{pin}"),')
print("]")
