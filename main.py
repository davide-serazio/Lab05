import flet as ft
from alert import AlertManager
from deposito_strumenti import DepositoStrumenti

FILE_STRUMENTI = "strumenti.csv"

def main(page: ft.Page):
    page.title = "Lab05"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.DARK

    # --- ALERT ---
    alert = AlertManager(page)

    # --- LA LOGICA DELL'APPLICAZIONE E' PRESA DAL DEPOSITO DI STRUMENTI DEL LAB03 ---
    deposito = DepositoStrumenti("Deposito Strumenti Musicali", "Alessandro Visconti")
    try:
        deposito.carica_file_strumenti(FILE_STRUMENTI)  # Carica il file
    except FileNotFoundError as e:
        alert.show_alert(f"❌ {e}")  # Fa apparire una finestra che mostra l'errore

    # --- UI ELEMENTI ---

    # Text per mostrare il nome e il responsabile del deposito
    txt_titolo = ft.Text(value=deposito.nome, size=38, weight=ft.FontWeight.BOLD)
    txt_responsabile = ft.Text(
        value=f"Responsabile: {deposito.get_responsabile()}",
        size=16,
        weight=ft.FontWeight.BOLD
    )

    # TextField per responsabile
    input_responsabile = ft.TextField(value=deposito.get_responsabile(), label="Responsabile")

    # ListView per mostrare la lista di strumenti aggiornata
    lista_strumenti = ft.ListView(expand=True, spacing=5, padding=10, auto_scroll=True)

    # Tutti i TextField per le info necessarie per aggiungere un nuovo strumento (tipo, marca, anno, contatore posti)
    input_tipo = ft.TextField(label="Tipo", value="", width=220)
    input_marca = ft.TextField(label="Marca", value="", width=220)
    input_anno = ft.TextField(label="Anno di acquisto", value="", width=180)

    input_valore = ft.TextField(
        label="Valore (€)",
        value="0",
        width=150,
        disabled=True,
        text_align=ft.TextAlign.CENTER
    )

    # --- FUNZIONI APP ---
    def aggiorna_lista_strumenti():
        lista_strumenti.controls.clear()
        for strumento in deposito.strumenti_ordinati_per_marca():
            stato = "✅" if strumento.disponibile else "⛔"
            lista_strumenti.controls.append(ft.Text(f"{stato} {strumento}"))

    # --- HANDLERS APP ---
    def cambia_tema(e):
        page.theme_mode = ft.ThemeMode.DARK if toggle_cambia_tema.value else ft.ThemeMode.LIGHT
        toggle_cambia_tema.label = "Tema scuro" if toggle_cambia_tema.value else "Tema chiaro"

    def conferma_responsabile(e):
        deposito.set_responsabile(input_responsabile.value)
        txt_responsabile.value = f"Responsabile: {deposito.get_responsabile()}"

    # Handlers per la gestione dei pulsanti utili all'inserimento di un nuovo strumento
    def aumenta_valore(e):
        valore_attuale = int(input_valore.value)
        input_valore.value = str(valore_attuale + 1)
        input_valore.update()

    def diminuisci_valore(e):
        valore_attuale = int(input_valore.value)
        input_valore.value = str(valore_attuale - 1)
        input_valore.update()

    def aggiungi_strumento(e):
        try:
            tipo = input_tipo.value
            marca = input_marca.value
            anno = int(input_anno.value)
            valore = float(input_valore.value)

            deposito.aggiungi_strumento(tipo, marca, anno, valore)

            input_tipo.value = ""
            input_marca.value = ""
            input_anno.value = ""
            input_valore.value = "0"

            aggiorna_lista_strumenti()
            page.update()

        except ValueError:
            alert.show_alert(
                "Inserisci un anno intero e un valore numerico."
            )

    # --- EVENTI ---
    toggle_cambia_tema = ft.Switch(label="Tema scuro", value=True, on_change=cambia_tema)
    pulsante_conferma_responsabile = ft.Button("Conferma", on_click=conferma_responsabile)

    # Pulsanti per la gestione dell'inserimento di un nuovo strumento
    pulsante_meno = ft.IconButton(
        icon=ft.Icons.REMOVE,
        on_click=diminuisci_valore
    )

    pulsante_piu = ft.IconButton(
        icon=ft.Icons.ADD,
        on_click=aumenta_valore
    )

    pulsante_aggiungi = ft.Button(
        content="Aggiungi strumento",
        on_click=aggiungi_strumento
    )

    # --- LAYOUT ---
    page.add(
        toggle_cambia_tema,

        # Sezione 1
        txt_titolo,
        txt_responsabile,
        ft.Divider(),

        # Sezione 2
        ft.Text("Modifica Informazioni", size=20),
        ft.Row(spacing=200,
               controls=[input_responsabile, pulsante_conferma_responsabile],
               alignment=ft.MainAxisAlignment.CENTER),

        # Sezione 3
        ft.Text("Aggiungi Nuovo Strumento", size=20),

        ft.Row(
            controls=[input_tipo, input_marca, input_anno],
            alignment=ft.MainAxisAlignment.CENTER
        ),

        ft.Row(
            controls=[pulsante_meno, input_valore, pulsante_piu],
            alignment=ft.MainAxisAlignment.CENTER
        ),

        pulsante_aggiungi,

        # Sezione 4
        ft.Divider(),
        ft.Text("Strumenti", size=20),
        lista_strumenti,
    )
    aggiorna_lista_strumenti()

ft.run(main)
