# Programování 1

## Informace

### Vyučující

| Vyučující       | Email (UK)                       |
| --------------- | -------------------------------- |
| Lenka Forstová  | <lenka.forstova@matfyz.cuni.cz>  |
| Peter Kvasnička | <peter.kvasnicka@matfyz.cuni.cz> |

### Zápočet

Následující podmínky musí být splněny

- 70% správných domácích úkolů
- Úspěšný zápočtový test (90min, cca obtížnost domácího úkolu)
- Zápočtový program (do poloviny září)
- Zápočet z teoretického cvičení (dle pí. Forstové)

### Odkazy

- <https://recodex.mff.cuni.cz/>
- <https://github.com/PKvasnick/Programovani-2>

## Lokální spouštění úkolů

Struktura v `src/`:

- `src/homework/` pro domácí úkoly
- `src/junk/` pro pokusy / scratch kód

Použití:

```bash
homework <task-id> [další-argumenty]
hw <task-id> [další-argumenty]
junk <task-id> [další-argumenty]
```

Příklady:

```bash
homework 1
hw 4.1
homework list
junk list
```

Mapování `task-id` na soubor:

- `4.1` hledá soubory jako `4_1.py`, `task_4_1.py`, `hw_4_1.py`
- `1` hledá např. `hw_1.py`
