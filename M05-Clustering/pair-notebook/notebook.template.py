# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo",
#     "igraph==1.0.0",
#     "matplotlib",
#     "seaborn",
#     "altair",
#     "numpy==2.5.3",
#     "pandas",
#     "pillow",
# ]
# ///

# The notebook a session starts from. Everything below is infrastructure that
# survives nb_fresh_start (only NAMED cells are wiped), and every cell the
# lesson adds is named.
#
# Community detection on the world airport network, in igraph and numpy only
# (graph-tool has no Windows build). The pictures are a longitude/latitude
# scatter and two charts; an improvised detour cell draws in matplotlib.

import marimo

__generated_with = "0.23.16"
app = marimo.App(width="medium", css_file="lecture-hall.css")


@app.cell(hide_code=True)
def _(mo):
    # One single string literal on purpose: marimo round-trips mo.md cells
    # through its markdown serializer, and implicit string concatenation
    # corrupts them (the code itself gets wrapped as markdown content).
    mo.md(
        r"""<p style="text-align:right; color:#6A6D75; font-size:12px; margin:0;">🐛 Something broken or odd? Email Prof. Sadamori Kojaku &middot; <a href="mailto:skojaku@binghamton.edu" style="color:#3959A6;">skojaku@binghamton.edu</a></p>"""
    )
    return


# ── The plumbing, and it lives at the BOTTOM of the page ─────────────────
# Everything from here to the appeal box is machinery: imports, the figure
# theme, the data, the drawing helpers. None of it is the lesson, and
# in marimo none of it has to sit above the lesson either — a notebook is a
# dependency graph, and where a cell SITS on the page has nothing to do
# with when it runs. So the notebook tool re-pins this whole block below
# every cell it inserts (the same move it has always made for the appeal
# box), and the student's page holds the exercise in hand and little else.
#
# Each of these cells carries `# tutor:plumbing` INSIDE its body, and that
# is what the pin looks for. A comment between cells — this one — does not
# survive marimo's own save; a comment inside a cell is part of its code
# and does. And the tell has to be opt-in rather than "every unnamed cell",
# or the first scratch cell a student adds for themselves would be swept
# to the bottom of their own notebook.
#
# Anonymous (def _) on purpose, like the appeal box: nb_fresh_start's wipe
# deletes every NAMED cell.


@app.cell(hide_code=True)
def _():
    # tutor:plumbing — kept below the lesson; see the note above.
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    # tutor:plumbing — the focus-mode switch.
    # With it on (the default), lecture-hall.css shows only the exercise in
    # hand: the newest *_work cell, its output, its brief, and the cells the
    # tutor puts after it. Everything above it and all of this plumbing is hidden, not
    # deleted; switching it off brings it all back. The .lh-focus-toggle
    # wrapper is exempt from the hiding and floats to the top of the page.
    focus_mode = mo.ui.switch(value=True, label="🎯 Show only the exercise I'm on")
    mo.Html(f"<div class='lh-focus-toggle'>{focus_mode}</div>")
    return (focus_mode,)


@app.cell(hide_code=True)
def _(mo):
    # tutor:plumbing — how the exercises work, first on the page, always.
    # It used to be chapter 1's opening, which focus mode hides as soon as
    # the second exercise lands. Lifted to the top by lecture-hall.css
    # (.lh-howto) and never hidden. Folded, in the same quiet dashed tab as
    # the answer fold (lecture-hall.css, .lh-answer): it is read once, and
    # left open it stood above every exercise for the whole session.
    _howto = mo.md(
        r"""
/// details | ℹ️ How the exercises work
    type: lh-answer

- Each exercise is a code cell with blanks marked `___`. Replace each blank with your code and run the cell.
- Click **📋 Task** above the cell to read the task. When you want your tutor to look, press **Submit to Tutor** under the cell.
- The 🧪 cell above each exercise is yours to try things in. Nothing in it is marked.

A name can be given a value in only one cell, so each exercise uses its own names. In the 🧪 cell, start your names with `_`.
///
"""
    )
    mo.Html(f"<div class='lh-howto'>{_howto.text}</div>")
    return


@app.cell(hide_code=True)
def _(mo):
    # tutor:plumbing — what the progress bar watches.
    # mo.watch.file re-runs the cells that READ `progress_log` whenever the
    # file changes, not this one — so the bar is the next cell. A directory
    # watch does not do it: it sees files come and go, not a line appended
    # (measured). The toolkit writes one line per closed checkpoint, and
    # creates the file on the first; it is created empty here so there is
    # something to watch from the start. An empty log reads as "nothing
    # logged" everywhere the toolkit reads it, resume included.
    from pathlib import Path as _Path

    _log = _Path("session_artifacts") / "session_log.jsonl"
    _log.parent.mkdir(exist_ok=True)
    _log.touch(exist_ok=True)
    progress_log = mo.watch.file(_log)
    return (progress_log,)


@app.cell(hide_code=True)
def _(mo, progress_log):
    # tutor:plumbing — the progress bar at the top of the page.
    # One segment per checkpoint in lesson/index.json: filled once the tutor
    # has logged it, amber for the one in hand. Reads, never writes. Pinned
    # to the top of the page, above everything, and kept there while the page
    # scrolls (lecture-hall.css, .lh-progress); never hidden by focus mode.
    import json as _json
    from pathlib import Path as _Path

    _ = progress_log  # the re-run trigger; the path is read directly below,
    #                   because a fresh start moves the file away for a moment
    _log = _Path("session_artifacts") / "session_log.jsonl"
    _lesson = _json.loads(_Path("lesson/index.json").read_text())
    _order = [_cp for _ch in _lesson["chapters"] for _cp in _ch["checkpoints"]]
    _done = set()
    if _log.exists():
        for _line in _log.read_text().splitlines():
            try:
                _row = _json.loads(_line)
            except ValueError:
                continue
            if _row.get("type") == "checkpoint":
                _done.add(str(_row.get("id", "")).removesuffix("_extra"))
    _now = next((i for i, _cp in enumerate(_order) if _cp not in _done), None)
    _segs = "".join(
        f"<span class='lh-seg {'done' if _cp in _done else ('now' if i == _now else '')}'></span>"
        for i, _cp in enumerate(_order)
    )
    _label = (
        f"Exercise {_now + 1} of {len(_order)}"
        if _now is not None
        else f"All {len(_order)} exercises done"
    )
    mo.Html(
        f"<div class='lh-progress'><div class='lh-progress-label'>{_label}</div>"
        f"<div class='lh-progress-track'>{_segs}</div></div>"
    )
    return


@app.cell(hide_code=True)
def _(focus_mode, mo):
    # tutor:plumbing — turns the switch into a marker the stylesheet can see.
    # The marker needs text in it: an empty span does not survive rendering.
    mo.Html(
        "" if focus_mode.value
        else "<span class='lh-show-all' style='display:none'>all</span>"
    )
    return


@app.cell(hide_code=True)
def _():
    # tutor:plumbing — kept below the lesson; see the note above.
    import matplotlib.pyplot as plt
    import numpy as np
    import seaborn as sns

    # Match figures to the lecture-hall notebook theme (lecture-hall.css).
    # seaborn first (set_theme resets rc), then our palette on top.
    sns.set_theme(style="ticks")
    plt.rcParams.update(
        {
            "figure.facecolor": "#FFFDF7",
            "axes.facecolor": "#FFFDF7",
            "savefig.facecolor": "#FFFDF7",
            "text.color": "#35373C",
            "axes.edgecolor": "#1D1E21",
            "axes.labelcolor": "#35373C",
            "axes.titlecolor": "#1D1E21",
            "xtick.color": "#35373C",
            "ytick.color": "#35373C",
            # Axis labels are read, not felt: the same system sans the page
            # prose uses (lecture-hall.css --lh-sans), one entry per platform.
            "font.family": "sans-serif",
            "font.sans-serif": [
                "Segoe UI",
                "Helvetica Neue",
                "Helvetica",
                "Arial",
                "Liberation Sans",
                "DejaVu Sans",
            ],
            # path.sketch is what draws by hand, and it is the ONLY thing that
            # does. Text is not a path, so labels stay crisp.
            "path.sketch": (1.1, 110, 2),
            "lines.linewidth": 2.2,
            "axes.linewidth": 1.8,
            "xtick.major.width": 1.4,
            "ytick.major.width": 1.4,
            "axes.spines.top": False,
            "axes.spines.right": False,
            # The accents are the lecture slides' own, verbatim: #3959A6 is
            # the object under discussion, #B14434 what THIS figure is about,
            # #DAB167 the comparison object.
            "axes.prop_cycle": plt.cycler(
                color=["#3959A6", "#B14434", "#22336B", "#DAB167", "#6A6D75"]
            ),
        }
    )
    sns.set_palette(["#3959A6", "#B14434", "#22336B", "#DAB167", "#6A6D75"])
    return np, plt, sns


@app.cell(hide_code=True)
def _():
    # tutor:plumbing — kept below the lesson; see the note above.
    import altair as alt
    import igraph as ig
    import pandas as pd

    # Altair draws its own type, so without this a chart would letter itself
    # in Vega's default face instead of the page's. The theme has to build
    # its own dict: marimo renames a cell's private names, and Altair calls
    # the theme back long after this cell has finished.
    def _lecture_hall_chart_theme():
        face = (
            'system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", '
            '"Noto Sans", "Liberation Sans", Arial, sans-serif'
        )
        return {
            "config": {
                "font": face,
                "background": "#FFFDF7",
                "view": {"stroke": "transparent"},
                "axis": {
                    "labelFont": face,
                    "titleFont": face,
                    "labelColor": "#35373C",
                    "titleColor": "#1D1E21",
                    "domainColor": "#1D1E21",
                    "domainWidth": 1.8,
                    "tickColor": "#1D1E21",
                    "gridColor": "#D9D2C2",
                },
                "legend": {"labelFont": face, "titleFont": face},
                "title": {"font": face, "fontSize": 15, "color": "#1D1E21", "anchor": "start"},
            }
        }

    try:  # Altair >= 5.5
        alt.theme.register("lecture_hall", enable=True)(_lecture_hall_chart_theme)
    except AttributeError:  # Altair < 5.5
        alt.themes.register("lecture_hall", _lecture_hall_chart_theme)
        alt.themes.enable("lecture_hall")

    return alt, ig, pd


@app.cell(hide_code=True)
def _():
    # tutor:plumbing — kept below the lesson; see the note above.
    # ── What this notebook gives you ─────────────────────────────────────
    # Folded like every other infrastructure cell: nothing is on the page
    # but the exercise in hand.
    #
    #   route_list, codes, continent, country
    #       the airport network: one (i, j) pair per route, the airport codes,
    #       and each airport's continent and country (see the data cell).
    #   block_density(g, groups), edge_ends(g, groups)
    #       the block model's P and m_rs for a partition, handed over.
    #   plot_world, plot_worlds, plot_scores, plot_degrees
    #       what the last line of an exercise calls: each draws what YOUR
    #       code produced, and judges nothing.
    #   formula, show_matrix, show_matrices, show_network, show_networks
    #       the parts the tutor builds an answer to a question from: a
    #       formula with every piece explained, a grid, a small network.
    #   check_graph, check_leiden, check_nmi, check_ari, check_compare,
    #   check_sbm, check_hubs, check_dcsbm
    #       the checks. Each runs in a hidden cell under your exercise and
    #       tells your tutor, not you, whether your code does the task.
    #   ___
    #       every blank in every exercise. Running a cell before you have
    #       filled one in says so, in those words.
    from bench import (
        ___,
        block_density,
        check_ari,
        check_compare,
        check_dcsbm,
        check_graph,
        check_hubs,
        check_leiden,
        check_nmi,
        check_sbm,
        edge_ends,
        formula,
        load_airports,
        plot_degrees,
        plot_scores,
        plot_world,
        plot_worlds,
        show_matrices,
        show_matrix,
        show_network,
        show_networks,
    )

    return (
        ___,
        block_density,
        check_ari,
        check_compare,
        check_dcsbm,
        check_graph,
        check_hubs,
        check_leiden,
        check_nmi,
        check_sbm,
        edge_ends,
        formula,
        load_airports,
        plot_degrees,
        plot_scores,
        plot_world,
        plot_worlds,
        show_matrices,
        show_matrix,
        show_network,
        show_networks,
    )


@app.cell(hide_code=True)
def _(load_airports):
    # tutor:plumbing — kept below the lesson; see the note above.
    # ── The data ─────────────────────────────────────────────────────────
    # Read from assets/airports/, never downloaded. OurAirports gives each
    # airport its continent and country; OpenFlights gives the routes (from
    # 2014, the last year it was updated; ODbL). Giant component only:
    # 3,360 airports and 18,783 routes. tools/build_assets.py makes the files.
    codes, names, route_list, continent, country, lon, lat = load_airports()
    return codes, continent, country, lat, lon, names, route_list


# The ⚖️ appeal box lives at the BOTTOM of the page, always: the notebook
# tool re-pins these two cells below every cell it inserts, finding them by
# the "tutor_stuck_send" marker in their code. They are anonymous (def _) on
# purpose — nb_fresh_start's wipe deletes every NAMED cell.
@app.cell(hide_code=True)
def _(mo):
    tutor_stuck_text = mo.ui.text_area(
        placeholder=(
            "What's going on? e.g. \"I answered this and I think it should count\", "
            "\"I'd like a fresh try at this one\", \"we're going in circles — let's move on\""
        ),
        rows=2,
    )
    tutor_stuck_send = mo.ui.run_button(label="⚖️ Tutor gets stuck — call the referee")
    # .lh-referee: focus mode keeps this box on screen (lecture-hall.css).
    mo.Html("<div class='lh-referee'>" + mo.as_html(mo.vstack([
        mo.md("<hr style='border:none;border-top:1px solid #E4E6EA;margin:18px 0 6px'>"),
        mo.md(
            "<span style='color:#6A6D75;font-size:13px'>⚖️ <strong>Stuck with your "
            "tutor?</strong> If the two of you are going in circles — you think an "
            "answer should count, you want a fresh try, or you'd rather move on — "
            "say so here and press the button, or type judge in the terminal. A "
            "second, stronger model reads the whole situation and makes a call "
            "your tutor has to follow. Using it is never held against you.</span>"
        ),
        tutor_stuck_text,
        tutor_stuck_send,
    ])).text + "</div>")
    return tutor_stuck_send, tutor_stuck_text


@app.cell(hide_code=True)
def _(mo, tutor_stuck_send, tutor_stuck_text):
    from pathlib import Path as _P_appeal

    if tutor_stuck_send.value:
        _P_appeal("session_artifacts").mkdir(exist_ok=True)
        (_P_appeal("session_artifacts") / "appeal.txt").write_text(
            (tutor_stuck_text.value or "").strip() or "(no details given)"
        )
        with open("session_artifacts/student_signal.txt", "a") as _f:
            _f.write("tutor_stuck\n")
        _appeal_out = mo.md(
            "<span style='color:#6A6D75;font-size:13px'>✅ <strong>The referee is "
            "reading your case.</strong> It can take a minute — your tutor will "
            "come back to you in the terminal with the decision.</span>"
        )
    else:
        _appeal_out = mo.md("")
    _appeal_out
    return


if __name__ == "__main__":
    app.run()
