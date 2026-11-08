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

__generated_with = "0.25.0"
app = marimo.App(width="medium", css_file="lecture-hall.css")


@app.cell(hide_code=True)
def _(mo):
    # One single string literal on purpose: marimo round-trips mo.md cells
    # through its markdown serializer, and implicit string concatenation
    # corrupts them (the code itself gets wrapped as markdown content).
    mo.md(r"""
    <p style="text-align:right; color:#6A6D75; font-size:12px; margin:0;">🐛 Something broken or odd? Email Prof. Sadamori Kojaku &middot; <a href="mailto:skojaku@binghamton.edu" style="color:#3959A6;">skojaku@binghamton.edu</a></p>
    """)
    return


@app.cell(hide_code=True)
def ch1_header(mo):
    mo.md(r"""
    ## Finding Groups in Code

    This module finds groups in the world airport network, scores them, and builds networks from groups.
    """)
    return


@app.cell
def cp1_graph_scratch(ig):
    # 🧪 Your space to try things out. Write any code here and run it.
    # Nothing in this cell is marked, and your tutor does not look at it.
    # Start your names with _ (like _small below): such a name belongs to
    # this cell only, so it never clashes with the exercise.
    _small = ig.Graph(n=3, edges=[(0, 1), (1, 2)])
    print(_small.degree())
    return


@app.cell(hide_code=True)
def cp1_graph_brief(mo):
    mo.md(r"""
    ### Exercise: the airport network

    /// details | 📋 Task
        type: lh-task

    **Carried over:**
    - `ig` is igraph, `np` is numpy, and `plot_world(mark=hub)` draws the airports and routes on a map and rings the airport with the code `hub`.
    - `route_list` holds one pair of airport numbers for each route, and `codes`, `continent` and `country` hold the code, the continent and the country of each airport number.

    **Task:**
    - Build the network from the routes in `route_list`.
    - Count the nodes and the edges of the network with the methods of `g`.
    - Find the largest degree in `g`, and the code of the airport with the largest degree.

    **Other tools:**
    - `[3, 9, 4].index(9)` gives `1`, the position of 9 in the list, and `np.argmax([3, 9, 4])` also gives `1`.
    - `["a", "b", "c"][1]` gives `"b"`, the entry at position 1.
    ///
    """)
    return


@app.cell(hide_code=True)
def cp1_graph_work(codes, continent, country, ig, plot_world, route_list):
    # Already defined in the notebook:
    #   `ig` is the igraph library (the notebook ran `import igraph as ig`; in your own file, write that line first).
    #   `route_list` is a list with one pair (i, j) for each route; i and j are airport numbers (route_list[0] is the first route).
    #   `codes` is a list with the code of each airport: codes[0] is the code of airport number 0.
    #   `continent` and `country` are lists in the same order: continent[0] and country[0] belong to airport number 0
    #   (a continent is a two-letter code like AF or EU).
    print(route_list[0], codes[0], continent[0], country[0])

    # 1. `g`: the airport network, with one node for each airport and one edge for each route.

    g = ig.Graph(n=len(codes), edges=route_list)

    # 2. `n_nodes` and `n_edges`: the number of nodes and the number of edges of g (two integers).
    #    Use the methods of g; do not type the numbers.
    n_nodes = g.vcount()
    n_edges = g.ecount()
    # 3. `g.degree()` is a list with the number of routes of each airport, in the order of the airport numbers:
    #    g.degree()[0] is the number of routes of airport number 0.
    #    `k_max`: the largest number in g.degree() (one integer).
    #    `hub`: the code of the airport that has k_max routes (a string).

    k_max = max(g.degree())
    hub = codes[g.degree().index(k_max)]

    print(n_nodes, n_edges, k_max, hub)
    plot_world(mark=hub)
    return (g,)


@app.cell(hide_code=True)
def cp1_graph_note(mo):
    mo.md(r"""
    ### The airport network

    ```python
    g = ig.Graph(n=len(codes), edges=route_list)
    g.vcount(), g.ecount()                  # 3360, 18783
    k_max = max(g.degree())
    hub = codes[g.degree().index(k_max)]
    ```

    Airports are from OurAirports and routes from OpenFlights (2014); the average airport has about 11 routes.
    """)
    return


@app.cell(hide_code=True)
def cp1_hub_robustness(ig, mo, plt):

    # A tiny hub network: node 0 links to every other node, and the others form a ring.
    _n = 8
    _edges = [(0, i) for i in range(1, _n)] + [(i, i + 1) for i in range(1, _n - 1)]
    _net = ig.Graph(n=_n, edges=_edges)

    def _largest_component_after(removed):
        _sub = _net.copy()
        _sub.delete_vertices(removed)
        return max(_sub.connected_components().sizes())

    _random_removed = [3]          # remove one random, non-hub node
    _hub_removed = [0]             # remove the single hub

    _md = mo.md(r"""### Hubs, robustness and fragility

    A hub is a node with far more edges than most nodes (AMS with 246 routes, when the average airport has about 11). This small network has one hub: node **0** touches every other node.

    - Removing a random, non-hub node (node **3**) leaves every other airport still connected in one piece.
    - Removing the hub (node **0**) leaves every other airport isolated.

    So an uneven network shrugs off random loss but breaks when its hubs are hit on purpose.""")

    _fig, _ax = plt.subplots(1, 3, figsize=(11, 3.2))
    for _a, _g in zip(_ax, [_net, _net.copy().copy() and _net.copy(), _net.copy()]):
        pass

    # draw the three states plainly
    _states = [None, _random_removed, _hub_removed]
    _titles = ["whole network", "random node gone", "hub gone"]
    for _a, _rem, _t in zip(_ax, _states, _titles):
        _g = _net.copy()
        _removed_set = set(_rem or [])
        _keep = [v for v in range(_n) if v not in _removed_set]
        _g.delete_vertices(list(_removed_set))
        _colors = ["#B14434" if v == 0 else "#3959A6" for v in _keep]
        _pos = _g.layout("circle")
        ig.plot(_g, target=_a, vertex_color=_colors, vertex_size=28,
                edge_color="#6A6D75", bbox=(0, 0, 300, 300), margin=30)
        _a.set_title(_t)
        _a.axis("off")
    plt.tight_layout()

    mo.vstack([
        mo.md(r"""> 🧭 **You asked:** “Would this kind of hub structure make the airport network more robust to random airport failures but more vulnerable if the highest-degree hubs were deliberately removed?”"""),_md, _fig])
    return


@app.cell
def cp2_leiden_scratch(ig):
    # 🧪 Your space to try things out. Write any code here and run it.
    # Nothing in this cell is marked, and your tutor does not look at it.
    # Start your names with _ (like _small below): such a name belongs to
    # this cell only, so it never clashes with the exercise.
    _small = ig.Graph(n=3, edges=[(0, 1), (1, 2)])
    print(_small.degree())
    return


@app.cell(hide_code=True)
def cp2_leiden_brief(mo):
    mo.md(r"""
    ### Exercise: groups with Leiden

    /// details | 📋 Task
        type: lh-task

    **Carried over:**
    - `g` is the airport network from cp1, and `plot_world(groups)` draws the airports and routes on a map, with a colour for each of the twelve biggest groups.

    **Task:**
    - Find groups of airports with Leiden, with modularity as the objective.
    - Save the group of each airport, the number of groups and the modularity.

    **Other tools:**
    - `community_leiden` is a method of `g`, written `g.community_leiden(...)`. On the [igraph page](https://python.igraph.org/en/stable/api/igraph.Graph.html#community_leiden) the first argument `graph` is `g`, and the option that sets the objective is `objective_function`.
    - A method that finds groups returns a clustering. The clustering's `.membership` is a list with one group number for each node, like `[0, 0, 1, 1]`.
    - `ig.Graph.Ring(4).modularity([0, 0, 1, 1])` gives the modularity of a list of group numbers on a small network.
    ///
    """)
    return


@app.cell(hide_code=True)
def cp2_leiden_work(g, plot_world):
    # `g` is the airport network from the last exercise.

    # 1. `leiden`: the result of the method `g.community_leiden`, with modularity as the objective.
    leiden = g.community_leiden(objective_function="modularity")

    # 2. `groups`: a list with the group number of each airport, in the order of the airport numbers.
    #    For example [0, 0, 1] means that airports 0 and 1 are in group 0 and airport 2 is in group 1.
    groups = leiden.membership

    # 3. `n_groups`: the number of different groups (one integer).
    n_groups = len(leiden)

    # 4. `q`: the modularity of `groups` on g (one number).
    q = g.modularity(groups)

    print(n_groups, "groups, modularity", round(q, 3))
    plot_world(groups)
    return (groups,)


@app.cell(hide_code=True)
def cp2_leiden_note(mo):
    mo.md(r"""
    ### Leiden, maximising modularity

    ```python
    leiden = g.community_leiden(objective_function="modularity")
    groups = leiden.membership
    n_groups, q = len(set(groups)), g.modularity(groups)
    ```

    Leiden finds about 17 to 20 groups, with a modularity near 0.67, and another run can differ a little.
    """)
    return


@app.cell(hide_code=True)
def cp2_leiden_stability(alt, g, mo, pd):
    # Run Leiden several times and watch what is stable and what moves.
    _runs = []
    for _i in range(5):
        _cl = g.community_leiden(objective_function="modularity")
        _runs.append(_cl.membership)

    _n_groups = [len(set(r)) for r in _runs]
    _q = [round(g.modularity(r), 3) for r in _runs]

    _md = mo.md(r"""### What is stable, and what moves

    Leiden is random, so I ran it **five** times on the airport network. Each dot below is one run: its number of groups on the left, its modularity on the right.

    - The **number of groups** and the **modularity** move a little from run to run.
    - The **large regional groups** are the stable part — airports deep inside a region stay together run after run, while a few boundary airports can land on either side, which is what changes the count.

    So trust the big, repeated structure and the modularity, and do not read much into the exact group count.""")

    _src = pd.DataFrame({"run": range(1, 6), "groups": _n_groups, "modularity": _q})

    _left = alt.Chart(_src).mark_point(size=90, filled=True, color="#3959A6").encode(
        x=alt.X("run:O", title="run"),
        y=alt.Y("groups:Q", title="number of groups", scale=alt.Scale(zero=False)),
    ).properties(height=160)

    _right = alt.Chart(_src).mark_point(size=90, filled=True, color="#B14434").encode(
        x=alt.X("run:O", title="run"),
        y=alt.Y("modularity:Q", title="modularity", scale=alt.Scale(zero=False)),
    ).properties(height=160)

    mo.vstack([
        mo.md(r"""> 🧭 **You asked:** “Does that mean the airport network's community structure is driven mainly by regional connections, while the long-distance international routes act mostly as links between those communities? Also, since Leiden is stochastic and the number of groups can change slightly between runs, should I think of the exact 17 groups as less important than the overall modularity and the stability of the larger regional communities?”"""),_md, _left | _right])
    return


@app.cell
def cp3_nmi_scratch(ig):
    # 🧪 Your space to try things out. Write any code here and run it.
    # Nothing in this cell is marked, and your tutor does not look at it.
    # Start your names with _ (like _small below): such a name belongs to
    # this cell only, so it never clashes with the exercise.
    _small = ig.Graph(n=3, edges=[(0, 1), (1, 2)])
    print(_small.degree())
    return


@app.cell(hide_code=True)
def cp3_nmi_brief(mo):
    mo.md(r"""
    ### Exercise: write NMI

    /// details | 📋 Task
        type: lh-task

    **Carried over:**
    - `np` is numpy.

    **Task:**
    - Write `nmi(a, b)` from the lecture's definition,
      $\mathrm{NMI} = \dfrac{2\,I(a;b)}{H(a) + H(b)}$, with
      $H = -\sum p \ln p$ and $I = \sum p_{ab} \ln \dfrac{p_{ab}}{p_a\,p_b}$.
    - $p_{ab}$ is the share of airports with each pair of labels, and $p_a$ and $p_b$ are the row totals and the column totals of $p_{ab}$.
    - The last line must print 1.0 and 0.0.

    **Other tools:**
    - `np.unique(x, return_inverse=True)[1]` numbers the labels of `x` from 0: for `["b", "a", "b"]` the result is `[1, 0, 1]`.
    - `np.add.at(t, (i, j), 1)` adds 1 to `t[i, j]` for each pair taken from the lists `i` and `j`.
    - `np.outer([1, 2], [3, 4])` is the table of every product: `[[3, 4], [6, 8]]`.
    ///
    """)
    return


@app.cell(hide_code=True)
def cp3_nmi_work(np):
    # `a` and `b` are two lists with one label for each airport, like a = ["EU", "EU", "AS"] and b = [0, 0, 1].
    # A label is a string or a number. nmi(a, b) is 1 when the two lists give the same grouping.

    def nmi(a, b):
        # 1. `ia` and `ib`: the labels of a and of b, renamed 0, 1, 2, ...
        #    (two numpy arrays with one entry for each airport; ["EU", "EU", "AS"] becomes [1, 1, 0]).
        _, ia = np.unique(a, return_inverse=True)
        _, ib = np.unique(b, return_inverse=True)

        # 2. `table[i, j]`: the number of airports with label i in ia and label j in ib.
        #    Add 1 to a cell for each airport. `p_ab[i, j]` is the share of all airports in cell (i, j).

        table = np.zeros((ia.max() + 1, ib.max() + 1))
        np.add.at(table, (ia, ib), 1)
        p_ab = table / table.sum()

        # 3. `p_a`: a list with the share of airports with each label of a (the row totals of p_ab).
        #    `p_b`: the same for b (the column totals of p_ab).
        p_a = p_ab.sum(axis=1)
        p_b = p_ab.sum(axis=0)
        # 4. `h_a` and `h_b`: the entropy of a and the entropy of b.
        #    The entropy of a is -1 times the sum of p_a * log(p_a); for b, use p_b.

        h_a = -np.sum(p_a[p_a > 0] * np.log(p_a[p_a > 0]))
        h_b = -np.sum(p_b[p_b > 0] * np.log(p_b[p_b > 0]))

        # 5. `mi`: the mutual information, the sum of p_ab[i, j] * log(p_ab[i, j] / (p_a[i] * p_b[j]))
        #    over the cells where p_ab is not 0. `seen` is True in the cells where p_ab is not 0.
        seen = p_ab > 0
        mi = np.sum(
            p_ab[seen]
            * np.log(
                p_ab[seen]
                / (p_a[:, None] * p_b[None, :])[seen]
            )
        )

        return 2 * mi / (h_a + h_b)

    print(nmi([0, 0, 1, 1], [0, 0, 1, 1]), nmi([0, 0, 1, 1], [0, 1, 0, 1]))
    return (nmi,)


@app.cell(hide_code=True)
def cp3_nmi_note(mo):
    mo.md(r"""
    ### NMI from a table of counts

    ```python
    ia, ib = np.unique(a, return_inverse=True)[1], np.unique(b, return_inverse=True)[1]
    table = np.zeros((ia.max() + 1, ib.max() + 1)); np.add.at(table, (ia, ib), 1)
    p_ab = table / table.sum(); p_a, p_b = p_ab.sum(axis=1), p_ab.sum(axis=0)
    h_a, h_b = -(p_a * np.log(p_a)).sum(), -(p_b * np.log(p_b)).sum()
    seen = p_ab > 0
    mi = (p_ab[seen] * np.log(p_ab[seen] / np.outer(p_a, p_b)[seen])).sum()
    nmi = 2 * mi / (h_a + h_b)
    ```

    Only the table of counts matters, so renaming the groups changes nothing. Tip: `np.add.at` fills the table without a loop over the airports.
    """)
    return


@app.cell(hide_code=True)
def cp3_nmi_relabel(mo, np, plt):
    # NMI ignores the labels: here are the same partition under two relabelings.
    _a = [0, 0, 1, 1, 2, 2]        # three groups, labelled 0, 1, 2
    _b = [5, 5, 9, 9, 3, 3]        # the SAME three groups, relabelled 5, 9, 3
    _c = [0, 1, 0, 1, 0, 1]        # a different split (every other node)

    def _cont(_x, _y):
        _ix, _iy = np.unique(_x, return_inverse=True)[1], np.unique(_y, return_inverse=True)[1]
        _t = np.zeros((_ix.max() + 1, _iy.max() + 1), dtype=int)
        np.add.at(_t, (_ix, _iy), 1)
        return _t

    fig, ax = plt.subplots(1, 2, figsize=(7, 3))
    _t1 = _cont(_a, _b)
    _t2 = _cont(_a, _c)
    im1 = ax[0].imshow(_t1, cmap="Blues")
    im2 = ax[1].imshow(_t2, cmap="Blues")
    for (_axx, _t, _ttl) in [(ax[0], _t1, "a vs b (same split)"), (ax[1], _t2, "a vs c (different split)")]:
        for i in range(_t.shape[0]):
            for j in range(_t.shape[1]):
                _axx.text(j, i, _t[i, j], ha="center", va="center", color="#35373C")
        _axx.set_title(_ttl, fontsize=10)
        _axx.set_xticks([]); _axx.set_yticks([])
    plt.tight_layout()

    md = mo.md(r"""### NMI reads the partition, not the labels

    Each square counts how many nodes share a pair of labels. Left: `a` against `b`, the same split with different labels, so the counts fall in a clean diagonal and `nmi(a, b)` is **1**. Right: `a` against `c`, a different split, so the counts spread out and `nmi(a, c)` is **0**.

    That is why NMI suits two runs of Leiden: each run numbers its groups differently, and NMI only asks whether the runs put the same airports together.""")

    mo.vstack([
        mo.md(r"""> 🧭 **You asked:** “Is that also why NMI is useful for comparing two different runs of Leiden?”"""),md, fig])
    return


@app.cell
def cp4_ari_scratch(ig):
    # 🧪 Your space to try things out. Write any code here and run it.
    # Nothing in this cell is marked, and your tutor does not look at it.
    # Start your names with _ (like _small below): such a name belongs to
    # this cell only, so it never clashes with the exercise.
    _small = ig.Graph(n=3, edges=[(0, 1), (1, 2)])
    print(_small.degree())
    return


@app.cell(hide_code=True)
def cp4_ari_brief(mo):
    mo.md(r"""
    ### Exercise: write ARI

    /// details | 📋 Task
        type: lh-task

    **Carried over:**
    - `np` is numpy.

    **Task:**
    - Write `ari(a, b)`: $\mathrm{ARI} = \dfrac{\text{both} - \text{expected}}{\frac{1}{2}(\text{in}_a + \text{in}_b) - \text{expected}}$.
    - The terms are defined in the comments of the cell.
    - The last line must print 1.0 and a negative number.
    ///
    """)
    return


@app.cell(hide_code=True)
def cp4_ari_work(np):
    def ari(a, b):
        # `a` and `b` are two lists with one label for each airport, as in nmi.
        # 1. `ia` and `ib`: the labels of a and of b, renamed 0, 1, 2, ... (two numpy arrays with one entry for each airport).
        _, ia = np.unique(a, return_inverse=True)
        _, ib = np.unique(b, return_inverse=True)

        # 2. `table[i, j]`: the number of airports with label i in ia and label j in ib.
        table = np.zeros((ia.max() + 1, ib.max() + 1))
        np.add.at(table, (ia, ib), 1)

        # 3. `pairs(x)`: x is a number of airports. Return the number of different pairs that x airports form:
        #    pairs(5) is 10, because airports 1 and 2 are the same pair as airports 2 and 1.
        #    x can also be a numpy array of such numbers: pairs(np.array([5, 3])) is np.array([10., 3.]).
        def pairs(x):
            return x * (x - 1) / 2

        # Two airports are together in a when the two airports have the same label in a; together in b is the same for b.
        # 4. `both`: the number of pairs together in a and together in b.
        #    The airports of one cell of the table form pairs(the number of airports in the cell) such pairs; add up all the cells.
        #    `in_a`: the number of pairs together in a. Each row of the table is one label of a;
        #    add up pairs(the number of airports in the row) over the rows.
        #    `in_b`: the number of pairs together in b: the same over the columns.
        both = pairs(table).sum()
        in_a = pairs(table.sum(axis=1)).sum()
        in_b = pairs(table.sum(axis=0)).sum()

        # 5. `expected`: the value of `both` that two unrelated groupings give:
        #    in_a times in_b, divided by the number of pairs among all n airports (`n` is the number of airports).
        n = table.sum()
        expected = in_a * in_b / pairs(n)

        return (both - expected) / (0.5 * (in_a + in_b) - expected)

    print(
        ari([0, 0, 1, 1], [0, 0, 1, 1]),
        ari([0, 0, 1, 1], [0, 1, 0, 1])
    )
    return (ari,)


@app.cell(hide_code=True)
def cp4_ari_note(mo):
    mo.md(r"""
    ### ARI from the same table

    ```python
    pairs = lambda x: x * (x - 1) / 2
    both, in_a, in_b = pairs(table).sum(), pairs(table.sum(axis=1)).sum(), pairs(table.sum(axis=0)).sum()
    expected = in_a * in_b / pairs(table.sum())
    ari = (both - expected) / ((in_a + in_b) / 2 - expected)
    ```

    Subtracting the expected value is why ARI is about 0 for unrelated groupings. Tip: `pairs(table).sum()` replaces a double loop over the cells.
    """)
    return


@app.cell(hide_code=True)
def cp4_ari_vs_rand(ari, mo, plt):
    # Plain Rand vs ARI on two unrelated groupings.
    def _rand4(a, b):
        n = len(a)
        agree = sum((a[i] == a[j]) == (b[i] == b[j]) for i in range(n) for j in range(i + 1, n))
        return agree / (n * (n - 1) / 2)

    _a4 = [i % 2 for i in range(20)]      # two groups of 10
    _b4 = [i % 4 for i in range(20)]      # four groups of 5

    fig4, ax4 = plt.subplots(figsize=(5, 3))
    _vals4 = [_rand4(_a4, _b4), ari(_a4, _b4)]
    _bars4 = ax4.bar(["Rand index", "ARI"], _vals4, color=["#3959A6", "#B14434"])
    ax4.set_ylim(0, 1)
    ax4.set_ylabel("score")
    for _b4b, _v4 in zip(_bars4, _vals4):
        ax4.text(_b4b.get_x() + _b4b.get_width()/2, _v4 + 0.02, f"{_v4:.2f}", ha="center")
    ax4.set_title("unrelated groupings", fontsize=10)

    md4 = mo.md(r"""### Rand index vs ARI on unrelated groupings

    The **Rand index** is the share of node pairs the two partitions treat the same way (together in both, or apart in both). On two unrelated groupings it is still high — here about 0.58 — because a random pair is almost always "apart in both".

    The **ARI** subtracts the agreement expected by chance, so it drops to about 0. That is the correction that makes ARI more informative.""")

    mo.vstack([
        mo.md(r"""> 🧭 **You asked:** “Since ARI corrects for agreement expected by chance, is that the main reason it is usually more informative than simply measuring the fraction of node pairs that the two partitions classify the same way?”"""),md4, fig4])
    return


@app.cell
def cp5_compare_scratch(ig):
    # 🧪 Your space to try things out. Write any code here and run it.
    # Nothing in this cell is marked, and your tutor does not look at it.
    # Start your names with _ (like _small below): such a name belongs to
    # this cell only, so it never clashes with the exercise.
    _small = ig.Graph(n=3, edges=[(0, 1), (1, 2)])
    print(_small.degree())
    return


@app.cell(hide_code=True)
def cp5_compare_brief(mo):
    mo.md(r"""
    ### Exercise: groups against continents and countries

    /// details | 📋 Task
        type: lh-task

    **Carried over:**
    - `g` is the airport network (cp1), `groups` holds the Leiden group number of each airport (cp2), and `nmi` and `ari` are your functions (cp3, cp4).
    - `continent` and `country` hold the continent and the country of each airport number (cp1), and `plot_scores` draws one dot for each score.

    **Task:**
    - Find groups with Infomap.
    - Score the Leiden groups against the continents and the countries, and the Infomap groups against the countries, with your `nmi` and `ari`.

    **Other tools:**
    - `g.community_infomap()` is another method that finds groups, called like `g.community_leiden`; try `ig.Graph.Ring(4).community_infomap()`.
    - Infomap was not in the lecture: Infomap puts airports in one group when a random walk on the network (a path that follows a randomly chosen route at each step) stays long among the airports of the group ([Rosvall and Bergstrom, 2008](https://doi.org/10.1073/pnas.0706851105); [Rosvall, Axelsson and Bergstrom, 2009](https://doi.org/10.1140/epjst/e2010-01179-1)).
    ///
    """)
    return


@app.cell(hide_code=True)
def cp5_compare_work(ari, continent, country, g, groups, nmi, plot_scores):
    # `groups` (cp2) is the Leiden group number of each airport; `nmi` (cp3) and `ari` (cp4) are your functions.
    # `continent[i]` and `country[i]` are the continent and the country of airport number i (cp1).

    # 1. `info`: the result of the method `g.community_infomap()`.
    #    `info_groups`: a list with the Infomap group number of each airport (like `groups` for Leiden).
    info = g.community_infomap()
    info_groups = info.membership

    # Each score below is one number: 1 for identical groupings, about 0 for unrelated groupings.

    # 2. Leiden's groups (`groups`) against the continents.
    nmi_cont = nmi(groups, continent)
    ari_cont = ari(groups, continent)

    # 3. Leiden's groups (`groups`) against the countries.
    nmi_ctry = nmi(groups, country)
    ari_ctry = ari(groups, country)

    # 4. Infomap's groups (`info_groups`) against the countries.
    nmi_info = nmi(info_groups, country)
    ari_info = ari(info_groups, country)

    print(len(set(info_groups)), "Infomap groups")
    plot_scores([
        ("Leiden, continents", nmi_cont, ari_cont),
        ("Leiden, countries", nmi_ctry, ari_ctry),
        ("Infomap, countries", nmi_info, ari_info),
    ])
    return


@app.cell(hide_code=True)
def cp5_compare_note(mo):
    mo.md(r"""
    ### Scores against continents and countries

    ```python
    info_groups = g.community_infomap().membership
    nmi(groups, continent), ari(groups, continent)
    nmi(info_groups, country), ari(info_groups, country)
    ```

    Infomap, with many small groups, matches the countries better than Leiden does. A continent or a country is a label that people gave, not a true answer.
    """)
    return


@app.cell(hide_code=True)
def cp5_nmi_vs_ari_sensitivity(alt, ari, mo, nmi, pd):
    # One coarse partition, one fine partition: how NMI and ARI respond.
    _n5 = 12
    _rows5 = []
    for _k in [2, 3, 4, 6, 12]:
        _fine = [i % _k for i in range(_n5)]      # _k groups of equal size
        _coarse = [0] * _n5                       # one big group
        _rows5.append({
            "groups in fine": _k,
            "NMI": round(nmi(_coarse, _fine), 2),
            "ARI": round(ari(_coarse, _fine), 2),
        })

    _tbl5 = pd.DataFrame(_rows5)

    _src5 = _tbl5.melt("groups in fine", var_name="score", value_name="value")
    _chart5 = alt.Chart(_src5).mark_line(point=True).encode(
        x=alt.X("groups in fine:O", title="number of groups in the fine partition"),
        y=alt.Y("value:Q", title="score"),
        color=alt.Color("score:N", scale=alt.Scale(range=["#3959A6", "#B14434"])),
    ).properties(height=220)

    md5 = mo.md(r"""### NMI and ARI respond differently to fine splits

    Here a **coarse** partition (one big group of 12 nodes) is compared with finer and finer splits (2, 3, 4, 6, and 12 groups).

    - Both scores fall as the split gets finer.
    - **ARI** falls faster, because every new cut pushes pairs apart, and ARI counts pairs.
    - **NMI** falls more gently, because one small group inside a big group barely changes the entropy.

    So when Infomap makes many small groups, its ARI against the few large continents drops further than its NMI does.""")

    mo.vstack([
        mo.md(r"""> 🧭 **You asked:** “The results seem to suggest that Leiden captures broader geographic structure better, since its communities align quite well with continents, while Infomap produces many smaller groups and matches countries more closely. I’m also noticing that NMI and ARI do not give exactly the same relative strength of agreement. Is that because NMI and ARI respond differently to the number and sizes of communities, especially when Infomap produces as many as 124 groups?”"""),md5, _chart5])
    return


@app.cell
def cp6_sbm_scratch(ig):
    # 🧪 Your space to try things out. Write any code here and run it.
    # Nothing in this cell is marked, and your tutor does not look at it.
    # Start your names with _ (like _small below): such a name belongs to
    # this cell only, so it never clashes with the exercise.
    _small = ig.Graph(n=3, edges=[(0, 1), (1, 2)])
    print(_small.degree())
    return


@app.cell(hide_code=True)
def cp6_sbm_brief(mo):
    mo.md(r"""
    ### Exercise: build a network from groups

    /// details | 📋 Task
        type: lh-task

    **Carried over:**
    - `g` is the real network (cp1), `groups` holds the Leiden group number of each airport (cp2), `np` is numpy and `ig` is igraph.
    - `block_density(g, groups)` gives the array `P` of the shares of the pairs of airports with a route, and `plot_worlds(groups, real=g, sbm=sbm_net)` draws the networks on maps side by side, with a dot as big as the number of routes of the airport.

    **Task:**
    - Write `sample_sbm(P, z)`, which builds a network from block probabilities and groups.
    - Build a network from the Leiden groups.

    **Other tools:**
    - `np.array([[1, 2], [3, 4]])[[0, 0, 1]]` selects rows 0, 0 and 1: `[[1, 2], [1, 2], [3, 4]]`. A second `[:, [0, 0, 1]]` selects columns the same way.
    - `np.random.default_rng().random((2, 2))` gives a 2 by 2 array of random numbers between 0 and 1.
    - `np.triu(x, k=1)` keeps the part of the array above the diagonal.
    - `ig.Graph(n=3, edges=[(0, 1), (1, 2)])` builds a network from a list of pairs.
    ///
    """)
    return


@app.cell(hide_code=True)
def cp6_sbm_work(block_density, g, groups, ig, np, plot_worlds):
    # `g` (cp1) is the real network and `groups` (cp2) the Leiden group number of each airport.
    # `P[r][s]` is the share of the pairs of airports that have a route, when one airport is in group r and the other in group s.
    # P is a K by K array, and K is the number of groups.
    P = block_density(g, groups)

    def sample_sbm(P, z):
        # `P` is a K by K array as above and `z` is a list with the group number of each node.
        # Return a network in which nodes i and j are linked with probability P[z[i]][z[j]],
        # independently for each pair, and no node is linked to the same node (no pair with i = j).
        z = np.asarray(z)
        n = len(z)

        # 1. Probability for every pair of nodes.
        p = P[z[:, None], z[None, :]]

        # 2. Randomly decide whether each pair is linked.
        linked = np.random.random((n, n)) < p

        # 3. Keep each pair only once, with i < j.
        linked = np.triu(linked, k=1)

        rows, cols = np.nonzero(linked)

        return ig.Graph(n=n, edges=list(zip(rows, cols)))

    sbm_net = sample_sbm(P, groups)

    print(
        sbm_net.vcount(),
        "airports and",
        sbm_net.ecount(),
        "routes; the real network has",
        g.ecount()
    )

    plot_worlds(groups, real=g, sbm=sbm_net)
    return (sbm_net,)


@app.cell(hide_code=True)
def cp6_sbm_note(mo):
    mo.md(r"""
    ### The stochastic block model

    ```python
    p = P[z][:, z]
    linked = np.triu(np.random.default_rng().random((n, n)) < p, k=1)
    rows, cols = np.nonzero(linked)
    ig.Graph(n=n, edges=list(zip(rows, cols)))
    ```

    The chance of a link between two nodes depends only on the two groups. Tip: `P[z][:, z]` builds all of p without a loop over the pairs.
    """)
    return


@app.cell(hide_code=True)
def cp6_sbm_interchangeable(mo, np, plt):
    # A tiny two-group block model: within a group, every node is interchangeable.
    _P6 = np.array([[0.9, 0.05],
                    [0.05, 0.9]])          # dense within a group, sparse between groups
    _z6 = [0, 0, 0, 1, 1, 1]              # three nodes in group 0, three in group 1
    _n6 = len(_z6)

    # Expected number of links for each node, from the per-pair probabilities.
    _p6 = _P6[np.asarray(_z6)[:, None], np.asarray(_z6)[None, :]]
    _exp6 = _p6.sum(axis=1)                # sum of probabilities over a node's row

    _fig6, _ax6 = plt.subplots(figsize=(5.5, 2.6))
    _ax6.bar(range(_n6), _exp6, color=["#3959A6"]*3 + ["#B14434"]*3)
    _ax6.set_xlabel("node")
    _ax6.set_ylabel("expected number of links")
    _ax6.set_title("all nodes in a group get the same expectation", fontsize=10)

    md6 = mo.md(r"""### Interchangeable within a group

    In the block model, node `i` and node `j` link with probability `P[z[i]][z[j]]`, and nothing else about `i` or `j` enters. So two nodes in the same group have the **same** probability with every other node, and the same expected number of links.

    Here three nodes sit in group 0 and three in group 1: the three in each group have identical expected degrees. The model stores group densities, but no per-airport difference — so any airport that is far busier than its neighbours is not something the model can produce.""")

    mo.vstack([
        mo.md(r"""> 🧭 **You asked:** “The block model seems to reproduce the large-scale community structure quite well because the connection probability depends on the groups of the two airports. However, within each pair of groups, airports are treated as interchangeable. Does that mean the model can preserve community-level densities while still failing to reproduce features such as the very high degree of hub airports or the exact degree distribution?”"""),md6, _fig6])
    return


@app.cell
def cp7_hubs_scratch(ig):
    # 🧪 Your space to try things out. Write any code here and run it.
    # Nothing in this cell is marked, and your tutor does not look at it.
    # Start your names with _ (like _small below): such a name belongs to
    # this cell only, so it never clashes with the exercise.
    _small = ig.Graph(n=3, edges=[(0, 1), (1, 2)])
    print(_small.degree())
    return


@app.cell(hide_code=True)
def cp7_hubs_brief(mo):
    mo.md(r"""
    ### Exercise: compare the degrees

    /// details | 📋 Task
        type: lh-task

    **Carried over:**
    - `g` is the real network (cp1), `sbm_net` is the network that `sample_sbm` built (cp6), and `np` is numpy.
    - `plot_degrees(real=g, sbm=sbm_net)` draws the CCDF of the degrees of each network; the CCDF at k is the share of airports with at least k routes.

    **Task:**
    - Find the largest degree of the real network and the largest degree of the block-model network.
    - Find how well the degrees of the same airports agree.

    **Other tools:**
    - `np.corrcoef(x, y)[0, 1]` is the correlation of two lists: `np.corrcoef([1, 2, 3], [2, 4, 6])[0, 1]` gives `1.0`.
    ///
    """)
    return


@app.cell(hide_code=True)
def cp7_hubs_work(g, np, plot_degrees, sbm_net):
    # `g` (cp1) is the real network and `sbm_net` (cp6) is the network that sample_sbm built.

    # 1. `max_real` and `max_sbm`: the largest degree of g and the largest degree of sbm_net.
    max_real = max(g.degree())
    max_sbm = max(sbm_net.degree())

    # 2. Correlation between each airport's degree in the real and SBM networks.
    corr_sbm = np.corrcoef(g.degree(), sbm_net.degree())[0, 1]

    print(max_real, max_sbm, round(corr_sbm, 2))
    plot_degrees(real=g, sbm=sbm_net)
    return


@app.cell(hide_code=True)
def cp7_hubs_note(mo):
    mo.md(r"""
    ### No hubs

    ```python
    max(g.degree()), max(sbm_net.degree())          # about 246 and 40
    np.corrcoef(g.degree(), sbm_net.degree())[0, 1]  # about 0.2
    ```

    The block model has the same group sizes and group densities as the real network, but no hubs.
    """)
    return


@app.cell(hide_code=True)
def cp7_dcsbm_motivation(mo, np, plt):
    # The degree-corrected idea on a tiny two-group block.
    _w7 = np.array([[8.0, 1.0],
                    [1.0, 8.0]])          # links between group r and s
    _z7 = [0, 0, 0, 1, 1, 1]
    _deg7 = np.array([4.0, 2.0, 1.0, 4.0, 2.0, 1.0])   # a hub in each group
    _kappa7 = np.bincount(_z7, weights=_deg7)          # total degree of each group
    _theta7 = _deg7 / _kappa7[np.asarray(_z7)]         # each node's share of its group

    # Expected links between i and j: theta_i * theta_j * w[group_i][group_j]
    _th7 = _theta7[:, None] * _theta7[None, :] * _w7[np.asarray(_z7)[:, None], np.asarray(_z7)[None, :]]
    _exp7 = _th7.sum(axis=1)

    _fig7, _ax7 = plt.subplots(figsize=(5.5, 2.6))
    _ax7.bar(range(6), _exp7, color=["#3959A6"]*3 + ["#B14434"]*3)
    _ax7.set_xlabel("node")
    _ax7.set_ylabel("expected number of links")
    _ax7.set_title("theta lets hubs stand out inside a group", fontsize=10)

    md7 = mo.md(r"""### The degree-corrected idea

    The plain block model gives every node in a group the same expected degree. The degree-corrected model keeps the block structure `w`, but each node `i` also gets a parameter `theta[i]`, its own share of its group's total degree. The mean number of links between `i` and `j` is then `theta[i] * theta[j] * w[group[i]][group[j]]`.

    Here each group has a hub (theta 4/7), a middle node, and a small node. The bars now differ **inside** a group, so the hub stands out — the degree heterogeneity the plain block model could not produce.""")

    mo.vstack([
        mo.md(r"""> 🧭 **You asked:** “Is this the main motivation for a degree-corrected stochastic block model, where each node gets its own degree-related parameter while the block structure is still preserved?”"""),md7, _fig7])
    return


@app.cell
def cp8_dcsbm_scratch(ig):
    # 🧪 Your space to try things out. Write any code here and run it.
    # Nothing in this cell is marked, and your tutor does not look at it.
    # Start your names with _ (like _small below): such a name belongs to
    # this cell only, so it never clashes with the exercise.
    _small = ig.Graph(n=3, edges=[(0, 1), (1, 2)])
    print(_small.degree())
    return


@app.cell(hide_code=True)
def cp8_dcsbm_brief(mo):
    mo.md(r"""
    ### Exercise: the degree-corrected block model

    /// details | 📋 Task
        type: lh-task

    **Carried over:**
    - `g` is the real network (cp1), `groups` holds the Leiden group number of each airport (cp2), `sbm_net` is the block-model network (cp6), `np` is numpy and `ig` is igraph.
    - `edge_ends(g, groups)` gives the array `w` of the numbers of routes between groups, `plot_worlds(...)` draws the networks on maps side by side (a dot as big as the number of routes of the airport), `plot_degrees(...)` draws the CCDFs, and `mo.vstack([a, b])` shows the pictures `a` and `b` one above the other.

    **Task:**
    - Compute $\kappa_r$ and $\hat\theta_i = k_i / \kappa_{c_i}$ as in the quiz.
    - Write `sample_dcsbm(theta, w, z)` and build a network from the Leiden groups.
    - Find the largest degree of the new network and how well the degrees of the new network agree with the real degrees.

    **Other tools:**
    - `np.bincount([0, 1, 1], weights=[5, 2, 3])` adds the weights by group: `[5., 5.]`.
    - `rng.poisson(means)` draws one Poisson number for each mean in an array, where `rng = np.random.default_rng()`.
    - `np.repeat([[0, 1], [2, 3]], [2, 1], axis=0)` repeats row 0 twice and row 1 once: `[[0, 1], [0, 1], [2, 3]]`.
    ///
    """)
    return


@app.cell
def cp8_dcsbm_work(
    edge_ends,
    g,
    groups,
    ig,
    mo,
    np,
    plot_degrees,
    plot_worlds,
    sbm_net,
):
    # `g` is the real network, `groups` the Leiden group of each airport,
    # and w[r][s] is the number of routes between groups r and s.
    w = edge_ends(g, groups)
    deg = np.array(g.degree())

    # 1. Total degree in each group
    kappa = np.bincount(groups, weights=deg)

    # 2. Each airport's share of its group's total degree
    theta = deg / kappa[np.array(groups)]

    def sample_dcsbm(theta, w, z):
        z = np.asarray(z)
        n = len(z)

        # 3. Expected number of routes between every pair of airports
        rate = (
            theta[:, None]
            * theta[None, :]
            * w[z[:, None], z[None, :]]
        )

        # 4. Draw Poisson edge counts and keep each pair only once
        counts = np.random.poisson(rate)
        counts = np.triu(counts, k=1)

        # 5. Build the multigraph:
        # if counts[i,j] = 3, add the edge (i,j) three times
        rows, cols = np.nonzero(counts)

        edges = []
        for i, j in zip(rows, cols):
            edges.extend([(int(i), int(j))] * int(counts[i, j]))

        return ig.Graph(n=n, edges=edges, directed=False)

    dc_net = sample_dcsbm(theta, w, groups)

    # 6. Compare its degrees with the real network
    max_dc = max(dc_net.degree())
    corr_dc = np.corrcoef(g.degree(), dc_net.degree())[0, 1]

    print(max_dc, round(corr_dc, 2), dc_net.ecount(), "routes")
    mo.vstack([
        plot_worlds(groups, real=g, sbm=sbm_net, dcsbm=dc_net),
        plot_degrees(real=g, sbm=sbm_net, dcsbm=dc_net)
    ])
    return corr_dc, dc_net, kappa, max_dc, sample_dcsbm, theta


@app.cell(hide_code=True)
def cp8_dcsbm_check(
    check_dcsbm,
    corr_dc,
    dc_net,
    g,
    groups,
    kappa,
    max_dc,
    sample_dcsbm,
    theta,
):
    check_dcsbm(sample_dcsbm, g, groups, kappa, theta, dc_net, max_dc, corr_dc)
    return


@app.cell(hide_code=True)
def cp8_dcsbm_send(mo):
    cp8_dcsbm_send = mo.ui.run_button(label="Submit to Tutor")
    cp8_dcsbm_send
    return (cp8_dcsbm_send,)


@app.cell(hide_code=True)
def cp8_dcsbm_sent(cp8_dcsbm_send, mo):
    from pathlib import Path as _P
    if cp8_dcsbm_send.value:
        _P("session_artifacts").mkdir(exist_ok=True)
        with open("session_artifacts/student_signal.txt", "a") as _f:
            _f.write("cp8_dcsbm_work" + "\n")
    mo.md(
        "<span style='color:#6A6D75;font-size:13px'>*Submit to Tutor hands "
        "this cell in; your tutor answers in the terminal.*</span>"
    )
    return


@app.cell(hide_code=True)
def cp8_dcsbm_note(mo):
    mo.md(r"""
    ### The degree-corrected block model

    ```python
    kappa = np.bincount(groups, weights=deg)
    theta = deg / kappa[groups]
    rate = np.outer(theta, theta) * w[z][:, z]
    counts = np.triu(np.random.default_rng().poisson(rate), k=1)
    rows, cols = np.nonzero(counts)
    ig.Graph(n=n, edges=np.repeat(np.column_stack([rows, cols]), counts[rows, cols], axis=0).tolist())
    ```

    Each airport has a theta, so the network has hubs again and the degrees agree with the real degrees. Tip: `np.outer(theta, theta) * w[z][:, z]` builds all of the rates without a loop.
    """)
    return


@app.cell(hide_code=True)
def cp8_two_effects(mo, np, plt):
    # w and theta: which groups connect, and which airports are hubs.
    _n8 = 6
    _z8 = [0, 0, 0, 1, 1, 1]
    _w8 = np.array([[8.0, 1.0],
                    [1.0, 8.0]])          # w: group 0 links a lot inside, group 1 links a lot inside
    _deg8 = np.array([4.0, 2.0, 1.0, 4.0, 2.0, 1.0])
    _kappa8 = np.bincount(_z8, weights=_deg8)
    _theta8 = _deg8 / _kappa8[np.asarray(_z8)]

    # The expected route count between i and j splits into a group part and a node part.
    _group_part8 = _w8[np.asarray(_z8)[:, None], np.asarray(_z8)[None, :]]
    _node_part8 = _theta8[:, None] * _theta8[None, :]
    _rate8 = _node_part8 * _group_part8

    _fig8, _ax8 = plt.subplots(1, 2, figsize=(9, 3))
    _im8 = _ax8[0].imshow(_group_part8, cmap="Blues")
    _ax8[0].set_title("w: which groups connect", fontsize=10)
    _ax8[0].set_xticks([]); _ax8[0].set_yticks([])
    _im82 = _ax8[1].imshow(_node_part8, cmap="OrRd")
    _ax8[1].set_title("theta x theta: which airports are active", fontsize=10)
    _ax8[1].set_xticks([]); _ax8[1].set_yticks([])
    plt.tight_layout()

    md8 = mo.md(r"""### Two effects, two factors

    The mean number of routes between airports `i` and `j` is `theta[i] * theta[j] * w[group[i]][group[j]]`, so it splits into two factors:

    - **`w`** (left) says which groups connect — the mesoscale community structure.
    - **`theta[i] * theta[j]`** (right) says which airports are active — the node-level hubs inside those groups.

    The plain block model keeps only the left panel, which is why it loses the hubs. The degree-corrected model multiplies in the right panel and gets both back.""")

    mo.vstack([
        mo.md(r"""> 🧭 **You asked:** “Is it fair to interpret this as separating two effects: w explains which groups connect, while theta explains which individual airports become hubs within those groups?”"""),md8, _fig8])
    return


@app.cell(hide_code=True)
def session_record(mo):
    mo.md(r"""
    ## 📋 Session record

    *Your answer to each question, and every word you typed while working on*
    *it — this is what gets reviewed, not the code. Hints are never held*
    *against you.*

    **cp1_graph** · pass

    *Build the airport network, count its nodes and edges, and find the largest degree and the airport with that degree.*

    > (no answer — the code is their answer)

    *You typed:* "Yes i can see it"

    *Tutor's note:* Built g with n=len(codes) and edges=route_list, counted with vcount/ecount, found k_max with max(g.degree()) and hub via g.degree().index(k_max) into codes — all four steps first time.

    **cp2_leiden** · pass

    *Find groups with Leiden using modularity, and save the group list, the number of groups, and the modularity.*

    > (no answer — the code is their answer)

    *You typed:* "The result makes sense. Since degree counts the number of routes connected to an airport, AMS being the highest-degree node means it acts as the largest hub in this network. I also notice that the average degree is only about 11 while AMS has 246 routes, so the degree distribution seems highly uneven. Would this kind of hub structure make the airport network more robust to random airport failures but more vulnerable if the highest-degree hubs were deliberately removed?" · "That makes sense. So the same degree heterogeneity that gives the network robustness to random failures also creates vulnerability to targeted hub removal. I’m ready to move on."

    *Tutor's note:* Set objective_function="modularity", took .membership for groups, used len(leiden) for n_groups (equivalent to len(set(groups))), and g.modularity(groups) — all first time.

    **cp3_nmi** · pass

    *Write nmi(a, b) from the lecture's definition, with the last line printing 1.0 and 0.0.*

    > (no answer — the code is their answer)

    *You typed:* "The modularity is about 0.67, which seems fairly high, and the detected groups also look geographically clustered on the map. Does that mean the airport network’s community structure is driven mainly by regional connections, while the long-distance international routes act mostly as links between those communities? Also, since Leiden is stochastic and the number of groups can change slightly between runs, should I think of the exact 17 groups as less important than the overall modularity and the stability of the larger regional communities?" · "Letsmove on"

    *Tutor's note:* Wrote nmi from the table of counts: np.unique with return_inverse for ia/ib, np.add.at to fill the table, axis sums for p_a/p_b, filtered entropies with p>0, and mutual information via p_a[:,None]*p_b[None,:] outer products, then 2*mi/(h_a+h_b). Used outer-product indexing rather than np.outer — same result.

    **cp4_ari** · pass

    *Write ari(a, b) from the lecture's definition, with the last line printing 1.0 and a negative number.*

    > (no answer — the code is their answer)

    *You typed:* "I think I understand why relabeling does not affect NMI: the labels themselves are arbitrary, and NMI only depends on how many nodes fall into each overlap between the two partitions. So two partitions can use completely different numerical labels but still have NMI = 1 if they divide the nodes in exactly the same way. Is that also why NMI is useful for comparing two different runs of Leiden?" · "Lets move on"

    *Tutor's note:* Wrote ari from the same table: pairs = x*(x-1)/2, both = pairs(table).sum(), in_a and in_b from pairs of the row and column sums, expected = in_a*in_b/pairs(n), and the ARI formula. All steps first time.

    **cp5_compare** · pass

    *Find groups with Infomap and score Leiden against continents and countries, and Infomap against countries, with nmi and ari.*

    > (no answer — the code is their answer)

    *You typed:* "Since ARI corrects for agreement expected by chance, is that the main reason it is usually more informative than simply measuring the fraction of node pairs that the two partitions classify the same way?" · "That makes sense. So ARI measures agreement beyond chance, with 1 indicating identical groupings and values near 0 indicating roughly chance-level agreement. I’m ready to move on." · "I accidentaly closed my notebook and browser"

    *Tutor's note:* Found Infomap groups with g.community_infomap().membership and wrote all six scores with the correct argument pairs: nmi/ari of groups vs continent, groups vs country, and info_groups vs country. All steps first time.

    **cp6_sbm** · pass

    *Write sample_sbm(P, z) that links each pair with probability P[z[i]][z[j]], and build a network from the Leiden groups.*

    > (no answer — the code is their answer)

    *You typed:* "The results seem to suggest that Leiden captures broader geographic structure better, since its communities align quite well with continents, while Infomap produces many smaller groups and matches countries more closely. I’m also noticing that NMI and ARI do not give exactly the same relative strength of agreement. Is that because NMI and ARI respond differently to the number and sizes of communities, especially when Infomap produces as many as 124 groups?" · "Move on"

    *Tutor's note:* Built p with P[z[:,None], z[None,:]] (fancy indexing for the same n-by-n block-probability table), linked with np.random.random((n,n)) < p, kept i<j with np.triu(k=1), and returned ig.Graph from zip(rows, cols). All steps first time.

    **cp7_hubs** · pass

    *Find the largest degree of the real and block-model networks, and the correlation of their degree lists.*

    > (no answer — the code is their answer)

    *You typed:* "The block model seems to reproduce the large-scale community structure quite well because the connection probability depends on the groups of the two airports. However, within each pair of groups, airports are treated as interchangeable. Does that mean the model can preserve community-level densities while still failing to reproduce features such as the very high degree of hub airports or the exact degree distribution?" · "That makes sense. So this SBM captures mesoscale structure through the block densities, but it does not model node-level heterogeneity within each block. A degree-corrected block model would therefore be more appropriate if we also wanted to reproduce the hub structure of the airport network. going to move on now"

    *Tutor's note:* Found max_real and max_sbm with max(g.degree()) and max(sbm_net.degree()), and corr_sbm with np.corrcoef(g.degree(), sbm_net.degree())[0,1]. All steps first time.

    **cp8_dcsbm** · pass

    *Compute kappa and theta by the quiz's estimates, write sample_dcsbm, build a network, and compare its degrees with the real network.*

    > (no answer — the code is their answer)

    *You typed:* "The result makes the limitation of the basic SBM very clear. The real network has a maximum degree of 246, while the sampled block model only reaches 36, and the node-level degree correlation is just 0.25. So even though the SBM preserves the connection densities between communities, it treats airports within the same group as statistically similar and cannot reproduce the strong degree heterogeneity of real airports. Is this the main motivation for a degree-corrected stochastic block model, where each node gets its own degree-related parameter while the block structure is still preserved?" · "That makes sense. So the block matrix (w) captures the mesoscale community structure, while the node-specific (\theta_i) captures degree heterogeneity within those communities. This separates “which groups tend to connect” from “which individual nodes are especially active.” Lets move"

    *Tutor's note:* Computed kappa with np.bincount(groups, weights=deg), theta = deg/kappa[groups], rate via outer products theta[:,None]*theta[None,:]*w[z[:,None],z[None,:]], Poisson counts with np.triu(k=1), and repeated each pair counts[i,j] times with a loop building the edge list (equivalent to np.repeat). max_dc and corr_dc correct. All steps first time.

    ### 🧭 Your own questions (8)

    - *Would this kind of hub structure make the airport network more robust to random airport failures but more vulnerable if the highest-degree hubs were deliberately removed?*
    - *Does that mean the airport network's community structure is driven mainly by regional connections, while the long-distance international routes act mostly as links between those communities? Also, since Leiden is stochastic and the number of groups can change slightly between runs, should I think of the exact 17 groups as less important than the overall modularity and the stability of the larger regional communities?*
    - *Is that also why NMI is useful for comparing two different runs of Leiden?*
    - *Since ARI corrects for agreement expected by chance, is that the main reason it is usually more informative than simply measuring the fraction of node pairs that the two partitions classify the same way?*
    - *Is that because NMI and ARI respond differently to the number and sizes of communities, especially when Infomap produces as many as 124 groups?*
    - *Does that mean the model can preserve community-level densities while still failing to reproduce features such as the very high degree of hub airports or the exact degree distribution?*
    - *Is this the main motivation for a degree-corrected stochastic block model, where each node gets its own degree-related parameter while the block structure is still preserved?*
    - *Is it fair to interpret this as separating two effects: w explains which groups connect, while theta explains which individual airports become hubs within those groups?*
    """)
    return


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
    return np, plt


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
        block_density,
        check_dcsbm,
        edge_ends,
        load_airports,
        plot_degrees,
        plot_scores,
        plot_world,
        plot_worlds,
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
    return codes, continent, country, route_list


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
