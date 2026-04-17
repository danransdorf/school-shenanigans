# Signal storage

Prototyp databáze časových řad.

Technické návody byly sepsány primárně pro MacOS/Linux, byla vynaložena snaha pokrýt Windows,
který by měl fungovat obdobně.

## Používání

### Spuštění serveru

První je třeba nastavit prostředí, pokud tak již nebylo učiněno:

```bash
uv venv .venv                        # vytvoř venv
./.venv/bin/activate                 # aktivuj venv, Windows: .\.venv\Scripts\activate
uv pip install .                     # nainstaluj projekt
```

Po nastavení prostředí lze program pustit příkazem:

```bash
signal-storage [args]
```

Popis očekávaných argumentů lze získat:

```bash
signal-storage --help
```

Ukázka použití:

```bash
signal-storage --host localhost --port 3000 --path test-db
```

#### Windows poznámka

V případě "skript nenalezen" (časté na Windows), možno zkusit:

```bash
uv run signal-storage [args]
```

Alternativně možno použít:

```bash
.\.venv\Scripts\signal-storage [args]
```

V případě, že žádná z možností nefunguje, je třeba se ujistit o existenci a aktivaci venvu.

### Ovládání databáze

Databázi lze ovládat přes endpoint `POST /query`, popis endpointu:

- Method: `POST`
- Header `Content-Type`: `text/plain`
- Body: `"<textová query viz Query jazyk>"`

#### Query jazyk

Jedna query obsahuje právě jeden příkaz na jednom řádku.

##### Dostupné příkazy

From/To: `FROM <x> TO <y>`, kde `x`,`y` jsou ISO8601 datum nebo `...` značící "neomezeno v daném směru"
Values: `VALUES (<dvojice1>, <dvojice2>, <atd...>)`, kde `dvojice#` je `(<ISO8601 datum>, <číselná hodnota>)`

- `GET`: Získá hodnoty signálu
  - Argument: čárkou slepené Rozmezí signálu
    - Rozmezí signálu: `<id signálu> <dobrovolné From/To>`
  - Odpověď:
    ```json
    {
      "message": "<x> rows fetched.",
      "data": "schématicky dict[signalId, dict[ISO8601, float]]"
    }
    ```
  - Příklady:
    ```bash
    GET signal1                                                     # vše
    GET signal1 FROM 2025-01-01T00:00:00Z TO 2026-01-01T00:00:00Z   # interval 2025..2026
    GET signal1 FROM ... TO 2026-01-01T00:00:00Z                    # vše do 2026-01-01
    GET signal1, signal2 FROM 2025-01-01T00:00:00Z TO ...           # `signal1` celý, `signal2` od 2025-01-01
    ```
- `LIST`: Získá seznam signálů. Příkaz nemá argumenty.
  - Odpověď:
    ```json
    {
      "message": "<x> signals listed.",
      "signal_ids": "schématicky list[str]"
    }
    ```
  - Příklad: `LIST`
- `PUT`: Zapíše data. Když dané časové body existují, jsou přepsány. Když signál neexistuje, je vytvořen. (Upsert+autocreate)
  - Argument: čárkou slepené Hodnoty jednotlivých signálů
    - Hodnoty signálu: `<id signálu> <neprázdné Values>`
  - Odpověď:
    ```json
    { "message": "Upserted <x> rows." }
    ```
  - Přiklady:
    ```bash
    PUT signal1 VALUES ((2025-01-01T00:00:00, 1), (2025-01-01T00:01:00, 2), (2025-01-01T00:02:00, 3.5))
    PUT signal1 VALUES ((2025-01-01T00:00:00, 1)), signal2 VALUES ((2025-01-01T00:01:00, 2), (2025-01-01T00:02:00, 3.5))
    ```
- `DELETE`: Smaže data. (syntax je obdobný ke `GETý)
  - Argument: čárkou slepené Rozmezí signálu
    - Rozmezí signálu: viz `GET`
  - Odpověď:
    ```json
    { "message": "Deleted successfully." }
    ```
  - Příklady:
    ```bash
    DELETE signal1                                                     # smaž celý signal1
    DELETE signal1 FROM 2025-01-01T00:00:00Z TO 2026-01-01T00:00:00Z   # smaž interval 2025..2026
    DELETE signal1 FROM ... TO 2026-01-01T00:00:00Z                    # smaž vše do 2026-01-01
    DELETE signal1, signal2 FROM 2025-01-01T00:00:00Z TO ...           # smaž `signal1` celý, `signal2` od 2025-01-01
    ```

## Vývoj

### Nastavení prostředí

Projekt používá manažer UV ([instalace](https://docs.astral.sh/uv/getting-started/installation/)).

```bash
uv venv .venv                        # vytvoř venv
./.venv/bin/activate                 # aktivuj venv, Windows: .\.venv\Scripts\activate
uv pip install -U -e .               # nainstaluj projekt (ve vývojovém režimu "editable")
uv pip install -r requirements.txt   # nainstaluj dev tools
```

### Testování

Automatizované testy lze pustit tímto příkazem:

```bash
pytest     # alternativně `python -m pytest` nebo `uv run pytest`
```

Manuálně lze testovat například programem `curl` takto:

```bash
curl -X POST \
  http://localhost:8080/query \
  -H "Content-Type: text/plain" \
  -d "PUT signal1 VALUES ((2026-01-01T00:00:00, 15.505), (2026-01-01T00:01:00, 54.123))"
```

### Návrh programu

Program má 3 vrstvy: HTTP, Parser, Executor
Tok:

1. HTTP vrstva příjme data
2. Parser vrstva data načte do příkazu
3. Executor vrstva vykoná příkaz
4. HTTP vrstva vrátí výsledek příkazu

### Stylistika

- Formátuj Ruffem s aktivovaným venvem
- Samotný kód piš anglicky, komentáře přirozeně CZ/EN hybridem
- Komentáře mají popisovat, PROČ kód něco dělá, ne CO kód dělá
  - (co kód dělá má být zřejmé z vhodného jmenování a struktury kódu)
