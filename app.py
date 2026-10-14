import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Gestor d'Avaluació per Rúbrica", page_icon="📊", layout="wide"
)

# ---------------------------------------------------------
# 1. BASE DE DADES D'ALUMNES I PINS ALEATORIS DE 4 XIFRES
# ---------------------------------------------------------
raw_alumnos = [
    ("Kelly", "A", "2824"),
    ("Valeria", "A", "1409"),
    ("Alejandro", "A", "5506"),
    ("Nora", "A", "5012"),
    ("Lucia", "B", "4657"),
    ("Carla", "B", "3286"),
    ("Alexia", "B", "2679"),
    ("Emelie", "B", "9935"),
    ("Víctor", "B", "2424"),
    ("Isabella", "B", "7912"),
    ("Helena", "C", "1520"),
    ("Alba", "C", "1488"),
    ("Vega", "C", "2535"),
    ("Dylan", "C", "4582"),
    ("Carla R", "C", "4811"),
    ("Aleix Q", "D", "9279"),
    ("Carla P", "D", "1434"),
    ("Lucia P", "D", "4257"),
    ("Mar", "D", "9928"),
    ("Maials", "D", "7873"),
    ("Valery", "E", "4611"),
    ("Ashley", "E", "8359"),
    ("Angelo", "E", "5557"),
    ("Aleix M", "E", "1106"),
    ("Sara", "E", "3615"),
    ("Carla Z", "E", "7924"),
]

df_alumnos = pd.DataFrame(raw_alumnos, columns=["Alumno", "Grupo", "PIN"])
grupos = df_alumnos["Grupo"].unique()

# Rúbrica oficial
RUBRICA = [
    {
        "criteri": "Presentació visual",
        "tipus": "grupal",
        "pes": 0.10,
        "nivells": {
            "1-2": (
                "La presentació és desorganitzada, poc llegible o incompleta."
                " No facilita la comprensió del contingut."
            ),
            "3-4": (
                "La presentació té una organització poc clara. Hi ha massa"
                " text, poca coherència visual o recursos poc adequats."
            ),
            "5-6": (
                "La presentació és entenedora i té una estructura bàsica."
                " Combina text i elements visuals, tot i que podria ser més"
                " clara o atractiva."
            ),
            "7-8": (
                "La presentació està ben estructurada, és visualment coherent"
                " i facilita la comprensió. Els textos i les imatges són"
                " adequats."
            ),
            "9-10": (
                "La presentació és molt clara, atractiva i coherent. Els"
                " recursos visuals estan ben seleccionats i reforcen"
                " significativament l’explicació."
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
                "El contingut és molt superficial, incomplet o conté errors"
                " conceptuals importants. No desenvolupa les idees principals."
            ),
            "3-4": (
                "Presenta informació bàsica, però poc desenvolupada. Hi falten"
                " exemples, explicacions o aspectes rellevants del tema."
            ),
            "5-6": (
                "Desenvolupa les característiques principals dels estils"
                " educatius i incorpora algun exemple, tot i que l’anàlisi és"
                " limitada."
            ),
            "7-8": (
                "Aprofundeix en els diferents estils, els compara i n’explica"
                " les possibles conseqüències en el desenvolupament dels"
                " infants i adolescents. Incorpora exemples pertinents."
            ),
            "9-10": (
                "Fa una anàlisi crítica i ben fonamentada, compara els estils"
                " educatius, en valora les implicacions i els relaciona amb"
                " situacions reals d’intervenció socioeducativa. Utilitza"
                " exemples significatius."
            ),
        },
    },
    {
        "criteri": "Repartiment equitatiu de l’exposició",
        "tipus": "grupal",
        "pes": 0.10,
        "nivells": {
            "1-2": (
                "La participació és molt desigual: una persona assumeix gairebé"
                " tota l’exposició i alguna altra no hi participa o hi participa"
                " mínimament."
            ),
            "3-4": (
                "El repartiment és força desigual. Hi ha diferències"
                " importants en el temps de participació i en la implicació"
                " dels membres."
            ),
            "5-6": (
                "Tots els membres participen, però el temps o el contingut es"
                " reparteixen de manera una mica desigual."
            ),
            "7-8": (
                "La participació és equilibrada. Tots els membres tenen un"
                " temps raonable i desenvolupen una part significativa del"
                " contingut."
            ),
            "9-10": (
                "El temps i el contingut es reparteixen de manera molt"
                " equilibrada. Tots els membres contribueixen activament i les"
                " transicions entre les parts són fluides i coherents."
            ),
        },
    },
    {
        "criteri": "Expressió oral en català",
        "tipus": "individual",
        "pes": 0.20,
        "nivells": {
            "1-2": (
                "Té moltes dificultats per expressar-se en català. El discurs"
                " és poc comprensible, desorganitzat o excessivament dependent"
                " de la lectura."
            ),
            "3-4": (
                "S’expressa amb poca fluïdesa i comet errors freqüents. Li"
                " costa mantenir un discurs clar i utilitzar vocabulari"
                " adequat."
            ),
            "5-6": (
                "S’expressa en català de manera comprensible, amb algunes"
                " vacil·lacions o errors. Utilitza un vocabulari generalment"
                " adequat."
            ),
            "7-8": (
                "S’expressa amb fluïdesa, claredat i correcció general."
                " Utilitza vocabulari específic i manté un ritme adequat."
            ),
            "9-10": (
                "S’expressa amb molta fluïdesa, seguretat i precisió."
                " Utilitza correctament el vocabulari tècnic, adapta el discurs"
                " al públic i comunica amb eficàcia."
            ),
        },
    },
    {
        "criteri": "Domini del que s’explica",
        "tipus": "individual",
        "pes": 0.25,
        "nivells": {
            "1-2": (
                "Mostra un desconeixement important del tema. Llegeix gairebé"
                " tota la informació i no aconsegueix explicar-ne el"
                " significat."
            ),
            "3-4": (
                "Coneix alguns conceptes, però presenta confusions o"
                " dificultats per explicar-los amb les seves paraules. Depèn"
                " molt dels apunts."
            ),
            "5-6": (
                "Demostra una comprensió bàsica dels estils educatius familiars"
                " i n’explica les característiques principals, tot i que"
                " necessita consultar sovint els apunts."
            ),
            "7-8": (
                "Demostra un bon coneixement del tema, explica els conceptes"
                " amb les seves paraules i diferencia correctament els estils"
                " educatius."
            ),
            "9-10": (
                "Demostra un domini sòlid del tema, explica els conceptes amb"
                " precisió, els relaciona entre si i respon adequadament les"
                " preguntes que li plantegen."
            ),
        },
    },
]


def obtenir_nivell_text(score, nivells_dict):
  if score <= 2:
    k = "1-2"
  elif score <= 4:
    k = "3-4"
  elif score <= 6:
    k = "5-6"
  elif score <= 8:
    k = "7-8"
  else:
    k = "9-10"
  return f"**[{k}]** {nivells_dict.get(k, '')}"


# ---------------------------------------------------------
# 2. CONTROL D'ACCÉS AL PANEL LATERAL (PROFESSORA)
# ---------------------------------------------------------
st.sidebar.header("🔐 Accés General")
password_profesora = "profe1234"

modo_profesor = st.sidebar.checkbox("🔓 Mode Professora (Desbloquejar panell)")

if modo_profesor:
  pwd_ingresada = st.sidebar.text_input(
      "Introdueix la contrasenya de professora:", type="password"
  )
  if pwd_ingresada != password_profesora:
    st.sidebar.error("Contrasenya incorrecta.")
    is_admin = False
  else:
    st.sidebar.success("Mode docent actiu.")
    is_admin = True
else:
  is_admin = False

# ---------------------------------------------------------
# 3. INTERFÍCIE SEGONS EL ROL
# ---------------------------------------------------------

if is_admin:
  st.title("👩‍🏫 Panell de Gestió i Avaluació (Docent)")

  tab1, tab2, tab3, tab4, tab5 = st.tabs(
      [
          "1️⃣ Grupal",
          "2️⃣ Individual",
          "3️⃣ Informes Grups",
          "4️⃣ Docent Global",
          "5️⃣ Portal Alumnes",
      ]
  )

  # 1. Grupal (AMB SELECTOR DE GRUP)
  with tab1:
    st.header("👥 Avaluació de la Part Grupal")
    grupo_sel_grup = st.selectbox(
        "Selecciona el grup a avaluar (Part Grupal):",
        options=grupos,
        key="sel_grup_aval",
    )

    criterios_grupales = [c for c in RUBRICA if c["tipus"] == "grupal"]
    if "notas_grupales" not in st.session_state:
      st.session_state.notas_grupales = {}

    if grupo_sel_grup not in st.session_state.notas_grupales:
      st.session_state.notas_grupales[grupo_sel_grup] = {}

    st.markdown(f"### 🏛️ Equip: Grup {grupo_sel_grup}")
    for c in criterios_grupales:
      st.markdown(f"#### 📌 {c['criteri']} *(Pes: {int(c['pes']*100)}%)*")

      text_nivells = "\n".join(
          [f"* **{k}:** {v}" for k, v in c["nivells"].items()]
      )
      st.info(f"**Descripció dels nivells:**\n\n{text_nivells}")

      val_actual = st.session_state.notas_grupales[grupo_sel_grup].get(
          c["criteri"], 7.0
      )
      nota = st.slider(
          f"Puntuació per a Grup {grupo_sel_grup} - {c['criteri']}",
          0.0,
          10.0,
          val_actual,
          0.5,
          key=f"g_{grupo_sel_grup}_{c['criteri']}",
      )
      st.session_state.notas_grupales[grupo_sel_grup][c["criteri"]] = nota

      st.success(
          f"Nivell actual seleccionat: {obtenir_nivell_text(nota, c['nivells'])}"
      )
      st.markdown("---")

  # 2. Individual
  with tab2:
    st.header("👤 Avaluació Individual")
    g_sel = st.selectbox("Selecciona grup a avaluar:", options=grupos)
    criterios_individuales = [c for c in RUBRICA if c["tipus"] == "individual"]

    if "notas_individuales" not in st.session_state:
      st.session_state.notas_individuales = {}

    for idx, row in df_alumnos[df_alumnos["Grupo"] == g_sel].iterrows():
      al = row["Alumno"]
      st.markdown(f"### 🧑‍🎓 {al}")
      if al not in st.session_state.notas_individuales:
        st.session_state.notas_individuales[al] = {}

      for c in criterios_individuales:
        st.markdown(f"#### 📌 {c['criteri']} *(Pes: {int(c['pes']*100)}%)*")

        text_nivells = "\n".join(
            [f"* **{k}:** {v}" for k, v in c["nivells"].items()]
        )
        st.info(f"**Descripció dels nivells:**\n\n{text_nivells}")

        val_i_act = st.session_state.notas_individuales[al].get(
            c["criteri"], 7.0
        )
        nota_i = st.slider(
            f"Puntuació per a {al} - {c['criteri']}",
            0.0,
            10.0,
            val_i_act,
            0.5,
            key=f"ind_{al}_{c['criteri']}",
        )
        st.session_state.notas_individuales[al][c["criteri"]] = nota_i

        st.success(
            f"Nivell actual seleccionat: {obtenir_nivell_text(nota_i, c['nivells'])}"
        )
        st.markdown("---")

      feed_act = st.session_state.get(f"feed_{al}", "")
      st.text_area(f"Feedback qualitatiu per a {al}", feed_act, key=f"feed_{al}")
      st.markdown("==========================================")

  # 3. Informes Grups
  with tab3:
    st.header("📄 Informes per a Grups (amb text exacte)")
    g_inf = st.selectbox("Tria grup:", options=grupos, key="inf_g")
    notas_grupales = st.session_state.get("notas_grupales", {})
    stored_i = st.session_state.get("notas_individuales", {})

    pesos_g = sum([c["pes"] for c in RUBRICA if c["tipus"] == "grupal"])
    pesos_i = sum([c["pes"] for c in RUBRICA if c["tipus"] == "individual"])

    st.markdown(f"### 🏛️ Avaluació Grupal - Grup {g_inf}")
    criterios_grupales = [c for c in RUBRICA if c["tipus"] == "grupal"]
    suma_g = 0
    for c in criterios_grupales:
      val = notas_grupales.get(g_inf, {}).get(c["criteri"], 7.0)
      suma_g += val * (c["pes"] / pesos_g)
      st.markdown(f"- **{c['criteri']}** (Puntuació: **{val} / 10**)")
      st.caption(f"  📝 {obtenir_nivell_text(val, c['nivells'])}")

    st.info(f"✨ **Mitjana Grupal Ponderada:** {round(suma_g, 2)} / 10")
    st.markdown("---")

    st.markdown("### 🧑‍🎓 Avaluació Individual de l'Equip")
    for idx, row in df_alumnos[df_alumnos["Grupo"] == g_inf].iterrows():
      al = row["Alumno"]
      st.markdown(f"#### Alumne/a: {al}")
      suma_i = 0
      for c in [x for x in RUBRICA if x["tipus"] == "individual"]:
        val_i = stored_i.get(al, {}).get(c["criteri"], 7.0)
        suma_i += val_i * (c["pes"] / pesos_i)
        st.markdown(f"  - **{c['criteri']}** (Puntuació: **{val_i} / 10**)")
        st.caption(f"    📝 {obtenir_nivell_text(val_i, c['nivells'])}")

      n_fin = (suma_g * pesos_g) + (suma_i * pesos_i)
      st.markdown(f"  * **🎯 Nota Final de {al}:** `{round(n_fin, 2)} / 10`")
      st.info(
          f"💬 **Feedback:** {st.session_state.get(f'feed_{al}', 'Sense comentaris.')}"
      )
      st.markdown("---")

  # 4. Docent Global
  with tab4:
    st.header("📊 Resum General de Classe i PINs")
    st.dataframe(df_alumnos, use_container_width=True)

  # 5. Portal Alumnes
  with tab5:
    st.info("Vista prèvia del portal de l'alumnat.")

else:
  # --- VISTA EXCLUSIVA PER A L'ALUMNAT ---
  st.title("🔒 Portal de Consulta de Notes")
  st.markdown(
      "Introdueix el teu nom i el teu **PIN de 4 xifres** per veure la teva"
      " qualificació detallada amb els descripdors de la rúbrica."
  )

  col1, col2 = st.columns(2)
  with col1:
    al_ing = st.selectbox(
        "El teu nom:",
        options=df_alumnos["Alumno"].sort_values().unique(),
        key="p_al",
    )
  with col2:
    pin_ing = st.text_input(
        "PIN de 4 xifres:", type="password", max_chars=4, key="p_pin"
    )

  if st.button("Consultar nota"):
    pin_real = df_alumnos[df_alumnos["Alumno"] == al_ing]["PIN"].values[0]

    if pin_ing == pin_real:
      st.success("✅ Accés correcte!")
      gr_al = df_alumnos[df_alumnos["Alumno"] == al_ing]["Grupo"].values[0]

      notas_grupales = st.session_state.get("notas_grupales", {})
      stored_i = st.session_state.get("notas_individuales", {})

      pesos_g = sum([c["pes"] for c in RUBRICA if c["tipus"] == "grupal"])
      pesos_i = sum([c["pes"] for c in RUBRICA if c["tipus"] == "individual"])

      st.markdown(f"### Hola, **{al_ing}** (Grup {gr_al})")

      # Desglossament Grupal
      st.markdown("#### 🏛️ Avaluació del Treball en Grup")
      suma_g = 0
      for c in [x for x in RUBRICA if x["tipus"] == "grupal"]:
        val = notas_grupales.get(gr_al, {}).get(c["criteri"], 7.0)
        suma_g += val * (c["pes"] / pesos_g)
        st.markdown(f"- **{c['criteri']}**: **{val} / 10**")
        st.caption(f"  📝 {obtenir_nivell_text(val, c['nivells'])}")

      # Desglossament Individual
      st.markdown("#### 👤 Avaluació Individual")
      suma_i = 0
      for c in [x for x in RUBRICA if x["tipus"] == "individual"]:
        val_i = stored_i.get(al_ing, {}).get(c["criteri"], 7.0)
        suma_i += val_i * (c["pes"] / pesos_i)
        st.markdown(f"- **{c['criteri']}**: **{val_i} / 10**")
        st.caption(f"  📝 {obtenir_nivell_text(val_i, c['nivells'])}")

      nfin = (suma_g * pesos_g) + (suma_i * pesos_i)
      st.success(f"### 🎯 Qualificació Final: {round(nfin, 2)} / 10")

      feed = st.session_state.get(
          f"feed_{al_ing}", "Sense comentaris addicionals."
      )
      st.markdown("#### 💬 Comentari del docent:")
      st.info(feed)
    else:
      st.error("❌ PIN incorrecte. Revisa el número de 4 xifres.")
