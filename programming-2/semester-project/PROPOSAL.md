# Návrh zadání zápočtového programu - Uložiště časových řad

Implementace MVP systému pro ukládání a čtení (query) časových řad / signálů pomocí jednoduchého syntaxu.
Signál je posloupnost dvojic (čas, hodnota), která je identifikována svým `signal_id`.

Data jednotlivých signálů budou ukládáná jako soubory po časových blocích umožňující efektivní vkládání i dotazy.

## Požadované funkce:

- Ukládání/aktualizace signálů
  - př. `PUT signal1 VALUES ((12:00, 15.505), (13:00, 54.123), ...)`
- Mazání signálů
  - př. `DEL signal1 FROM 12:00 TO 16:30`
- Výpis dostupných signálů `LIST`
- Dotazování se nad několika signály dle času
  - př. `GET signal1 FROM 12:00 TO 16:30, signal2 FROM 06:00 TO 10:00`

## Forma

Systém bude implementován jako Python program,
který spustí Flask server s jedním endpointem na
příkazy `POST /query`.

## Vývoj

- Projekt bude implementován jako Python projekt se souborem `pyproject.toml`.
- Bude použit manažer [UV](https://docs.astral.sh/uv/).
- Interní funkce budou preferovaně implementovány deterministicky, aby se daly čistě pokrýt unit testy.
- Aplikace jako celek bude také zvenku otestována integračními testy.
