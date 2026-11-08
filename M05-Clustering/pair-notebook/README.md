# Pair Notebook 05 — Finding Groups in Code

**This is an assignment.** Instead of handing in a script, you work through a
**one-on-one tutoring session**: an AI tutor builds a [marimo](https://marimo.io)
notebook with you, cell by cell, and keeps a log of the conversation. At the
end you have a notebook that is both your own lecture note and the thing that
gets graded.

**You write code in this one.** You find groups in the world airport network,
write the two scores that compare groups (NMI and ARI), and write two models
that build a network from groups. Every exercise is a real notebook cell with a
few lines already written and a few blanks. **What is graded is your code and how you got there**,
not whether a blank was right first time. A session takes about 90 minutes,
and you can stop and pick up later.

---

## For students

### One-time setup (5 minutes)

Everything below happens in a **terminal** — the app where you type commands.
On macOS it is **Terminal** (⌘-Space, type "terminal"); on Windows it is
**Windows Terminal** or **PowerShell** (Start menu, type "powershell"). Open it,
then `cd` into this folder — the one holding this README:

```bash
cd path/to/this/folder
```

**1. Install three things**, whatever your operating system:

| | what it is | Windows | macOS |
|---|---|---|---|
| [Node.js](https://nodejs.org) 24+ | your tutor runs on it | `winget install OpenJS.NodeJS` | `brew install node` |
| [uv](https://docs.astral.sh/uv/getting-started/installation/) | runs the notebook | `winget install astral-sh.uv` | `brew install uv` |
| [git](https://git-scm.com) | fetches your tutor's toolkit, and hands your work in | `winget install Git.Git` | `xcode-select --install` |

**Already have one of them? Check its version.** An old `uv` is the commonest
reason the notebook never opens.

```bash
node --version   # v24 or newer
uv --version     # 0.7.21 or newer
```

If `uv` is older, update it. On macOS run `brew upgrade uv`; on Windows run
`winget upgrade astral-sh.uv`; if you installed it another way, run `uv self update`.
You do not need to install Python: `uv` fetches the right one by itself.

**2. Put your key where your terminal can see it.** Your instructor issues you
one (`sk-nsci-…`). It is not the same command on the two systems:

**macOS / Linux** — add this line to `~/.zshrc` (or `~/.bashrc`), then open a
**new** terminal so it takes effect:

```bash
export NETSCI_API_KEY="sk-nsci-..."
```

**Windows (PowerShell)** — run this once, then open a **new** terminal.
`setx` only affects terminals opened *afterwards*, so the window you type it in
will not see it:

```powershell
setx NETSCI_API_KEY "sk-nsci-..."
```

Paste the key on **one line**, with nothing around it. A key that arrives in an
email is often wrapped onto two lines; join it back up.

**Never paste the key into a file in this folder.** You submit by pushing this
folder to your own GitHub repository, and a key committed there is a key that
has to be revoked and reissued.

**3. Run the setup script.**

```bash
node setup-pi.mjs
```

It installs `pi` (the agent your tutor runs on), adds the course model to
`~/.pi/agent/models.json`, tells `pi` that this folder is yours so it does not
have to ask, downloads the notebook's Python packages so your first session
starts fast, and makes one real request so you find out **here**, not
mid-lesson, whether your key works. It is safe to re-run, it keeps a backup of
your old `models.json`, and it leaves any providers you already had alone.

The package download is a few hundred megabytes and takes a couple of minutes
on a slow connection. That is the slowest part of the whole setup, and it only
happens once.

When it prints `You are set`, you are done.

<details>
<summary>If you would rather do it by hand</summary>

Install pi with `npm install -g @earendil-works/pi-coding-agent`, then create
`~/.pi/agent/models.json` — or merge this `netsci` block into the one you
already have. Copy it exactly; it reads the key from your environment, so there
is nothing to fill in:

```jsonc
{
  "providers": {
    "netsci": {
      "baseUrl": "https://llm.skojaku.com/v1",
      "api": "openai-completions",
      "apiKey": "$NETSCI_API_KEY",
      "compat": { "supportsDeveloperRole": false },
      "models": [
        { "id": "tutor",   "name": "Course Tutor",   "reasoning": true,
          "input": ["text"], "contextWindow": 131072, "maxTokens": 32768,
          "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 } },
        { "id": "vision",  "name": "Course Vision",
          "input": ["text", "image"], "contextWindow": 1048576, "maxTokens": 8192,
          "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 } },
        { "id": "referee", "name": "Course Referee", "reasoning": true,
          "input": ["text"], "contextWindow": 131072, "maxTokens": 8192,
          "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 } }
      ]
    }
  }
}
```

</details>

Your key has a per-week allowance. To see what is left of it, run:

```bash
curl -H "Authorization: Bearer $NETSCI_API_KEY" https://llm.skojaku.com/v1/usage
```

(Opening that address in a browser will not work — it needs your key.)

**4. Nothing else.** The tutor's own toolkit —
[`pi-pair-notebook`](https://github.com/skojaku/pi-pair-notebook) and its
dialog companion — is listed in `.pi/settings.json`, and `pi` fetches it the
first time you run. That first start takes a few seconds longer than the rest.

> **If `pi` ever asks "Trust project folder?"** — answer **Trust**, the first
> option. It is asking whether this folder may set up your tutor, and this
> folder is your own assignment. The setup script normally answers it for you,
> so you will only see it if you skipped step 3 or moved the folder. If you
> answered "Do not trust" by mistake, your tutor will start but have no
> notebook and no tools; run `pi --approve` once to undo it.

### Every session

Run this **inside this folder**:

```bash
pi
```

Say hello. Your tutor starts the notebook itself, opens it in your browser, and
closes it again when you are done — there is nothing else to launch.

Two windows appear:

| Window | What it is |
|---|---|
| **Terminal** (tutor) | Where you and your tutor talk — questions and answers happen here. |
| **Browser** (notebook) | The whiteboard, and where you write. This module opens marimo's **editor**, not a read-only page: the exercises are real cells and you edit them in place. |

**Nothing to install, nothing to set up, no pen and paper.** This module is
entirely on screen.

### How an exercise works

Every one of the eight checkpoints is a **real cell** in the notebook, in the
editor you will keep using after this course:

1. A short brief above the cell: **Carried over** (the names from earlier
   exercises and from the notebook that the cell uses), the task, and under
   **Other tools** any call you have not met, with a tiny example.
2. **The cell.** A few lines of Python are already written, with blanks marked
   `___`. Click into it and fill them in.
3. **Run it** — the ▶ at the cell's right, or Ctrl-Enter.
   Click **📋 Task** above the cell to read the task. Run it as often as
   you like: nothing you type can break anything, and if it errors marimo
   shows you where.
4. When you want your tutor to look, press **Submit to Tutor** under the cell.
   Your tutor reads your code and says something short in the terminal.
5. 🧪 The cell above each exercise is yours to try things in. Nothing in it is
   marked.

**One marimo message is worth recognising, because it is not a mistake in
your Python.** *"This cell redefines variables from other cells"* means a name
you used is already made by an earlier cell. Give yours a different name.

**Leiden is random**, so your numbers differ a little from a classmate's.

### What gets turned in

The session produces everything automatically — you don't "write up" anything:

- `notebook.py` — the notebook you built together
- `session_artifacts/session_log.jsonl` — your answers, verbatim
- `session_artifacts/session_summary.md` — a summary for the instructor

**Your tutor hands it in for you.** Say so in the terminal — "can you submit
this?" — at any point in the session, as often as you like, and it commits
your work and hands it in. It does the same by itself when you finish the
module. Nothing to remember, and nothing to type.

That works because you cloned the repository the course assignment link
created for you and ran the session inside it. If you are working somewhere
else, your tutor will say so when you ask.

<details>
<summary>If you would rather hand it in by hand</summary>

Two steps, and the second one is the one that counts:

```bash
git add -A && git commit -m "Pair Notebook 05" && git push
git tag "submit/$(date -u +%Y-%m-%dT%H-%M-%SZ)-$(git rev-parse --short HEAD)" && git push --tags
```

The first line saves and uploads your work. The second one is what tells the
course that this is a submission — a push on its own is filed and not marked.
Your tutor does both when it hands in for you.

</details>

The commit history is part of the picture: it shows when the work happened, and
a session finished in three sittings is exactly as good as one finished in one.

**Honesty note:** needing hints is *not* penalized. Your tutor's notes are read for how you worked, not for how few hints you used.

### When something goes wrong

**Nothing you have already done is ever lost.** Your answers are written to
`session_artifacts/` as they happen, and marimo saves the notebook every time
you run a cell — your code IS `notebook.py`. Whatever the
problem, closing the terminal and running `pi` again picks up where you
stopped — it will ask whether to continue or start fresh.

Find the line you actually saw on screen:

| What you see | What it means | What to do |
|---|---|---|
| `⚠ Your tutor cannot reach the course server` | Your key or the address is wrong — the message says which. | Do what it says; it usually means re-running `node setup-pi.mjs`. |
| `Connection error.`, repeated | Your computer cannot reach the internet, or the course server is down. | Check your connection, wait a few minutes, run `pi` again. Tell your instructor if it keeps happening. |
| `invalid_api_key` | The key is wrong, or was never set in *this* terminal window. | Check it, open a new terminal, run `node setup-pi.mjs` again. |
| something about your **allowance** or `402` | You have used this week's quota. | Tell your instructor. Your work is saved; you can carry on when it resets. |
| `model backend is unavailable` + a `request_id` | The course server's own upstream is having a moment. Not your fault. | Wait a few minutes and run `pi` again. Send your instructor the `request_id` if it persists. |
| `uv 0.7.21 or newer is required … found 0.7.13` (any older number) | Your `uv` is too old to start the notebook. Your tutor then falls back to a plain terminal and nothing is saved to the notebook. | Update `uv` as in the setup step above, check `uv --version`, then run `pi` again. |
| A cell printed `NameError` or `SyntaxError` | Ordinary. Something in the cell is not spelled the way Python wants. | Read the line it names, fix it, run it again. If you cannot see it, say so in the terminal. |
| `This cell redefines variables from other cells` | A name you used is already made by an earlier cell. Not a mistake in your code. | Give yours a different name, or use the one that already exists. Your tutor will say which. |
| The notebook page went blank, or you closed the tab | The whiteboard lost its connection. | Nothing — your tutor reopens it by itself. If it does not, say so in the terminal. |
| `⚠ something hiccuped — your tutor is on it` | A notebook operation failed and your tutor is retrying. | Nothing. Keep talking. |
| Your tutor keeps asking the same thing | It is stuck. | Use the **⚖️** box at the bottom of the notebook — that is exactly what it is for. |

If you get truly stuck, say so in the terminal in your own words. Your tutor is
told to keep teaching rather than debug, so for anything that looks like the
list above, email your instructor — with the line you saw, copied out.

---

## For the instructor / TA

### What this module teaches

Eight checkpoints in one chapter, "Finding Groups in Code", in igraph and numpy
only (graph-tool has no Windows build, and nothing on PyPI infers a stochastic
block model). It covers the course's module 5, on the world airport network
(3,360 airports, 18,783 routes from 2014, with a continent and a country for
each airport).

| checkpoints | what the student writes |
|---|---|
| `cp1_graph`, `cp2_leiden` | the network from a route list; `community_leiden` with the modularity objective |
| `cp3_nmi`, `cp4_ari` | NMI and ARI from a table of counts, by hand |
| `cp5_compare` | Leiden and Infomap scored against continents and countries |
| `cp6_sbm`, `cp7_hubs` | a stochastic block model sampler; the missing hubs (largest degree about 40 against 246) |
| `cp8_dcsbm` | the quiz's estimate of theta, and a degree-corrected sampler; the hubs back (largest degree about 245) |

The module ends at cp8. There is no graph-tool notebook (decided 2026-10-13).

### What's in this folder

| File | Role |
|---|---|
| `lesson/` | The curriculum (`index.json` + `ch1-finding-groups.yaml`): scaffold, brief, accept criteria, hints and note for each checkpoint. **Edit these to change the lesson.** |
| `AGENTS.md` | The tutor's behaviour contract (auto-loaded by pi). |
| `notebook.template.py` | Pristine starter. `notebook.py` is the working copy, created on first run. |
| `bench.py` | The checks and pictures. Beside the notebook, not in it: in the editor every cell is one click from being read. |
| `assets/airports/` | The two CSVs, built by `tools/build_assets.py` from OurAirports and OpenFlights. |
| `tools/test_bench.py`, `tools/test_scaffolds.py` | Run the checks against reference solutions and wrong answers, and every scaffold filled with its solution. Source repo only. |
| `plan.md` | Why the module is shaped this way. Source repo only. |
| `.pi/settings.json` | The model, thinking level and the toolkit **pinned by tag**. |

The `nb_*` toolkit itself is shared by every module and lives in
[`skojaku/pi-pair-notebook`](https://github.com/skojaku/pi-pair-notebook).

### Credits

Airports and their continents and countries: [OurAirports](https://ourairports.com) (public domain).
Routes: [OpenFlights](https://openflights.org/data.html) (Open Database License), from 2014.

### Known limitations

- The chapter scripts ship in the folder, so a determined student can read the
  accept criteria. Fine for formative use.
- The checks mark the answer, not the route to it.
- Leiden is random, so no figure of the student's is compared with a literal.
- Per-student cost control lives in the course LLM gateway, not here.
- The marimo server runs with `--no-token` on localhost, fine on a laptop and
  not on a shared host.
