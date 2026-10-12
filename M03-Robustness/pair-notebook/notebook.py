# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "marimo",
#     "igraph==1.0.0",
#     "matplotlib",
#     "seaborn",
#     "altair",
#     "numpy==2.5.3",
#     "pandas",
#     "pillow",
#     "powerlaw==2.0.0",
# ]
# ///

# The notebook a session starts from. Everything below is infrastructure that
# survives nb_fresh_start (only NAMED cells are wiped), and every cell the
# lesson adds is named.
#
# No netviz here, unlike m01/m02. This module's two pictures are a geographic
# map and a line chart; neither wants a drag-able force layout, and dropping
# it takes ~270 lines of vendored d3/rough.js out of the file. An improvised
# detour cell that needs a network picture draws it in matplotlib.

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
    ## A Network in Code

    This module builds networks in code with the `igraph` library, and asks them questions.
    """)
    return


@app.cell
def cp1_build_scratch(ig):
    # 🧪 Your space to try things out. Write any code here and run it.
    # Nothing in this cell is marked, and your tutor does not look at it.
    # Start your names with _ (like _small below): such a name belongs to
    # this cell only, so it never clashes with the exercise.
    _small = ig.Graph(n=3, edges=[(0, 1), (1, 2)])
    print(_small.degree())
    return


@app.cell(hide_code=True)
def cp1_build_brief(mo):
    mo.md(r"""
    ### Exercise: build a network, then edit a copy

    /// details | 📋 Task
        type: lh-task

    **Task:**
    - Build the network in igraph. It has 7 nodes, numbered 0 to 6, and
      the 9 edges in `edge_list`.
    - Ask the network how many nodes and how many edges it has.
    - Make a copy of the network.
    - Add one node to the copy, and one edge from the new node to node 6.
    - Delete node 0 from the copy.
    - Find the new number of the node that used to be node 2.

    The igraph calls are in [the walkthrough](https://molab.marimo.io/notebooks/nb_7hrZrDkZgWps8uHkfsuBA3), steps 1 to 3.
    ///
    """)
    return


@app.cell(hide_code=True)
def cp1_build_work(draw_net, ig, mo, protect):
    # Libraries this cell uses. The notebook has imported them already;
    # in your own Python file, install them once and import them:
    #   import igraph as ig   # pip install igraph==1.0.0

    # The network has 7 nodes, numbered 0 to 6, and these 9 edges.
    edge_list = [(0, 1), (0, 2), (1, 2), (1, 3), (2, 3),
                 (3, 4), (4, 5), (4, 6), (5, 6)]

    # 1. `g`: an igraph network with 7 nodes and the edges in edge_list.
    g = ig.Graph(n=7, edges=edge_list)
    # Every exercise after this one uses g. The next line stops g from
    # being changed, so change a copy of g, never g itself.
    protect(g)

    # 2. `n_nodes`: the number of nodes in g (one integer).
    #    `n_edges`: the number of edges in g (one integer).
    #    Ask g itself; do not type the numbers by hand.
    n_nodes = g.vcount()
    n_edges = g.ecount()

    # 3. `edited`: a copy of g, so that g itself stays as it is.
    # 3. Make an independent copy.
    edited = g.copy()

    # 4. Add one new node to `edited`, then one edge from the new node
    #    to node 6. The new node gets the next free number, 7.
    edited.add_vertices(1)
    edited.add_edges([(7, 6)])
    # 5. Delete node 0 from `edited` — the node itself, not only its edges.
    edited.delete_vertices([0])
    # 6. `was_2_now`: the number that the node which used to be node 2
    #    has now (one integer). Run the cell and look at the second picture.
    was_2_now = 1

    print(n_nodes, n_edges, was_2_now)
    mo.hstack([draw_net(g, title="g"), draw_net(edited, title="edited")])
    return (g,)


@app.cell(hide_code=True)
def cp1_build_note(mo):
    mo.md(r"""
    ### Building a network, and editing a copy

    ```python
    g = ig.Graph(n=7, edges=edge_list)
    g.vcount(), g.ecount()        # 7, 9
    edited = g.copy()
    edited.add_vertices(1)        # the new node is number 7
    edited.add_edges([(7, 6)])    # one edge, from 7 to 6
    edited.delete_vertices([0])   # node 0, and both of its edges
    ```

    A list of edges only mentions nodes that have at least one edge. `n`
    sets how many nodes there are, so a node with no edges still exists.

    `delete_vertices()` removes the node and its edges: the copy goes from
    8 nodes and 10 edges to **7 nodes and 8 edges**. Every node after the
    deleted one moves down by one number, so the node that was number 2
    is now number **1**. Save node numbers after deleting, or use node
    names (`g.vs["name"]`) instead.
    """)
    return


@app.cell
def detour_vertex_names(draw_net, ig, mo):
    _d = ig.Graph(n=4, edges=[(0, 1), (1, 2), (2, 3)])
    _d.vs["name"] = ["a", "b", "c", "d"]
    _d.delete_vertices([0])
    mo.vstack([
        mo.md(r"""### 🧭 Detour: node names survive deleting

    Yes — store the label as a **vertex attribute** with `g.vs["name"]`. A name
    is a string that travels with its node. When a node is deleted, the
    surviving nodes keep their names, even though their **numbers** shift down.

    Below, the four nodes are named a, b, c, d, then node 0 (named a) is
    deleted. The survivors are still b, c, d."""),
        draw_net(_d, title="names after deleting a"),
    ])
    return


@app.cell
def cp2_matrix_scratch(ig):
    # 🧪 Your space to try things out. Write any code here and run it.
    # Nothing in this cell is marked, and your tutor does not look at it.
    # Start your names with _ (like _small below): such a name belongs to
    # this cell only, so it never clashes with the exercise.
    _small = ig.Graph(n=3, edges=[(0, 1), (1, 2)])
    print(_small.degree())
    return


@app.cell(hide_code=True)
def cp2_matrix_brief(mo):
    mo.md(r"""
    ### Exercise: the network as a square of numbers

    /// details | 📋 Task
        type: lh-task

    **Task:**
    - Write the network `g` as its adjacency matrix `A`, a numpy array.
    - Add up each row of `A`.
    - Ask `g` directly for the degree of every node — how many edges each
      node has.
    - Find the average degree.

    **Other tools:**
    - `np.mean(x)` gives the average of a list of numbers.
      `np.mean([1, 2, 1])` gives `1.333…`.

    The igraph calls are in [the walkthrough](https://molab.marimo.io/notebooks/nb_7hrZrDkZgWps8uHkfsuBA3), steps 4 and 5.
    ///
    """)
    return


@app.cell(hide_code=True)
def cp2_matrix_work(g, np):
    # Libraries this cell uses. The notebook has imported them already;
    # in your own Python file, install them once and import them:
    #   import numpy as np   # pip install numpy==2.5.3

    # The network from the last exercise is still in `g`.

    # 1. `A`: the adjacency matrix of g as a numpy array (7 rows, 7 columns).
    #    A[i, j] is 1 when nodes i and j share an edge, and 0 otherwise.
    A = np.array(g.get_adjacency().data)

    # 2. Sum each row — `sum` takes an `axis`. https://numpy.org/doc/2.3/reference/generated/numpy.sum.html
    #    `row_sums`: a numpy array of 7 numbers, one total per row.
    row_sums = row_sums = A.sum(axis=1)

    # 3. `deg`: the degree of every node in g — how many edges each node
    #    has — as a list of 7 integers, in node order. Ask g directly.
    deg = g.degree()

    # 4. `k_mean`: the average of the numbers in `deg` (one number).
    k_mean = np.mean(deg)

    print(A)
    print("row sums:", row_sums)
    print("degrees: ", deg)
    print("mean degree:", k_mean)
    return


@app.cell(hide_code=True)
def cp2_matrix_note(mo):
    mo.md(r"""
    ### Adjacency matrix, row sums and degree

    ```python
    A = np.array(g.get_adjacency().data)   # 7 by 7
    A.sum(axis=1)                          # [2, 3, 3, 3, 3, 2, 2]
    g.degree()                             # [2, 3, 3, 3, 3, 2, 2]
    np.mean(g.degree())                    # 2.571
    ```

    The adjacency matrix ${\bf A}$ has $A_{ij} = 1$ when nodes $i$ and $j$
    share an edge, and $A_{ij} = 0$ otherwise. `axis=1` adds along each
    row. The network has no direction, so ${\bf A}$ is symmetric and
    `axis=0` gives the same numbers.

    Each row total is the **degree** of that node, its number of edges. All
    the entries add up to $2M = 18$: each of the $M = 9$ edges is counted
    once from each end. The **mean degree** is
    $\langle k \rangle = 18 / 7 \approx 2.571$.

    A network with $N$ nodes has an $N \times N$ matrix; at $N = 10^6$ that
    is $10^{12}$ entries, almost all zero. `g.degree()` reads igraph's own
    list of each node's neighbours and never builds the matrix.
    """)
    return


@app.cell
def detour_adjacency_list(draw_net, g, mo):
    mo.vstack([
        mo.md(r"""### 🧭 Detour: igraph keeps lists, not a full matrix

    igraph stores each node's **neighbours** as a list — an **adjacency list** —
    rather than a whole matrix of ones and zeros. So `g.degree()` only reads the
    length of each node's neighbour list. For a large, sparse network this
    stays cheap, while a full $N \times N$ matrix would be mostly zeros.

    Below: node 2's neighbour list is `[0, 1, 3]`, so its degree is 3."""),
        draw_net(g, highlight=(2,), title="node 2 and its neighbours"),
    ])
    return


@app.cell
def cp3_paths_scratch(ig):
    # 🧪 Your space to try things out. Write any code here and run it.
    # Nothing in this cell is marked, and your tutor does not look at it.
    # Start your names with _ (like _small below): such a name belongs to
    # this cell only, so it never clashes with the exercise.
    _small = ig.Graph(n=3, edges=[(0, 1), (1, 2)])
    print(_small.degree())
    return


@app.cell(hide_code=True)
def cp3_paths_brief(mo):
    mo.md(r"""
    ### Exercise: routes, and the pieces left after a cut

    /// details | 📋 Task
        type: lh-task

    **Task:**
    - In the network `g`, list every route from node 0 to node 6.
    - Pick out one shortest route from node 0 to node 6.
    - Count the edges that route crosses.
    - Make a copy of `g`, and remove every edge at node 4 from the copy.
    - Find the groups of nodes in the copy that can still reach each other.
    - Find the size of each group, and the size of the largest group.

    **Other tools:**
    - `len(x)` gives the length of a list, and `max(x)` its largest number.

    The igraph calls are in [the walkthrough](https://molab.marimo.io/notebooks/nb_7hrZrDkZgWps8uHkfsuBA3), steps 3, 6, 7 and 8.
    ///
    """)
    return


@app.cell(hide_code=True)
def cp3_paths_work(draw_net, g, mo):
    # The network is still in `g`.

    # 1. `all_routes`: every route from node 0 to node 6 that never visits a
    #    node twice (a list of routes; each route is a list of node numbers).
    all_routes = g.get_all_simple_paths(0, to=6)

    # 2. `shortest`: one shortest route from node 0 to node 6 — a list of
    #    node numbers that starts with 0 and ends with 6.
    shortest = g.get_shortest_paths(0, to=6)[0]

    # 3. `hops`: how many edges `shortest` crosses (one integer).
    hops = len(shortest) - 1

    # 4. `cut`: a copy of g with every edge at node 4 removed.

    cut = g.copy()
    cut.delete_edges(cut.incident(4))

    # 5. `groups`: the groups of nodes in `cut` that can reach each other
    #    along edges — a list of groups, each a list of node numbers.
    groups = list(cut.connected_components())

    # 6. `sizes`: how many nodes each group has (a list of integers).
    #    `biggest`: the number of nodes in the largest group (one integer).
    sizes = [len(group) for group in groups]
    biggest = max(sizes)

    print(len(all_routes), "routes; shortest:", shortest, "crosses", hops, "edges")
    print("sizes:", sizes, "biggest:", biggest)
    mo.hstack([draw_net(g, route=shortest, highlight=(0, 6), title="shortest route"),
               draw_net(cut, closed=(4,), title="node 4 cut off")])
    return


@app.cell(hide_code=True)
def cp3_paths_note(mo):
    mo.md(r"""
    ### Routes, and the pieces after a cut

    ```python
    g.get_all_simple_paths(0, to=6)   # 8 routes
    g.get_shortest_paths(0, to=6)[0]  # [0, 1, 3, 4, 6]
    cut = g.copy()
    cut.delete_edges(cut.incident(4))
    [len(c) for c in cut.connected_components()]  # [4, 2, 1]
    ```

    A **simple path** never visits a node twice. There are 8 from node 0
    to node 6. `get_shortest_paths` gives a **list** of routes, because two
    routes, `[0, 1, 3, 4, 6]` and `[0, 2, 3, 4, 6]`, both cross 4 edges.

    A **connected component** is a group of nodes that can all reach each
    other along edges. Cutting node 4's edges leaves three: `[4, 2, 1]`.
    `[4, 2, 1]` and `[6, 1, 1]` are both three pieces, so the count does
    not show the damage. The size of the **largest component** does.
    """)
    return


@app.cell
def detour_articulation_point(draw_net, g, mo):
    _cut = g.copy()
    _cut.delete_edges(_cut.incident(4))
    _del = g.copy()
    _del.delete_vertices([4])
    mo.vstack([
        mo.md(r"""### 🧭 Detour: articulation point — cut edges vs delete the node

    Node 4 is an **articulation point** (a cut vertex): removing it splits the
    connected network into more than one piece.

    Cutting its edges leaves node 4 standing as an isolated node — **3 pieces,
    7 nodes**. Deleting the node removes it entirely — **2 pieces, 6 nodes**.
    The total changes, so the connectivity number (largest piece ÷ total) is not
    the same."""),
        mo.hstack([
            draw_net(_cut, closed=(4,), title="edges cut: node 4 stays"),
            draw_net(_del, title="node 4 deleted"),
        ]),
    ])
    return


@app.cell
def cp4_measure_scratch(ig):
    # 🧪 Your space to try things out. Write any code here and run it.
    # Nothing in this cell is marked, and your tutor does not look at it.
    # Start your names with _ (like _small below): such a name belongs to
    # this cell only, so it never clashes with the exercise.
    _small = ig.Graph(n=3, edges=[(0, 1), (1, 2)])
    print(_small.degree())
    return


@app.cell(hide_code=True)
def cp4_measure_brief(mo):
    mo.md(r"""
    ### Exercise: connectivity and the R-index

    /// details | 📋 Task
        type: lh-task

    **Task:**
    - Write the function `connectivity(g)`. It says how much of a network
      is still in one piece: the number of nodes in its largest connected
      group, divided by the number of nodes in the network.
    - Write the function `r_index(closed, connectivities)`. It turns a
      whole curve of connectivity into one number R: its average height.

    $$\text{connectivity} = \frac{\text{nodes in the largest group}}{\text{nodes in the network}},\qquad R = \frac{1}{T}\sum_{t=1}^{T} \text{connectivity}_t$$

    The last line closes the nodes of a real network one at a time, in a
    random order, until 60% are closed. It runs your connectivity after
    each closure, draws the curve, and shows your R. A closed node stays
    in the network with no edges. The grey band is what the network
    really did. Because closed nodes still count in the total, R is at
    most 0.7 over this range.

    **Other tools:**
    - `len(x)` gives the length of a list, and `max(x)` its largest number.
    - `np.mean(x)` gives the average of a list of numbers.
      `np.mean([0.4, 0.6, 1.0])` gives `0.666…`.

    The igraph calls are in [the walkthrough](https://molab.marimo.io/notebooks/nb_7hrZrDkZgWps8uHkfsuBA3), steps 2 and 8.
    ///
    """)
    return


@app.cell(hide_code=True)
def cp4_measure_work(np, plot_connectivity):
    # Libraries this cell uses. The notebook has imported them already;
    # in your own Python file, install them once and import them:
    #   import numpy as np   # pip install numpy==2.5.3

    def connectivity(g):
        # Return the share of g's nodes that are in its largest connected
        # group (one number between 0 and 1).
        # Steps: find the groups, take the size of the largest one, and
        #        divide it by the number of nodes in g.
        groups = g.connected_components()
        biggest = max(len(group) for group in groups)
        return biggest / g.vcount()

    def r_index(closed, connectivities):
        # `closed`: the share of nodes closed at each step (a list of numbers).
        # `connectivities`: the connectivity at each step (a list of numbers).
        # Return R: the average of `connectivities` (one number).
        return np.mean(connectivities)

    plot_connectivity(connectivity, r_index)
    return connectivity, r_index


@app.cell(hide_code=True)
def cp4_measure_note(mo):
    mo.md(r"""
    ### Connectivity, the robustness curve and R

    ```python
    def connectivity(g):
        groups = g.connected_components()
        return max(len(group) for group in groups) / g.vcount()

    def r_index(closed, connectivities):
        return np.mean(connectivities)
    ```

    **Connectivity** is the share of a network's nodes in its largest
    connected group. A whole network has connectivity $1$. A closed node
    stays in the network with no edges, so the total does not change.

    Running connectivity after every closure gives a **robustness curve**.
    The **R-index** is its average height:

    $$R = \frac{1}{T}\sum_{t=1}^{T} \text{connectivity}_t$$

    After closing a share $f$ of the nodes, connectivity is at most
    $1 - f$, so over the range $f = 0$ to $0.6$ the best case is $R = 0.7$,
    and a network that falls apart at once gives $R$ close to $0$. This
    network gives $R = 0.338$. A reported $R$ always comes with its range.
    """)
    return


@app.cell
def detour_r_hides_shape(mo, plt):
    import numpy as _np
    _x = _np.linspace(0, 0.6, 61)
    _gradual = 1 - _x            # falls steadily
    _sudden = _np.where(_x < 0.45, 1.0, 1 - (_x - 0.45) / 0.15 * 0.9)  # holds, then collapses
    _fig, _ax = plt.subplots(figsize=(6, 3.5))
    _ax.plot(_x, _gradual, color="#B14434", label="falls gradually")
    _ax.plot(_x, _sudden, color="#3959A6", label="holds, then collapses")
    _ax.set_xlabel("share closed")
    _ax.set_ylabel("connectivity")
    _ax.set_ylim(0, 1.05)
    _ax.legend()
    _ax.set_title("same R, different shapes")
    _fig.tight_layout()
    mo.vstack([
        mo.md(r"""### 🧭 Detour: the same R can hide very different curves

    R is the **average height** of the robustness curve, so it hides the shape.
    Two networks can share the same R while one falls gradually from the start
    and the other stays near 1 for a long time, then collapses suddenly."""),
        _fig,
    ])
    return


@app.cell
def cp5_grow_scratch(ig):
    # 🧪 Your space to try things out. Write any code here and run it.
    # Nothing in this cell is marked, and your tutor does not look at it.
    # Start your names with _ (like _small below): such a name belongs to
    # this cell only, so it never clashes with the exercise.
    _small = ig.Graph(n=3, edges=[(0, 1), (1, 2)])
    print(_small.degree())
    return


@app.cell(hide_code=True)
def cp5_grow_brief(mo):
    mo.md(r"""
    ### Exercise: grow a network by preferential attachment

    /// details | 📋 Task
        type: lh-task

    **Task:**
    - Start from 4 nodes, each linked to every other.
    - Add nodes one at a time until there are 2000.
    - Each new node links to $m = 3$ different nodes that are already
      there.
    - It picks node $i$ with probability $p_i = k_i / \sum_j k_j$, where
      $k_i$ is the degree of node $i$. A node with many edges is picked
      more often. This rule is called **preferential attachment**.

    The chart compares your network with two others of the same size:
    igraph's own Barabási–Albert network, and the same growth where each
    new node picks its nodes at random, ignoring degree.

    **Other tools:**
    - `x / x.sum()` divides every entry of the array `x` by the sum of
      all its entries. For `x = np.array([1, 3])`: `[0.25, 0.75]`.
    - `rng.choice(4, size=2, replace=False, p=[0.1, 0.2, 0.3, 0.4])`
      gives 2 different numbers from 0 to 3. Each number is drawn with
      the probability at its place in `p`.
    - `range(4, 10)` gives the numbers 4, 5, ..., 9, one per pass of the
      `for` loop.

    The igraph calls are in [the walkthrough](https://molab.marimo.io/notebooks/nb_7hrZrDkZgWps8uHkfsuBA3), steps 3 and 4.
    ///
    """)
    return


@app.cell(hide_code=True)
def cp5_grow_work(ig, np, plot_growth):
    # Libraries this cell uses. The notebook has imported them already;
    # in your own Python file, install them once and import them:
    #   import igraph as ig   # pip install igraph==1.0.0
    #   import numpy as np    # pip install numpy==2.5.3

    rng = np.random.default_rng(42)   # random numbers, the same on every run
    m = 3                             # the edges each new node arrives with

    # The network starts as 4 nodes, each linked to every other.
    pa = ig.Graph.Full(m + 1)

    # Nodes 4, 5, ..., 1999 arrive one at a time.
    for new in range(m + 1, 2000):
        # 1. `k_now`: the degree of every node now in pa (a numpy array).
        k_now = np.array(pa.degree())

        # 2. `p`: for each node now in pa, the probability that the new
        #    node links to it: its degree divided by the sum of all
        #    degrees (a numpy array, as long as k_now).
        p = k_now / k_now.sum()

        # 3. `targets`: m different nodes of pa, drawn at random with the
        #    probabilities in p (a numpy array of m node numbers).
        targets = rng.choice(
            pa.vcount(),
            size=m,
            replace=False,
            p=p
        )

        # 4. Add the new node to pa. It gets the number `new`.
        #    Then add one edge from `new` to each node in targets.
        pa.add_vertices(1)
        pa.add_edges([(new, int(target)) for target in targets])

    print(pa.vcount(), "nodes and", pa.ecount(), "edges")
    plot_growth(pa)
    return (pa,)


@app.cell(hide_code=True)
def cp5_grow_note(mo):
    mo.md(r"""
    ### Preferential attachment, written by hand

    ```python
    rng = np.random.default_rng(42)
    m = 3
    pa = ig.Graph.Full(m + 1)
    for new in range(m + 1, 2000):
        k_now = np.array(pa.degree())
        p = k_now / k_now.sum()
        targets = rng.choice(pa.vcount(), size=m, replace=False, p=p)
        pa.add_vertices(1)
        pa.add_edges([(new, t) for t in targets])
    ```

    Each new node links to node $i$ with probability
    $p_i = k_i / \sum_j k_j$. This is **preferential attachment**: a node
    that already has many edges is more likely to get the next one. It is
    the rule of the **Barabási–Albert model**, and `ig.Graph.Barabasi(2000, 3)`
    grows the same kind of network.

    The oldest nodes had the most time to collect edges, so they become
    the hubs: in a network of 2000 nodes the largest degree is above 100.
    When each new node picks at random instead, the largest degree is
    about 26, and there are no hubs.
    """)
    return


@app.cell
def detour_growth_vs_preferential(mo, pa, plt):
    import numpy as _np
    _k = _np.array(pa.degree())
    _fig, _ax = plt.subplots(figsize=(6, 3.5))
    _ax.scatter(_np.arange(pa.vcount()), _k, s=4, color="#3959A6", alpha=0.5)
    _ax.set_xlabel("node number (order it arrived)")
    _ax.set_ylabel("degree")
    _ax.set_title("old nodes (small numbers) hold the most edges")
    _fig.tight_layout()
    mo.vstack([
        mo.md(r"""### 🧭 Detour: growth and preferential attachment work together

    In the Barabási–Albert model, two rules act at once. **Growth** means nodes
    arrive one at a time, so some nodes are older than others. **Preferential
    attachment** means a node with more edges is more likely to be picked next.

    Each node's number is the order it arrived. Older nodes — the small numbers —
    had more chances to be picked, and their early lead grew because the rich get
    richer. That is why the big degrees sit on the left."""),
        _fig,
    ])
    return


@app.cell
def cp6_powerlaw_scratch(ig):
    # 🧪 Your space to try things out. Write any code here and run it.
    # Nothing in this cell is marked, and your tutor does not look at it.
    # Start your names with _ (like _small below): such a name belongs to
    # this cell only, so it never clashes with the exercise.
    _small = ig.Graph(n=3, edges=[(0, 1), (1, 2)])
    print(_small.degree())
    return


@app.cell(hide_code=True)
def cp6_powerlaw_brief(mo):
    mo.md(r"""
    ### Exercise: the degree distribution of a network with hubs

    /// details | 📋 Task
        type: lh-task

    **Task:**
    - Build a Barabási–Albert network. In it, nodes arrive one at a time,
      and each new node links to existing nodes, preferring nodes that
      already have many edges.
    - Find the degree of every node.
    - For each degree, find the share of nodes whose degree is at least
      that value.
    - Read the power-law exponent $\alpha$ from the slope of a straight
      line on the log-log plot.
    - Estimate $\alpha$ again with the `powerlaw` package.

    For this model, $\alpha$ should come out close to 3.

    When the share of nodes with degree $k$ falls like
    $p(k) \propto k^{-\alpha}$, the share of nodes with degree **at least**
    $k$ falls like $k^{-(\alpha - 1)}$. On a log-log plot that is a
    straight line with slope $1 - \alpha$.

    A straight line through the plot is a first look. The `powerlaw`
    package estimates $\alpha$ in a more reliable way, by maximum
    likelihood, following [Clauset, Shalizi and Newman (2009), "Power-law
    distributions in empirical data"](https://arxiv.org/abs/0706.1062).
    Use it on the tail, degrees 10 and above, where the power law holds.

    **Other tools:**
    - `(x >= 2).mean()` gives the share of entries of the array `x` that
      are at least 2. For `x = np.array([1, 2, 3, 4])`: `0.75`.
    - `np.array([f(v) for v in [1, 2, 3]])` makes an array with one value
      of `f(v)` for each `v`.
    - `np.log(x)` gives the natural log of every entry.
    - `np.polyfit(x, y, 1)` fits a straight line to the points and gives
      `[slope, intercept]`. `np.polyfit([0, 1, 2], [1, 3, 5], 1)` gives
      `[2.0, 1.0]`.
    - `powerlaw.Fit(x, discrete=True, xmin=5)` fits a power law to the
      whole numbers in `x`, using only values of 5 and above.
    - `fit.power_law.alpha` gives the exponent of that fit, one number.

    The igraph calls are in [the walkthrough](https://molab.marimo.io/notebooks/nb_7hrZrDkZgWps8uHkfsuBA3), steps 4, 9 and 10.
    ///
    """)
    return


@app.cell(hide_code=True)
def cp6_powerlaw_work(ig, np, plot_ccdf, powerlaw):
    # Libraries this cell uses. The notebook has imported them already;
    # in your own Python file, install them once and import them:
    #   import igraph as ig   # pip install igraph==1.0.0
    #   import numpy as np    # pip install numpy==2.5.3
    #   import powerlaw       # pip install powerlaw==2.0.0

    # 1. `ba`: a Barabási–Albert network with 2000 nodes, where each new
    #    node arrives with 3 edges.
    ba = ig.Graph.Barabasi(n=2000, m=3)

    # 2. `k`: the degree of every node in ba, as a numpy array.
    k = np.array(ba.degree())

    # 3. `ks`: every different degree in k, from smallest to largest
    #    (a numpy array).
    #    `ccdf`: for each value in ks, the share of nodes whose degree is at
    #    least that value (a numpy array, as long as ks).
    ks = np.unique(k)
    ccdf = np.array([np.mean(k >= degree) for degree in ks])

    # 4. `slope`: the slope of the straight line that best fits log(ccdf)
    #    against log(ks) (one number).
    #    `alpha`: the power-law exponent of the degree distribution
    #    (one number).
    slope = np.polyfit(np.log(ks), np.log(ccdf), 1)[0]

    # For p(k) ~ k^(-alpha), CCDF ~ k^(1-alpha).
    alpha = 1 - slope

    # 5. `fit`: a power-law fit of the degrees in k by the powerlaw package,
    #    using only degrees of 10 and above — the tail, where the power law
    #    holds.
    #    `alpha_fit`: the exponent this fit gives (one number).
    fit = powerlaw.Fit(k, xmin=10, discrete=True, verbose=False)
    alpha_fit = fit.power_law.alpha

    print("alpha from the slope:   ", alpha)
    print("alpha from powerlaw.Fit:", alpha_fit)
    plot_ccdf(ks, ccdf, alpha, alpha_fit)
    return (ba,)


@app.cell(hide_code=True)
def cp6_powerlaw_note(mo):
    mo.md(r"""
    ### The degree distribution of a Barabási–Albert network

    ```python
    ba = ig.Graph.Barabasi(2000, 3)
    k = np.array(ba.degree())
    ks = np.unique(k)
    ccdf = np.array([(k >= x).mean() for x in ks])
    slope = np.polyfit(np.log(ks), np.log(ccdf), 1)[0]
    alpha = 1 - slope      # about 3.1

    fit = powerlaw.Fit(k, discrete=True, xmin=10)
    alpha_fit = fit.power_law.alpha   # about 3.0
    ```

    In a Barabási–Albert network, each new node links to nodes that
    already have many edges more often than to nodes with few. The degree
    distribution then follows a **power law**,
    $p(k) \propto k^{-\alpha}$, with $\alpha = 3$.

    The share of nodes with degree **at least** $k$ follows
    $k^{-(\alpha-1)}$, a straight line of slope $1 - \alpha$ on log-log
    axes. It is much less noisy than the plain distribution: with 2000
    nodes, fitting the plain distribution gives an exponent between 2.2
    and 2.8, while the cumulative one gives about 3.

    A straight line fitted to a log-log plot is a first look, not an
    estimate to report. `powerlaw.Fit` estimates $\alpha$ by **maximum
    likelihood**, from the degrees at or above a lower cut-off
    $k_{\min}$. The power law describes the tail, so the cut-off matters:
    with $k_{\min} = 10$ it gives about 3.0, and if the package is left to
    pick a low $k_{\min}$ on 2000 nodes it gives about 2.6 to 2.7.

    The method, and why a straight line on a log-log plot is not enough, is
    in [Clauset, Shalizi and Newman (2009), "Power-law distributions in
    empirical data", *SIAM Review* 51(4)](https://arxiv.org/abs/0706.1062).
    """)
    return


@app.cell
def detour_tail_fit(ba, mo, plt):
    import numpy as _np
    _k = _np.array(ba.degree())
    _ks = _np.unique(_k)
    _ccdf = _np.array([(_k >= x).mean() for x in _ks])
    _tail = _ks >= 10
    _fig, _ax = plt.subplots(figsize=(6, 3.5))
    _ax.loglog(_ks[~_tail], _ccdf[~_tail], "o", color="#DAB167", label="low degrees (bend)")
    _ax.loglog(_ks[_tail], _ccdf[_tail], "o", color="#3959A6", label="tail k ≥ 10 (straight)")
    _ax.set_xlabel("degree k")
    _ax.set_ylabel("share with degree ≥ k")
    _ax.set_title("the tail is the straight part")
    _ax.legend()
    _fig.tight_layout()
    mo.vstack([
        mo.md(r"""### 🧭 Detour: why fit the tail?

    A power law describes the **large-degree tail**. At low degrees the curve
    bends away from a straight line — the minimum degree, the early growth, and
    finite size all leave their mark there. Including those low degrees drags the
    fitted slope away from the true exponent, so fitting only the tail
    ($k \ge 10$) gives the cleaner estimate."""),
        _fig,
    ])
    return


@app.cell
def cp7_robust_scratch(ig):
    # 🧪 Your space to try things out. Write any code here and run it.
    # Nothing in this cell is marked, and your tutor does not look at it.
    # Start your names with _ (like _small below): such a name belongs to
    # this cell only, so it never clashes with the exercise.
    _small = ig.Graph(n=3, edges=[(0, 1), (1, 2)])
    print(_small.degree())
    return


@app.cell(hide_code=True)
def cp7_robust_brief(mo):
    mo.md(r"""
    ### Exercise: how robust is a network with hubs?

    /// details | 📋 Task
        type: lh-task

    **Task:**
    - Write the function `kappa(g)`. kappa says how uneven the degrees of
      a network are: it is large when a few nodes have far more edges
      than the rest.
    - Write the function `f_c(kappa_value)`. f_c is the share of nodes
      that, closed at random, breaks the network apart.
    - Use both functions on your Barabási–Albert network `ba` and on the
      random network `er_net`.

    **Other tools:**
    - Arithmetic on a numpy array works on every entry at once:
      `np.array([1, 2, 3]) * 10` gives `[10, 20, 30]`, and
      `np.array([1, 2, 3]) + 1` gives `[2, 3, 4]`.
    - `np.mean(x)` gives the average. `np.mean([1, 2, 6])` gives `3.0`.

    The igraph calls are in [the walkthrough](https://molab.marimo.io/notebooks/nb_7hrZrDkZgWps8uHkfsuBA3), step 4.
    ///
    """)
    return


@app.cell
def cp7_robust_work(ba, connectivity, er_net, np, plot_robustness, r_index):
    # Libraries this cell uses. The notebook has imported them already;
    # in your own Python file, install them once and import them:
    #   import numpy as np   # pip install numpy==2.5.3

    def kappa(g):
        # `k`: the degree of every node in g, as a numpy array.
        k = np.array(g.degree())

        # Return kappa = <k^2> / <k>.
        return np.mean(k**2) / np.mean(k)


    def f_c(kappa_value):
        # Critical fraction for random node removal.
        return 1 - 1 / (kappa_value - 1)


    # `ba` is your network from the last exercise. `er_net` is a random
    # network with the same number of nodes and almost the same number of
    # edges.

    kappa_ba = kappa(ba)
    fc_ba = f_c(kappa_ba)

    kappa_er = kappa(er_net)
    fc_er = f_c(kappa_er)

    print("BA network:     kappa =", kappa_ba, " f_c =", fc_ba)
    print("random network: kappa =", kappa_er, " f_c =", fc_er)

    plot_robustness(ba, er_net, fc_ba, fc_er, connectivity, r_index)
    return f_c, fc_ba, fc_er, kappa, kappa_ba, kappa_er


@app.cell(hide_code=True)
def cp7_robust_check(
    ba,
    check_robust,
    f_c,
    fc_ba,
    fc_er,
    kappa,
    kappa_ba,
    kappa_er,
):
    check_robust(ba, kappa, f_c, kappa_ba, fc_ba, kappa_er, fc_er)
    return


@app.cell(hide_code=True)
def cp7_robust_send(mo):
    cp7_robust_send = mo.ui.run_button(label="Submit to Tutor")
    cp7_robust_send
    return (cp7_robust_send,)


@app.cell(hide_code=True)
def cp7_robust_sent(cp7_robust_send, mo):
    from pathlib import Path as _P
    if cp7_robust_send.value:
        _P("session_artifacts").mkdir(exist_ok=True)
        with open("session_artifacts/student_signal.txt", "a") as _f:
            _f.write("cp7_robust_work" + "\n")
    mo.md(
        "<span style='color:#6A6D75;font-size:13px'>*Submit to Tutor hands "
        "this cell in; your tutor answers in the terminal.*</span>"
    )
    return


@app.cell(hide_code=True)
def cp7_robust_note(mo):
    mo.md(r"""
    ### Kappa, the critical threshold, and a network with hubs

    ```python
    def kappa(g):
        k = np.array(g.degree())
        return np.mean(k ** 2) / np.mean(k)

    def f_c(kappa_value):
        return 1 - 1 / (kappa_value - 1)
    ```

    $$\kappa = \frac{\langle k^2 \rangle}{\langle k \rangle},\qquad f_c = 1 - \frac{1}{\kappa - 1}$$

    Both come from the degrees alone, without closing a single node. The
    BA network and the random network have almost the same average degree,
    but the BA network's hubs make $\langle k^2 \rangle$, and so $\kappa$,
    about twice as large. Its $f_c$ is larger too: under random closure, a
    network with hubs holds together longer.

    The formula for $f_c$ is exact only for an infinite random network, so
    on 2000 nodes it gives the size of the answer, not its decimals.
    Closing the busiest nodes first is called a targeted attack. It breaks
    a network with hubs much sooner, and the lecture note covers it.
    """)
    return


@app.cell
def detour_targeted_attack(ba, er_net, mo, plt):
    import numpy as _np

    def _connectivity(_g):
        return max(len(c) for c in _g.connected_components()) / _g.vcount()

    def _curve_random(_g, n):
        _g2 = _g.copy()
        _order = _np.random.default_rng(0).permutation(_g.vcount())
        _out = []
        for _i, _v in enumerate(_order):
            _g2.delete_edges(_g2.incident(_v))
            if (_i + 1) % (n // 40) == 0:
                _out.append(((_i + 1) / _g.vcount(), _connectivity(_g2)))
        return _out

    def _curve_targeted(_g, n):
        _g2 = _g.copy()
        _out = []
        for _i in range(n):
            _v = _np.argmax(_np.array(_g2.degree()))
            _g2.delete_edges(_g2.incident(_v))
            if (_i + 1) % (n // 40) == 0:
                _out.append(((_i + 1) / _g.vcount(), _connectivity(_g2)))
        return _out

    _fig, _ax = plt.subplots(figsize=(6, 3.5))
    for _g, _lab, _col in [(ba, "BA", "#3959A6"), (er_net, "random", "#B14434")]:
        _x, _y = zip(*_curve_targeted(_g, 200))
        _ax.plot(_x, _y, color=_col, label=f"{_lab} targeted", linestyle="--")
        _x, _y = zip(*_curve_random(_g, 200))
        _ax.plot(_x, _y, color=_col, label=f"{_lab} random", linestyle="-")
    _ax.set_xlabel("share closed")
    _ax.set_ylabel("connectivity")
    _ax.set_title("targeted vs random removal")
    _ax.legend(fontsize=8)
    _fig.tight_layout()
    mo.vstack([
        mo.md(r"""### 🧭 Detour: targeted attack flips the story

    The hubs hold the BA network together. Remove the **highest-degree** nodes
    first (targeted) and it collapses almost at once — far sooner than random
    removal. The random network has no hubs to aim at, so it barely notices the
    difference."""),
        _fig,
    ])
    return


@app.cell(hide_code=True)
def session_record(mo):
    mo.md(r"""
    ## 📋 Session record

    *Your answer to each question, and every word you typed while working on*
    *it — this is what gets reviewed, not the code. Hints are never held*
    *against you.*

    **cp0_walkthrough** · pass

    *Work through the igraph walkthrough and come back when every step shows ✅.*

    > Finished. Please proceed.

    *You typed:* "I can see it" · "Finished. Please proceed."

    *Tutor's note:* They worked through the walkthrough and reported finishing it.

    **cp1_build** · pass

    *Build the network, ask it its size, make and edit a copy, and find the new number of the node that was node 2.*

    > (no answer — the code is their answer)

    *Tutor's note:* They filled every blank correctly first time: built g, asked it its size with vcount/ecount, copied and edited it, and named was_2_now = 1.

    **cp2_matrix** · pass

    *Write the network as an adjacency matrix, sum its rows, ask g for degrees, and find the mean degree.*

    > (no answer — the code is their answer)

    *You typed:* "Yes. Since igraph vertex numbers are positions and can change after deleting a vertex, what is the usual way to preserve a node’s original identity when we need stable labels across edits? Would we store an attribute such as a name or ID on each vertex?" · "That makes sense. I am ready to move on."

    *Tutor's note:* They built the adjacency matrix, summed its rows, asked g for its degrees, and averaged them — every blank right first time.

    **cp3_paths** · pass

    *List every route from 0 to 6, pick a shortest, count its edges, cut node 4, and measure the pieces.*

    > (no answer — the code is their answer)

    *You typed:* "Since adjacency matrices become very inefficient for large sparse networks, is igraph internally using something closer to adjacency lists or another sparse representation when methods like g.degree() are called?" · "Makes sense. I am ready to move on."

    *Tutor's note:* They listed all routes, picked the [0] shortest route, counted hops as len−1, cut node 4's edges on a copy, and measured the largest component — every blank right first time.

    **cp4_measure** · pass

    *Write connectivity(g) and r_index(closed, connectivities).*

    > (no answer — the code is their answer)

    *You typed:* "Since every path from nodes on the left to nodes 5 and 6 goes through node 4, would node 4 be considered an articulation point? And is removing all of its incident edges equivalent to deleting the vertex when we are measuring connectivity, except that the isolated node itself remains?" · "Makes sense. Let's move on."

    *Tutor's note:* They wrote connectivity as largest group over vcount and r_index as np.mean of connectivities — both right first time, curve on the band.

    **cp5_grow** · pass

    *Grow a 2000-node network by preferential attachment.*

    > (no answer — the code is their answer)

    *You typed:* "If two networks have the same R-index, could they still have very different robustness behavior? For example, one failing gradually and another staying connected for a long time and then collapsing suddenly?" · "Great. let's move on..."

    *Tutor's note:* They wrote the full preferential-attachment loop first time: degree array, probabilities, rng.choice without replacement, then add the node and its edges.

    **cp6_powerlaw** · pass

    *Build a Barabási–Albert network and read its power-law exponent two ways.*

    > (no answer — the code is their answer)

    *You typed:* "Does preferential attachment alone explain the heavy-tailed degree distribution, or is the fact that nodes enter at different times also important because older nodes have had more opportunities to collect edges?" · "thanks. ready to move on."

    *Tutor's note:* They built ba, computed the cumulative degree share, read alpha as 1 − slope, and fitted powerlaw on degrees 10 and up — all correct first time.

    **cp7_robust** · pass

    *Write kappa and f_c, and use them on ba and er_net.*

    > (no answer — the code is their answer)

    *You typed:* "Why is fitting only the tail generally more reliable for estimating the power-law exponent? Is it because the low-degree part of the distribution does not follow the asymptotic power-law behavior very closely?" · "That makes sense. So the low-degree region reflects finite-size and growth effects, while the tail is the part that more closely follows the asymptotic power-law behavior. Lets ready to move on."

    *Tutor's note:* They wrote kappa as mean of k squared over mean k and f_c as 1 − 1/(kappa−1), then applied both to ba and er_net — every blank right first time.

    ### 🧭 Your own questions (7)

    - *Since igraph vertex numbers are positions and can change after deleting a vertex, what is the usual way to preserve a node's original identity when we need stable labels across edits? Would we store an attribute such as a name or ID on each vertex?*
    - *Since adjacency matrices become very inefficient for large sparse networks, is igraph internally using something closer to adjacency lists or another sparse representation when methods like g.degree() are called?*
    - *Since every path from nodes on the left to nodes 5 and 6 goes through node 4, would node 4 be considered an articulation point? And is removing all of its incident edges equivalent to deleting the vertex when we are measuring connectivity, except that the isolated node itself remains?*
    - *If two networks have the same R-index, could they still have very different robustness behavior? For example, one failing gradually and another staying connected for a long time and then collapsing suddenly?*
    - *Does preferential attachment alone explain the heavy-tailed degree distribution, or is the fact that nodes enter at different times also important because older nodes have had more opportunities to collect edges?*
    - *Why is fitting only the tail generally more reliable for estimating the power-law exponent? Is it because the low-degree part of the distribution does not follow the asymptotic power-law behavior very closely?*
    - *Since the BA network is more robust to random deletion because most randomly selected nodes are low-degree nodes, would the opposite happen under targeted deletion, where we always remove the highest-degree node first? Would its robustness then become substantially worse than the random network?*
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

    - Each exercise is a code cell with blanks marked `___`. Replace each blank with your code, then run the cell.
    - Before the first exercise, work through [the igraph walkthrough](https://molab.marimo.io/notebooks/nb_7hrZrDkZgWps8uHkfsuBA3). It shows every igraph call the exercises use.
    - The comments in the cell say what goes into each variable. **📋 Task** above the cell opens the task, and says which steps of the walkthrough to use.
    - Run the cell as often as you like. When you want your tutor to look, press **Submit to Tutor** under the cell.
    - The 🧪 cell above each exercise is yours to try things in. Nothing in it is marked.

    **One rule of marimo:** a variable name can be given a value in only one cell. Each exercise uses its own names (`g`, `edited`, `cut`, and so on). In the 🧪 cell, start your names with `_`, like `_small`: such a name belongs to that cell only.
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
    import powerlaw
    import seaborn as sns
    import warnings

    # powerlaw's optimiser warns on every fit ("Initial guess is not within
    # the specified bounds"). It is not the student's to act on, and it would
    # print under their cell every time they run it.
    warnings.filterwarnings("ignore", message="Initial guess is not within")

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
            #
            # The MAP is the one figure that turns it off (see london_map):
            # 430 sketched rail links on top of 36 sketched borough outlines
            # reads as static, and a map's job is to be recognised as London.
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
    return np, plt, powerlaw


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
    # but the exercise in hand. The names below are the ones every exercise
    # calls, and the fold opens with one click when a student goes looking.
    #
    #   draw_net(g), plot_connectivity(...), plot_growth(...), plot_ccdf(...), plot_robustness(...)
    #       what the last line of an exercise calls: each draws what YOUR
    #       code produced, and judges nothing.
    #   check_build, check_matrix, check_paths, check_measure,
    #   check_grow, check_powerlaw, check_robust
    #       the checks. Each runs in a hidden cell under your exercise and
    #       tells your tutor, not you, whether your code does the task —
    #       your tutor reads it when you press Submit to Tutor.
    #   protect(g)
    #       makes g refuse to change, so the exercises after the first can
    #       only change a copy of it.
    #   N_NODES, EDGES
    #       the seven-node network chapters 1 and 2 are built on.
    #   ___
    #       every blank in every exercise. Running a cell before you have
    #       filled one in says so, in those words.
    from bench import (
        ___,
        EDGES,
        N_NODES,
        check_build,
        check_grow,
        check_matrix,
        check_measure,
        check_paths,
        check_powerlaw,
        check_robust,
        draw_net,
        plot_ccdf,
        plot_connectivity,
        plot_growth,
        plot_robustness,
        protect,
    )

    return (
        check_robust,
        draw_net,
        plot_ccdf,
        plot_connectivity,
        plot_growth,
        plot_robustness,
        protect,
    )


@app.cell(hide_code=True)
def _(ig, np):
    # tutor:plumbing — kept below the lesson; see the note above.
    # ── The data ─────────────────────────────────────────────────────────
    # Read from assets/, never generated. Note cells quote exact numbers —
    # "42 of 369", "kappa = 16.4", "R = 0.223" — and a network drawn fresh
    # each session would make those sentences false. tools/build_assets.py
    # is what produces these files, and plan.md section 2 records what they
    # measure.
    import csv as _csv
    import json as _json
    from pathlib import Path as _Path

    _A = _Path("assets")

    def _read_links(path, n=None):
        pairs = [
            (int(r["source"]), int(r["target"]))
            for r in _csv.DictReader(open(path))
        ]
        size = n if n is not None else max(max(p) for p in pairs) + 1
        return ig.Graph(n=size, edges=pairs)

    _stations = list(_csv.DictReader(open(_A / "london" / "stations.csv")))
    station_names = [r["name"] for r in _stations]
    station_lon = np.array([float(r["lon"]) for r in _stations])
    station_lat = np.array([float(r["lat"]) for r in _stations])
    borough_rings = _json.loads((_A / "london" / "boroughs.json").read_text())
    # The order London closes in, and the curve that order produces. Chapter
    # 3's slider walks along the order; check_measure() marks the student's
    # own function against the curve. Same event, two views of it.
    breaking = _json.loads((_A / "london" / "breaking.json").read_text())
    reference_R = _json.loads((_A / "reference_attacks.json").read_text())
    synthetic_meta = _json.loads((_A / "synthetic" / "meta.json").read_text())

    london = _read_links(_A / "london" / "links.csv", n=len(_stations))
    er_net = _read_links(_A / "synthetic" / "er.csv", n=synthetic_meta["er"]["n"])
    airline_net = _read_links(
        _A / "synthetic" / "airline.csv", n=synthetic_meta["airline"]["n"]
    )
    return (
        borough_rings,
        er_net,
        london,
        station_lat,
        station_lon,
        station_names,
    )


@app.cell(hide_code=True)
def _(borough_rings, london, np, plt, station_lat, station_lon, station_names):
    # tutor:plumbing — kept below the lesson; see the note above.
    # ── The map ──────────────────────────────────────────────────────────
    # The module's reward image, and the only picture in it that is a place.
    #
    # Two styles, because the map does two different jobs:
    #   "pieces" — every surviving group its own colour. Shows FRAGMENTATION.
    #              cp7's reward image, where the count of pieces is the shock.
    #   "giant"  — blue is the largest surviving group, amber everything cut
    #              off from it. Shows the MEASURE: the blue fraction is
    #              exactly the number every chart in this module plots.
    # Blue means the same thing in both, and the same thing as in the charts.
    MAP_BLUE, MAP_AMBER, MAP_DUST, MAP_CLOSED, MAP_PAPER = (
        "#3959A6", "#DAB167", "#CFC8B8", "#9A9388", "#FFFDF7",
    )
    # Eight more hues for "pieces". They are not the lecture palette (it has
    # three accents and this needs twelve); they are chosen to sit at the
    # same weight so no fragment shouts louder than another.
    MAP_PIECES = [
        "#B14434", "#DAB167", "#2E6E5B", "#7B5EA7", "#C9762F", "#4B86C4",
        "#8C6E4A", "#B8567F", "#5E8C3A", "#A8478E", "#D08A5A", "#3E7E8C",
    ]

    def london_map(closed=(), style="giant", title=None, ax=None):
        """Draw London with `closed` stations shut. Returns the figure.

        closed: station ids (ints) or names (str).
        style:  "giant" (blue = still in one piece) or "pieces" (one colour
                per surviving group).
        """
        from matplotlib.collections import LineCollection

        ids = set()
        for c in closed:
            ids.add(c if isinstance(c, (int, np.integer)) else station_names.index(c))
        n = london.vcount()
        alive = [i for i in range(n) if i not in ids]
        sub = london.subgraph(alive)
        comps = sub.connected_components()
        sizes = [len(c) for c in comps]
        biggest = int(np.argmax(sizes)) if sizes else -1
        member = np.full(n, -1)
        for ci, comp in enumerate(comps):
            for v in comp:
                member[alive[v]] = ci

        if style == "pieces":
            rank = {ci: r for r, ci in enumerate(np.argsort(-np.array(sizes)))}

            def colour(ci):
                if ci == biggest:
                    return MAP_BLUE
                r = rank[ci] - 1
                return MAP_PIECES[r] if r < len(MAP_PIECES) else MAP_DUST
        else:
            def colour(ci):
                return MAP_BLUE if ci == biggest else MAP_AMBER

        made = ax is None
        if made:
            fig, ax = plt.subplots(figsize=(7.4, 5.6))
        else:
            fig = ax.figure
        # A map is recognised, not felt: the hand-drawn line that suits a
        # 6-point chart turns 430 rail links into noise at this density.
        with plt.rc_context({"path.sketch": None}):
            for ring in borough_rings:
                pts = np.asarray(ring)
                ax.plot(pts[:, 0], pts[:, 1], lw=0.6, color="#E6E1D4", zorder=0)
            live_links = [
                (a, b)
                for a, b in london.get_edgelist()
                if a not in ids and b not in ids
            ]
            ax.add_collection(
                LineCollection(
                    [
                        [(station_lon[a], station_lat[a]), (station_lon[b], station_lat[b])]
                        for a, b in live_links
                    ],
                    colors=[colour(member[a]) for a, _ in live_links],
                    linewidths=1.5,
                    alpha=0.75,
                    zorder=1,
                )
            )
            if ids:
                shut = sorted(ids)
                ax.scatter(
                    station_lon[shut], station_lat[shut],
                    s=40, marker="x", c=MAP_CLOSED, linewidths=1.1, zorder=2,
                )
            ax.scatter(
                station_lon[alive], station_lat[alive],
                s=[22 if member[i] == biggest else 13 for i in alive],
                c=[colour(member[i]) for i in alive],
                edgecolors=MAP_PAPER, linewidths=0.55, zorder=3,
            )
        # London is at 51.5°N, so a degree of longitude is only cos(51.5) of
        # a degree of latitude. Without this the city comes out stretched.
        ax.set_aspect(1 / np.cos(np.radians(51.5)))
        ax.axis("off")
        ax.set_facecolor(MAP_PAPER)
        if title is None:
            big = sizes[biggest] if sizes else 0
            title = (
                f"{len(ids)} stations closed  ·  largest piece {big}/{n} "
                f"= {big / n:.2f}  ·  {len(comps)} pieces"
            )
        ax.set_title(title, fontsize=11)
        if made:
            fig.tight_layout()
        return fig

    return


@app.cell(hide_code=True)
def _(alt, pd):
    # tutor:plumbing — kept below the lesson; see the note above.
    # ── The curve ────────────────────────────────────────────────────────
    # x: how much of the network has been closed. y: how much of it is still
    # in one piece. Every chart in this module is this chart.
    CURVE_COLOUR = {
        "your attack": "#B14434",     # what THIS figure is about
        "random closures": "#6A6D75",  # the floor
        "benchmark": "#DAB167",        # the comparison object
        "airline network": "#B14434",
        "random network": "#3959A6",
    }

    def robustness_curve(series, title=None, height=250):
        """series: {label: (xs, ys)} — fractions closed, fractions surviving."""
        rows = [
            {"label": label, "closed": float(x), "surviving": float(y)}
            for label, (xs, ys) in series.items()
            for x, y in zip(xs, ys)
        ]
        order = list(series)
        chart = (
            alt.Chart(pd.DataFrame(rows))
            .mark_line()
            .encode(
                x=alt.X("closed:Q", title="fraction of stations closed",
                        axis=alt.Axis(format="%")),
                y=alt.Y("surviving:Q", title="fraction still in one piece",
                        scale=alt.Scale(domain=[0, 1])),
                # The domain MUST be bound: without it Vega sorts the labels
                # and hands "your attack" somebody else's colour.
                color=alt.Color(
                    "label:N",
                    title=None,
                    scale=alt.Scale(
                        domain=order,
                        range=[CURVE_COLOUR.get(k, "#22336B") for k in order],
                    ),
                    legend=alt.Legend(orient="top-right"),
                ),
            )
            .properties(height=height, width="container")
        )
        return chart.properties(title=title) if title else chart

    return


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
