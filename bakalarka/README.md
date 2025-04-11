# Dvojhráčová hra v Pygame: Platformer, Sokoban a Prototype

Tento projekt je vytvorený ako súčasť bakalárskej práce a pozostáva z troch hier pre dvoch hráčov na jednej klávesnici. Hra je inšpirovaná sériou Fireboy and Watergirl a hrou Sokoban, kladie dôraz na spoluprácu a logické myslenie.

## Hry

### Sokoban
- Logická hra s tlačením debničiek na cieľové polia.
- Mapa je mriežková (grid-based), načítaná ako matica.
- Ovládanie:
  - P1: Šípky
  - P2: WASD

### Platformer
- 2D plošinovka s gravitáciou, skákaním a prekážkami.
- Hráči musia aktivovať tlačidlá a otvoriť si cestu k cieľu.
- Podpora viacerých cieľových polí (oba hráči musia byť v cieľovej oblasti).

### Prototype
- Experimentálna hra s fyzikou pomocou Pymunk.
- Hráči pohybujú rotujúcimi telesami a tlačia debničky na cieľové polia.

## Spustenie

1. Aktivuj virtuálne prostredie:
   ```
   venv\Scripts\activate
   ```

2. Spusti hlavné menu:
   ```
   python menu.py
   ```

3. Pre editor máp:
   ```
   python editor_menu.py
   ```

## Ovládanie

| Akcia                 | Hráč 1       | Hráč 2       |
|----------------------|--------------|--------------|
| Pohyb                | WASD         | Šípky        |
| Skok (platformer)    | W            | ↑            |
| Reštart úrovne       | R            |              |
| Návrat do menu       | ESC          |              |

## Štruktúra projektu

- `platformer.py`, `sokoban.py`, `prototype.py` – jednotlivé herné režimy
- `menu.py`, `editor.py`, `editor_menu.py` – výber režimu, editor máp
- `scripts/` – obsahuje všetku logiku pre načítanie máp, hráčov, fyziku, vykresľovanie, UI

## Editor

- Vstavaný editor pre hry Platformer a Prototype
- Výber dlaždíc (myšou + koliesko), prepínanie medzi objektmi (O)
- Uloženie mapy: S
- Prepnutie mriežky / voľného umiestňovania: G

Vyvinuté ako súčasť bakalárskej práce – [Tvoja univerzita a študijný program sem]