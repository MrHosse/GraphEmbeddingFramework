install.packages("tidyverse")

library(tidyverse)

evaluations <- list(
    list("average_error_link_prediction", "f_score", data.frame()),
    list("precision_at_k_link_prediction", "pk_ratio", data.frame())
)

folder <- "input_data"

group_names <- list.dirs(path = file.path(getwd(), folder), recursive = FALSE, full.names = FALSE)
group_paths <- list.dirs(path = file.path(getwd(), folder), recursive = FALSE, full.names = TRUE)
graph_groups <- Map(c, group_names, group_paths)

for (evaluation in evaluations) {
    metric <- evaluation[1]
    data_frame <- evaluation[3]

    for (group in graph_groups) {
        name <- group[1]
        path <- group[2]
        
        graphs <- list.dirs(path = path, recursive = FALSE, full.names = TRUE)

        for (graph in graphs) {
            results <- read.csv(file.path(graph, paste(metric, ".csv", sep = "")))
            results$graph_group = paste(name)
            data_frame <- rbind(data_frame, results)
        }
    }
}

for (evaluation in evaluations) {
  ggplot(evaluation[3], aes(x = graph_group, y = evaluation[2], fill = embedder)) +
    geom_boxplot()
  ggsave(file.path("evaluation_result", paste(evaluation[1], ".pdf", sep = "")), width = 16)
}