#Spiegel Link (2-24): https://www.spiegel.de/suche/?suchbegriff=Wirecard&seite=2&inhalt=ueberschriften-und-vorspann&erschienenBei=der-spiegel%2Cspiegel-plus
import json

# Spiegel Links (2-24)
spiegel_base_url = "https://www.spiegel.de/suche/?suchbegriff=Wirecard&seite={}&inhalt=ueberschriften-und-vorspann&erschienenBei=der-spiegel%2Cspiegel-plus"
spiegel_links = [spiegel_base_url.format(page_number) for page_number in range(2, 25)]

# Speichere die Spiegel Links in einer JSON-Datei
with open('spiegel_links.json', 'w') as spiegel_json_file:
    json.dump(spiegel_links, spiegel_json_file, indent=2)

print("Spiegel Links wurden in 'spiegel_links.json' gespeichert.")

# Manager Magazin Links (2-30)
manager_magazin_base_url = "https://www.manager-magazin.de/suche/?suchbegriff=Wirecard&seite={}&inhalt=ueberschriften-und-vorspann&erschienenBei=manager-magazin%2Cmanager-magazin-plus"
manager_magazin_links = [manager_magazin_base_url.format(page_number) for page_number in range(2, 31)]

# Speichere die Manager Magazin Links in einer JSON-Datei
with open('mm_links.json', 'w') as mm_json_file:
    json.dump(manager_magazin_links, mm_json_file, indent=2)

print("Manager Magazin Links wurden in 'mm_links.json' gespeichert.")
