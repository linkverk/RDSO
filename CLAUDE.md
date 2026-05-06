# RDSO Wiki — Schema & Instructies

## Structuur

```
input/              ← Bronbestanden (.docx) — alleen lezen, niet wijzigen
RSDO/               ← Obsidian vault (open deze map in Obsidian)
  index.md          ← Inhoudsoverzicht van alle wiki-pagina's
  log.md            ← Append-only log van ingest- en queryoperaties
  entities/         ← Entiteitpagina's (personen, concepten, organisaties, etc.)
    <slug>.md
  <boek-naam>/      ← Per boek een submap
    <boek>-index.md ← Inhoudsopgave van het boek
    01-<sectie>.md
    02-<sectie>.md
    ...
```

## Operaties

### Ingest

```powershell
python ingest.py
```

Verwerkt alle `.docx` bestanden in `input/` die nog niet in `log.md` staan.
Per sectie genereert Claude: samenvatting, entiteiten en kruisverwijzingen.

```powershell
python ingest.py --dry-run   # preview zonder schrijven
```

### Query

Stel vragen door te zoeken in `wiki/` of via Obsidian Graph View.
Antwoorden kunnen als nieuwe pagina's in de wiki worden opgeslagen.

### Lint

Controleer de wiki periodiek op:
- Weespagina's (geen inkomende links)
- Ontbrekende entiteitpagina's voor genoemde namen
- Verouderde samenvattingen na herziening van bronbestanden

## Conventies

- **Bestandsnamen**: `slugified-lowercase.md`
- **Frontmatter**: altijd aanwezig — `title`, `tags`, `created`
- **Entiteittypes**: `person`, `concept`, `place`, `org`, `event`
- **Kruisverwijzingen**: Obsidian wikilinks `[[pad|label]]`
- **Samenvattingen**: 2-3 zinnen in het Nederlands, ook als frontmatter `summary`-veld
- **Navigatie**: wikilinks naar vorige/volgende sectie bovenaan en onderaan

## Configuratie

Model (`ingest.py`, regel `MODEL`):

| Model | Kwaliteit | Kosten |
|---|---|---|
| `claude-opus-4-7` | Beste | Hoog |
| `claude-haiku-4-5` | Goed | ~20x lager |

Stel de API key in:
```powershell
$env:ANTHROPIC_API_KEY = "sk-ant-..."
```
