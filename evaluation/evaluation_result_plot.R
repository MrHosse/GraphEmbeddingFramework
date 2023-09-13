# install.packages("tidyverse")

library(tidyverse)

randomGeoAvgErr <- read.csv("evaluation_result/input_data/geometric_graphs/average_error_link_prediction.csv")
ggplot(randomGeoAvgErr, aes(x=embedder, y=f_score)) +
  geom_boxplot() +
  geom_jitter(width = 0.2)
ggsave("evaluation_result/input_data/geometric_graphs/average_error_link_prediction.pdf", width = 8)

randomGeoPreAtK <- read.csv("evaluation_result/input_data/geometric_graphs/precision_at_k_10_link_prediction.csv")
ggplot(randomGeoPreAtK, aes(x=embedder, y=pk_ratio)) +
  geom_boxplot() +
  geom_jitter(width = 0.2)
ggsave("evaluation_result/input_data/geometric_graphs/precision_at_k_10_link_prediction.pdf", width = 8)

graph_groups <- list(
  list("1.0", "0.0", "100-0"),
  list("0.9", "0.1", "90-10"),
  list("0.8", "0.2", "80-20"),
  list("0.7", "0.3", "70-30"),
  list("0.6", "0.4", "60-40"),
  list("0.5", "0.5", "50-50")
)

allBlocksAvgErr <- data.frame()
allBlocksPrAtK <- data.frame()

for (group in graph_groups) {
  inGro <- group[1]
  btwGro <- group[2]
  ratio <- group[3]
  
  AvgErr <- read.csv(paste("evaluation_result/input_data/5_10_graphs_", inGro, "g_", btwGro, "ng/average_error_link_prediction.csv", sep = ""))
  ggplot(AvgErr, aes(x=embedder, y=f_score)) + 
    geom_boxplot() +
    geom_jitter(width = 0.2)
  ggsave(paste("evaluation_result/input_data/5_10_graphs_", inGro, "g_", btwGro, "ng/average_error_link_prediction.pdf", sep = ""), width = 8)
  
  AvgErr$ratio = paste(ratio)
  allBlocksAvgErr <- rbind(allBlocksAvgErr, AvgErr)
  
  PrAtK <- read.csv(paste("evaluation_result/input_data/5_10_graphs_", inGro, "g_", btwGro, "ng/precision_at_k_10_link_prediction.csv", sep = ""))
  ggplot(PrAtK, aes(x=embedder, y=pk_ratio)) + 
    geom_boxplot() +
    geom_jitter(width = 0.2)
  ggsave(paste("evaluation_result/input_data/5_10_graphs_", inGro, "g_", btwGro, "ng/precision_at_k_10_link_prediction.pdf", sep = ""), width = 8)
  
  PrAtK$ratio = paste(ratio)
  allBlocksPrAtK <- rbind(allBlocksPrAtK, PrAtK)
}

write.csv(allBlocksAvgErr, file = "evaluation_result/input_data/5_10_graphs_all_avgErr.csv", row.names = FALSE)
ggplot(allBlocksAvgErr, aes(x=embedder, y=f_score)) + 
  geom_boxplot() + 
  geom_jitter(width = 0.3, aes(color=ratio))
ggsave("evaluation_result/input_data/5_10_graphs_all_avgErr.pdf", width = 8)

write.csv(allBlocksPrAtK, file = "evaluation_result/input_data/5_10_graphs_all_PrAtK.csv", row.names = FALSE)
ggplot(allBlocksPrAtK, aes(x=embedder, y=pk_ratio)) + 
  geom_boxplot() +
  geom_jitter(width = 0.3, aes(color=ratio))
ggsave("evaluation_result/input_data/5_10_graphs_all_PrAtK.pdf", width = 8)