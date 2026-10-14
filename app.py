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

# ---------------------------------------------------------
# 2. CONTROL D'ACCÉS AL PANEL LATERAL (PROFESSORA)
# ---------------------------------------------------------
st.sidebar.header("🔐 Accés General")
password_profesora = "profe1234"  # Pots canviar la teva contrasenya mestra aquí

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
  # --- VISTA DE LA PROFESSORA (Tot visible i editable) ---
  st.title("👩‍🏫 Panell de Gestió i Avaluació (Docent)")
  st.markdown(
      "Tens accés total per avaluar grups, alumnes i veure informes generals."
  )

  tab1, tab2, tab3, tab4, tab5 = st.tabs(
      [
          "1️⃣ Grupal",
          "2️⃣ Individual",
          "3️⃣ Informes Grups",
          "4️⃣ Docent Global",
          "5️⃣ Portal Alumnes",
      ]
  )

  # 1. Grupal
  with tab1:
    st.header("Avaluació de la Part Grupal")
    criterios_grupales = [c for c in RUBRICA if c["tipus"] == "grupal"]
    if "notas_grupales" not in st.session_state:
      st.session_state.notas_grupales = {}

    for grupo in grupos:
      st.subheader(f"Grup {grupo}")
      if grupo not in st.session_state.notas_grupales:
        st.session_state.notas_grupales[grupo] = {}
      for c in criterios_grupales:
        val_actual = st.session_state.notas_grupales[grupo].get(
            c["criteri"], 7.0
        )
        st.session_state.notas_grupales[grupo][c["criteri"]] = st.slider(
            f"Grup {grupo} - {c['criteri']}",
            0.0,
            10.0,
            val_actual,
            0.5,
            key=f"g_{grupo}_{c['criteri']}",
        )

  # 2. Individual
  with tab2:
    st.header("Avaluació Individual")
    g_sel = st.selectbox("Selecciona grup a avaluar:", options=grupos)
    criterios_individuales = [c for c in RUBRICA if c["tipus"] == "individual"]

    if "notas_individuales" not in st.session_state:
      st.session_state.notas_individuales = {}

    for idx, row in df_alumnos[df_alumnos["Grupo"] == g_sel].iterrows():
      al = row["Alumno"]
      st.markdown(f"### {al}")
      if al not in st.session_state.notas_individuales:
        st.session_state.notas_individuales[al] = {}

      for c in criterios_individuales:
        val_i_act = st.session_state.notas_individuales[al].get(
            c["criteri"], 7.0
        )
        st.session_state.notas_individuales[al][c["criteri"]] = st.slider(
            f"{al} - {c['criteri']}",
            0.0,
            10.0,
            val_i_act,
            0.5,
            key=f"ind_{al}_{c['criteri']}",
        )

      feed_act = st.session_state.get(f"feed_{al}", "")
      st.text_area(f"Feedback per a {al}", feed_act, key=f"feed_{al}")
      st.markdown("---")

  # 3. Informes Grups
  with tab3:
    st.header("Informes per a Grups")
    g_inf = st.selectbox("Tria grup:", options=grupos, key="inf_g")
    notas_grupales = st.session_state.get("notas_grupales", {})
    stored_i = st.session_state.get("notas_individuales", {})

    pesos_g = sum([c["pes"] for c in RUBRICA if c["tipus"] == "grupal"])
    pesos_i = sum([c["pes"] for c in RUBRICA if c["tipus"] == "individual"])

    suma_g = sum([
        notas_grupales.get(g_inf, {}).get(c["criteri"], 0)
        * (c["pes"] / pesos_g)
        for c in RUBRICA
        if c["tipus"] == "grupal"
    ])
    st.info(f"Mitjana Grupal Ponderada: **{round(suma_g, 2)} / 10**")

    for idx, row in df_alumnos[df_alumnos["Grupo"] == g_inf].iterrows():
      al = row["Alumno"]
      suma_i = sum([
          stored_i.get(al, {}).get(c["criteri"], 0) * (c["pes"] / pesos_i)
          for c in RUBRICA
          if c["tipus"] == "individual"
      ])
      n_fin = (suma_g * pesos_g) + (suma_i * pesos_i)
      st.markdown(f"- **{al}**: Nota Final = `🎯 {round(n_fin, 2)}`")
      st.write(
          f"  *Feedback:* {st.session_state.get(f'feed_{al}', 'Sense comentaris.')}"
      )

  # 4. Docent Global
  with tab4:
    st.header("Resum General de Classe i Llista de PINs")
    st.dataframe(df_alumnos, use_container_width=True)

    if st.button("Calcular resum de notes"):
      res = []
      notas_grupales = st.session_state.get("notas_grupales", {})
      stored_i = st.session_state.get("notas_individuales", {})
      pesos_g = sum([c["pes"] for c in RUBRICA if c["tipus"] == "grupal"])
      pesos_i = sum([c["pes"] for c in RUBRICA if c["tipus"] == "individual"])

      for idx, row in df_alumnos.iterrows():
        al = row["Alumno"]
        gr = row["Grupo"]
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
        res.append(
            {"Alumno": al, "Grupo": gr, "Nota Final": round(nfin, 2)}
        )

      df_res = pd.DataFrame(res)
      st.dataframe(df_res, use_container_width=True)

  # 5. Portal Alumnes des de vista docent
  with tab5:
    st.info(
        "Aquesta és la vista que tindrà l'alumnat en entrar sense la contrasenya"
        " docent."
    )

else:
  # --- VISTA EXCLUSIVA PER A L'ALUMNAT (Només el portal amb PIN) ---
  st.title("🔒 Portal de Consulta de Notes")
  st.markdown(
      "Introdueix el teu nom i el teu **PIN de 4 xifres** per veure la teva"
      " qualificació de forma privada."
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

      ng = sum([
          notas_grupales.get(gr_al, {}).get(c["criteri"], 0)
          * (c["pes"] / pesos_g)
          for c in RUBRICA
          if c["tipus"] == "grupal"
      ])
      ni = sum([
          stored_i.get(al_ing, {}).get(c["criteri"], 0) * (c["pes"] / pesos_i)
          for c in RUBRICA
          if c["tipus"] == "individual"
      ])
      nfin = (ng * pesos_g) + (ni * pesos_i)

      st.markdown(f"### Hola, **{al_ing}** (Grup {gr_al})")
      st.metric(label="🎯 Qualificació Final", value=f"{round(nfin, 2)} / 10")

      feed = st.session_state.get(
          f"feed_{al_ing}", "Sense comentaris addicionals."
      )
      st.markdown("#### 💬 Comentari del docent:")
      st.info(feed)
    else:
      st.error("❌ PIN incorrecte. Revisa el número de 4 xifres.")
