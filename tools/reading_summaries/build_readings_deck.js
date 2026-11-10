// Build a DS 501 "reading summaries" deck: title slide, two slides per paper, closing slide.
// Usage: node build_readings_deck.js <content.json> <weekNum> <weekTitle> <out.pptx>
const fs = require("fs");
const pptxgen = require("pptxgenjs");

const [, , contentPath, weekNum, weekTitle, outPath] = process.argv;
const papers = JSON.parse(fs.readFileSync(contentPath, "utf8"));
const W = parseInt(weekNum, 10);

// Template v2 identity (matches the weekly decks)
const K = {
  bordo: "7A1F2B", bordoCard: "8E2D3A", red: "C8102E", gold: "E9C46A",
  paper: "FBF8F5", card: "FFFFFF", line: "E7DCD5", ink: "2A2526", soft: "3A3335",
  muted: "6E6467", chip: "F2E6E3", band: "F8F1EE", onDark: "FBF8F5", onDark2: "F0D9DC",
  greenBg: "E9F2EE", greenInk: "1E4D43",
};
const SANS = "Source Sans 3", MONO = "IBM Plex Mono";

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in, same as the weekly decks
pres.author = "DS 501";
pres.title = `DS 501 · Week ${W} · Reading Summaries`;
pres.theme = { headFontFace: SANS, bodyFontFace: SANS };

const SW = 13.333, MX = 0.89, CW = SW - 2 * MX; // margins as in the weekly decks
const total = 2 + papers.length * 2;
let n = 0;

function tb(slide, text, o) { slide.addText(text, Object.assign({ isTextBox: true, margin: 0, fontFace: SANS }, o)); }

function footer(slide) {
  n += 1;
  tb(slide, `DS 501 · Week ${W} · Reading summaries`, { x: MX, y: 6.95, w: 7, h: 0.3, fontSize: 11, color: K.muted, charSpacing: 0.5 });
  tb(slide, `${n} / ${total}`, { x: SW - MX - 1.5, y: 6.95, w: 1.5, h: 0.3, fontSize: 11, color: K.muted, align: "right" });
  slide.addShape(pres.shapes.RECTANGLE, { x: 0, y: 7.42, w: SW, h: 0.08, fill: { color: K.line }, line: { type: "none" } });
  slide.addShape(pres.shapes.RECTANGLE, { x: 0, y: 7.42, w: SW * n / total, h: 0.08, fill: { color: K.red }, line: { type: "none" } });
}

function header(slide, label, title, pill) {
  tb(slide, label.toUpperCase(), { x: MX, y: 0.66, w: 9, h: 0.3, fontFace: MONO, fontSize: 13, color: K.red, charSpacing: 1.5 });
  const fs = title.length > 48 ? 25 : title.length > 40 ? 27 : 30;
  tb(slide, title, { x: MX, y: 0.98, w: CW, h: 0.62, fontSize: fs, bold: true, color: K.bordo, valign: "middle" });
  slide.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: SW - MX - 1.5, y: 0.66, w: 1.5, h: 0.33, rectRadius: 0.16, fill: { color: K.chip }, line: { type: "none" } });
  tb(slide, pill, { x: SW - MX - 1.5, y: 0.66, w: 1.5, h: 0.33, fontFace: MONO, fontSize: 12, color: K.bordo, align: "center", valign: "middle" });
}

function card(slide, x, y, w, h, dark) {
  slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x, y, w, h, rectRadius: 0.12,
    fill: { color: dark ? K.bordo : K.card }, line: dark ? { type: "none" } : { color: K.line, width: 0.75 },
  });
}

function capLabel(slide, text, x, y, w, color) {
  tb(slide, text.toUpperCase(), { x, y, w, h: 0.3, fontFace: MONO, fontSize: 12.5, color, charSpacing: 1.5 });
}

// ---------------------------------------------------------------- title slide
{
  const s = pres.addSlide(); s.background = { color: K.bordo };
  n += 1;
  tb(s, "DS 501 · INTRODUCTION TO DATA SCIENCE", { x: MX, y: 0.8, w: 7, h: 0.3, fontFace: MONO, fontSize: 14, color: K.gold, charSpacing: 1.5 });
  tb(s, `Week ${String(W).padStart(2, "0")} · ${weekTitle}`, { x: MX, y: 2.4, w: 6.6, h: 0.45, fontFace: MONO, fontSize: 20, color: K.gold });
  tb(s, "Reading Summaries", { x: MX, y: 2.95, w: 6.8, h: 0.95, fontSize: 44, bold: true, color: K.onDark });
  tb(s, "Two slides per paper: the problem and key ideas, then what to take away and how it connects to this week. Use them after your own first pass, not instead of it.",
    { x: MX, y: 4.05, w: 6.4, h: 1.2, fontSize: 17, color: K.onDark2, valign: "top" });
  tb(s, "International Balkan University", { x: MX, y: 6.45, w: 6, h: 0.3, fontSize: 14, color: K.onDark2 });
  tb(s, "THE PAPERS", { x: 8.0, y: 1.55, w: 4.4, h: 0.3, fontFace: MONO, fontSize: 13, color: K.onDark2, charSpacing: 1.5 });
  let r = 0, o = 0;
  papers.forEach((p, i) => {
    const code = p.kind === "Required" ? `R${++r}` : `O${++o}`;
    const y = 1.95 + i * 1.0;
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 8.0, y, w: 4.45, h: 0.85, rectRadius: 0.1,
      fill: { color: K.bordoCard }, line: p.kind === "Required" ? { type: "none" } : { color: K.gold, width: 0.75 } });
    tb(s, code, { x: 8.18, y, w: 0.6, h: 0.85, fontFace: MONO, fontSize: 18, bold: true, color: K.gold, valign: "middle" });
    tb(s, p.label, { x: 8.9, y: y + 0.12, w: 3.45, h: 0.32, fontSize: 15, bold: true, color: K.onDark });
    tb(s, `${p.kind} · ${p.short_title}`, { x: 8.9, y: y + 0.44, w: 3.45, h: 0.3, fontSize: 11.5, color: K.onDark2, fit: "shrink" });
  });
  s.addNotes("These summaries support the reading; they do not replace it. Do Keshav's first pass on each paper yourself (title, abstract, introduction, headings, conclusions), then use the two slides to check what you found. Your half-page note for each required paper should still be in your own words: the problem, the key idea, and how it connects to this week.");
}

// ---------------------------------------------------------------- per paper
let rq = 0, op = 0;
for (const p of papers) {
  const isReq = p.kind === "Required";
  const idx = isReq ? ++rq : ++op;
  const label = `Week ${W} · ${p.kind} reading ${idx} · ${p.label}`;
  const pill = isReq ? "Required" : "Optional";

  // Slide A: problem, key ideas, key term
  {
    const s = pres.addSlide(); s.background = { color: K.paper };
    header(s, label, p.short_title, pill);
    tb(s, p.citation, { x: MX, y: 1.66, w: CW, h: 0.5, fontSize: 12, italic: true, color: K.muted, valign: "top" });
    // left: the problem
    const top = 2.35, h = 3.0;
    card(s, MX, top, 4.6, h, true);
    capLabel(s, "The problem", MX + 0.28, top + 0.25, 4.0, K.gold);
    tb(s, p.problem, { x: MX + 0.28, y: top + 0.65, w: 4.05, h: h - 0.85, fontSize: 16, color: K.onDark, valign: "top", lineSpacingMultiple: 1.12 });
    // right: key ideas
    const rx = MX + 4.6 + 0.35, rw = CW - 4.6 - 0.35;
    card(s, rx, top, rw, h, false);
    capLabel(s, "Key ideas", rx + 0.28, top + 0.25, 4, K.red);
    p.key_ideas.forEach((k, i) => {
      const y = top + 0.68 + i * 0.75;
      tb(s, String(i + 1).padStart(2, "0"), { x: rx + 0.28, y, w: 0.55, h: 0.6, fontFace: MONO, fontSize: 17, bold: true, color: K.red, valign: "top" });
      tb(s, k, { x: rx + 0.9, y, w: rw - 1.15, h: 0.68, fontSize: 15.5, color: K.ink, valign: "top" });
    });
    // bottom: key term
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: MX, y: 5.65, w: CW, h: 0.85, rectRadius: 0.12, fill: { color: K.band }, line: { color: K.line, width: 0.75 } });
    tb(s, [
      { text: "Key term: ", options: { color: K.red, bold: true } },
      { text: p.key_term.term, options: { color: K.bordo, bold: true } },
      { text: ` — ${p.key_term.definition}`, options: { color: K.ink } },
    ], { x: MX + 0.3, y: 5.65, w: CW - 0.6, h: 0.85, fontSize: 15.5, valign: "middle" });
    footer(s);
    s.addNotes(p.notes_slide1);
  }

  // Slide B: takeaways, course link, limitation, note question
  {
    const s = pres.addSlide(); s.background = { color: K.paper };
    header(s, label, p.slide2_title, pill);
    const top = 1.85, h = 3.5, lw = 6.9;
    card(s, MX, top, lw, h, false);
    capLabel(s, "What to take away", MX + 0.28, top + 0.25, 5, K.red);
    p.findings.forEach((f, i) => {
      const y = top + 0.7 + i * 0.9;
      s.addShape(pres.shapes.OVAL, { x: MX + 0.28, y: y + 0.02, w: 0.42, h: 0.42, fill: { color: K.chip }, line: { type: "none" } });
      tb(s, String(i + 1), { x: MX + 0.28, y: y + 0.02, w: 0.42, h: 0.42, fontFace: MONO, fontSize: 14, bold: true, color: K.bordo, align: "center", valign: "middle" });
      tb(s, f, { x: MX + 0.9, y, w: lw - 1.15, h: 0.8, fontSize: 15.5, color: K.ink, valign: "top" });
    });
    const rx = MX + lw + 0.35, rw = CW - lw - 0.35;
    card(s, rx, top, rw, h, true);
    capLabel(s, `This week`, rx + 0.28, top + 0.25, rw - 0.5, K.gold);
    tb(s, p.course_link, { x: rx + 0.28, y: top + 0.62, w: rw - 0.56, h: 1.5, fontSize: 14.5, color: K.onDark, valign: "top" });
    capLabel(s, "Limitation", rx + 0.28, top + 2.05, rw - 0.5, K.gold);
    tb(s, p.limitation, { x: rx + 0.28, y: top + 2.4, w: rw - 0.56, h: 0.95, fontSize: 13.5, color: K.onDark2, valign: "top" });
    // bottom: question for the note
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: MX, y: 5.65, w: CW, h: 0.85, rectRadius: 0.12, fill: { color: K.greenBg }, line: { type: "none" } });
    tb(s, [
      { text: isReq ? "For your half-page note: " : "To think about: ", options: { color: K.greenInk, bold: true } },
      { text: p.note_question, options: { color: K.ink } },
    ], { x: MX + 0.3, y: 5.65, w: CW - 0.6, h: 0.85, fontSize: 15.5, valign: "middle" });
    footer(s);
    s.addNotes(p.notes_slide2);
  }
}

// ---------------------------------------------------------------- closing slide
{
  const s = pres.addSlide(); s.background = { color: K.bordo };
  tb(s, `DS 501 · WEEK ${W} · READING SUMMARIES`, { x: MX, y: 0.8, w: 8, h: 0.3, fontFace: MONO, fontSize: 14, color: K.gold, charSpacing: 1.5 });
  tb(s, "Writing Your Half-Page Note", { x: MX, y: 1.4, w: CW, h: 0.8, fontSize: 38, bold: true, color: K.onDark, charSpacing: 1 });
  const steps = [
    ["01", "The problem", "What was broken or missing before this paper? One or two sentences."],
    ["02", "The key idea", "The one idea you would keep if you forgot everything else. Your own words."],
    ["03", "The connection", "Where it shows up this week: a lesson, the lab, or your project data."],
  ];
  const cw = (CW - 2 * 0.35) / 3;
  steps.forEach(([num, head, body], i) => {
    const x = MX + i * (cw + 0.35);
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y: 2.6, w: cw, h: 2.6, rectRadius: 0.12, fill: { color: K.bordoCard }, line: { type: "none" } });
    tb(s, num, { x: x + 0.3, y: 2.85, w: 1, h: 0.6, fontFace: MONO, fontSize: 28, bold: true, color: K.gold });
    tb(s, head, { x: x + 0.3, y: 3.55, w: cw - 0.6, h: 0.45, fontSize: 20, bold: true, color: K.onDark });
    tb(s, body, { x: x + 0.3, y: 4.05, w: cw - 0.6, h: 1.0, fontSize: 15, color: K.onDark2, valign: "top" });
  });
  tb(s, "Half a page means about 150–200 words. Bring it to the next class; one quiz question may refer to the required reading.",
    { x: MX, y: 5.6, w: CW, h: 0.6, fontSize: 15, color: K.onDark2 });
  n += 1;
  tb(s, `${n} / ${total}`, { x: SW - MX - 1.5, y: 6.95, w: 1.5, h: 0.3, fontSize: 11, color: K.onDark2, align: "right" });
  s.addNotes("A good note is short and specific. Name the problem the paper addresses, state its main idea in one or two sentences of your own, and connect it to something concrete from this week: a lesson, the lab notebook, or the dataset you are considering for your project. If you used an AI tool to help you understand the paper, say so in one line at the end, as for any other submission.");
}

pres.writeFile({ fileName: outPath }).then(f => console.log("wrote", f));
