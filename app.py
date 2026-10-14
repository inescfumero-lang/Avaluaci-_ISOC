import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Gestor d'Avaluació Docent", page_icon="👩‍🏫", layout="wide"
)

st.title("🎓 Panell de Control - Docent")
st.markdown("Eina per avaluar i generar el fitxer de resultats de l'alumnat.")

# Rúbrica oficial
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

# Alumnes, grups i PINs de 4 xifres
raw_alumnos = [
    ("Kelly", "A", "1001"),
    ("Valeria", "A", "1002"),
    ("Alejandro", "A", "1003"),
    ("Nora", "A", "1004"),
    ("Lucia", "B", "2001"),
    ("Carla", "B", "2002"),
    ("Alexia", "B", "2003"),
    ("Emelie", "B", "2004"),
    ("Víctor", "B", "2005"),
    ("Isabella", "B", "2006"),
    ("Helena", "C", "3001"),
    ("Alba", "C", "3002"),
    ("Vega", "C", "3003"),
    ("Dylan", "C", "3004"),
    ("Carla R", "C", "3005"),
    ("Aleix Q", "D", "4001"),
    ("Carla P", "D", "4002"),
    ("Lucia P", "D", "4003"),
    ("Mar", "D", "4004"),
    ("Maials", "D", "4005"),
    ("Valery", "E", "5001"),
    ("Ashley", "E", "5002"),
    ("Angelo", "E", "5003"),
    ("Aleix M", "E", "5004"),
    ("Sara", "E", "5005"),
    ("Carla Z", "E", "5006"),
]

df_alumnos = pd.DataFrame(raw_alumnos, columns=["Alumno", "Grupo", "PIN"])
grupos = df_alumnos["Grupo"].unique()

tab1, tab2, tab3 = st.tabs(
    ["1️⃣ Avaluació Grupal", "2️⃣ Avaluació Individual", "3️⃣ Generar Fitxer Web"]
)

with tab1:
  st.header("Avaluació Grupal")
  criterios_grupales = [c for c in RUBRICA if c["tipus"] == "grupal"]
  notas_grupales = {}
  for grupo in grupos:
    st.subheader(f"Grup {grupo}")
    notas_grupales[grupo] = {}
    for c in criterios_grupales:
      notas_grupales[grupo][c["criteri"]] = st.slider(
          f"Grup {grupo} - {c['criteri']}",
          0.0,
          10.0,
          7.0,
          0.5,
          key=f"g_{grupo}_{c['criteri']}",
      )

with tab2:
  st.header("Avaluació Individual")
  g_sel = st.selectbox("Tria grup:", options=grupos)
  criterios_individuales = [c for c in RUBRICA if c["tipus"] == "individual"]
  if "notas_individuales" not in st.session_state:
    st.session_state.notas_individuales = {}

  for idx, row in df_alumnos[df_alumnos["Grupo"] == g_sel].iterrows():
    al = row["Alumno"]
    st.markdown(f"**{al}**")
    if al not in st.session_state.notas_individuales:
      st.session_state.notas_individuales[al] = {}
    for c in criterios_individuales:
      st.session_state.notas_individuales[al][c["criteri"]] = st.slider(
          f"{al} - {c['criteri']}",
          0.0,
          10.0,
          7.0,
          0.5,
          key=f"ind_{al}_{c['criteri']}",
      )
    st.text_area(f"Feedback per a {al}", key=f"feed_{al}")
    st.markdown("---")

with tab3:
  st.header("Generar dades per al Portal d'Alumnes")
  st.markdown(
      "Després de posar les notes, clica el botó. Descarrega el fitxer"
      " `resultats.csv` i puja'l al teu repositori de GitHub (al costat de"
      " `app.py` i `portal.py`)."
  )

  if st.button("Generar dades"):
    res = []
    pesos_g = sum([c["pes"] for c in RUBRICA if c["tipus"] == "grupal"])
    pesos_i = sum([c["pes"] for c in RUBRICA if c["tipus"] == "individual"])
    stored_i = st.session_state.get("notas_individuales", {})

    for idx, row in df_alumnos.iterrows():
      al = row["Alumno"]
      gr = row["Grupo"]
      pin = row["PIN"]

      ng = sum([
          notas_grupales.get(gr, {}).get(c["criteri"], 0)
          * (c["pes"] / pesos_g)
          for c in RUBRICA
          if c["tipus"] == "grupal"
      ])
      ni = sum([
          stored_i.get(al, {}).get(c["criteri"], 0) * (c["pes"] / pesos_i)
          for c in RUBRICA
          if c["tipus"] == "individual"
      ])
      nfin = (ng * pesos_g) + (ni * pesos_i)
      feed = st.session_state.get(f"feed_{al}", "Sense comentaris.")

      res.append({
          "Alumno": al,
          "Grupo": gr,
          "PIN": pin,
          "NotaFinal": round(nfin, 2),
          "Feedback": feed,
      })

    df_export = pd.DataFrame(res)
    csv_data = df_export.to_csv(index=False).encode("utf-8")
    st.download_button(
        "📥 Descarregar `resultats.csv`",
        data=csv_data,
        file_name="resultats.csv",
        mime="text/csv",
    )
