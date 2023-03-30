# purpose: this code outlines the computation of network positional measures
# ---------------------------------------------------------------------------------------
# notes:
#   * This script only serve as a template for how they are computed
#
#   # Generally, the computation follows these steps
#     (1) load data sets: edge list data
#         perform any subset/filtering/cleaning here
#
#     (2) create network object using igraph
#         `igraph::graph_from_data_frame()`
#
#     (3) use igraph to compute various network measures
#
#     (4) summarize network measures & centralities
#         use either the 'e1071' or 'moments' package for computing kurtosis/skewness
# ---------------------------------------------------------------------------------------
#########################################################################################

# (0) start
rm(list = ls())


# (1) read data sets
df_el = data.table::fread("edgelist data sets")
df_el = clean_data(df_el) # perform any cleaning of edge list data (e.g., de-dup, apply selection criteria, etc.)


# (2) create network data
ig = igraph::graph_from_data_frame(d = df_el, directed = FALSE)


# (2.5) a synthetic network for demonstration
set.seed(123)
ig = igraph::sample_gnp(n = 500, p = 0.005) # this simulates a network for demonstration purposes ONLY


# (3) compute various network measures
ig.N = length(igraph::V(ig))
ig.dgr = igraph::degree(ig)
ig.btw = igraph::betweenness(ig, normalized = F) # set `normalized = TRUE` to normalize the measures
ig.cls = igraph::closeness(ig, normalized = F)   # set `normalized = TRUE` to normalize the measures

ig.den = igraph::edge_density(ig) * 100
ig.cluster_coef = igraph::transitivity(ig)
ig.avg_dist = igraph::mean_distance(ig)

ig.comp = igraph::components(ig)


# (4) summarize measures
cat(
  "\n",
  "\n       Network Size = ", ig.N,
  "\n        Mean degree = ", mean(ig.dgr),
  "\n       SD of degree = ", sd(ig.dgr),
  "\n Skewness of degree = ", moments::skewness(ig.dgr),
  "\n Kurtosis of degree = ", moments::kurtosis(ig.dgr),
  "\n --------------------------------------------",
  "\n    Network density (%) = ", sprintf("%.3f", ig.den),
  "\n Betweenness centrality = ", mean(ig.btw),
  "\n   Closeness centrality = ", mean(ig.cls),
  "\n --------------------------------------------",
  "\n     Clustering Coef. = ", mean(ig.cluster_coef),
  "\n  Average Path Length = ", mean(ig.avg_dist),
  "\n --------------------------------------------",
  "\n   Number of components = ", ig.comp$no,
  "\n Average component size = ", mean(ig.comp$csize),
  "\n --------------------------------------------",
  sep = ""
)



#done
