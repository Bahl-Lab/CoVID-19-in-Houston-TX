# purpose: this code outlines the computation of exposure from a network exposure model
# ---------------------------------------------------------------------------------------
# notes:
#   * This script only serve as a template for how the exposure measure is computed
#
#   # Generally, the computation follows these steps
#     (1) load data sets:
#         specimen data + one-mode edge list
#
#     (2) create network object
#         create one-mode adjacency matrix (rows=people; cols=people; cells=contacts)
#
#     (3) subset of specimen data set
#         keep only individuals who are in the one-mode network data
#
#     (4) create the outcome vector (disease status), coded as 0s and 1s
#         since COVID-19 status changes over time,
#         we created the vector of 'ever positive' within a specified period
#
#     (5) Compute exposure measure using network exposure model
#         exposure = (C %*% y)/rowSum(C)
# ---------------------------------------------------------------------------------------
#########################################################################################

# (0) start
rm(list = ls())


# (1) read data sets
df_1m_el = data.table::fread("one-mode edge list data")
df_spec = data.table::fread("covid-19 testing data set")


# (2) create network data
df_1m_el = clean_data(df_1m_el) # perform any cleaning of edge list data (e.g., de-dup, apply selection criteria, etc.)
ig_1m = igraph::graph_from_data_frame(d = df_1m_el, directed = FALSE)
adj_mat_1m = as.matrix(ig_1m)


# (3) subset specimen data
id_keep = rownames(adj_mat_1m)
df_spec = df_spec[df_spec$EVENT_ID %in% id_keep, ]


# (4) create the outcome vector
ever_pos = df_spec |>
  dplyr::group_by(EVENT_ID) %>%
  dplyr::summarise(
    v.ever_covid = dplyr::case_when(any(tolower(RESULT_NAME) %in% c("detected", "positive", "severe acute")) ~ 1,
                                    !any(tolower(RESULT_NAME) %in% c("detected", "positive", "severe acute")) ~ 0)
  ) |>
  dplyr::ungroup() |>
  dplyr::pull(v.ever_covid, EVENT_ID)
ever_pos = ever_pos[rownames(adj_mat_1m)] # sort such that each element of the vector matches the 1mode adjacency matrix's ordering


# (5) compute affiliation network exposure term
exposure = (adj_mat_1m %*% ever_pos)/rowSums(adj_mat_1m)
exposure = as.numeric(exposure)
names(exposure) = names(exposure)


# (xx) others/visualizations
library(ggplot2)
exposure_plot = ggplot() +
  geom_histogram(aes(x = exposure), fill = 'salmon3') +
  labs(x = "Proption of Exposure", y = 'Freq.') +
  theme_bw() +
  theme(title = element_text(face = 'bold'))


