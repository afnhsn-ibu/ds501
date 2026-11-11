# Reading summaries

Two slides per paper, placed in the **Papers to Read** section of the weekly deck
(after "Optional Reading", before "Reading Questions for Discussion").

- `w01.json` to `w05.json`: the text of each summary (two slides per paper, with speaker notes).
- `build_readings_deck.js`: turns one of them into slides in the course template.
- `merge_into_weekly.ps1`: inserts those slides into the weekly deck, renumbers the
  section footers, saves the deck and exports its PDF (needs PowerPoint on Windows).

```bash
npm install pptxgenjs@3.12.0
# build only the paper slides, numbered 4..11 of a 12-slide section (4 papers x 2 + the deck's own 4)
node build_readings_deck.js w04.json 4 "Databases and SQL" w04_papers.pptx 4 12
```

```powershell
# insert them after slide 61 ("Optional Reading") of the weekly deck; run once per deck
powershell -ExecutionPolicy Bypass -File merge_into_weekly.ps1 `
  -Weekly ..\..\slides\DS501_W04_Databases_and_SQL.pptx -Summary w04_papers.pptx -After 61
```

Without the last two arguments, `build_readings_deck.js` builds a stand-alone summary deck instead.

Export with **Source Sans 3** and **IBM Plex Mono** installed (both free, SIL Open Font
License). Without them PowerPoint substitutes a font and the PDF can repeat words at line breaks.

Finally set `reading_summaries: true` under the week in `course.yml` (adds a pointer on the
week page and the Papers page) and run `python tools/build_site.py`.
