# Dvojhráčová hra v Pygame: Platformer, Sokoban a Prototype

Tento projekt je vytvorený ako súčasť bakalárskej práce a pozostáva z troch hier pre dvoch hráčov na jednej klávesnici. Aplikácia je inšpirovaná sériou Fireboy and Watergirl a hrou Sokoban, kladie dôraz na spoluprácu a logické myslenie.

Najnovšia verzia softvéru je dostupná ako .zip archív v sekcii Releases na GitHub repozitári – aktuálna verzia: pygamegame 5.0.

## Spustenie

1. Rozbaľte celý obsah ZIP archívu do jednej zložky (napr. `PygameHra`).
2. Spustite:
   - `menu.exe` – hlavné menu pre výber a spustenie úrovní
   - `editor_menu.exe` – spustenie editora máp

!!! Hru vždy spúšťajte priamo zo zložky – neodporúča sa vytvárať skratky alebo presúvať `.exe` mimo priečinka!!!

## Hry

### Sokoban
- Logická hra s tlačením debničiek na cieľové polia.
- Mapa je mriežková (grid-based), načítaná ako matica.

### Platformer
- 2D plošinovka s gravitáciou, skákaním a prekážkami.
- Hráči musia aktivovať tlačidlá a otvoriť si cestu k cieľu.
- Podpora viacerých cieľových polí (obaja hráči musia byť v cieľovej oblasti).

### Prototype
- Experimentálna hra s fyzikou pomocou Pymunk.
- Hráči pohybujú fyzikálnymi telesami a tlačia debničky na cieľové polia.


## Ovládanie

| Akcia                | Hráč 1       | Hráč 2       |
|----------------------|--------------|--------------|
| Pohyb                | WASD         | Šípky        |
| Skok (platformer)    | W            | ↑            |
| Reštart úrovne       | R                           |
| Návrat do menu       | ESC                         |


## Štruktúra priečinka

- `menu.exe`, `editor_menu.exe` – spustiteľné súbory
- `assets/`, `lvls/`, `scripts/` – herné dáta, mapy a skripty
- `platformer.py`, `sokoban.py`, `prototype.py` – jednotlivé hry


## Editor

- Vstavaný editor máp pre hry Platformer a Prototype
- Výber dlaždíc: myšou + koliesko
- Prepínanie medzi objektmi: O
- Uloženie mapy: S
- Prepnutie medzi mriežkou a voľným umiestňovaním: G
- Spustenie Editovaného levelu: P

 Poznámka:
Ak sa vytvorí nová úroveň, je nutné ju manuálne premenovať vo lvls/''hra''/''new_map_hra'', pokiaľ chcete vytvoriť ďalšiu novú úroveň. V opačnom prípade editor pri spustení otvorí posledný vytvorený súbor.

Sokoban úrovne nie je možné editovať vizuálne. Nachádzajú sa v súbore lvls/sokoban/skoban_lvl.py a je potrebné ich upraviť ručne ako maticu znakov v zdrojovom kóde.

Vyvinuté ako súčasť bakalárskej práce 
Autor Miroslav Majerský
