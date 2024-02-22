import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
import re
import tempfile
import os

def show_start_screen():
    root = tk.Tk()
    root.title("Markdown Pfad-Anpassungstool")

    # Informationen über den Ersteller
    info_text = "Dieses Skript wurde von Raffael Richter erstellt.\nKontakt: rr@com-con.net\n\nDieses Programm ermöglicht Ihnen die Auswahl einer Markdown-Datei,\num automatisch die Pfade aller darin enthaltenen Bilder anzupassen.\nNachdem Sie eine Datei ausgewählt haben, zeigt Ihnen\nein weiteres Fenster den geänderten Text an, den Sie kopieren und verwenden können."
    tk.Label(root, text=info_text, padx=20, pady=20).pack()

    # Button, um den Prozess zu starten
    start_button = tk.Button(root, text="Markdown-Datei auswählen", command=lambda: [root.destroy(), main()])
    start_button.pack(pady=20)

    root.mainloop()

def select_file():
    root = tk.Tk()
    root.withdraw()  # Versteckt das Tkinter-Hauptfenster
    file_path = filedialog.askopenfilename(title="Wählen Sie eine Markdown-Datei aus", filetypes=[("Markdown files", "*.md")])
    return file_path

def create_temp_file_with_adjusted_paths(original_file_path):
    with open(original_file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    adjusted_content = re.sub(r'(\!\[.*?\]\()(?!/)(.*?)', r'\1/\2', content)

    # Erstellt eine temporäre Datei
    temp_file = tempfile.NamedTemporaryFile(delete=False, mode='w+', encoding='utf-8', suffix='.md')
    temp_file.write(adjusted_content)
    temp_file.close()  # Schließen, damit der Inhalt gesichert wird

    return temp_file.name

def show_adjusted_content(temp_file_path):
    root = tk.Tk()
    root.title("Angepasste Markdown-Pfade")
    text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=100, height=30)
    text_area.pack(padx=10, pady=10)

    with open(temp_file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        text_area.insert(tk.INSERT, content)

    # Funktion zum Kopieren des Inhalts in die Zwischenablage
    def copy_to_clipboard():
        root.clipboard_clear()  # Zwischenablage löschen
        root.clipboard_append(content)  # Neuen Inhalt zur Zwischenablage hinzufügen
        root.update()  # Zwischenablage aktualisieren
        messagebox.showinfo("Kopiert", "Der Text wurde in die Zwischenablage kopiert.")

    # Button, um den gesamten Text zu kopieren
    copy_button = tk.Button(root, text="Alles kopieren", command=copy_to_clipboard)
    copy_button.pack(side=tk.LEFT, padx=10, pady=10)

    # Funktion, um das Skript zu beenden
    def exit_script():
        root.destroy()  # Schließt das GUI-Fenster
        os.unlink(temp_file_path)  # Löscht die temporäre Datei

    # Button, um das Skript zu beenden
    exit_button = tk.Button(root, text="Beenden", command=exit_script)
    exit_button.pack(side=tk.LEFT, padx=10, pady=10)

    text_area.config(state=tk.DISABLED)  # Verhindert die Bearbeitung des Textes
    root.mainloop()


def main():
    file_path = select_file()
    if file_path:  # Prüfen, ob ein Pfad ausgewählt wurde
        temp_file_path = create_temp_file_with_adjusted_paths(file_path)
        show_adjusted_content(temp_file_path)
    else:
        messagebox.showinfo("Info", "Es wurde keine Datei ausgewählt.")

if __name__ == "__main__":
    show_start_screen()