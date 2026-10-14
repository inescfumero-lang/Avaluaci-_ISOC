import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Avaluació per Rúbrica i Generador d'Informes",
    page_icon="📊",
    layout="wide"
)

st.title("🎓 Aplicació d'Avaluació per Rúbrica i Generador d'Informes")
st.markdown(
    "Eina integral per avaluar projectes mixtes (grupal e individual), "
    "generar **informes individuals per compartir amb l'alumnat** i un **informe docent global**."
)

# --- DEFINICIÓ DE LA RÚBRICA ---
RUBRICA = [
    {
        "criteri": "Presentació visual",
        "tipus": "grupal",
        "pes": 0.10,
        "nivells": {
            "1-2": "La presentació és desorganitzada, poc llegible o incompleta.",
            "3-4": "Organització poc clara. Massa text o recursos inadequats.",
            "5-6": "Entenedora i amb estructura bàsica.",
            "7-8": "Ben estructurada, visualment coherent.",
            "9-10": "Molt clara, atractiva i coherent."
        }
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
            "9-10": "Cap falta d’ortografia (0 faltes)."
        }
    },
    {
        "criteri": "Aprofundiment",
        "tipus": "grupal",
        "pes": 0.25,
        "nivells": {
            "1-2": "Contingut molt superficial o amb errors conceptuals.",
            "3-4": "Informació bàsica poc desenvolupada.",
            "5-6": "Desenvolupa característiques principals (anàlisi limitada).",
            "7-8": "Aprofundeix i explica conseqüències amb exemples.",
            "9-10": "Anàlisi crítica i ben fonamentada."
        }
    },
    {
        "criteri": "Repartiment equitatiu de l’exposició",
        "tipus": "grupal",
        "pes": 0.10,
        "nivells": {
            "1-2": "Participació molt desigual.",
            "3-4": "Repartiment força desigual en temps i implicació.",
            "5-6": "Tots participen però el temps o contingut és irregular.",
            "7-8": "Participació equilibrada entre tots els membres.",
            "9-10": "Temps i contingut molt equilibrats. Transicions fluides."
        }
    },
    {
        "criteri": "Expressió oral en català",
        "tipus": "individual",
        "pes": 0.20,
        "nivells": {
            "1-2": "Moltes dificultats. Discurs poc comprensible o molt llegit.",
            "3-4": "Poca fluïdesa i errors freqüents.",
            "5-6": "De manera comprensible, amb algunes vacil·lacions.",
            "7-8": "Amb fluïdesa, claredat i correcció general.",
            "9-10": "Molta fluïdesa, seguretat i precisió."
        }
    },
    {
        "criteri": "Domini del que s’explica",
        "tipus": "individual",
        "pes": 0.25,
        "nivells": {
            "1-2": "Desconeixement important. Llegeix gairebé tot.",
            "3-4": "Coneix alguns conceptes però presenta confusions.",
            "5-6": "Comprensió bàsica, necessita consultar apunts.",
            "7-8": "Bon coneixement, ho explica amb les seves paraules.",
            "9-10": "Domini sòlid, precisió i respon adequadament."
        }
    }
]

criterios_grupales = [c for c in RUBRICA if c["tipus"] == "grupal"]
criterios_individuales = [c for c in RUBRICA if c["tipus"] == "individual"]

# --- BARRA LATERAL: ENTRADA DE DADES ---
st.sidebar.header("1. Configuració de Grups i Alumnes")
st.sidebar.markdown("Introdueix un alumne per línia (`Nom, Grup`):")

default_text = "Anna Pérez, Grup A\nCarlos Gómez, Grup A\nLucía Martínez, Grup B\nMarcos Ruiz, Grup B"
input_alumnos = st.sidebar.text_area("Llistat d'alumnes", default_text, height=140)

lista_alumnos = []
for linea in input_alumnos.split("\n"):
    if "," in linea:
        partes = linea.split(",")
        lista_alumnos.append({"Alumno": partes[0].strip(), "Grupo": partes[1].strip()})

df_alumnos = pd.DataFrame(lista_alumnos)

if df_alumnos.empty:
    st.warning("Afegeix alumnes i grups a la barra lateral per començar.")
else:
    grupos = df_alumnos["Grupo"].unique()

    # Pestanyes principals de treball
    tab1, tab2, tab3, tab4 = st.tabs([
        "1️⃣ Avaluació Grupal", 
        "2️⃣ Avaluació Individual", 
        "3️⃣ Informes Individuals (Alumnat)", 
        "4️⃣ Informe Global (Docent)"
    ])

    # --- TAB 1: AVALUACIÓ GRUPAL ---
    with tab1:
        st.header("👥 Avaluació de la Part Grupal")
        notas_grupales = {}
        comentarios_grupales = {}

        for grupo in grupos:
            st.subheader(f"Grup: {grupo}")
            notas_grupales[grupo] = {}
            
            for c in criterios_grupales:
                with st.expander(f"{c['criteri']} (Pes: {int(c['pes']*100)}%)"):
                    st.caption(" **Nivells d'orientació:** " + " | ".join([f"**{k}**: {v}" for k, v in c["nivells"].items()]))
                    nota = st.slider(f"Nota (0-10) - {grupo} - {c['criteri']}", 0.0, 10.0, 7.0, 0.5, key=f"g_{grupo}_{c['criteri']}")
                    notas_grupales[grupo][c['criteri']] = nota
            
            comentarios_grupales[grupo] = st.text_input(f"💬 Comentari/Feedback grupal per a {grupo}:", key=f"com_g_{grupo}")
            st.markdown("---")

    # --- TAB 2: AVALUACIÓ INDIVIDUAL ---
    with tab2:
        st.header("👤 Avaluació de la Part Individual")
        notas_individuales = {}
        comentarios_individuales = {}

        for idx, row in df_alumnos.iterrows():
            alumno = row["Alumno"]
            grupo = row["Grupo"]
            st.markdown(f"### 🧑‍🎓 {alumno} *(Grup: {grupo})*")
            notas_individuales[alumno] = {}

            for c in criterios_individuales:
                with st.expander(f"{c['criteri']} (Pes: {int(c['pes']*100)}%)"):
                    st.caption(" **Nivells d'orientació:** " + " | ".join([f"**{k}**: {v}" for k, v in c["nivells"].items()]))
                    nota = st.slider(f"Nota (0-10) - {alumno} - {c['criteri']}", 0.0, 10.0, 7.0, 0.5, key=f"ind_{alumno}_{c['criteri']}")
                    notas_individuales[alumno][c['criteri']] = nota
            
            comentarios_individuales[alumno] = st.text_input(f"💬 Comentari personalitzat per a {alumno}:", key=f"com_ind_{alumno}")
            st.markdown("---")

    # --- CÀLCUL DE RESULTATS GENERALS ---
    resultados = []
    for idx, row in df_alumnos.iterrows():
        alumno = row["Alumno"]
        grupo = row["Grupo"]

        # Càlculs grupal
        sum_g = sum([notas_grupales[grupo][c["criteri"]] * c["pes"] for c in criterios_grupales])
        peso_g = sum([c["pes"] for c in criterios_grupales])
        nota_g = sum_g / peso_g if peso_g > 0 else 0

        # Càlculs individual
        sum_i = sum([notas_individuales[alumno][c["criteri"]] * c["pes"] for c in criterios_individuales])
        peso_i = sum([c["pes"] for c in criterios_individuales])
        nota_i = sum_i / peso_i if peso_i > 0 else 0

        # Nota final global (suma ponderada)
        nota_final = (sum_g + sum_i)  # Atès que la suma de tots els pesos de la rúbrica és 1.0 (100%)

        resultados.append({
            "Alumno": alumno,
            "Grupo": grupo,
            "Nota Grupal": round(nota_g, 2),
            "Nota Individual": round(nota_i, 2),
            "Nota Final": round(nota_final, 2)
        })

    df_resultados = pd.DataFrame(resultados)

    # --- TAB 3: INFORMES INDIVIDUALS PER ALUMNES ---
    with tab3:
        st.header("📄 Generador d'Informes Individuals (Per compartir amb l'alumnat)")
        st.markdown("Selecciona un alumne per veure, imprimir o desar la seva fitxa de retroalimentació personalitzada.")

        alumne_seleccionat = st.selectbox("Selecciona un alumne:", df_alumnos["Alumno"].tolist())
        
        if alumne_seleccionat:
            grupo_alumne = df_alumnos[df_alumnos["Alumno"] == alumne_seleccionat]["Grupo"].values[0]
            dades_alumne = df_resultados[df_resultados["Alumno"] == alumne_seleccionat].iloc[0]

            # Contenidor per a la fitxa d'avaluació
            st.markdown("---")
            report_md = f"""
            # 📄 Fitxa d'Avaluació del Projecte
            **Alumne/a:** {alumne_seleccionat}  
            **Grup:** {grupo_alumne}  

            ---

            ### 📊 Resum de la Qualificació
            * **Nota Grupal (45%):** `{dades_alumne['Nota Grupal']} / 10`
            * **Nota Individual (55%):** `{dades_alumne['Nota Individual']} / 10`
            * **🎯 NOTA FINAL GLOBAL:** **`{dades_alumne['Nota Final']} / 10`**

            ---

            ### 📋 Desglossament de Criteris

            #### 👥 Criteris Grupals
            """

            for c in criterios_grupales:
                val = notas_grupales[grupo_alumne][c["criteri"]]
                report_md += f"- **{c['criteri']}** (Pes {int(c['pes']*100)}%): **{val}/10**\n"
            
            if comentarios_grupales[grupo_alumne]:
                report_md += f"\n> **Observacions del grup:** {comentarios_grupales[grupo_alumne]}\n"

            report_md += "\n#### 👤 Criteris Individuals\n"
            for c in criterios_individuales:
                val = notas_individuales[alumne_seleccionat][c["criteri"]]
                report_md += f"- **{c['criteri']}** (Pes {int(c['pes']*100)}%): **{val}/10**\n"

            if comentarios_individuales[alumne_seleccionat]:
                report_md += f"\n> **Feedback individual:** {comentarios_individuales[alumne_seleccionat]}\n"

            # Mostrar informe en pantalla
            st.markdown(report_md)

            # Botó de descàrrega de l'informe individual en Markdown
            st.download_button(
                label=f"📥 Descarregar Informe de {alumne_seleccionat} (.txt / .md)",
                data=report_md,
                file_name=f"Informe_{alumne_seleccionat.replace(' ', '_')}.md",
                mime="text/markdown"
            )

    # --- TAB 4: INFORME GLOBAL PER AL DOCENT ---
    with tab4:
        st.header("📊 Informe General i Resum Docent")
        st.markdown("Vista completa de les qualificacions de tots els grups i alumnes.")

        col1, col2, col3 = st.columns(3)
        col1.metric("Mitjana Global de la Classe", round(df_resultados["Nota Final"].mean(), 2))
        col2.metric("Nota Més Alta", df_resultados["Nota Final"].max())
        col3.metric("Nota Més Baixa", df_resultados["Nota Final"].min())

        st.subheader("📋 Taula Completa de Qualificacions")
        st.dataframe(df_resultados, use_container_width=True)

        st.subheader("📈 Mitjanes per Grup")
        df_grups = df_resultados.groupby("Grupo")[["Nota Grupal", "Nota Individual", "Nota Final"]].mean().round(2)
        st.dataframe(df_grups, use_container_width=True)

        # Descàrrega de la taula completa en CSV per al docent
        csv_global = df_resultados.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Descarregar Taula Completa Docent (CSV)",
            data=csv_global,
            file_name="Informe_General_Docent.csv",
            mime="text/csv"
        )
