# install.packages("tidyverse")

library(tidyverse)

evaluations <- list(
  list("average_error_link_prediction", "f_score"),
  list("precision_at_k_link_prediction", "pk_ratio")
)

folder <- file.path(getwd(), 'evaluation_result', "real_time")

graphs <- list.dirs(path = folder, recursive = FALSE, full.names = TRUE)

# for (evaluation in evaluations) {
#   metric <- evaluation[1]
#   name <- evaluation[2]
#     
#   for (graph in graphs) {
#     data_frame <- read.csv(file.path(graph, paste(metric, ".csv", sep = "")))
#     
#     embedder <- "embedder"
#     ggplot(data_frame, aes(x = .data[[embedder]], y = .data[[name]])) +
#       geom_line()
#     ggsave(file.path("evaluation_result", folder, paste(metric, ".pdf", sep = "")), width = 16)
#   }
# }

for (graph in graphs) {
  data_frame <- read.csv(file.path(graph, paste("average_error_link_prediction", ".csv", sep = "")))
  
  ggplot(data_frame, aes(x = embedder, y = f_score)) +
    geom_point(size = 4)
  ggsave(file.path(graph, paste("average_error_link_prediction", ".pdf", sep = "")))
}

for (graph in graphs) {
  data_frame <- read.csv(file.path(graph, paste("precision_at_k_link_prediction", ".csv", sep = "")))
  
  ggplot(data_frame, aes(x = embedder, y = pk_ratio)) +
    geom_point(size = 4)
  ggsave(file.path(graph, paste("precision_at_k_link_prediction", ".pdf", sep = "")))
}