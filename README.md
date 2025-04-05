# Dvojhráčová hra v Pygame: Platformer, Sokoban a Prototype

Tento projekt je vytvorený ako súčasť bakalárskej práce a pozostáva z troch hier pre dvoch hráčov na jednej klávesnici. Aplikácia je inšpirovaná sériou Fireboy and Watergirl a hrou Sokoban, kladie dôraz na spoluprácu a logické myslenie.

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


Vyvinuté ako súčasť bakalárskej práce 
Autor Miroslav Majerský
