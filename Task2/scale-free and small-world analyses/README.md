## Overview

This folder contains R codes to perform the supplementary analyses we conducted for this project, mainly consisting of the analysis of network structural modeling. We tested whether the empirical SARS-CoV-2 transmission network can be classified as a **scale-free** network, a **small-world** network, or both. 

### `test scale free.R`

*Scale-free networks* are networks characterized by an uneven distribution of connectivity (degree) among its nodes. The underlying mechanism is that the degree distribution conforms to a discrete power-law model. In a scale-free network, the majority of the nodes have relatively few connections, while a small number of nodes have a disproportionately large number of connections.

This R script contains the code to test the scale-free network structure. The step-by-step procedures are outlined within the .R file. For technical details regarding the methodology see [Broido & Clauset (2019)](https://doi.org/10.1038/s41467-019-08746-5).

### `test small world.R`

*Small-world networks* are networks characterized by the combination of high local clustering and small average path lengths among its nodes. The concept is often referred to as the "six degrees of separation", which posits that any two individuals in the network are connected by a small number of intermediate acquaintances/nodes. In a small-world network, we expect to observe high local clustering (i.e., a group nodes forming a tightly-knitted community) and only few long-range connections that bridge distant clusters (shortcuts).

This R script contains the code to test the small-world network structure. The step-by-step procedures are outlined within the .R file. For technical details regarding the methodology see [Watts & Strogatz (1998)](https://www.nature.com/articles/30918) and [Humphries & Gurney (2008)](https://doi.org/10.1371/journal.pone.0002051).

<br/>

## Authors

* Jacky Kuo
* Kayo Fujimoto
