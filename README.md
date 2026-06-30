# Fruit Loop

Individuell examinationsuppgift i kursen Programmering med Python (TAP VT26).

## Starta projektet

Kör följande kommando i terminalen från projektets rotmapp:

```commandline
python -m src.game
```

## Kör tester

```commandline
pytest tests/
```

## Hur man spelar

| Tangent | Handling |
|---------|----------|
| `W` `A` `S` `D` | Rörelse uppåt / vänster / nedåt / höger |
| `JW` `JA` `JS` `JD` | Hoppa två steg i en riktning |
| `I` | Visa inventory |
| `Q` / `X` | Avsluta spelet |

## Symboler på kartan

| Symbol | Betydelse |
|--------|-----------|
| `@` | Spelaren |
| `?` | Frukt (+20 poäng) |
| `X` | Fälla (-10 poäng, ligger kvar) |
| `P` | Spade (tar bort nästa vägg du går in i) |
| `K` | Nyckel |
| `C` | Kista (+100 poäng, kräver nyckel) |
| `E` | Exit (vinn spelet när alla frukter är plockade) |
| `■` | Vägg |

## Implementerade krav

| Version 1 | Status |
|-----------|--------|
| A – Spelaren börjar nära mitten         | ✅ |
| B – WASD i alla fyra riktningar         | ✅ |
| C – Kan inte gå igenom väggar           | ✅ |
| D – Fruktsallad (+20 poäng)             | ✅ |
| E – Inventory-lista                     | ✅ |
| F – Kommando "i" för inventory          | ✅ |
| G – The floor is lava (-1/steg)         | ✅ |
| H – For-loopar för inner-väggar         | ✅ |

| Version 2 | Status |
|-----------|--------|
| Fällor (-10 poäng, ligger kvar)         | ✅ |
| Spade (tar bort en vägg)               | ✅ |
| Nycklar och kistor (+100 poäng)         | ✅ |
| Bördig jord (ny frukt var 25:e drag)   | ✅ |
| Exit (vinn när alla frukter plockats)  | ✅ |
| Jump (JW/JA/JS/JD hoppar två steg)    | ✅ |

| Version 3 | Status |
|-----------|--------|
| Grace period (5 steg utan avdrag)      | ✅ |
| TDD med pytest (23 tester)             | ✅ |
