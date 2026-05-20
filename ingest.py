#!/usr/bin/env python3
"""
ingest.py — LLM Wiki Ingestor (Karpathy patroon)
Verwerkt alle nieuwe .docx en .pdf bestanden in input/ en bouwt wiki/ op met
LLM-gegenereerde samenvattingen, entiteiten en kruisverwijzingen.

Gebruik:
    python ingest.py               # Verwerk alle nieuwe bestanden
    python ingest.py --dry-run     # Toon wat er gemaakt zou worden

Vereisten:
    pip install anthropic python-docx pdfplumber
    $env:ANTHROPIC_API_KEY = "sk-ant-..."
"""

import os
import re
import sys
from datetime import datetime
from pathlib import Path


def check_deps():
    missing = []
    for pkg, import_name in [
        ("anthropic", "anthropic"),
        ("python-docx", "docx"),
        ("pdfplumber", "pdfplumber"),
    ]:
        try:
            __import__(import_name)
        except ImportError:
            missing.append(pkg)
    if missing:
        print(f"❌ Ontbrekende libraries: {', '.join(missing)}")
        print(f"   Installeer met: pip install {' '.join(missing)}")
        sys.exit(1)


check_deps()

import anthropic
import pdfplumber
from docx_to_obsidian import clean_lines, docx_to_sections, slugify

# ── PDF ondersteuning ─────────────────────────────────────────────────────────

PAGES_PER_SECTION = 5  # aantal PDF-pagina's per wiki-sectie


def pdf_to_sections(pdf_path: str, pages_per_section: int = PAGES_PER_SECTION):
    """Lees een PDF en groepeer pagina's in secties van `pages_per_section` pagina's."""
    sections = []
    with pdfplumber.open(pdf_path) as pdf:
        total = len(pdf.pages)
        for start in range(0, total, pages_per_section):
            end = min(start + pages_per_section, total)
            title = f"Pagina {start + 1}–{end}"
            lines = []
            for page in pdf.pages[start:end]:
                text = page.extract_text() or ""
                lines.extend(text.splitlines())
                lines.append("")
            sections.append((title, lines))
    return sections if sections else [(Path(pdf_path).stem, [])]


def get_sections(file_path: Path):
    """Geef secties terug op basis van bestandstype."""
    if file_path.suffix.lower() == ".docx":
        return docx_to_sections(str(file_path), "heading1")
    elif file_path.suffix.lower() == ".pdf":
        return pdf_to_sections(str(file_path))
    raise ValueError(f"Niet-ondersteund bestandstype: {file_path.suffix}")

# ── Paden ─────────────────────────────────────────────────────────────────────

ROOT = Path(__file__).parent
INPUT_DIR = ROOT / "input"
WIKI_DIR = ROOT / "RSDO"
ENTITIES_DIR = WIKI_DIR / "entities"
LOG_FILE = WIKI_DIR / "log.md"
INDEX_FILE = WIKI_DIR / "index.md"

# ── Claude ────────────────────────────────────────────────────────────────────

client = anthropic.Anthropic()

# Wijzig naar "claude-haiku-4-5" voor ~20x lagere kosten (minder kwaliteit)
MODEL = "claude-opus-4-7"

SYSTEM_PROMPT = """Je bent een kennisbeheerder die een persoonlijke Obsidian wiki opbouwt.

Je analyseert secties uit documenten en extraheert gestructureerde informatie:
1. Een beknopte samenvatting (2-3 zinnen in het Nederlands)
2. Entiteiten die voorkomen in de sectie (personen, concepten, organisaties, plaatsen, gebeurtenissen)
3. Kruisverwijzingen naar bestaande wiki-entiteiten die relevant zijn

Wees precies: extraheer alleen informatie die daadwerkelijk aanwezig is in de sectie.
Gebruik de `record_analysis` tool om je bevindingen op te slaan."""

ANALYZE_TOOL = {
    "name": "record_analysis",
    "description": "Sla de analyse van een documentsectie op.",
    "input_schema": {
        "type": "object",
        "properties": {
            "summary": {
                "type": "string",
                "description": "2-3 zinnen samenvatting van de sectie in het Nederlands",
            },
            "entities": {
                "type": "array",
                "description": "Entiteiten die voorkomen in de sectie",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "description": "Naam van de entiteit"},
                        "type": {
                            "type": "string",
                            "enum": ["person", "concept", "place", "org", "event"],
                            "description": "Type entiteit",
                        },
                        "description": {
                            "type": "string",
                            "description": "Één zin beschrijving van de entiteit",
                        },
                    },
                    "required": ["name", "type", "description"],
                },
            },
            "cross_refs": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Namen van bestaande wiki-entiteiten die relevant zijn voor deze sectie",
            },
        },
        "required": ["summary", "entities", "cross_refs"],
    },
}


# ── LLM analyse ───────────────────────────────────────────────────────────────


def analyze_section(
    book_title: str,
    section_title: str,
    content: str,
    existing_entities: list,
) -> dict:
    """Analyseer een sectie met Claude en extraheer gestructureerde informatie."""
    existing_str = ", ".join(existing_entities[:60]) if existing_entities else "geen"

    response = client.messages.create(
        model=MODEL,
        max_tokens=2048,
        thinking={"type": "adaptive"},
        system=[
            {
                "type": "text",
                "text": SYSTEM_PROMPT,
                "cache_control": {"type": "ephemeral"},  # cache system prompt over alle calls
            }
        ],
        tools=[ANALYZE_TOOL],
        tool_choice={"type": "tool", "name": "record_analysis"},
        messages=[
            {
                "role": "user",
                "content": (
                    f"Analyseer deze sectie:\n\n"
                    f"**Boek:** {book_title}\n"
                    f"**Sectie:** {section_title}\n\n"
                    f"**Inhoud:**\n{content[:4000]}\n\n"
                    f"**Bestaande wiki-entiteiten:** {existing_str}"
                ),
            }
        ],
    )

    for block in response.content:
        if block.type == "tool_use" and block.name == "record_analysis":
            return block.input

    return {"summary": "", "entities": [], "cross_refs": []}


# ── Wiki bestandsbeheer ───────────────────────────────────────────────────────


def get_existing_entities() -> list:
    if not ENTITIES_DIR.exists():
        return []
    return [f.stem for f in ENTITIES_DIR.glob("*.md")]


def get_processed_files() -> set:
    if not LOG_FILE.exists():
        return set()
    text = LOG_FILE.read_text(encoding="utf-8")
    processed = set()
    for line in text.splitlines():
        if line.startswith("- **INGEST**"):
            match = re.search(r"`([^`]+\.(docx|pdf))`", line)
            if match:
                processed.add(match.group(1))
    return processed


def write_entity_page(entity: dict, source_ref: str):
    ENTITIES_DIR.mkdir(parents=True, exist_ok=True)
    slug = slugify(entity["name"])
    entity_file = ENTITIES_DIR / f"{slug}.md"

    if entity_file.exists():
        existing = entity_file.read_text(encoding="utf-8")
        if source_ref not in existing:
            entity_file.write_text(existing.rstrip() + f"\n- {source_ref}\n", encoding="utf-8")
    else:
        today = datetime.now().date().isoformat()
        content = (
            f"---\n"
            f"title: \"{entity['name']}\"\n"
            f"entity_type: {entity['type']}\n"
            f"tags:\n"
            f"  - entity\n"
            f"  - {entity['type']}\n"
            f"created: {today}\n"
            f"---\n\n"
            f"# {entity['name']}\n\n"
            f"{entity['description']}\n\n"
            f"## Voorkomt in\n\n"
            f"- {source_ref}\n"
        )
        entity_file.write_text(content, encoding="utf-8")


def append_to_log(entry: str):
    WIKI_DIR.mkdir(parents=True, exist_ok=True)
    if not LOG_FILE.exists():
        LOG_FILE.write_text(
            "# Wiki Log\n\n"
            "Chronologisch overzicht van alle ingest- en queryoperaties.\n\n",
            encoding="utf-8",
        )
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(entry + "\n")


def update_global_index(book_title: str, sections_info: list):
    WIKI_DIR.mkdir(parents=True, exist_ok=True)
    if not INDEX_FILE.exists():
        INDEX_FILE.write_text("# Wiki Index\n\n", encoding="utf-8")

    existing = INDEX_FILE.read_text(encoding="utf-8")
    if f"## {book_title}" not in existing:
        new_block = f"\n## {book_title}\n\n"
        for title, filepath, summary in sections_info:
            rel = filepath.relative_to(WIKI_DIR).with_suffix("").as_posix()
            short = (summary[:120] + "…") if len(summary) > 120 else summary
            new_block += f"- [[{rel}|{title}]] — {short}\n"
        with open(INDEX_FILE, "a", encoding="utf-8") as f:
            f.write(new_block)


# ── Verwerking ────────────────────────────────────────────────────────────────


def process_file(file_path: Path, dry_run: bool = False) -> int:
    book_title = file_path.stem
    book_slug = slugify(book_title)
    book_dir = WIKI_DIR / book_slug

    print(f"\n📖 {file_path.name}")

    sections = get_sections(file_path)
    total = len(sections)
    print(f"   {total} secties gevonden")

    if not dry_run:
        book_dir.mkdir(parents=True, exist_ok=True)

    existing_entities = get_existing_entities()
    sections_info = []
    all_new_entities = []

    for i, (title, lines) in enumerate(sections, 1):
        content = clean_lines(lines)
        if not content.strip():
            print(f"   [{i}/{total}] {title[:50]}… (leeg, overgeslagen)")
            continue

        print(f"   [{i}/{total}] {title[:50]}…", end=" ", flush=True)

        analysis = analyze_section(book_title, title, content, existing_entities)

        summary = analysis.get("summary", "")
        entities = analysis.get("entities", [])
        cross_refs = analysis.get("cross_refs", [])

        filename = f"{i:02d}-{slugify(title)}.md"
        filepath = book_dir / filename

        # Navigatie
        nav_parts = []
        if i > 1:
            nav_parts.append(
                f"← [[{(i-1):02d}-{slugify(sections[i-2][0])}|{sections[i-2][0]}]]"
            )
        if i < total:
            nav_parts.append(
                f"[[{(i+1):02d}-{slugify(sections[i][0])}|{sections[i][0]}]] →"
            )
        nav_str = "   ".join(nav_parts)

        # Zie ook
        see_also = ""
        if cross_refs:
            links = [f"[[entities/{slugify(r)}|{r}]]" for r in cross_refs]
            see_also = "\n\n## Zie ook\n\n" + "\n".join(f"- {l}" for l in links)

        today = datetime.now().date().isoformat()
        safe_summary = summary.replace('"', "'")
        fm = (
            f"---\n"
            f"title: \"{title}\"\n"
            f"book: \"{book_title}\"\n"
            f"tags:\n"
            f"  - boek\n"
            f"  - {book_slug}\n"
            f"created: {today}\n"
            f"chapter: {i}\n"
            f"total_chapters: {total}\n"
            f"summary: \"{safe_summary}\"\n"
            f"---\n\n"
        )

        parts = [fm]
        if nav_str:
            parts.append(nav_str + "\n\n---\n\n")
        parts.append(f"# {title}\n\n")
        if summary:
            parts.append(f"> {summary}\n\n")
        parts.append(content)
        parts.append(see_also)
        if nav_str:
            parts.append(f"\n\n---\n{nav_str}")

        if dry_run:
            print(f"[DRY RUN] → {filename} | {len(entities)} entiteiten")
        else:
            filepath.write_text("".join(parts), encoding="utf-8")

            source_ref = f"[[{book_slug}/{filename[:-3]}|{title}]] ({book_title})"
            for entity in entities:
                write_entity_page(entity, source_ref)
                if entity["name"] not in existing_entities:
                    existing_entities.append(entity["name"])

            all_new_entities.extend(e["name"] for e in entities)
            print(f"✅ | {len(entities)} entiteiten")

        sections_info.append((title, filepath, summary))

    if dry_run:
        print(f"\n   [DRY RUN] Zou {len(sections_info)} pagina's schrijven")
        return len(sections_info)

    # Boek-index
    today = datetime.now().date().isoformat()
    index_path = book_dir / f"{book_slug}-index.md"
    index_lines = [
        f"---\ntitle: \"{book_title} - Index\"\ntags:\n  - boek\n  - index\ncreated: {today}\n---\n\n",
        f"# {book_title}\n\n## Secties\n\n",
    ]
    for j, (t, fp, s) in enumerate(sections_info, 1):
        short = (s[:100] + "…") if len(s) > 100 else s
        index_lines.append(f"{j}. [[{fp.name[:-3]}|{t}]] — {short}\n")
    index_path.write_text("".join(index_lines), encoding="utf-8")

    # Globale index & log
    update_global_index(book_title, sections_info)

    unique_entities = list(dict.fromkeys(all_new_entities))
    preview = ", ".join(unique_entities[:8]) + ("…" if len(unique_entities) > 8 else "")
    now = datetime.now().isoformat(timespec="seconds")
    append_to_log(
        f"- **INGEST** `{file_path.name}` — {now} — "
        f"{len(sections_info)} secties, {len(unique_entities)} entiteiten"
        f"{(': ' + preview) if preview else ''}"
    )

    print(f"\n   🎉 {len(sections_info)} pagina's → wiki/{book_slug}/")
    return len(sections_info)


# ── Hoofdprogramma ────────────────────────────────────────────────────────────


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="LLM Wiki Ingestor — bouwt een Obsidian wiki vanuit .docx en .pdf bestanden."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Toon wat er gemaakt zou worden zonder te schrijven",
    )
    args = parser.parse_args()

    print("🔍 LLM Wiki Ingestor\n")

    if not INPUT_DIR.exists():
        print("❌ input/ map niet gevonden")
        sys.exit(1)

    all_files = sorted(INPUT_DIR.glob("*.docx")) + sorted(INPUT_DIR.glob("*.pdf"))
    all_files.sort(key=lambda f: f.name)
    if not all_files:
        print("📭 Geen .docx of .pdf bestanden gevonden in input/")
        sys.exit(0)

    processed = get_processed_files()
    new_files = [f for f in all_files if f.name not in processed]

    if not new_files:
        print(f"✅ Alle {len(all_files)} bestanden al verwerkt.")
        print(f"   Wiki staat in: {WIKI_DIR}")
        sys.exit(0)

    print(f"📚 {len(new_files)} nieuw(e) bestand(en):")
    for f in new_files:
        print(f"   • {f.name}")

    if not args.dry_run and not os.environ.get("ANTHROPIC_API_KEY"):
        print("\n❌ ANTHROPIC_API_KEY niet ingesteld.")
        print("   PowerShell: $env:ANTHROPIC_API_KEY = 'sk-ant-...'")
        sys.exit(1)

    total_pages = 0
    for file_path in new_files:
        total_pages += process_file(file_path, dry_run=args.dry_run)

    if not args.dry_run:
        print(f"\n{'='*50}")
        print(f"✅ Klaar! {total_pages} wiki pagina's aangemaakt")
        print(f"📋 Log:        {LOG_FILE}")
        print(f"📑 Index:      {INDEX_FILE}")
        print(f"🏷️  Entiteiten: {ENTITIES_DIR}")


if __name__ == "__main__":
    main()
