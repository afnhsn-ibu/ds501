# Reading-summary decks

`w04.json`, `w05.json`: the text of each summary (two slides per paper plus speaker notes).
`build_readings_deck.js`: turns one of them into a deck in the course template.

```bash
npm install pptxgenjs@3.12.0
node build_readings_deck.js w04.json 4 "Databases and SQL" ../../slides/DS501_W04_Reading_Summaries.pptx
```

Export the PDF from PowerPoint with **Source Sans 3** and **IBM Plex Mono** installed
(both free, SIL Open Font License). Without them, PowerPoint substitutes a font and the
PDF can repeat words at line breaks.

Then add `summaries: "DS501_W04_Reading_Summaries"` under the week in `course.yml`
and run `python tools/build_site.py`.
