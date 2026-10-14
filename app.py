import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Avaluació per Rúbrica", page_icon="📊", layout="wide"
)

st.title("🎓 Aplicació d'Avaluació per Rúbrica")
st.markdown(
    "Eina per gestionar la rúbrica grupal i individual amb els alumnes i grups"
    " preconfigurats."
)

# Definició de la rúbrica oficial
RUBRICA = [
    {
        "criteri": "Presentació visual",
        "tipus": "grupal",
        "pes": 0.10,
        "nivells": {
            "1-2": (
                "La presentació és desorganitzada, poc llegible o incompleta."
                " No facilita la comprensió."
            ),
            "3-4": (
                "Organització poc clara. Massa text, poca coherència visual o"
                " recursos inadequats."
            ),
            "5-6": (
                "Entenedora i amb estructura bàsica. Combina text i visuals,"
                " pot millorar."
            ),
            "7-8": (
                "Ben estructurada, visualment coherent i facilita la"
                " comprensió."
            ),
            "9-10": (
                "Molt clara, atractiva i coherent. Recursos visuals ben"
                " seleccionats."
            ),
        },
    },
    {
        "criteri": "Faltes d’ortografia",
        "tipus": "grupal",
        "pes": 0.10,
        "nivells": {
            "1-2": "Més de 15 faltes d’ortografia.",
            "3-4": "Entre 11 i 15 faltes d’ortografia.",
            "5-6": "Entre 6 i 10 faltes d’ortografia.",
            "7-8": "Entre 1 i 5 faltes d’ortografia.",
            "9-10": "Cap falta d’ortografia (0 faltes).",
        },
    },
    {
        "criteri": "Aprofundiment",
        "tipus": "grupal",
        "pes": 0.25,
        "nivells": {
            "1-2": (
                "Contingut molt superficial, incomplet o amb errors"
                " conceptuals."
            ),
            "3-4": (
                "Informació bàsica poc desenvolupada. Falten exemples o"
                " aspectes rellevants."
            ),
            "5-6": (
                "Desenvolupa característiques principals i algun exemple"
                " (anàlisi limitada)."
            ),
            "7-8": (
                "Aprofundeix, compara estils i explica conseqüències amb"
                " exemples pertinents."
            ),
            "9-10": (
                "Anàlisi crítica i ben fonamentada, valora implicacions i"
                " relaciona amb situacions reals."
            ),
        },
    },
    {
        "criteri": "Repartiment equitatiu de l’exposició",
        "tipus": "grupal",
        "pes": 0.10,
        "nivells": {
            "1-2": (
                "Participació molt desigual: una persona assumeix gairebé tot"
                " i algú no participa."
            ),
            "3-4": (
                "Repartiment força desigual amb diferències importants en"
                " temps i implicació."
            ),
            "5-6": (
                "Tots participen però el temps o contingut es reparteix de"
                " manera irregular."
            ),
            "7-8": (
                "Participació equilibrada. Tots tenen temps raonable i"
                " desenvolupen part significativa."
            ),
            "9-10": (
                "Temps i contingut molt equilibrats. Transicions fluides i"
                " coherents."
            ),
        },
    },
    {
        "criteri": "Expressió oral en català",
        "tipus": "individual",
        "pes": 0.20,
        "nivells": {
            "1-2": (
                "Moltes dificultats per expressar-se en català. Discurs poc"
                " comprensible o molt dependent de lectura."
            ),
            "3-4": (
                "Poca fluïdesa i errors freqüents. Costa mantenir un discurs"
                " clar."
            ),
            "5-6": (
                "De manera comprensible, amb algunes vacil·lacions. Vocabulari"
                " generalment adequat."
            ),
            "7-8": (
                "Amb fluïdesa, claredat i correcció general. Utilitza"
                " vocabulari específic."
            ),
            "9-10": (
                "Molta fluïdesa, seguretat i precisió. Vocabulari tècnic i"
                " comunicació eficaç."
            ),
        },
    },
    {
        "criteri": "Domini del que s’explica",
        "tipus": "individual",
        "pes": 0.25,
        "nivells": {
            "1-2": (
                "Desconeixement important. Llegeix gairebé tot i no explica el"
                " significat."
            ),
            "3-4": (
                "Coneix alguns conceptes però presenta confusions. Depèn molt"
                " dels apunts."
            ),
            "5-6": (
                "Comprensió bàsica i característiques principals, necessita"
                " consultar apunts."
            ),
            "7-8": (
                "Bon coneixement, explica amb les seves paraules i diferencia"
                " correctament els estils."
            ),
            "9-10": (
                "Domini sòlid, precisió, relaciona conceptes i respon"
                " adequadament."
            ),
        },
    },
]

# --- LLISTAT PRECONFIGURAT D'ALUMNES I GRUPS ---
raw_alumnos = [
    ("Kelly", "A"),
    ("Valeria", "A"),
    ("Alejandro", "A"),
    ("Nora", "A"),
    ("Lucia", "B"),
    ("Carla", "B"),
    ("Alexia", "B"),
    ("Emelie", "B"),
    ("Víctor", "B"),
    ("Isabella", "B"),
    ("Helena", "C"),
    ("Alba", "C"),
    ("Vega", "C"),
    ("Dylan", "C"),
    ("Carla R", "C"),
    ("Aleix Q", "D"),
    ("Carla P", "D"),
    ("Lucia P", "D"),
    ("Mar", "D"),
    ("Maials", "D"),
    ("Valery", "E"),
    ("Ashley", "E"),
    ("Angelo", "E"),
    ("Aleix M", "E"),
    ("Sara", "E"),
    ("Carla Z", "E"),
]

df_alumnos = pd.DataFrame(raw_alumnos, columns=["Alumno", "Grupo"])
grupos = df_alumnos["Grupo"].unique()

# Barra lateral informativa
st.sidebar.header("📊 Estat de l'App")
st.sidebar.success(
    f"Carregats {len(df_alumnos)} alumnes repartits en {len(grupos)} grups (A-E)."
)

# Pestanyes de navegació
tab1, tab2, tab3, tab4 = st.tabs(
    [
        "1️⃣ Avaluació Grupal",
        "2️⃣ Avaluació Individual",
        "3️⃣ Informes per Grups",
        "4️⃣ Informe General Docent",
    ]
)

# --- TAB 1: AVALUACIÓ GRUPAL ---
with tab1:
  st.header("👥 Avaluació de la Part Grupal")
  st.markdown("Criteris comuns per a cada equip (Grups A al E).")

  criterios_grupales = [c for c in RUBRICA if c["tipus"] == "grupal"]
  notas_grupales = {}

  for grupo in grupos:
    st.subheader(f"Grup: {grupo}")
    notas_grupales[grupo] = {}
    for c in criterios_grupales:
      with st.expander(f"Criteri: {c['criteri']} (Pes: {int(c['pes']*100)}%)"):
        st.markdown(
            "* **Nivells:**\n"
            + "\n".join([f"  * **{k}:** {v}" for k, v in c["nivells"].items()])
        )
        nota = st.slider(
            f"Puntuació (0-10) - Grup {grupo} - {c['criteri']}",
            0.0,
            10.0,
            7.0,
            0.5,
            key=f"g_{grupo}_{c['criteri']}",
        )
        notas_grupales[grupo][c["criteri"]] = nota
    st.markdown("---")

# --- TAB 2: AVALUACIÓ INDIVIDUAL (AMB FILTRE DE GRUP) ---
with tab2:
  st.header("👤 Avaluació de la Part Individual")
  st.markdown(
      "Selecciona un grup per avaluar només els seus integrants i evitar"
      " saturar la pantalla."
  )

  grupo_seleccionado = st.selectbox(
      "Selecciona el grup a avaluar:", options=grupos
  )

  criterios_individuales = [c for c in RUBRICA if c["tipus"] == "individual"]

  if "notas_individuales" not in st.session_state:
    st.session_state.notas_individuales = {}

  st.markdown(f"### Alumnes del Grup {grupo_seleccionado}")
  alumnos_grupo = df_alumnos[df_alumnos["Grupo"] == grupo_seleccionado]

  for idx, row in alumnos_grupo.iterrows():
    alumno = row["Alumno"]
    st.markdown(f"#### 🧑‍🎓 {alumno}")
    if alumno not in st.session_state.notas_individuales:
      st.session_state.notas_individuales[alumno] = {}

    for c in criterios_individuales:
      with st.expander(f"Criteri: {c['criteri']} (Pes: {int(c['pes']*100)}%)"):
        st.markdown(
            "* **Nivells:**\n"
            + "\n".join([f"  * **{k}:** {v}" for k, v in c["nivells"].items()])
        )
        nota_actual = st.session_state.notas_individuales[alumno].get(
            c["criteri"], 7.0
        )
        nota = st.slider(
            f"Nota {alumno} - {c['criteri']}",
            0.0,
            10.0
