Bankkontoverwaltungsprogramm
Überblick
Dieses Programm ist eine einfache Simulation eines Bankkontoverwaltungssystems. Es ermöglicht das Eröffnen neuer Konten, das Überweisen von Geld zwischen Konten derselben Bank und speichert alle Kontoinformationen in individuellen Ordnern. Zusätzlich werden alle durchgeführten Operationen mit genauem Datum und Uhrzeit aufgezeichnet, sodass eine klare Transaktionshistorie entsteht.
Funktionen
- Neues Konto eröffnen: Erstelle ein neues Konto mit einer eindeutigen ID, einem Namen und einem Anfangssaldo.
- Geld überweisen: Überweise Geld von einem Konto zu einem anderen innerhalb derselben Bank.
- Datenpersistenz: Die Informationen jedes Kontos (ID, Name, Passwort, Kontostand) werden in einem eigenen Ordner gespeichert, um eine einfache Verwaltung zu gewährleisten.
- Operationsprotokollierung: Jede Aktion (Kontoerstellung, Anmeldung, Überweisung usw.) wird mit Zeitstempel gespeichert und sorgt für eine vollständige Aktivitätsaufzeichnung.
Verwendung
- Setup: Stelle sicher, dass Python installiert ist und die benötigten Pakete (wie Argon2 für Passwort-Hashing) vorhanden sind.
- Konto erstellen: Starte das Programm und folge den Anweisungen, um ein neues Konto zu erstellen. Das Passwort wird sicher gehasht und die Kontodaten gespeichert.
- Anmelden: Verwende die log_in-Funktion, um dich mit Konto-ID, Name und Passwort einzuloggen.
- Geld überweisen: Nach der Anmeldung kannst du Geld von einem Konto auf ein anderes übertragen.
- Protokolle ansehen: Im jeweiligen Konto-Ordner findest du die Log-Datei mit allen Operationen inklusive Datum und Uhrzeit.
Voraussetzungen
- Python 3.x
- argon2-cffi für Passwort-Hashing
