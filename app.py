import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Wimbledon 2026", layout="wide")

#CONFIGURAZIONI FILE
FILE_SALVATAGGIO = "pronostici_wimbledon.csv"
FILE_RISULTATI = "risultati_ufficiali.csv"
PASSWORD_ADMIN = "secco123"

# STILE GRAFICO AVANZATO
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght=400;700;900&display=swap');
    
    .stApp { background-color: #f0f7f0; }
    body, .stMarkdown p, label { font-family: 'Montserrat', sans-serif !important; }

    /* Titoli */
    .wimbledon-title {
        color: #536D33 !important; text-align: center; font-weight: 900 !important;
        font-size: calc(2.2rem + 2vw) !important; margin-top: 15px; margin-bottom: 0px;
        text-transform: uppercase; letter-spacing: 2px; line-height: 1.1;
    }
    .wimbledon-subtitle {
        text-align: center; font-weight: 700; color: #4C336C;
        font-size: calc(1.0rem + 0.4vw); letter-spacing: 2px; text-transform: uppercase; margin-bottom: 10px; opacity: 0.9;
    }
    .wimbledon-deadline-notice {
        text-align: center; font-weight: 700; color: #D32F2F; font-size: 1rem;
        text-transform: uppercase; letter-spacing: 1px; margin-bottom: 5px; padding: 0 10px;
    }
    .wimbledon-paride-notice {
        text-align: center; font-weight: 700; color: #4C336C; font-size: 1rem;
        text-transform: uppercase; letter-spacing: 1px; margin-bottom: 35px; padding: 0 10px;
    }
    
    /* Logo */
    .wimbledon-logo {
        display: block; margin: 20px auto 0px auto; width: 90px; height: 90px;
        background: conic-gradient(#536D33 0% 50%, #4C336C 50% 100%);
        border-radius: 50%; border: 4px solid #ffffff; box-shadow: 0px 4px 12px rgba(0,0,0,0.08); position: relative;
    }
    .wimbledon-logo::before {
        content: ''; position: absolute; top: 50%; left: 5%; width: 90%; height: 4px; background: white; transform: translateY(-50%);
    }

    /* Regolamento */
    .rules-always-visible {
        background-color: #ffffff; padding: 20px; border-radius: 4px; border-left: 6px solid #536D33;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.04); margin-bottom: 35px;
    }
    .rules-title { font-weight: 900; font-size: 1.4rem; color: #536D33; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 15px; }
    .rules-list { font-size: 1.05rem; color: #4C336C; line-height: 1.8; font-weight: 700; list-style-type: none; padding-left: 0; }
    .rules-item { margin-bottom: 10px; border-bottom: 1px dashed #e0e0e0; padding-bottom: 8px; }
    .rules-item-important { margin-bottom: 10px; border-bottom: 1px dashed #e0e0e0; padding-bottom: 8px; color: #D32F2F !important; }
    .rules-marker { color: #536D33; margin-right: 10px; }
    .rules-marker-important { color: #D32F2F; margin-right: 10px; }

    /* Testo a capo forzato ed espanso nelle tabelle per smartphone */
    div[data-testid="stDataFrame"] td, div[data-testid="stDataFrame"] th {
        white-space: normal !important;
        word-wrap: break-word !important;
        line-height: 1.4 !important;
    }

    label p { font-size: 1.1rem !important; font-weight: 700 !important; color: #536D33 !important; text-transform: uppercase; letter-spacing: 1px; }
    h3 { font-size: 1.6rem !important; font-weight: 900; color: #4C336C !important; text-transform: uppercase; letter-spacing: 1px; }
    
    /* Bottoni */
    div.stButton > button:first-child {
        background-color: #536D33 !important; color: white !important; font-weight: 900 !important;
        text-transform: uppercase !important; letter-spacing: 2px !important; border-radius: 4px !important;
        border: none !important; padding: 12px 25px !important; font-size: 1rem !important; transition: 0.3s ease; width: 100%; max-width: 350px;
    }
    div.stButton > button:first-child:hover { background-color: #4C336C !important; }
    .btn-elimina > div div.stButton > button:first-child { background-color: #A32A2A !important; }
    .btn-elimina > div div.stButton > button:first-child:hover { background-color: #D32F2F !important; }
    </style>
    """, unsafe_allow_html=True)

# LISTA TOP 100 ATP
lista_atp = [
    "Jannik Sinner", "Carlos Alcaraz", "Alexander Zverev", "Felix Auger-Aliassime", 
    "Ben Shelton", "Alex De Minaur", "Novak Djokovic", "Daniil Medvedev", 
    "Taylor Fritz", "Flavio Cobolli", "Alexander Bublik", "Jiri Lehecka", 
    "Andrey Rublev", "Casper Ruud", "Karen Khachanov", "Lorenzo Musetti", 
    "Jakub Mensik", "Luciano Darderi", "Learner Tien", "Valentin Vacherot", 
    "Arthur Fils", "Alejandro Davidovich Fokina", "Rafael Jodar", "Arthur Rinderknech", 
    "Joao Fonseca", "Frances Tiafoe", "Francisco Cerundolo", "Tommy Paul", 
    "Cameron Norrie", "Tomas Martin Etcheverry", "Alejandro Tabilo", "Brandon Nakashima", 
    "Ugo Humbert", "Matteo Arnaldi", "Ignacio Buse", "Corentin Moutet", 
    "Alexander Blockx", "Alex Michelsen", "Mariano Navone", "Zizou Bergs", 
    "Tallon Griekspoor", "Denis Shapovalov", "Tomas Machac", "Jaume Munar", 
    "Juan Manuel Cerundolo", "Adrian Mannarino", "Marin Cilic", "Matteo Berrettini", 
    "Miomir Kecmanovic", "Nuno Borges", "Raphael Collignon", "Thiago Agustin Tirante", 
    "Terence Atmane", "Gabriel Diallo", "Botic Van De Zandschulp", "Sebastian Baez", 
    "Camilo Ugo Carabelli", "Martin Landaluce", "Yannick Hanfmann", "Sebastian Korda", 
    "Fabian Marozsan", "Zachary Svajda", "Roman Andres Burruchaga", "Holger Rune", 
    "Vit Kopriva", "Lorenzo Sonego", "Ethan Quinn", "Hamad Medjedovic", 
    "Aleksandar Kovacevic", "Dino Prizmic", "Pablo Carreno-Busta", "Adolfo Daniel Vallejo", 
    "Jenson Brooksby", "Valentin Royer", "Marton Fucsovics", "Kamil Majchrzak", 
    "Jan-Lennard Struff", "Mattia Bellucci", "James Duckworth", "Marco Trungelliti", 
    "Arthur Cazaux", "Daniel Merida Aguilar", "Jesper De Jong", "Stefanos Tsitsipas", 
    "Daniel Altmaier", "Reilly Opelka", "Alexei Popyrin", "Damir Džumhur", 
    "Alexander Shevchenko", "Quentin Halys", "Eliot Spizzirri", "Yibing Wu", 
    "Patrick Kypson", "Emilio Nava", "Benjamin Bonzi", "Aleksandar Vukić", 
    "Adam Walton", "Rinky Hijikata", "Hubert Hurkacz", "Luca Van Assche", 
    "Altro / Qualificato"
]

lista_con_vuoto = ["-"] + lista_atp
lista_italiani_quarti = ["-"] + [str(i) for i in range(9)] 
lista_italiani_primo = ["-"] + [str(i) for i in range(11)] 
lista_italiani_ritirati = ["-"] + [str(i) for i in range(11)] 
lista_set_semifinali = ["-"] + [str(i) for i in range(6, 11)] 
lista_tie_break = ["-"] + [str(i) for i in range(6)] 

# FUNZIONI FILE
def carica_pronostici():
    if os.path.exists(FILE_SALVATAGGIO):
        try:
            return pd.read_csv(FILE_SALVATAGGIO, dtype={'Password': str, 'Italiani ai Quarti': str, 'Italiani fuori al Primo': str, 'Italiani Ritirati': str, 'Set Semifinali': str, 'Tie Break': str}).to_dict(orient="records")
        except:
            return []
    return []

def salva_tutti_i_pronostici(lista_pronostici):
    df = pd.DataFrame(lista_pronostici)
    df.to_csv(FILE_SALVATAGGIO, index=False, encoding="utf-8")

def carica_risultati_ufficiali():
    if os.path.exists(FILE_RISULTATI):
        try:
            df = pd.read_csv(FILE_RISULTATI)
            return df.iloc[0].to_dict()
        except:
            pass
    return {"Quarti": "", "Semi": "", "Finale": "", "Vincitore": "", "Italiani ai Quarti": "-", "Italiani fuori al Primo": "-", "Italiani Ritirati": "-", "Set Semifinali": "-", "Durata": "-", "Tie Break": "-"}

def salva_risultati_ufficiali(dati_risultati):
    df = pd.DataFrame([dati_risultati])
    df.to_csv(FILE_RISULTATI, index=False, encoding="utf-8")

# CALCOLO PUNTEGGI
def calcola_punteggio_utente(p, uff):
    punti = 0
    if not uff["Quarti"] and not uff["Semi"] and not uff["Vincitore"] and uff["Italiani ai Quarti"] == "-" and uff["Italiani fuori al Primo"] == "-" and uff.get("Italiani Ritirati", "-") == "-" and uff.get("Set Semifinali", "-") == "-" and uff["Durata"] == "-" and uff.get("Tie Break", "-") == "-":
        return 0
        
    if uff["Quarti"]:
        lista_uff_q = [x.strip().lower() for x in str(uff["Quarti"]).split(",")]
        lista_ut_q = [x.strip().lower() for x in str(p["Quarti"]).split(",")]
        for atleta in lista_ut_q:
            if atleta in lista_uff_q: punti += 5
            
    if uff["Semi"]:
        lista_uff_s = [x.strip().lower() for x in str(uff["Semi"]).split(",")]
        lista_ut_s = [x.strip().lower() for x in str(p["Semi"]).split(",")]
        for atleta in lista_ut_s:
            if atleta in lista_uff_s: punti += 10
            
    if uff["Finale"] and "vs" in str(uff["Finale"]):
        lista_uff_f = [x.strip().lower() for x in str(uff["Finale"]).split("vs")]
        lista_ut_f = [x.strip().lower() for x in str(p["Finale"]).split("vs")]
        for atleta in lista_ut_f:
            if atleta in lista_uff_f: punti += 15
            
    if uff["Vincitore"] and str(p["Vincitore"]).strip().lower() == str(uff["Vincitore"]).strip().lower():
        punti += 25
        
    if uff["Italiani ai Quarti"] != "-" and str(p["Italiani ai Quarti"]) == str(uff["Italiani ai Quarti"]):
        punti += 10

    if "Italiani fuori al Primo" in uff and uff["Italiani fuori al Primo"] != "-" and str(p.get("Italiani fuori al Primo", "-")) == str(uff["Italiani fuori al Primo"]):
        punti += 10

    if "Italiani Ritirati" in uff and uff["Italiani Ritirati"] != "-" and str(p.get("Italiani Ritirati", "-")) == str(uff["Italiani Ritirati"]):
        punti += 10
        
    if "Set Semifinali" in uff and uff["Set Semifinali"] != "-" and str(p.get("Set Semifinali", "-")) == str(uff["Set Semifinali"]):
        punti += 10

    if uff["Durata"] != "-" and str(p["Durata"]) == str(uff["Durata"]):
        punti += 10

    if "Tie Break" in uff and uff["Tie Break"] != "-" and str(p.get("Tie Break", "-")) == str(uff["Tie Break"]):
        punti += 10
        
    return punti

# INTESTAZIONE
st.markdown('<div class="wimbledon-logo"></div>', unsafe_allow_html=True)
st.markdown('<div class="wimbledon-title">Wimbledon 2026</div>', unsafe_allow_html=True)
st.markdown('<div class="wimbledon-subtitle">Championships Predictor De Noartri</div>', unsafe_allow_html=True)
st.markdown('<div class="wimbledon-deadline-notice">Termine ultimo di consegna: Domenica 28 Giugno</div>', unsafe_allow_html=True)
st.markdown('<div class="wimbledon-paride-notice">PUO\' PARTECIPARE ANCHE PARIDE</div>', unsafe_allow_html=True)

# REGOLAMENTO
st.markdown("""
<div class="rules-always-visible">
    <div class="rules-title">§ Regolamento Ufficiale e Punteggi</div>
    <ul class="rules-list">
        <li class="rules-item-important"><span class="rules-marker-important">⚠</span> <b>Scadenza Tassativa:</b> I PRONOSTICI devono essere inviati entro e non oltre <b>Domenica 28 Giugno</b>.</li>
        <li class="rules-item-important"><span class="rules-marker-important">⚠</span> <b>Modifica e Password:</b> Puoi eliminare e rifare il tuo PRONOSTICO fino alla scadenza usando la tua password personale in fondo alla pagina.</li>
        <li class="rules-item-important"><span class="rules-marker-important">🔒</span> <b>Vincitore Segreto fino alla fine:</b> Il nome del Campione scelto rimarrà nascosto da un punto interrogativo (<b>?</b>) nella tabella pubblica fino al termine dell'intero torneo.</li>
        <li class="rules-item"><span class="rules-marker">▪</span> <b>LA CAPORETTO AZZURRA:</b> 10 Punti addizionali per chi indovina il numero esatto di italiani eliminati al Primo Turno</li>
        <li class="rules-item"><span class="rules-marker">▪</span> <b>IL DRAMMA DEGLI INFORTUNI:</b> 10 Punti addizionali per chi indovina il numero di italiani ritirati per infortunio nei primi due turni</li>
        <li class="rules-item"><span class="rules-marker">▪</span> <b>Quarti di Finale:</b> 5 Punti per ciascun giocatore indovinato (Selezionare 8 atleti)</li>
        <li class="rules-item"><span class="rules-marker">▪</span> <b>Quota Azzurra:</b> 10 Punti addizionali per il numero esatto di italiani ai Quarti</li>
        <li class="rules-item"><span class="rules-marker">▪</span> <b>Semifinali:</b> 10 Punti per ciascun giocatore indovinato (Selezionare 4 atleti)</li>
        <li class="rules-item"><span class="rules-marker">▪</span> <b>MARATONA SEMIFINALI:</b> 10 Punti addizionali per chi indovina il totale di Set complessivi giocati nelle due semifinali (Scelta da 6 a 10)</li>
        <li class="rules-item"><span class="rules-marker">▪</span> <b>Finalisti:</b> 15 Punti per ciascun finalista esatto</li>
        <li class="rules-item"><span class="rules-marker">▪</span> <b>Vincitore del Torneo:</b> 25 Punti per il corretto pronostico del Campione</li>
        <li class="rules-item"><span class="rules-marker">▪</span> <b>Durata Incontro:</b> 10 Punti addizionali per il numero esatto di Set della Finale</li>
        <li class="rules-item"><span class="rules-marker">▪</span> <b>TENSION TIE-BREAK:</b> 10 Punti addizionali per chi indovina il numero esatto di Tie-Break giocati durante la Finale (Scelta da 0 a 5)</li>
    </ul>
</div>
""", unsafe_allow_html=True)

pronostici_attuali = carica_pronostici()
risultati_uff = carica_risultati_ufficiali()

# --- CLASSIFICA ---
st.subheader("🏆 Classifica Generale in Tempo Reale")
if pronostici_attuali:
    dati_classifica = []
    for p in pronostici_attuali:
        pt = calcola_punteggio_utente(p, risultati_uff)
        dati_classifica.append({"Posizione": 1, "Partecipante": p["Nome e Cognome"], "Punti Totali": pt})
    
    df_classifica = pd.DataFrame(dati_classifica)
    df_classifica = df_classifica.sort_values(by="Punti Totali", ascending=False).reset_index(drop=True)
    df_classifica["Posizione"] = df_classifica["Punti Totali"].rank(ascending=False, method="min").astype(int)
    st.dataframe(df_classifica, use_container_width=True)
else:
    st.info("La classifica verrà generata automaticamente non appena saranno registrati i primi PRONOSTICI.")

st.markdown("<hr>", unsafe_allow_html=True)

# --- ARCHIVIO PUBBLICO CORRETTO (MULTILINEA CON CHIP VISIBILI) ---
st.subheader("📋 Archivio Storico dei PRONOSTICI Registrati")
if pronostici_attuali:
    df_pubblico = pd.DataFrame(pronostici_attuali).copy()
    if "Password" in df_pubblico.columns:
        df_pubblico = df_pubblico.drop(columns=["Password"])
        
    if "Vincitore" in df_pubblico.columns:
        if not risultati_uff["Vincitore"]:
            df_pubblico["Vincitore"] = "🔒 ?"
            
    # Convertiamo le stringhe separate da virgola in liste per renderle visibili
    df_pubblico["Quarti"] = df_pubblico["Quarti"].apply(lambda x: [i.strip() for i in str(x).split(",")] if pd.notna(x) else [])
    df_pubblico["Semi"] = df_pubblico["Semi"].apply(lambda x: [i.strip() for i in str(x).split(",")] if pd.notna(x) else [])
    
    # Configurazione colonne nativa per liste ed elenchi lunghi
    configurazione_colonne = {
        "Quarti": st.column_config.ListColumn("Quarti di Finale", width="large"),
        "Semi": st.column_config.ListColumn("Semifinali", width="medium"),
        "Finale": st.column_config.TextColumn("Finale", width="medium")
    }
    
    st.dataframe(df_pubblico, use_container_width=True, column_config=configurazione_colonne)
else:
    st.info("Nessun PRONOSTICO attualmente registrato nell'archivio di gruppo.")

st.markdown("<hr>", unsafe_allow_html=True)

# --- COMPILAZIONE PRONOSTICO ---
st.subheader("✍️ Compilazione del PRONOSTICO")
col_nome, col_pass = st.columns(2)
with col_nome: nome = st.text_input("Nome e Cognome del Partecipante:", value="")
with col_pass: password = st.text_input("Crea una Password personale (Servirà se vorrai modificarlo):", type="password", value="")

# RIGA SPECIALE ITALIANI
col_caporetto, col_infortuni = st.columns(2)
with col_caporetto:
    italiani_primo = st.selectbox("LA CAPORETTO AZZURRA (Quanti italiani eliminati al primo turno?):", lista_italiani_primo)
with col_infortuni:
    italiani_ritirati = st.selectbox("IL DRAMMA DEGLI INFORTUNI (Quanti italiani ritirati per infortunio nei primi due turni?):", lista_italiani_ritirati)

st.markdown("<br>", unsafe_allow_html=True)

# QUARTI E QUOTA AZZURRA
col_q, col_qa = st.columns(2)
with col_q: 
    quarti = st.multiselect("Quarti di Finale (Selezionare 8 atleti):", lista_atp, default=None)
with col_qa:
    quanti_italiani = st.selectbox("Quanti tennisti italiani si qualificheranno ai Quarti? (Da 0 a 8):", lista_italiani_quarti)

st.markdown("<br>", unsafe_allow_html=True)

# SEMIFINALI E MARATONA SEMIFINALI
col_s, col_ms = st.columns(2)
with col_s:
    semifinali = st.multiselect("Semifinali (Selezionare 4 atleti):", lista_atp, default=None)
with col_ms:
    set_semifinali = st.selectbox("MARATONA SEMIFINALI (Quanti Set TOTALI giocati nelle due semifinali?):", lista_set_semifinali)

st.markdown("<br>", unsafe_allow_html=True)

# FINALISTI
col_f1, col_f2 = st.columns(2)
with col_f1: fin1 = st.selectbox("Primo Finalista:", lista_con_vuoto, key="k1")
with col_f2: fin2 = st.selectbox("Secondo Finalista:", lista_con_vuoto, key="k2")

opzioni_vincitore = ["-"]
if fin1 != "-" and fin2 != "-": opzioni_vincitore = ["-", fin1, fin2]
elif fin1 != "-": opzioni_vincitore = ["-", fin1]
elif fin2 != "-": opzioni_vincitore = ["-", fin2]

vincitore = st.selectbox("Campione del Torneo (Rimarrà segreto fino alla fine del torneo!):", opzioni_vincitore)

# RIGHE DURATA FINALE E TIE-BREAK
col_dur_fin, col_tie_fin = st.columns(2)
with col_dur_fin:
    durata = st.selectbox("Numero totale di Set previsti per la finale:", ["-", "3 Set", "4 Set", "5 Set"])
with col_tie_fin:
    tie_break = st.selectbox("TENSION TIE-BREAK (Quanti Tie-Break complessivi verranno giocati in finale? - Da 0 a 5):", lista_tie_break)


if st.button("Registra PRONOSTICO"):
    nomi_registrati = [p["Nome e Cognome"].strip().lower() for p in pronostici_attuali]
    if not nome.strip(): st.error("Inserimento richiesto: Specificare il nome e il cognome.")
    elif not password.strip(): st.error("Inserimento richiesto: Creare una password personale.")
    elif nome.strip().lower() in nomi_registrati: st.error("Nome già presente! Se vuoi modificarlo, usa la sezione in fondo.")
    elif italiani_primo == "-": st.error("Specificare il valore per LA CAPORETTO AZZURRA.")
    elif italiani_ritirati == "-": st.error("Specificare il valore per IL DRAMMA DEGLI INFORTUNI.")
    elif len(quarti) != 8: st.error("Selezionare esattamente 8 quartifinalisti.")
    elif len(semifinali) != 4: st.error("Selezionare esattamente 4 semifinalisti.")
    elif fin1 == "-" or fin2 == "-": st.error("Selezionare entrambi i finalisti.")
    elif fin1 == fin2: st.error("I due finalisti devono essere giocatori distinti.")
    elif vincitore == "-": st.error("Scegliere il vincitore del torneo.")
    elif quanti_italiani == "-": st.error("Specificare il numero previsto di italiani ai quarti.")
    elif set_semifinali == "-": st.error("Specificare il totale set previsti per le semifinali.")
    elif durata == "-": st.error("Specificare la durata della finale in Set.")
    elif tie_break == "-": st.error("Specificare il numero di tie-break per la finale.")
    else:
        nuovo_p = {
            "Nome e Cognome": nome.strip(), "Password": str(password), "Quarti": ", ".join(quarti),
            "Semi": ", ".join(semifinali), "Finale": f"{fin1} vs {fin2}", "Vincitore": vincitore,
            "Italiani ai Quarti": quanti_italiani, "Italiani fuori al Primo": italiani_primo, 
            "Italiani Ritirati": italiani_ritirati, "Set Semifinali": set_semifinali, "Durata": durata,
            "Tie Break": tie_break
        }
        pronostici_attuali.append(nuovo_p)
        salva_tutti_i_pronostici(pronostici_attuali)
        st.success("Il tuo PRONOSTICO è stato registrato con successo!")
        st.rerun()

# --- MODIFICA ---
st.markdown("<hr>", unsafe_allow_html=True)
st.subheader("🛠️ Modifica il tuo PRONOSTICO")
if pronostici_attuali:
    lista_nomi_iscritti = ["-"] + [p["Nome e Cognome"] for p in pronostici_attuali]
    col_del_nome, col_del_pass = st.columns(2)
    with col_del_nome: utente_da_eliminare = st.selectbox("Seleziona il tuo Nome per cancellare:", lista_nomi_iscritti)
    with col_del_pass: password_verifica = st.text_input("Inserisci la tua Password:", type="password", key="pass_del")
    
    st.markdown('<div class="btn-elimina">', unsafe_allow_html=True)
    if st.button("Elimina il mio PRONOSTICO"):
        if utente_da_eliminare == "-": st.error("Seleziona il tuo Nome e Cognome.")
        elif not password_verifica.strip(): st.error("Inserisci la password.")
        else:
            trovato, corretta = False, False
            for p in pronostici_attuali:
                if p["Nome e Cognome"] == utente_da_eliminare:
                    trovato = True
                    if str(p["Password"]) == str(password_verifica):
                        corretta = True
                        pronostici_attuali.remove(p)
                        break
            if not trovato: st.error("Utente non trovato.")
            elif not corretta: st.error("Password errata!")
            else:
                salva_tutti_i_pronostici(pronostici_attuali)
                st.success("Pronostico rimosso! Compila pure il modulo sopra per inserirne uno nuovo.")
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- ADMIN PANELS ---
st.markdown("<hr>", unsafe_allow_html=True)
with st.expander("⚙️ Pannello Amministratore (Inserimento Risultati Ufficiali)"):
    pass_admin_input = st.text_input("Inserisci Password di Amministrazione:", type="password")
    if pass_admin_input == PASSWORD_ADMIN:
        st.write("### Aggiorna i Risultati del Torneo Reale")
        
        adm_ita_primo = st.selectbox("LA CAPORETTO AZZURRA (Numero finale di Italiani eliminati al Primo Turno):", lista_italiani_primo, index=lista_italiani_primo.index(risultati_uff["Italiani fuori al Primo"]) if "Italiani fuori al Primo" in risultati_uff and risultati_uff["Italiani fuori al Primo"] in lista_italiani_primo else 0)
        adm_ita_ritirati = st.selectbox("IL DRAMMA DEGLI INFORTUNI (Numero finale di Italiani ritirati nei primi due turni):", lista_italiani_ritirati, index=lista_italiani_ritirati.index(risultati_uff["Italiani Ritirati"]) if "Italiani Ritirati" in risultati_uff and risultati_uff["Italiani Ritirati"] in lista_italiani_ritirati else 0)
        
        def_q = [x.strip() for x in risultati_uff["Quarti"].split(", ")] if isinstance(risultati_uff["Quarti"], str) and pd.notna(risultati_uff["Quarti"]) else None
        adm_q = st.multiselect("Quanti e quali atleti sono passati ai Quarti reali?", lista_atp, default=def_q)
        
        def_s = [x.strip() for x in risultati_uff["Semi"].split(", ")] if risultati_uff["Semi"] else None
        adm_s = st.multiselect("Quali atleti sono passati in Semifinale reali?", lista_atp, default=def_s)
        
        lista_f_uff = risultati_uff["Finale"].split(" vs ") if (risultati_uff["Finale"] and " vs " in risultati_uff["Finale"]) else ["-", "-"]
        adm_f1 = st.selectbox("Finalista Reale 1:", lista_con_vuoto, index=lista_con_vuoto.index(lista_f_uff[0]) if lista_f_uff[0] in lista_con_vuoto else 0)
        adm_f2 = st.selectbox("Finalista Reale 2:", lista_con_vuoto, index=lista_con_vuoto.index(lista_f_uff[1]) if lista_f_uff[1] in lista_con_vuoto else 0)
        
        adm_v = st.selectbox("Vincitore Reale del Torneo:", lista_con_vuoto, index=lista_con_vuoto.index(risultati_uff["Vincitore"]) if risultati_uff["Vincitore"] in lista_con_vuoto else 0)
        adm_ita = st.selectbox("Numero esatto finale di Italiani arrivati ai Quarti:", lista_italiani_quarti, index=lista_italiani_quarti.index(risultati_uff["Italiani ai Quarti"]) if risultati_uff["Italiani ai Quarti"] in lista_italiani_quarti else 0)
        adm_set_semi = st.selectbox("MARATONA SEMIFINALI (Numero totale effettivo di set giocati nelle due semifinali):", lista_set_semifinali, index=lista_set_semifinali.index(risultati_uff["Set Semifinali"]) if "Set Semifinali" in risultati_uff and risultati_uff["Set Semifinali"] in lista_set_semifinali else 0)
        adm_durata = st.selectbox("Durata in set dell'incontro finale:", ["-", "3 Set", "4 Set", "5 Set"], index=["-", "3 Set", "4 Set", "5 Set"].index(risultati_uff["Durata"]))
        adm_tie = st.selectbox("TENSION TIE-BREAK (Numero totale effettivo di tie-break giocati in finale):", lista_tie_break, index=lista_tie_break.index(risultati_uff["Tie Break"]) if "Tie Break" in risultati_uff and risultati_uff["Tie Break"] in lista_tie_break else 0)
        
        if st.button("Salva Risultati Ufficiali"):
            risultati_salva = {
                "Quarti": ", ".join(adm_q), "Semi": ", ".join(adm_s),
                "Finale": f"{adm_f1} vs {adm_f2}" if adm_f1 != "-" and adm_f2 != "-" else "",
                "Vincitore": adm_v if adm_v != "-" else "", "Italiani ai Quarti": adm_ita, 
                "Italiani fuori al Primo": adm_ita_primo, "Italiani Ritirati": adm_ita_ritirati,
                "Set Semifinali": adm_set_semi, "Durata": adm_durata, "Tie Break": adm_tie
            }
            salva_risultati_ufficiali(risultati_salva)
            st.success("Risultati di gioco aggiornati! La classifica si è ricalcolata.")
            st.rerun()
