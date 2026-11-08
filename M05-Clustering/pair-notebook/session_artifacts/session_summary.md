# Session summary

Module: m05-community-detection v1.0.0
Checkpoints completed: 8 of 8
Detours (student's own questions): 8

## cp1_graph — pass (0 hints)
Question: Build the airport network, count its nodes and edges, and find the largest degree and the airport with that degree.
Answer (verbatim): (no answer — the code is their answer)
Typed by the student: ["Yes i can see it"]
Tutor's note: Built g with n=len(codes) and edges=route_list, counted with vcount/ecount, found k_max with max(g.degree()) and hub via g.degree().index(k_max) into codes — all four steps first time.

## cp2_leiden — pass (0 hints)
Question: Find groups with Leiden using modularity, and save the group list, the number of groups, and the modularity.
Answer (verbatim): (no answer — the code is their answer)
Typed by the student: ["The result makes sense. Since degree counts the number of routes connected to an airport, AMS being the highest-degree node means it acts as the largest hub in this network. I also notice that the average degree is only about 11 while AMS has 246 routes, so the degree distribution seems highly uneven. Would this kind of hub structure make the airport network more robust to random airport failures but more vulnerable if the highest-degree hubs were deliberately removed?","That makes sense. So the same degree heterogeneity that gives the network robustness to random failures also creates vulnerability to targeted hub removal. I’m ready to move on."]
Tutor's note: Set objective_function="modularity", took .membership for groups, used len(leiden) for n_groups (equivalent to len(set(groups))), and g.modularity(groups) — all first time.

## cp3_nmi — pass (0 hints)
Question: Write nmi(a, b) from the lecture's definition, with the last line printing 1.0 and 0.0.
Answer (verbatim): (no answer — the code is their answer)
Typed by the student: ["The modularity is about 0.67, which seems fairly high, and the detected groups also look geographically clustered on the map. Does that mean the airport network’s community structure is driven mainly by regional connections, while the long-distance international routes act mostly as links between those communities? Also, since Leiden is stochastic and the number of groups can change slightly between runs, should I think of the exact 17 groups as less important than the overall modularity and the stability of the larger regional communities?","Letsmove on"]
Tutor's note: Wrote nmi from the table of counts: np.unique with return_inverse for ia/ib, np.add.at to fill the table, axis sums for p_a/p_b, filtered entropies with p>0, and mutual information via p_a[:,None]*p_b[None,:] outer products, then 2*mi/(h_a+h_b). Used outer-product indexing rather than np.outer — same result.

## cp4_ari — pass (0 hints)
Question: Write ari(a, b) from the lecture's definition, with the last line printing 1.0 and a negative number.
Answer (verbatim): (no answer — the code is their answer)
Typed by the student: ["I think I understand why relabeling does not affect NMI: the labels themselves are arbitrary, and NMI only depends on how many nodes fall into each overlap between the two partitions. So two partitions can use completely different numerical labels but still have NMI = 1 if they divide the nodes in exactly the same way. Is that also why NMI is useful for comparing two different runs of Leiden?","Lets move on"]
Tutor's note: Wrote ari from the same table: pairs = x*(x-1)/2, both = pairs(table).sum(), in_a and in_b from pairs of the row and column sums, expected = in_a*in_b/pairs(n), and the ARI formula. All steps first time.

## cp5_compare — pass (0 hints)
Question: Find groups with Infomap and score Leiden against continents and countries, and Infomap against countries, with nmi and ari.
Answer (verbatim): (no answer — the code is their answer)
Typed by the student: ["Since ARI corrects for agreement expected by chance, is that the main reason it is usually more informative than simply measuring the fraction of node pairs that the two partitions classify the same way?","That makes sense. So ARI measures agreement beyond chance, with 1 indicating identical groupings and values near 0 indicating roughly chance-level agreement. I’m ready to move on.","I accidentaly closed my notebook and browser"]
Tutor's note: Found Infomap groups with g.community_infomap().membership and wrote all six scores with the correct argument pairs: nmi/ari of groups vs continent, groups vs country, and info_groups vs country. All steps first time.

## cp6_sbm — pass (0 hints)
Question: Write sample_sbm(P, z) that links each pair with probability P[z[i]][z[j]], and build a network from the Leiden groups.
Answer (verbatim): (no answer — the code is their answer)
Typed by the student: ["The results seem to suggest that Leiden captures broader geographic structure better, since its communities align quite well with continents, while Infomap produces many smaller groups and matches countries more closely. I’m also noticing that NMI and ARI do not give exactly the same relative strength of agreement. Is that because NMI and ARI respond differently to the number and sizes of communities, especially when Infomap produces as many as 124 groups?","Move on"]
Tutor's note: Built p with P[z[:,None], z[None,:]] (fancy indexing for the same n-by-n block-probability table), linked with np.random.random((n,n)) < p, kept i<j with np.triu(k=1), and returned ig.Graph from zip(rows, cols). All steps first time.

## cp7_hubs — pass (0 hints)
Question: Find the largest degree of the real and block-model networks, and the correlation of their degree lists.
Answer (verbatim): (no answer — the code is their answer)
Typed by the student: ["The block model seems to reproduce the large-scale community structure quite well because the connection probability depends on the groups of the two airports. However, within each pair of groups, airports are treated as interchangeable. Does that mean the model can preserve community-level densities while still failing to reproduce features such as the very high degree of hub airports or the exact degree distribution?","That makes sense. So this SBM captures mesoscale structure through the block densities, but it does not model node-level heterogeneity within each block. A degree-corrected block model would therefore be more appropriate if we also wanted to reproduce the hub structure of the airport network. going to move on now"]
Tutor's note: Found max_real and max_sbm with max(g.degree()) and max(sbm_net.degree()), and corr_sbm with np.corrcoef(g.degree(), sbm_net.degree())[0,1]. All steps first time.

## cp8_dcsbm — pass (0 hints)
Question: Compute kappa and theta by the quiz's estimates, write sample_dcsbm, build a network, and compare its degrees with the real network.
Answer (verbatim): (no answer — the code is their answer)
Typed by the student: ["The result makes the limitation of the basic SBM very clear. The real network has a maximum degree of 246, while the sampled block model only reaches 36, and the node-level degree correlation is just 0.25. So even though the SBM preserves the connection densities between communities, it treats airports within the same group as statistically similar and cannot reproduce the strong degree heterogeneity of real airports. Is this the main motivation for a degree-corrected stochastic block model, where each node gets its own degree-related parameter while the block structure is still preserved?","That makes sense. So the block matrix (w) captures the mesoscale community structure, while the node-specific (\\theta_i) captures degree heterogeneity within those communities. This separates “which groups tend to connect” from “which individual nodes are especially active.” Lets move"]
Tutor's note: Computed kappa with np.bincount(groups, weights=deg), theta = deg/kappa[groups], rate via outer products theta[:,None]*theta[None,:]*w[z[:,None],z[None,:]], Poisson counts with np.triu(k=1), and repeated each pair counts[i,j] times with a loop building the edge list (equivalent to np.repeat). max_dc and corr_dc correct. All steps first time.
