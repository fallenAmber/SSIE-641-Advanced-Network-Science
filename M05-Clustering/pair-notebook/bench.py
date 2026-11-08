"""The benches: what marks every code cell in this module, out of sight.

Imported by notebook.py, NOT defined in it. In marimo's editor `hide_code` is a
fold and not a hiding place, so the answers live here, in a file beside the
notebook, with the same standing as the chapter scripts and their `accept:`
blocks.

Two kinds of function live here, and the student only ever sees one:

  * `plot_*` and `block_density`, `edge_ends` -- what a scaffold calls. The
    plots draw what the student's own code produced and judge nothing; the two
    helpers hand over a quantity the exercise does not ask them to compute.
  * `check_*` -- called from a hidden `<checkpoint>_check` cell under the
    student's. A check renders nothing visible: only a hidden marker,
    `data-tutor-verdict="pass"` or `"fail"`, which the toolkit reads when the
    student presses Submit to Tutor and hands to the tutor.

One rule holds for every check: RECOMPUTE the right answer rather than hold a
literal. Leiden is not deterministic, so no check compares against a number
from one run; it compares the student's output with what the student's own
input implies.
"""

from __future__ import annotations

import csv
import html
import random
from pathlib import Path

import altair as alt
import igraph as ig
import marimo as mo
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

_A = Path("assets") / "airports"


# ── the blank ────────────────────────────────────────────────────────────
# Every exercise ships with `___` where the student's code goes. A blank that
# quietly worked (0, None) would let a cell run and be marked wrong, which is a
# worse lesson than an error with a clear sentence in it, so `___` refuses
# every operation with the same sentence.
class _Blank:
    """`___` -- a blank the student has not filled in yet."""

    _WHY = "___ is a blank: replace it with your answer, then run the cell again."

    def _refuse(self, *_a, **_k):
        raise TypeError(self._WHY)

    __index__ = __int__ = __float__ = __len__ = __iter__ = _refuse
    __call__ = __add__ = __radd__ = __sub__ = __rsub__ = _refuse
    __mul__ = __rmul__ = __truediv__ = __rtruediv__ = __getitem__ = _refuse
    __round__ = __neg__ = __pow__ = __rpow__ = __floordiv__ = __mod__ = _refuse
    __lt__ = __le__ = __gt__ = __ge__ = __matmul__ = __rmatmul__ = _refuse

    def __getattr__(self, name):
        # A leading underscore is a PROGRAM asking what this object is (marimo
        # looking for _repr_html_, numpy for __array__); only a student's own
        # `___.sum()` gets the sentence.
        if name.startswith("_"):
            raise AttributeError(name)
        self._refuse()

    def __repr__(self):
        return "___"


___ = _Blank()


# ── the data ─────────────────────────────────────────────────────────────
# Read with the csv module, never pandas: pandas reads the continent code "NA"
# (North America) as a missing value.
def load_airports():
    """codes, names, route_list, continent, country, lon, lat -- one entry per airport."""
    rows = list(csv.DictReader(open(_A / "airports.csv", encoding="utf-8")))
    codes = [r["iata"] for r in rows]
    index = {c: i for i, c in enumerate(codes)}
    route_list = [
        (index[r["src"]], index[r["dst"]])
        for r in csv.DictReader(open(_A / "routes.csv", encoding="utf-8"))
    ]
    return (
        codes,
        [r["name"] for r in rows],
        route_list,
        [r["continent"] for r in rows],
        [r["country"] for r in rows],
        np.array([float(r["lon"]) for r in rows]),
        np.array([float(r["lat"]) for r in rows]),
    )


_codes, _names, _routes, _continent, _country, _lon, _lat = load_airports()
N_AIRPORTS = len(_codes)


def _real():
    return ig.Graph(n=N_AIRPORTS, edges=_routes)


_g = _real()
_deg = np.array(_g.degree())


# ── the reference scores ─────────────────────────────────────────────────
# The lecture's definitions. NMI = 2 I(X;Y) / (H(X) + H(Y)); ARI = (Rand -
# E[Rand]) / (max Rand - E[Rand]). Natural log; the base cancels in the ratio.
def _table(a, b):
    ai = np.unique(np.asarray(a), return_inverse=True)[1]
    bi = np.unique(np.asarray(b), return_inverse=True)[1]
    t = np.zeros((ai.max() + 1, bi.max() + 1))
    np.add.at(t, (ai, bi), 1)
    return t


def _ref_nmi(a, b):
    t = _table(a, b)
    n = t.sum()
    pa, pb = t.sum(1) / n, t.sum(0) / n
    nz = t > 0
    mi = (t[nz] / n * np.log(t[nz] * n / np.outer(pa * n, pb * n)[nz])).sum()
    h = lambda p: -(p[p > 0] * np.log(p[p > 0])).sum()
    return float(2 * mi / (h(pa) + h(pb)))


def _ref_ari(a, b):
    t = _table(a, b)
    n = t.sum()
    c2 = lambda x: x * (x - 1) / 2
    s, sa, sb = c2(t).sum(), c2(t.sum(1)).sum(), c2(t.sum(0)).sum()
    expected = sa * sb / c2(n)
    return float((s - expected) / ((sa + sb) / 2 - expected))


def _ref_leiden(seed=0):
    # The checks run while the student works, so leave Python's random state as found:
    # a student's own Leiden runs must stay different from one another.
    state = random.getstate()
    try:
        random.seed(seed)
        return _g.community_leiden(objective_function="modularity").membership
    finally:
        random.setstate(state)


# ── given quantities ─────────────────────────────────────────────────────
def _relabel(groups):
    return np.unique(np.asarray(groups), return_inverse=True)[1]


def edge_ends(g, groups):
    """m[r][s]: edge ends in group r whose other end is in group s (an edge
    inside r counts twice in m[r][r]). The quiz's m_rs."""
    z = _relabel(groups)
    k = z.max() + 1
    m = np.zeros((k, k))
    for u, v in g.get_edgelist():
        m[z[u], z[v]] += 1
        m[z[v], z[u]] += 1
    return m


def block_density(g, groups):
    """P[r][s]: the share of airport pairs between group r and group s that
    have a route (within a group, the share of its pairs)."""
    z = _relabel(groups)
    n = np.bincount(z).astype(float)
    pairs = np.outer(n, n)
    np.fill_diagonal(pairs, n * (n - 1))
    return edge_ends(g, groups) / np.maximum(pairs, 1)


# ── the verdict ──────────────────────────────────────────────────────────
# The toolkit reads data-tutor-verdict from the hidden check cell's output when
# the student presses Submit to Tutor. A pass that forgets it is read as a
# fail. It needs text inside it: an empty span does not survive rendering.
def _verdict(ok, why=None):
    word = "pass" if ok else "fail"
    extra = f' data-why="{html.escape(str(why), quote=True)}"' if why else ""
    return mo.Html(f'<span data-tutor-verdict="{word}"{extra} style="display:none">{word}</span>')


def _same(got, want, tol=1e-6):
    try:
        return abs(float(got) - float(want)) <= tol
    except (TypeError, ValueError):
        return False


def _guard(check):
    """A check's own failure is a fail with Python's words, never a crash."""

    def run(*args, **kwargs):
        try:
            return check(*args, **kwargs)
        except Exception as exc:  # noqa: BLE001 -- Python's own words, to the tutor
            return _verdict(False, why=f"{type(exc).__name__}: {exc}")

    run.__name__ = check.__name__
    run.__doc__ = check.__doc__
    return run


# ── cp1 ──────────────────────────────────────────────────────────────────
@_guard
def check_graph(g, n_nodes, n_edges, k_max, hub):
    """cp1 -- the airport network from its route list, its size, its busiest airport."""
    if not isinstance(g, ig.Graph) or g.is_directed():
        return _verdict(False, why="g is not an undirected igraph Graph")
    if g.vcount() != N_AIRPORTS or g.ecount() != len(_routes):
        return _verdict(False)
    if sorted(map(tuple, map(sorted, g.get_edgelist()))) != sorted(map(tuple, map(sorted, _routes))):
        return _verdict(False)
    top = int(_deg.max())
    busiest = {_codes[i] for i in np.flatnonzero(_deg == top)}
    ok = (
        _same(n_nodes, N_AIRPORTS)
        and _same(n_edges, len(_routes))
        and _same(k_max, top)
        and str(hub) in busiest
    )
    return _verdict(ok)


# ── cp2 ──────────────────────────────────────────────────────────────────
@_guard
def check_leiden(g, groups, n_groups, q):
    """cp2 -- Leiden with the modularity objective: the partition, its size, its Q.

    The default objective is CPM, which gives tiny groups and a Q near zero;
    a Q of 0.6 or more is what the modularity objective gives on this network."""
    groups = list(groups)
    if len(groups) != g.vcount():
        return _verdict(False, why=f"groups has {len(groups)} entries, the network has {g.vcount()} nodes")
    if not all(float(x).is_integer() for x in groups):
        return _verdict(False)
    ok = (
        _same(n_groups, len(set(groups)))
        and _same(q, g.modularity(groups), tol=1e-6)
        and g.modularity(groups) >= 0.6
    )
    return _verdict(ok)


# ── cp3 ──────────────────────────────────────────────────────────────────
@_guard
def check_nmi(nmi):
    """cp3 -- the student's nmi(a, b) against the lecture's definition."""
    rng = np.random.default_rng(3)
    leiden = _ref_leiden()
    cases = [
        ([0, 0, 1, 1, 2, 2], [0, 0, 1, 1, 2, 2]),                # identical -> 1
        ([0, 0, 1, 1, 2, 2], [5, 5, 9, 9, 7, 7]),                # same partition, other labels
        ([0, 0, 0, 0, 1, 1, 1, 1], [0, 1, 0, 1, 0, 1, 0, 1]),    # independent -> 0
        ([0, 0, 0, 1, 1, 2, 2, 2, 2], [0, 0, 1, 1, 1, 1, 2, 2, 0]),
        (_continent, _country),                                  # strings
        (leiden, _continent),
        (leiden, rng.integers(0, 25, N_AIRPORTS)),
    ]
    for a, b in cases:
        got, want = nmi(list(a), list(b)), _ref_nmi(a, b)
        if not _same(got, want, tol=1e-6):
            return _verdict(False)
    return _verdict(True)


# ── cp4 ──────────────────────────────────────────────────────────────────
@_guard
def check_ari(ari):
    """cp4 -- the student's ari(a, b) against the lecture's definition."""
    rng = np.random.default_rng(4)
    leiden = _ref_leiden()
    cases = [
        ([0, 0, 1, 1, 2, 2], [0, 0, 1, 1, 2, 2]),
        ([0, 0, 1, 1, 2, 2], [5, 5, 9, 9, 7, 7]),
        ([0, 0, 0, 0, 1, 1, 1, 1], [0, 1, 0, 1, 0, 1, 0, 1]),
        ([0, 0, 0, 1, 1, 2, 2, 2, 2], [0, 0, 1, 1, 1, 1, 2, 2, 0]),
        (_continent, _country),
        (leiden, _continent),
        (leiden, rng.integers(0, 25, N_AIRPORTS)),               # random -> about 0
    ]
    for a, b in cases:
        got, want = ari(list(a), list(b)), _ref_ari(a, b)
        if not _same(got, want, tol=1e-6):
            return _verdict(False)
    return _verdict(True)


# ── cp5 ──────────────────────────────────────────────────────────────────
@_guard
def check_compare(groups, info_groups, nmi_cont, ari_cont, nmi_ctry, ari_ctry, nmi_info, ari_info):
    """cp5 -- six scores, from the student's own groups and their own Infomap run."""
    groups, info_groups = list(groups), list(info_groups)
    if len(info_groups) != N_AIRPORTS:
        return _verdict(False)
    # igraph's Infomap finds about 130 groups here; Leiden finds about 18.
    if not 60 <= len(set(info_groups)) <= 250:
        return _verdict(False, why=f"info_groups has {len(set(info_groups))} groups")
    pairs = [
        (nmi_cont, _ref_nmi(groups, _continent)),
        (ari_cont, _ref_ari(groups, _continent)),
        (nmi_ctry, _ref_nmi(groups, _country)),
        (ari_ctry, _ref_ari(groups, _country)),
        (nmi_info, _ref_nmi(info_groups, _country)),
        (ari_info, _ref_ari(info_groups, _country)),
    ]
    return _verdict(all(_same(got, want, tol=1e-4) for got, want in pairs))


# ── cp6 ──────────────────────────────────────────────────────────────────
def _pairs_in(n_r, n_s, same):
    return n_r * (n_r - 1) / 2 if same else n_r * n_s


def _block_counts(g, z):
    k = int(z.max()) + 1
    e = np.zeros((k, k))
    for u, v in g.get_edgelist():
        r, s = sorted((int(z[u]), int(z[v])))
        e[r, s] += 1
    return e


@_guard
def check_sbm(sample_sbm, g, groups, sbm_net):
    """cp6 -- sample_sbm(P, z) on a small made-up case, then on the airports."""
    # A small case with a zero block, so a swapped (r, s) or a stray edge shows.
    z = np.repeat([0, 1, 2], [120, 100, 80])
    P = np.array([[0.30, 0.05, 0.00], [0.05, 0.20, 0.10], [0.00, 0.10, 0.40]])
    small = sample_sbm(P, z)
    if not isinstance(small, ig.Graph) or small.vcount() != len(z) or small.is_directed():
        return _verdict(False, why="sample_sbm did not return an undirected Graph with one node per entry of z")
    if not small.is_simple():
        return _verdict(False, why="the sample has a self-loop or a repeated edge")
    got = _block_counts(small, z)
    n = np.bincount(z)
    for r in range(3):
        for s in range(r, 3):
            pairs = _pairs_in(n[r], n[s], r == s)
            mean = P[r, s] * pairs
            sd = (pairs * P[r, s] * (1 - P[r, s])) ** 0.5
            if abs(got[r, s] - mean) > 5 * sd + 2:
                return _verdict(False)
    # And on the airports: the student's own sbm_net, built from their groups.
    if not isinstance(sbm_net, ig.Graph) or sbm_net.vcount() != g.vcount():
        return _verdict(False)
    want_m = float(np.sum(_block_counts(g, _relabel(groups))))
    return _verdict(abs(sbm_net.ecount() - want_m) <= 0.05 * want_m and sbm_net.is_simple())


# ── cp7 ──────────────────────────────────────────────────────────────────
@_guard
def check_hubs(g, sbm_net, max_real, max_sbm, corr_sbm):
    """cp7 -- the largest degree of each network, and how well the SBM's degrees follow the real ones."""
    real, other = np.array(g.degree()), np.array(sbm_net.degree())
    ok = (
        _same(max_real, real.max())
        and _same(max_sbm, other.max())
        and _same(corr_sbm, np.corrcoef(real, other)[0, 1], tol=1e-6)
    )
    return _verdict(ok)


# ── cp8 ──────────────────────────────────────────────────────────────────
@_guard
def check_dcsbm(sample_dcsbm, g, groups, kappa, theta, dc_net, max_dc, corr_dc):
    """cp8 -- kappa and theta by the quiz's formulas; sample_dcsbm on a small case, then on the airports."""
    deg = np.array(g.degree(), dtype=float)
    z = _relabel(groups)
    want_kappa = np.bincount(z, weights=deg)
    if not np.allclose(np.asarray(kappa, dtype=float), want_kappa):
        return _verdict(False, why="kappa is not the total degree of each group")
    if not np.allclose(np.asarray(theta, dtype=float), deg / want_kappa[z]):
        return _verdict(False, why="theta is not k_i divided by the total degree of i's group")

    # A small case: two groups, spread-out theta, so hubs and leaves both exist.
    rng = np.random.default_rng(8)
    zs = np.repeat([0, 1], [200, 200])
    th = rng.lognormal(0, 1.0, 400)
    for r in (0, 1):
        th[zs == r] /= th[zs == r].sum()
    w = np.array([[6000.0, 800.0], [800.0, 7000.0]])
    small = sample_dcsbm(th, w, zs)
    if not isinstance(small, ig.Graph) or small.vcount() != 400 or small.is_directed():
        return _verdict(False, why="sample_dcsbm did not return an undirected Graph with one node per entry of z")
    if any(small.is_loop()):
        return _verdict(False, why="the sample has self-loops: keep each pair once, with i < j")
    rate = np.outer(th, th) * w[zs][:, zs]
    iu = np.triu_indices(400, 1)
    mean_edges = rate[iu].sum()
    if abs(small.ecount() - mean_edges) > 5 * mean_edges**0.5 + 2:
        return _verdict(False)
    expected_deg = rate.sum(1) - np.diag(rate)
    if np.corrcoef(small.degree(), expected_deg)[0, 1] < 0.9:
        return _verdict(False, why="degrees do not follow theta")

    # And on the airports.
    if not isinstance(dc_net, ig.Graph) or dc_net.vcount() != g.vcount():
        return _verdict(False)
    other = np.array(dc_net.degree())
    ok = (
        abs(dc_net.ecount() - g.ecount()) <= 0.05 * g.ecount()
        and _same(max_dc, other.max())
        and _same(corr_dc, np.corrcoef(deg, other)[0, 1], tol=1e-6)
        and corr_dc >= 0.9
    )
    return _verdict(ok)


# ── pictures ─────────────────────────────────────────────────────────────
# The last line of a scaffold. They draw what the student's code produced and
# judge nothing. A picture shows a shape, never a printed number. Palette: the
# lecture slides' blue / rust / amber, then dust; dots and routes stay pale so
# that the ring and the group colours are what the eye finds.
_BLUE, _RUST, _AMBER, _DUST, _PAPER = "#3959A6", "#B14434", "#DAB167", "#CFC8B8", "#FFFDF7"
_DOT, _ROUTE = "#7F8AAE", "#C6CAD6"
_PIECES = ["#B14434", "#3959A6", "#DAB167", "#2E6E5B", "#7B5EA7", "#C9762F",
           "#4B86C4", "#8C6E4A", "#B8567F", "#5E8C3A", "#A8478E", "#3E7E8C"]
_PANEL_TITLES = {"real": "Real network", "sbm": "Block model", "dcsbm": "Degree-corrected block model"}


def _pairs(net):
    """The routes of `net` as sorted (i, j) pairs, each once. A repeated pair
    (the degree-corrected model draws some) is one line; a self-loop is none."""
    edges = _routes if net is None else net.get_edgelist()
    return sorted({(min(i, j), max(i, j)) for i, j in edges if i != j})


def _segments(pairs):
    """One straight line per route, in longitude and latitude. A route over the
    180th meridian is cut in two, so it does not cross the whole map."""
    out = []
    for i, j in pairs:
        (x1, y1), (x2, y2) = sorted([(_lon[i], _lat[i]), (_lon[j], _lat[j])])
        if x2 - x1 > 180:
            out += [((x1, y1), (x2 - 360, y2)), ((x1 + 360, y1), (x2, y2))]
        else:
            out.append(((x1, y1), (x2, y2)))
    return out


def _draw_world(ax, net=None, groups=None, mark=None, by_degree=False):
    from matplotlib.collections import LineCollection

    pairs = _pairs(net)
    z = None if groups is None else np.asarray(groups)
    colour_of = {}
    if z is not None:
        order = [r for r, _ in sorted(((r, (z == r).sum()) for r in set(z)), key=lambda p: -p[1])]
        colour_of = dict(zip(order, _PIECES))
    plain = [p for p in pairs if z is None or z[p[0]] != z[p[1]] or z[p[0]] not in colour_of]
    ax.add_collection(LineCollection(_segments(plain), colors=_ROUTE, linewidths=0.25, alpha=0.4, zorder=1))
    for r, colour in colour_of.items():
        inside = [p for p in pairs if z[p[0]] == r and z[p[1]] == r]
        ax.add_collection(LineCollection(_segments(inside), colors=colour, linewidths=0.3, alpha=0.5, zorder=1))
    # A dot grows with the airport's routes in this network (the panels of
    # plot_worlds), so a hub is a big dot and a network without hubs has none.
    if by_degree:
        deg = np.zeros(len(_codes))
        for i, j in pairs:
            deg[i] += 1
            deg[j] += 1
        size = 2.0 + 0.4 * deg
    else:
        size = np.full(len(_codes), 3.0)
    if z is None:
        ax.scatter(_lon, _lat, s=size, color=_DOT, linewidths=0, zorder=2)
    else:
        ax.scatter(_lon, _lat, s=size, color=_DUST, linewidths=0, zorder=2)
        for r, colour in colour_of.items():
            pick = z == r
            ax.scatter(_lon[pick], _lat[pick], s=size[pick] + 1, color=colour, linewidths=0, zorder=2)
    if isinstance(mark, _Blank):
        mark._refuse()
    if mark is not None:
        for code in ([mark] if isinstance(mark, str) else list(mark) if isinstance(mark, (list, tuple, set)) else []):
            if code in _codes:
                i = _codes.index(code)
                ax.scatter([_lon[i]], [_lat[i]], s=110, facecolors="none", edgecolors=_RUST, linewidths=2.2, zorder=3)
    ax.set_xlim(-180, 180)
    ax.set_ylim(-60, 80)
    ax.set_xticks([])
    ax.set_yticks([])
    for side in ("left", "bottom", "top", "right"):
        ax.spines[side].set_visible(False)


def plot_world(groups=None, mark=None, title=None, net=None):
    """The airports as dots at their longitude and latitude, and the routes of
    `net` (the real network when it is left out) as thin lines. With `groups`,
    the twelve biggest groups get a colour, and a route inside one group takes
    that colour. `mark` is an airport code (or several) ringed in rust."""
    with plt.rc_context({"path.sketch": None}):
        fig, ax = plt.subplots(figsize=(9, 4.3))
        _draw_world(ax, net, groups, mark)
        ax.set_title(title or ("Each colour is a group; grey is the rest." if groups is not None
                               else "The ringed airport." if mark is not None
                               else "Every airport and every route."), loc="left")
        plt.close(fig)
    return fig


def plot_worlds(groups=None, **networks):
    """Several networks on the same map, one panel each, a dot as big as the
    airport's routes: plot_worlds(groups, real=g, sbm=sbm_net)."""
    n = len(networks)
    cols = n if n <= 2 else 2
    rows = -(-n // cols)
    with plt.rc_context({"path.sketch": None}):
        fig, axes = plt.subplots(rows, cols, figsize=(5.6 * cols, 2.9 * rows), squeeze=False)
        for ax in axes.ravel():
            ax.axis("off")
        for ax, (name, net) in zip(axes.ravel(), networks.items()):
            ax.axis("on")
            _draw_world(ax, net, groups, by_degree=True)
            ax.set_title(_PANEL_TITLES.get(name, name), loc="left", fontsize=10)
        fig.tight_layout()
        plt.close(fig)
    return fig


def plot_scores(rows):
    """rows: [(label, nmi, ari), ...]. One dot per comparison, in two panels:
    only the dots of one score are set side by side."""
    frame = pd.DataFrame(
        [(label, name, float(v)) for label, n, a in rows for name, v in (("NMI", n), ("ARI", a))],
        columns=["comparison", "score", "value"],
    )
    order = [r[0] for r in rows]
    y = alt.Y("comparison:N", sort=order, title=None, axis=alt.Axis(labelLimit=240))
    colour = alt.Color("score:N", scale=alt.Scale(domain=["NMI", "ARI"], range=[_BLUE, _RUST]), legend=None)
    stem = alt.Chart().transform_calculate(zero="0").mark_rule(color=_DUST, strokeWidth=2).encode(
        x=alt.X("zero:Q", title="score (1 is identical)", scale=alt.Scale(domain=[0, 1])), x2="value:Q", y=y)
    dot = alt.Chart().mark_point(filled=True, size=150, opacity=1).encode(
        x=alt.X("value:Q", scale=alt.Scale(domain=[0, 1])), y=y, color=colour)
    return alt.layer(stem, dot, data=frame).properties(height=110, width=210).facet(
        column=alt.Column("score:N", sort=["NMI", "ARI"], title=None, header=alt.Header(labelFontSize=13)),
    ).properties(title="How closely the groups match the labels")


def _ccdf(graph):
    k = np.array(graph.degree())
    ks = np.unique(k[k > 0])
    return pd.DataFrame({"degree": ks, "share": [(k >= x).mean() for x in ks]})


def plot_degrees(**networks):
    """The CCDF of the degrees, both axes logarithmic, one line per network:
    plot_degrees(real=g, sbm=sbm_net)."""
    colours = {"real": _BLUE, "sbm": _AMBER, "dcsbm": _RUST}
    frames = []
    for name, graph in networks.items():
        f = _ccdf(graph)
        f["network"] = name
        frames.append(f)
    colour_keys = list(networks)
    names = list(networks)
    labels = {"real": "real network", "sbm": "block model", "dcsbm": "degree-corrected"}
    for f, n in zip(frames, names):
        f["network"] = labels.get(n, n)
    names = [labels.get(n, n) for n in names]
    chart = alt.Chart(pd.concat(frames)).mark_line(point=True, strokeWidth=2).encode(
        x=alt.X("degree:Q", scale=alt.Scale(type="log"), title="routes at an airport (k)", axis=alt.Axis(grid=False)),
        y=alt.Y("share:Q", scale=alt.Scale(type="log"), title="CCDF", axis=alt.Axis(grid=False)),
        color=alt.Color("network:N", scale=alt.Scale(domain=names, range=[colours.get(n, _DUST) for n in colour_keys]), title=None),
    ).properties(height=250, width="container", title="CCDF: the share of airports with at least k routes")
    return chart


# ── parts for a tutor's answer to a follow-up question ───────────────────
# A question a student asks falls in one of three kinds, and each is answered
# from these parts so that its shape is the same every time: a formula with
# every piece explained under it, a grid, a small network. A figure here shows
# a shape and never a printed number.
def formula(parts):
    """parts: [(latex, meaning), ...]; a meaning of None leaves the piece bare
    (an equals sign, say). Each other piece gets an underbrace and its meaning."""
    body = " ".join(
        tex if meaning is None else rf"\underbrace{{{tex}}}_{{\text{{{meaning}}}}}"
        for tex, meaning in parts
    )
    return mo.md("$$\n" + body + "\n$$")


def _grid(ax, M, title=None):
    ax.imshow(np.asarray(M, dtype=float), cmap=plt.cm.Blues, vmin=0, aspect="equal")
    ax.set_xticks([])
    ax.set_yticks([])
    for side in ax.spines.values():
        side.set_color(_DUST)
    if title:
        ax.set_title(title, loc="left", fontsize=10)


def show_matrix(M, title=None):
    """A matrix as a grid of squares, darker for larger. No numbers in it."""
    with plt.rc_context({"path.sketch": None}):
        fig, ax = plt.subplots(figsize=(2.6, 2.6))
        _grid(ax, M, title)
        plt.close(fig)
    return fig


def show_matrices(before, after, titles=("before", "after")):
    """Two matrices side by side, on one colour scale."""
    with plt.rc_context({"path.sketch": None}):
        fig, axes = plt.subplots(1, 2, figsize=(5.2, 2.6))
        top = max(np.max(before), np.max(after))
        for ax, M, t in zip(axes, (before, after), titles):
            ax.imshow(np.asarray(M, dtype=float), cmap=plt.cm.Blues, vmin=0, vmax=top, aspect="equal")
            ax.set_xticks([])
            ax.set_yticks([])
            ax.set_title(t, loc="left", fontsize=10)
        fig.tight_layout()
        plt.close(fig)
    return fig


def _draw_network(ax, net, groups=None, title=None):
    n = net.vcount()
    xy = np.array(net.layout_circle().coords) if n else np.zeros((0, 2))
    z = np.zeros(n, dtype=int) if groups is None else np.asarray(groups)
    levels = {r: i for i, r in enumerate(sorted(set(z)))}
    for i, j in _pairs(net):
        ax.plot(xy[[i, j], 0], xy[[i, j], 1], color=_ROUTE, linewidth=1.2, zorder=1)
    ax.scatter(xy[:, 0], xy[:, 1], s=110, zorder=2, linewidths=0,
               c=[(_PIECES if groups is not None else [_BLUE])[levels[r] % len(_PIECES)] for r in z])
    ax.set_aspect("equal")
    ax.axis("off")
    if title:
        ax.set_title(title, loc="left", fontsize=10)


def show_network(net, groups=None, title=None):
    """A small network on a circle, a dot per node coloured by group. No node numbers."""
    with plt.rc_context({"path.sketch": None}):
        fig, ax = plt.subplots(figsize=(2.6, 2.6))
        _draw_network(ax, net, groups, title)
        plt.close(fig)
    return fig


def show_networks(before, after, groups=None, titles=("before", "after")):
    """Two small networks side by side."""
    with plt.rc_context({"path.sketch": None}):
        fig, axes = plt.subplots(1, 2, figsize=(5.2, 2.6))
        for ax, net, t in zip(axes, (before, after), titles):
            _draw_network(ax, net, groups, t)
        plt.close(fig)
    return fig
