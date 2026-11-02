import json
import os
import streamlit as st
from PIL import Image

PLIK_BAZY = "baza_form.json"
PLIK_PARAMETROW = "szablon_parametrow.json"

DOMYSLNE_PARAMETRY = [
    {"klucz": "temp_cylindra", "nazwa": "🌡️ Temp. cylindra", "jednostka": "°C"},
    {"klucz": "temp_goracych_kanalow", "nazwa": "🔥 Temp. gorących kanałów", "jednostka": "°C"},
    {"klucz": "droga_1", "nazwa": "📏 Droga wtrysku - profil 1", "jednostka": "mm"},
    {"klucz": "droga_2", "nazwa": "📏 Droga wtrysku - profil 2", "jednostka": "mm"},
    {"klucz": "droga_3", "nazwa": "📏 Droga wtrysku - profil 3", "jednostka": "mm"},
    {"klucz": "droga_4", "nazwa": "📏 Droga wtrysku - profil 4", "jednostka": "mm"},
    {"klucz": "droga_5", "nazwa": "📏 Droga wtrysku - profil 5", "jednostka": "mm"},
    {"klucz": "predkosc_1", "nazwa": "⚡ Prędkość wtrysku - profil 1", "jednostka": "cm³/s"},
    {"klucz": "predkosc_2", "nazwa": "⚡ Prędkość wtrysku - profil 2", "jednostka": "cm³/s"},
    {"klucz": "predkosc_3", "nazwa": "⚡ Prędkość wtrysku - profil 3", "jednostka": "cm³/s"},
    {"klucz": "predkosc_4", "nazwa": "⚡ Prędkość wtrysku - profil 4", "jednostka": "cm³/s"},
    {"klucz": "predkosc_5", "nazwa": "⚡ Prędkość wtrysku - profil 5", "jednostka": "cm³/s"},
    {"klucz": "cisnienie_docisku", "nazwa": "📉 Ciśnienie docisku", "jednostka": "bar"},
    {"klucz": "przeciwcisnienie", "nazwa": "🔄 Przeciwciśnienie", "jednostka": "bar"},
    {"klucz": "objetosc_dozowania", "nazwa": "🧊 Objętość dozowania", "jednostka": "cm³"},
    {"klucz": "uwagi_maszyny", "nazwa": "💬 Uwagi do maszyny", "jednostka": "-"}
]

def wczytaj_szablon():
    if os.path.exists(PLIK_PARAMETROW):
        with open(PLIK_PARAMETROW, "r", encoding="utf-8") as f:
            return json.load(f)
    return DOMYSLNE_PARAMETRY

def zapisz_szablon(parametry):
    with open(PLIK_PARAMETROW, "w", encoding="utf-8") as f:
        json.dump(parametry, f, ensure_ascii=False, indent=4)

def wczytaj_baze():
    if os.path.exists(PLIK_BAZY):
        with open(PLIK_BAZY, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "101": {
            "lokalizacja": "Hala duża",
            "waga": "450 kg",
            "wymiary": "400 x 500 x 350 mm",
            "gk": "Tak",
            "gniazdowosc": "4",
            "uwagi": "Brak uwag bieżących.",
            "maszyny": ["Krauss Maffei (KM-01)", "Ferromatik (FM-02)"],
            "dokumentacja": {}
        }
    }

def zapisz_baze(baza):
    with open(PLIK_BAZY, "w", encoding="utf-8") as f:
        json.dump(baza, f, ensure_ascii=False, indent=4)

baza_form = wczytaj_baze()
szablon_parametrow = wczytaj_szablon()

st.title("🏭 Aplikacja Nira - System Form")

# Menu boczne
menu = st.sidebar.selectbox("Wybierz moduł", ["Wyszukaj / Przeglądaj formę", "🔐 Panel Administratora"])

if menu == "Wyszukaj / Przeglądaj formę":
    st.header("🔍 Wyszukiwanie formy")
    numer_formy = st.text_input("Wpisz numer formy (np. 101):")
    
    if numer_formy:
        if numer_formy in baza_form:
            f = baza_form[numer_formy]
            st.success(f"Znaleziono formę: {numer_formy}")
            
            st.subheader("📍 Dane i parametry formy")
            st.write(f"**Lokalizacja:** {f.get('lokalizacja', '-')}")
            st.write(f"**Waga:** {f.get('waga', '-')}")
            st.write(f"**Wymiary:** {f.get('wymiary', '-')}")
            st.write(f"**Gorący kanał:** {f.get('gk', '-')}")
            st.write(f"**Gniazdowość:** {f.get('gniazdowosc', '-')}")
            st.write(f"**Uwagi bieżące:** {f.get('uwagi', '-')}")
            
            with st.expander("✏️ Edytuj podstawowe dane formy"):
                nowa_lok = st.text_input("Lokalizacja", f.get('lokalizacja', ''))
                nowa_wag = st.text_input("Waga", f.get('waga', ''))
                nowe_wym = st.text_input("Wymiary", f.get('wymiary', ''))
                nowy_gk = st.text_input("Gorący kanał (Tak/Nie)", f.get('gk', ''))
                nowa_gn = st.text_input("Gniazdowość", f.get('gniazdowosc', ''))
                nowe_uwagi = st.text_area("Uwagi bieżące", f.get('uwagi', ''))
                maszyny_str = st.text_input("Maszyny (oddzielone przecinkami)", ", ".join(f.get('maszyny', [])))
                
                if st.button("Zapisz zmiany formy"):
                    lista_m = [m.strip() for m in maszyny_str.split(",")] if maszyny_str else []
                    baza_form[numer_formy]["lokalizacja"] = nowa_lok
                    baza_form[numer_formy]["waga"] = nowa_wag
                    baza_form[numer_formy]["wymiary"] = nowe_wym
                    baza_form[numer_formy]["gk"] = nowy_gk
                    baza_form[numer_formy]["gniazdowosc"] = nowa_gn
                    baza_form[numer_formy]["uwagi"] = nowe_uwagi
                    baza_form[numer_formy]["maszyny"] = lista_m
                    zapisz_baze(baza_form)
                    st.rerun()

            st.subheader("🏭 Dokumentacja maszynowa")
            maszyny = f.get("maszyny", [])
            if maszyny:
                wybrana_maszyna = st.selectbox("Wybierz maszynę do edycji dokumentacji", maszyny)
                if wybrana_maszyna:
                    dok_dane = f.get("dokumentacja", {}).get(wybrana_maszyna, {})
                    
                    st.markdown(f"**Parametry technologiczne dla: {wybrana_maszyna}**")
                    nowe_wartosci_dok = {}
                    for p in szablon_parametrow:
                        etykieta = f"{p['nazwa']} [{p['jednostka']}]" if p['jednostka'] != "-" else p['nazwa']
                        akt_val = dok_dane.get(p["klucz"], "")
                        nowe_wartosci_dok[p["klucz"]] = st.text_input(etykieta, value=akt_val, key=f"p_{p['klucz']}")
                    
                    # Obsługa zdjęć bezpośrednio z galerii lub aparatu w telefonie
                    st.markdown("---")
                    st.subheader("📷 Zdjęcia dokumentacji")
                    istniejace_zdjecia = dok_dane.get("zdjęcia", dok_dane.get("zdjecia", []))
                    
                    if istniejace_zdjecia:
                        st.write("Przypisane zdjęcia:")
                        for idx, img_path in enumerate(istniejace_zdjecia):
                            st.write(f"- {os.path.basename(img_path)}")
                    
                    nowe_zdjecie = st.file_uploader("Dodaj zdjęcie (wybierz z galerii lub zrób aparatem)", type=["png", "jpg", "jpeg"], key=f"upl_{wybrana_maszyna}")
                    
                    if st.button("💾 Zapisz dokumentację maszyny"):
                        if "dokumentacja" not in baza_form[numer_formy]:
                            baza_form[numer_formy]["dokumentacja"] = {}
                        
                        dane_zapis = nowe_wartosci_dok
                        dane_zapis["zdjecia"] = istniejace_zdjecia
                        
                        if nowe_zdjecie is not None:
                            os.makedirs("zdjecia_zapisane", exist_ok=True)
                            sciezka_zapisu = os.path.join("zdjecia_zapisane", nowe_zdjecie.name)
                            with open(sciezka_zapisu, "wb") as f_out:
                                f_out.write(nowe_zdjecie.getbuffer())
                            if sciezka_zapisu not in dane_zapis["zdjecia"]:
                                dane_zapis["zdjecia"].append(sciezka_zapisu)
                                
                        baza_form[numer_formy]["dokumentacja"][wybrana_maszyna] = dane_zapis
                        zapisz_baze(baza_form)
                        st.success("Dokumentacja zaktualizowana pomyślnie!")
            else:
                st.info("Brak przypisanych maszyn do tej formy.")
        else:
                    st.error("Nie znaleziono formy o podanym numerze.")

elif menu == "🔐 Panel Administratora":
    st.header("🛠️ Panel Administratora")
    tab1, tab2 = st.tabs(["Zarządzanie Formami", "Szablon Parametrów i Jednostek"])
    
    with tab1:
        st.subheader("Dodaj nową formę")
        nowy_nr = st.text_input("Numer nowej formy:")
        nowa_lokalizacja = st.text_input("Lokalizacja nowej formy:")
        if st.button("➕ Utwórz formę"):
            if nowy_nr:
                if nowy_nr in baza_form:
                    st.warning("Taka forma już istnieje!")
                else:
                    baza_form[nowy_nr] = {
                        "lokalizacja": nowa_lokalizacja, "waga": "", "wymiary": "", 
                        "gk": "Nie", "gniazdowosc": "1", "uwagi": "Nowa forma", "maszyny": [], "dokumentacja": {}
                    }
                    zapisz_baze(baza_form)
                    st.success(f"Dodano formę {nowy_nr}!")
                    st.rerun()
            else:
                st.warning("Podaj numer formy.")
                
        st.subheader("Usuń istniejącą formę")
        do_usuniecia = st.selectbox("Wybierz formę do usunięcia", ["Wybierz..."] + list(baza_form.keys()))
        if do_usuniecia != "Wybierz...":
            if st.button("🗑️ Usuń tę formę"):
                del baza_form[do_usuniecia]
                zapisz_baze(baza_form)
                st.success(f"Usunięto formę {do_usuniecia}.")
                st.rerun()

    with tab2:
        st.subheader("Dodaj nowy parametr maszynowy")
        p_nazwa = st.text_input("Nazwa parametru (np. Czas wtrysku)")
        p_jedn = st.text_input("Jednostka (np. s)")
        if st.button("➕ Dodaj do szablonu"):
            if p_nazwa:
                klucz = p_nazwa.lower().replace(" ", "_").replace("ą", "a").replace("ć", "c").replace("ę", "e").replace("ł", "l").replace("ń", "n").replace("ó", "o").replace("ś", "s").replace("ź", "z").replace("ż", "z")
                szablon_parametrow.append({"klucz": klucz, "nazwa": p_nazwa, "jednostka": p_jedn})
                zapisz_szablon(szablon_parametrow)
                st.success("Dodano nowy parametr do systemu!")
                st.rerun()
            else:
                st.warning("Podaj nazwę parametru.")
                
        st.write("### Aktywne parametry w systemie:")
        for idx, param in enumerate(szablon_parametrow):
            col1, col2 = st.columns([4, 1])
            col1.write(f"• **{param['nazwa']}** [{param['jednostka']}]")
            if col2.button("Usuń", key=f"del_param_{idx}"):
                szablon_parametrow.pop(idx)
                zapisz_szablon(szablon_parametrow)
                st.rerun()