# DS 501 · Introduction to Data Science — course site

Public course site for DS 501 at International Balkan University, Skopje.
Live at https://afnhsn-ibu.github.io/ds501/

## How it is put together

`course.yml` is the single source of truth: the 12 weeks, their lessons, labs,
papers, milestones and the assessment table. `tools/build_site.py` turns it into
the finished HTML in `docs/`, the same way `tools/build_deck.py` turns a week's
content file into a deck. The site carries the Template v2 identity: bordeaux
`#7A1F2B`, IBU red `#C8102E`, gold `#E9C46A` on bordeaux, warm paper `#FBF8F5`,
Source Sans 3 and IBM Plex Mono.

```bash
pip install pyyaml
python3 tools/build_site.py            # writes docs/
python3 -m http.server -d docs 8000    # look at it locally
python3 tools/build_site.py --preview  # one shareable file
```

Never edit anything in `docs/` by hand; it is overwritten on every build.

## Setup

In **Settings → Pages**, set the source to branch `main`, folder `/docs`. There
is nothing to install on the server and no build step in the cloud. The included
Action only checks that `docs/` was rebuilt after `course.yml` changed.

## What is public and what is not

| Public, this repository | Private, `ds501-instructor` |
|---|---|
| Site pages, `course.yml` | Quiz keys and model answers |
| `notebooks/student/` | `notebooks/solutions/` (`*_SOLUTION.ipynb`) |
| Reading handouts, papers list | Instructor guides, marking guides |

Nothing under `instructor/` or `solutions/` belongs in this repository.

## Corrections

Students and colleagues: open an issue or send a pull request. Corrections are
welcome and credited.
