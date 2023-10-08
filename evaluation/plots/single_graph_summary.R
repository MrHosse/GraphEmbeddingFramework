# install.packages("tidyverse")

library(tidyverse)

evaluations <- list(
  list("average_error_link_prediction", "f_score"),
  list("precision_at_k_link_prediction", "pk_ratio")
)

folder <- file.path(getwd(), 'evaluation_result', "real_time")

graphs <- list.dirs(path = folder, recursive = FALSE, full.names = TRUE)

avgErr <- data.frame()
prk <- data.frame()

for (graph in graphs) {
  data_frame <- read.csv(file.path(graph, paste("average_error_link_prediction", ".csv", sep = "")))
  avgErr <- rbind(avgErr, data_frame)
  
  data_frame <- read.csv(file.path(graph, paste("precision_at_k_link_prediction", ".csv", sep = "")))
  prk <- rbind(prk, data_frame)
}

ggplot(avgErr, aes(x = embedder, y = f_score)) +
  geom_boxplot()
ggsave(file.path("evaluation_result", folder, paste("average_error_link_prediction", ".pdf", sep = "")))

ggplot(prk, aes(x = embedder, y = pk_ratio)) +
  geom_boxplot()
ggsave(file.path("evaluation_result", folder, paste("precision_at_k_link_prediction", ".pdf", sep = "")))