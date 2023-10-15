# install.packages("tidyverse")

library(tidyverse)
library(dplyr)

evaluations <- list(
  list("average_error_link_prediction", "f_score"),
  list("precision_at_k_link_prediction", "pk_ratio"),
  list("time", "time")
)

for (evaluation in evaluations) {
  metric <- evaluation[[1]]
  eval_type <- evaluation[[2]]
  
  data <- read.csv('output/all_graphs.csv')
  data <- subset(data, type == eval_type)
  
  data <- data %>% mutate(Embedder_SimMetric = paste(embedder, similarity_metric, sep = "#"))
  ggplot(data, aes(x = group, y = value, fill = Embedder_SimMetric)) +
    geom_boxplot() + 
    labs(y = eval_type)
  ggsave(file.path("output", paste(metric, ".pdf", sep = "")), width = 16)
}