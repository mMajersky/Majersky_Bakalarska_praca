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
- Hráči musia spolupracovať a aktivovať tlačidlá na otvorenie ciest.
- Každý hráč musí doraziť na svoje cieľové pole.

### Prototype
- Experimentálna hra s fyzikou pomocou knižnice Pymunk.
- Hráči pohybujú rotujúcimi telesami a tlačia debničky na cieľové polia.

## Spustenie projektu

### Postup pre prvé spustenie na novom počítači

1. (Odporúčané) Vytvor nové virtuálne prostredie:
   ```bash
   python -m venv venv
   ```

2. Aktivuj virtuálne prostredie:
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - Linux/macOS:
     ```bash
     source venv/bin/activate
     ```

3. Nainštaluj všetky potrebné knižnice:
   ```bash
   pip install -r requirements.txt
   ```

4. Spusť hru alebo editor:
   - Hlavné menu:
     ```bash
     python menu.py
     ```
   - Editor máp:
     ```bash
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
- `menu.py`, `editor.py`, `editor_menu.py` – hlavné menu a editor
- `scripts/` – logika pre hráčov, načítanie máp, fyziku, UI a ďalšie
- `assets/` – obrázky a sprity
- `lvls/` – uložené mapy
- `requirements.txt` – zoznam knižníc potrebných na spustenie
- `README.md` – tento súbor

## Editor

- Vstavaný editor pre hry Platformer a Prototype
- Ovládanie:
  - Výber dlaždíc: myš + koliesko
  - Prepínanie medzi skupinami: koliesko
  - Varianty dlaždíc: Shift + koliesko
  - Uloženie mapy: O
  - Prepnutie medzi mriežkou a voľným umiestňovaním: G

Vyvinuté ako súčasť bakalárskej práce – [Tvoja univerzita a študijný program sem]