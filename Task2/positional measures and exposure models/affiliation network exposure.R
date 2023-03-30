# purpose: this code outlines the computation of affiliation network exposure
# ---------------------------------------------------------------------------------------
# notes:
#   * This script only serve as a template for how the affiliation exposure are computed
#
#   * Generally, the steps to perform this are ....
#     (1) load data sets:
#         specimen data + two-mode edge list
#
#     (2) create network object
#         create two-mode adjacency matrix (rows=people; cols=outbreak places; cells=affiliation)
#
#     (3) subset of specimen data set
#         keep only individuals who are in the two-mode network data
#
#     (4) perform bipartite projection to create co-affiliation network
#         use `A * A_transpose` or `igraph::bipartite_projection()`
#         dichotomize into 0s and 1s
#
#     (5) create the outcome vector (disease status), coded as 0s and 1s
#         since COVID-19 status changes over time,
#         we created the vector of 'ever positive' within a specified period
#
#     (6) Compute Affiliation Network Exposure
#         aff_exp = (A %*% y)/rowSum(A)
#########################################################################################

# (0) start
rm(list = ls())


# (1) read data sets
df_2m_el = data.table::fread("two-mode edge list data")
df_spec = data.table::fread("covid-19 testing data set")


# (2) create network data
ig_2m = igraph::graph_from_data_frame(d = df_2m_el) # 2mode edge list --> 2mode igraph


# (3) subset specimen data
id_keep = igraph::V(ig_2m) |> names()
df_spec = df_spec[df_spec$EVENT_ID %in% id_keep, ]


# (4) perform bipartite projection
ig_1m = igraph::bipartite_projection(graph = ig_2m) # 2mode igraph --> 1mode igraph
adj_mat_1m = as.matrix(ig_1m)                       # 1mode igraph --> 1m adj. matrix


# (5) create the outcome vector
ever_pos = df_spec |>
  dplyr::group_by(EVENT_ID) %>%
  dplyr::summarise(
    v.ever_covid = dplyr::case_when(any(tolower(RESULT_NAME) %in% c("detected", "positive", "severe acute")) ~ 1,
                                    !any(tolower(RESULT_NAME) %in% c("detected", "positive", "severe acute")) ~ 0)
  ) |>
  dplyr::ungroup() |>
  dplyr::pull(v.ever_covid, EVENT_ID)
ever_pos = ever_pos[rownames(adj_mat_1m)] # sort such that each element of the vector matches the 1mode adjacency matrix's ordering


# (6) compute affiliation network exposure term
aff_exp = (adj_mat_1m %*% ever_pos)/rowSums(adj_mat_1m)
aff_exp = as.numeric(aff_exp)
names(aff_exp) = names(aff_exp)


# (xx) others/visualizations
library(ggplot2)
aff_exp_plot = ggplot() +
  geom_histogram(aes(x = aff_exp)) +
  labs(x = "COVID-19 Exposure Measures", y = "", title = "Distribution of COVID-19 Exposure through Outbreak Site projection") +
  theme_bw() +
  theme(axis.text.y = element_blank())
