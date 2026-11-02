import sqlite3
import streamlit as st

# 1. Konfiguracja prostej bazy danych SQLite
def init_db():
  conn = sqlite3.connect('nira.db')
  c = conn.cursor()
  # Tabela dla form
  c.execute('''
        CREATE TABLE IF NOT EXISTS formy (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nazwa TEXT,
            klient TEXT,
            status TEXT
        )
    ''')
  conn.commit()
  conn.close()


init_db()

# 2. Słownik tłumaczeń interfejsu
translations = {
    'Polski': {
        'title': 'System Zarządzania Formami Nira',
        'tab1': '🛠️ Konserwacja, Naprawy i Przeglądy',
        'tab2': '📸 Modyfikacje Form',
        'tab3': '🔬 Próby Form',
        'lang_label': 'Wybierz język / Sprache wählen / Dil seçin',
    },
    'Deutsch': {
        'title': 'Nira Formenenverwaltungs-System',
        'tab1': '🛠️ Wartung, Reparaturen & Inspektionen',
        'tab2': '📸 Formenänderungen',
        'tab3': '🔬 Mustermachen / Erprobung',
        'lang_label': 'Wybierz język / Sprache wählen / Dil seçin',
    },
    'Türkçe': {
        'title': 'Nira Kalıp Yönetim Sistemi',
        'tab1': '🛠️ Bakım, Onarım ve Muayene',
        'tab2': '📸 Kalıp Modifikasyonları',
        'tab3': '🔬 Kalıp Denemeleri',
        'lang_label': 'Wybierz język / Sprache wählen / Dil seçin',
    },
}

# 3. Panel boczny - wybór języka
st.sidebar.title('⚙️ Ustawienia')
selected_lang = st.sidebar.selectbox(
    'Język / Language', ['Polski', 'Deutsch', 'Türkçe']
)
t = translations[selected_lang]

# 4. Nagłówek aplikacji
st.title(t['title'])

# 5. Zakładki główne
tab1, tab2, tab3 = st.tabs([t['tab1'], t['tab2'], t['tab3']])

with tab1:
  st.header(t['tab1'])
  st.write(
      'Tutaj znajdzie się rejestr przeglądów, uwag oraz historia awarii form.'
  )
  # Miejsce na formularze i tabelę przeglądów

with tab2:
  st.header(t['tab2'])
  st.write(
      'Tutaj znajdzie się historia modyfikacji form wraz ze zdjęciami przed i'
      ' po.'
  )
  # Miejsce na wgrywanie zdjęć i opis modyfikacji

with tab3:
  st.header(t['tab3'])
  st.write('Tutaj znajdzie się rejestr prób form i testów technologicznych.')
  # Miejsce na raporty z prób