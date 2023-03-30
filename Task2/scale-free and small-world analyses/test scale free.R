# purpose: outlines the analysis to determine scale free network structure
# -------------------------------------------------------------------------------------------------------
# notes:
#   * Generally, the analysis follows the following steps:
#     (1) read in network objects to be analyzed
#         they should have already been constructed and saved as igraph objects, in .RData format
#
#     (2) fit the power law model and perform goodness-of-fit test
#         use `sink()` function to log any progress in the computation
#
#     (3) fit alternative model: exponential
#     (4) fit alternative model: log-normal
#     (5) fit alternative model: power-law with exponential cutoff
#     (6) fit alternative model: Weibull
#
#     (7) use LRT to compare power law to the alternatives
#
#     (8) decision rule as to whether network can be
#         classified as scale-free are discussed in the Nature's Communication paper
# -------------------------------------------------------------------------------------------------------
#########################################################################################################

# (0) start
rm(list = ls())
library(SFdegree) # this is a custom package developed for performing the scale-free network analysis


# (1) load networks, in igraph object format
load("load igraph objects which will be analyzed")
"suppose the igraph object is named `ig`"




# (2) fit power law & perform GoF
sink(file = "...<log_progress_if_needed.txt>...") # opens `sink()`

my_dgr = igraph::degree(ig) |> as.numeric() # observed degree data
my_fit.PL = igraph::fit_power_law(x = my_dgr, xmin = NULL) # fit Power law using igraph

my_fit.PL.gof = SFdegree::gof_PL( # performs GoF
  k = my_dgr,
  kmin = my_fit.PL$xmin,
  alpha = my_fit.PL$alpha,
  Nsim = 2500,
  ss = 123
)

cat( # prints summary message
  "\n mean degree of the empirical data was: ", mean(my_dgr),
  "\n         power-law estimated alpha was: ", my_fit.PL$alpha,
  "\n         power-law estimated k_min was: ", my_fit.PL$xmin,
  sep = ""
)

sink() # closes `sink()`




# (3) fitting Exponential
my_dgr = igraph::degree(ig) |> as.numeric()
my_fit.PL = igraph::fit_power_law(x = my_dgr, xmin = NULL)
my_fit.exp = list( # fit, while trying different initial values
  fit_exp(k = my_dgr, kmin = my_fit.PL$xmin, inits = c(log.lambda = -3.5)),
  fit_exp(k = my_dgr, kmin = my_fit.PL$xmin, inits = c(log.lambda = -0.8)),
  fit_exp(k = my_dgr, kmin = my_fit.PL$xmin, inits = c(log.lambda = 0.8)),
  fit_exp(k = my_dgr, kmin = my_fit.PL$xmin, inits = c(log.lambda = 3.5))
)

my_fit.exp.par = my_fit.exp[[sapply(my_fit.exp, function(x) x$LL) |> which.max()]]$par |> unname() # vector of parameter




# (4) fit Log-Normal
my_dgr = igraph::degree(ig) |> as.numeric()
my_fit.PL = igraph::fit_power_law(x = my_dgr, xmin = NULL)
my_fit.lognorm = list( # fit, while trying different intial values
  fit_lognorm(k = my_dgr, kmin = my_fit.PL$xmin, inits = c(mu = -10, log.sigma = -6)),
  fit_lognorm(k = my_dgr, kmin = my_fit.PL$xmin, inits = c(mu = -1, log.sigma = -6)),
  fit_lognorm(k = my_dgr, kmin = my_fit.PL$xmin, inits = c(mu = 1, log.sigma = -6)),
  fit_lognorm(k = my_dgr, kmin = my_fit.PL$xmin, inits = c(mu = 10, log.sigma = -6))
)

my_fit.lognorm.par = my_fit.lognorm[[sapply(my_fit.lognorm, function(x) x$LL) |> which.max()]]$par |> unname() # vector of parameter




# (5) fit Power Law with Exponential cutoff
my_dgr = igraph::degree(ig) |> as.numeric()
my_fit.PL = igraph::fit_power_law(x = my_dgr, xmin = NULL)
my_fit.PLc = list( # fit, while trying different intial values
  fit_PLc(k = my_dgr, kmin = my_fit.PL$xmin, inits = c(log.alpha = -6, log.lambda = -4)),
  fit_PLc(k = my_dgr, kmin = my_fit.PL$xmin, inits = c(log.alpha = -2, log.lambda = -4)),
  fit_PLc(k = my_dgr, kmin = my_fit.PL$xmin, inits = c(log.alpha = 2, log.lambda = -4)),
  fit_PLc(k = my_dgr, kmin = my_fit.PL$xmin, inits = c(log.alpha = 6, log.lambda = -4))
)

my_fit.PLc.par = my_fit.PLc[[sapply(my_fit.PLc, function(x) x$LL) |> which.max()]]$par |> unname() # vector of parameter




# (6) fit Weibull -----------
my_dgr = igraph::degree(ig) |> as.numeric()
my_fit.PL = igraph::fit_power_law(x = my_dgr, xmin = NULL)
my_fit.weib = list( # fit, while trying different intial values
  fit_weib(k = my_dgr, kmin = my_fit.PL$xmin, inits = c(log.a = -10, log.b = -7)),
  fit_weib(k = my_dgr, kmin = my_fit.PL$xmin, inits = c(log.a = -1, log.b = -7)),
  fit_weib(k = my_dgr, kmin = my_fit.PL$xmin, inits = c(log.a = 0.5, log.b = -7)),
  fit_weib(k = my_dgr, kmin = my_fit.PL$xmin, inits = c(log.a = 2, log.b = -7))
)

my_fit.weib.par = my_fit.weib[[sapply(my_fit.weib, function(x) x$LL) |> which.max()]]$par |> unname() # vector of parameter




# (7) perform LRT, comparison between power-law and alternative models
my_dgr = igraph::degree(ig) |> as.numeric()
my_fit.PL = igraph::fit_power_law(x = my_dgr, xmin = NULL)
LRTest( # exp
  LLi1 = PL_LLi(k = my_dgr, kmin = my_fit.PL$xmin, params = list(alpha = my_fit.PL$alpha), log = TRUE),
  LLi2 = exp_LLi(k = my_dgr, kmin = my_fit.PL$xmin, params = list(lambda = my_fit.exp.par), log = TRUE)
)

LRTest( # log norm
  LLi1 = PL_LLi(k = my_dgr, kmin = my_fit.PL$xmin, params = list(alpha = my_fit.PL$alpha), log = TRUE),
  LLi2 = lognorm_LLi(k = my_dgr, kmin = my_fit.PL$xmin, params = list(mu = my_fit.lognorm.par[1], sigma = my_fit.lognorm.par[2]), log = TRUE)
)

LRTest( # power law w/ exp cut
  LLi1 = PL_LLi(k = my_dgr, kmin = my_fit.PL$xmin, params = list(alpha = my_fit.PL$alpha), log = TRUE),
  LLi2 = PLc_LLi(k = my_dgr, kmin = my_fit.PL$xmin, params = list(alpha = my_fit.PLc.par[1], lambda = my_fit.PLc.par[2]), log = TRUE)
)

LRTest( # weibull
  LLi1 = PL_LLi(k = my_dgr, kmin = my_fit.PL$xmin, params = list(alpha = my_fit.PL$alpha), log = TRUE),
  LLi2 = weib_LLi(k = my_dgr, kmin = my_fit.PL$xmin, params = list(a = my_fit.weib.par[1], b = my_fit.weib.par[2]), log = TRUE)
)

