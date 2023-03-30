# purpose: this scripts outlines the analysis of small-world network structure
# -------------------------------------------------------------------------------------------
# notes:
#   * Generally, the steps to perform this analysis is the follows:
#     (0) initialize the script
#         contains 4 custom functions that are essential for the analysis of small-world network
#          1] split_network        ~ splits network by component into a list
#          2] sim_smallworld_comps ~ component-wise simulates the network
#          3] compute_SW           ~ computes avg. path length & clustering coef. for the input network
#          4] compute_SW_overall   ~ computes the overall avg. path length & clustering coef. for a list of subgraphs/components
#
#     (1) read in network objects to be analyzed
#         they should have already been constructed and saved as igraph objects, in .RData format
#
#     (2) split network into a list object
#         where each element is a connected subgraph (i.e., component)
#
#     (3) compute the small-world statistics (avg. path length, clustering coef.)
#         for each subgraph from step(2)
#
#     (4) perfor simulation for `N_sim` times for each subgraph
#         also computes the small-world statistics for each simulation
#
#     (5) computes the small-world-ness index which is what we used as the decision rule to determine
#         whether a network can be classified as small-world or not
#         the index is described here: https://doi.org/10.1371/journal.pone.0002051
#
#   * Small World networks are characterized by two network measures
#     (1) Average Path Length
#     (2) Clustering Coefficients
#     (*) https://www.nature.com/articles/30918
#
#   * Typically, small-world is not applicable to unconnected graphs
#     - for this reason, we computed component-wise path length & clustering coefficients
#     - took the average of all components
#     - and applied the analysis on the aggrgated measures
# -------------------------------------------------------------------------------------------
#############################################################################################




# (0) start
rm(list = ls())
library(igraph)

# this function splits an igraph object by component. The output is a list object with length equal to the number of component in the input argument `ig`
split_network = function(ig){
  # get network vertex names & component distribution
  ig.v_names = names(igraph::V(ig))
  ig.cl = igraph::clusters(graph = ig)

  # loop through each component and create sub networks, then append to the list `ig_list`
  ig_list = list()
  for (c in 1:ig.cl$no) {
    v_names.keep = names(ig.cl$membership)[which(ig.cl$membership == c)]
    ig.sub = igraph::delete.vertices(graph = ig, v = !(ig.v_names %in% v_names.keep))

    ig_list[[c]] = ig.sub
  }

  # return
  return(ig_list)
}

# simulation by re-wiring
sim_smallworld_comps = function(ig_list, rewire_p){
  # checks
  if (!is.list(ig_list)) stop("`ig_list` should be a list object")
  if (!all(sapply(ig_list, class) == "igraph")) stop("`ig_list` should contain only igraph objects")
  if (!all(sapply(ig_list, igraph::is_connected))) stop("all igraph objects within `ig_list` should be a connected graph")

  # loop through each igraph in `ig_list`
  smallworld_list = list()
  for (i in 1:length(ig_list)) {
    # network
    ig.sub = ig_list[[i]]

    # network stat
    ig.sub.size = length(igraph::V(ig.sub))
    ig.sub.k = mean(igraph::degree(ig.sub))
    ig.sub.k_rounded = ((ig.sub.k %/% 2) + ((ig.sub.k %% 2) >= 1)) * 2 # rounding to nearest even number

    ig.smallworld = igraph::sample_smallworld(
      dim = 1,
      size = ig.sub.size,
      nei = ig.sub.k_rounded,
      p = rewire_p,
      multiple = FALSE
    )

    smallworld_list[[i]] = ig.smallworld
  }

  # return
  return(smallworld_list)
}


# computes the two measures used in Watts paper (avg. path length and clustering coefficient)
compute_SW = function(ig){
  # path length ~ exclude infinite/NA lengths (disconnected) & zero lenghts (self)
  #               isolated nodes will return NaN
  L = igraph::mean_distance(graph = ig, directed = FALSE)

  # clustering coefficient ~ remove NAs when taking average
  #                          non-triples will return NaN
  C = mean(igraph::transitivity(graph = ig, type = "local"), na.rm = TRUE)

  # network size
  net_size = length(igraph::V(ig))

  # return
  out = c(L = L, C = C, net_size = net_size)
  out
}


# computes the overall SmallWorld measures by taking the average
compute_SW_overall = function(df, weight_type = c("none", "net_size", "net_size_sq", "exp_net_size")){
  # checks
  exit.cond1 = ncol(df) != 3
  exit.cond2 = !all(c('L', 'C', 'net_size') %in% colnames(df))
  if (exit.cond1 || exit.cond2) stop("`df` must contain 3 columns: `L`, `C`, and `net_size`")

  # remove NaNs (`NaN` are conidered as `NA` by R)
  df.L = df[!is.na(df$L), ]
  df.C = df[!is.na(df$C), ]

  # compute weight vector
  if (weight_type == "none") {
    w1 = rep(1, nrow(df.L))
    w2 = rep(1, nrow(df.C))
  } else if (weight_type == "net_size") {
    w1 = df.L$net_size
    w2 = df.C$net_size
  } else if (weight_type == "net_size_sq") {
    w1 = (df.L$net_size)^2
    w2 = (df.C$net_size)^2
  } else if (weight_type == "exp_net_size") {
    w1 = exp(df.L$net_size)
    w2 = exp(df.C$net_size)
  } else {
    stop("Incorrect `weight_type` option")
  }

  # average length
  L_mean = mean(df.L$L)
  L_mean.wt = (df.L$L %*% w1) / sum(w1)

  # average length
  C_mean = mean(df.C$C)
  C_mean.wt = (df.C$C %*% w2) / sum(w2)

  # output
  c(L_mean = L_mean, L_mean.wt = L_mean.wt,
    C_mean = C_mean, C_mean.wt = C_mean.wt)
}





# (1) load networks, in igraph object format
load("load igraph objects which will be analyzed")
"suppose the igraph object is named `ig`"


# (2) split network into a list object, where each element is a connected subgraph (i.e., component)
ig.by_comp = split_network(ig = ig)


# (3) compute the small-world statistics (avg. path length, clustering coef.) for each subgraph from the previous step
ig.stat = lapply(
  X = 1:length(ig.by_comp),
  FUN = function(c){
    x = ig.by_comp[[c]]
    compute_SW(ig = x)
  }
)
ig.stat = do.call(`rbind`, ig.stat)
ig.stat = data.frame(ig.stat)




# (4) perfor simulation for `N_sim` times for each subgraph also computes the small-world statistics for each simulation
N_sim = 200
sim_result = list()
for (s in 1:N_sim) {
  rand_SW.by_comp = sim_smallworld_comps(ig_list = ig.by_comp, rewire_p = 1) # generate a list of small world networks

  rand_SW.stat = lapply( # compute L & C ~ by components
    X = 1:length(rand_SW.by_comp),
    FUN = function(c){
      x = rand_SW.by_comp[[c]]

      if (!igraph::is.connected(x)) {
        cat("  - WARNING: the s=", s, "th simulation, ", "component #", c, " was not a connected graph \n", sep = "")
      }

      compute_SW(ig = x)
    }
  )
  rand_SW.stat = do.call(`rbind`, rand_SW.stat)
  rand_SW.stat = data.frame(rand_SW.stat)

  sim_result[[s]] = compute_SW_overall(rand_SW.stat, weight_type = "net_size") # compute L & C for the overall nework
}

sim_result = do.call(`rbind`, sim_result)
rownames(sim_result) = paste("sim_", 1:N_sim, sep = "") # tidy simulation result

sw_out = list( # combine measure from empirical data & simulated into a list
  stat.obs = compute_SW_overall(ig.stat, weight_type = "net_size"),
  stat.sim = sim_result
)



# (5) computes the small-world-ness-index
c_actual = sw_out$stat.obs["C_mean.wt"]
c_simulated = mean(sw_out$stat.sim[, "C_mean.wt"])
numerator = unname(c_obs/c_sim)

l_actual = sw_out$stat.obs["L_mean.wt"]
l_simulated = mean(sw_out$stat.sim[, "L_mean.wt"])
denominator = unname(l_obs/l_sim)

s_index = numerator/denominator  # ratio of two ratios ... small-world:  s>1; not small-world: s<1
print(s_index)

