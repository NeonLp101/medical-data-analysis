# Import der notwendigen Bibliotheken
import streamlit as st  # Streamlit für die Web-UI
import pandas as pd  # Pandas für die Datenverarbeitung
import matplotlib.pyplot as plt  # Matplotlib für Diagramme
import seaborn as sns  # Seaborn für ansprechende Visualisierungen

# Titel der Streamlit-Anwendung
st.title("Datenvisualisierungstool")

# Datei-Upload-Widget, um eine CSV-Datei hochzuladen
uploaded_file = st.file_uploader("Lade eine CSV-Datei hoch", type=["csv"])

# Überprüfung, ob eine Datei hochgeladen wurde
if uploaded_file is not None:
    # Einlesen der CSV-Datei in einen Pandas DataFrame
    df = pd.read_csv(uploaded_file)

    # Anzeigen der Datenübersicht
    st.subheader("Daten-Übersicht")

    # Automatische Erkennung numerischer und kategorischer Spalten
    numerical_columns = df.select_dtypes(include=['number']).columns.tolist()
    categorical_columns = df.select_dtypes(exclude=['number']).columns.tolist()

    # Ausgabe der Spaltentypen
    st.write(f"Numerische Spalten: {numerical_columns}")
    st.write(f"Kategorische Spalten: {categorical_columns}")

    # Option zum Anzeigen statistischer Analysen
    if st.checkbox("Statistische Analyse anzeigen"):
        st.write(df.describe())  # Zeigt Standardstatistiken wie Mittelwert, Standardabweichung etc.

    # Abschnitt für die Erstellung von Diagrammen
    st.subheader("Diagramm-Erstellung")

    # Auswahl des Diagrammtyps
    chart_type = st.selectbox("Wähle einen Diagrammtyp", ["Histogramm", "Scatterplot", "Balkendiagramm"])

    # Auswahl der X-Achse (immer notwendig)
    column_x = st.selectbox("X-Achse", numerical_columns)

    # Auswahl der Y-Achse (nur für Scatterplots und Balkendiagramme erforderlich)
    column_y = None
    if chart_type in ["Scatterplot", "Balkendiagramm"]:
        column_y = st.selectbox("Y-Achse", numerical_columns)

    # Erstellen der Visualisierung basierend auf der Auswahl des Benutzers
    st.subheader("Visualisierung")
    fig, ax = plt.subplots()  # Matplotlib-Plot erstellen

    if chart_type == "Histogramm":
        # Erzeugung eines Histogramms für die gewählte X-Achsen-Spalte
        sns.histplot(df[column_x], bins=30, kde=True, ax=ax)
        ax.set_title(f"Verteilung von {column_x}")
        ax.set_xlabel(column_x)
        ax.set_ylabel("Häufigkeit")

    elif chart_type == "Scatterplot":
        # Erzeugung eines Scatterplots für zwei numerische Variablen
        sns.scatterplot(x=df[column_x], y=df[column_y], alpha=0.7, ax=ax)
        ax.set_title(f"{column_x} vs. {column_y}")
        ax.set_xlabel(column_x)
        ax.set_ylabel(column_y)

    elif chart_type == "Balkendiagramm":
        # Erzeugung eines Balkendiagramms für zwei numerische Variablen
        sns.barplot(x=df[column_x], y=df[column_y], ax=ax)
        ax.set_title(f"Balkendiagramm: {column_x} vs. {column_y}")
        ax.set_xlabel(column_x)
        ax.set_ylabel(column_y)

    # Das erstellte Diagramm in Streamlit anzeigen
    st.pyplot(fig)
