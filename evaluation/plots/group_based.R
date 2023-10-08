# install.packages("tidyverse")

library(tidyverse)

evaluations <- list(
  list("average_error_link_prediction", "f_score"),
  list("precision_at_k_link_prediction", "pk_ratio")
)

folder <- "input_data"

graph_groups <- list.dirs(path = file.path(getwd(), folder), recursive = FALSE, full.names = FALSE)

plots <- list()

for (evaluation in evaluations) {
  metric <- evaluation[1]
  name <- evaluation[2]
  
  data_frame <- data.frame()

  for (group in graph_groups) {
    path <- file.path(getwd(), "evaluation_result", folder, group)
    
    graphs <- list.dirs(path = path, recursive = FALSE, full.names = TRUE)
    
    for (graph in graphs) {
      results <- read.csv(file.path(graph, paste(metric, ".csv", sep = "")))
      results$group = paste(group)
        data_frame <- rbind(data_frame, results)
    }
  }
  
  write.csv(data_frame, file = file.path("evaluation_result", folder, paste(metric, ".csv", sep = "")), row.names = FALSE)
  
  #group <- "group"
  #embedder <- "embedder"
  #plots[[i]] <- ggplot(data_frame, aes(x = .data[[group]], y = .data[[name]], fill = .data[[embedder]])) +
    #geom_boxplot()
  
  #ggsave(file.path("evaluation_result", folder, paste(metric, ".pdf", sep = "")), width = 16)
}

data_frame1 <- read.csv(file.path("evaluation_result", folder, paste("average_error_link_prediction", ".csv", sep = "")))
ggplot(data_frame1, aes(x = group, y = f_score, fill = embedder)) +
  geom_boxplot()
ggsave(file.path("evaluation_result", folder, paste("average_error_link_prediction", ".pdf", sep = "")), width = 16)

data_frame2 <- read.csv(file.path("evaluation_result", folder, paste("precision_at_k_link_prediction", ".csv", sep = "")))
ggplot(data_frame2, aes(x = group, y = pk_ratio, fill = embedder)) +
  geom_boxplot()
ggsave(file.path("evaluation_result", folder, paste("precision_at_k_link_prediction", ".pdf", sep = "")), width = 16)