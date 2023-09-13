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
allBlocksPrAt10 <- data.frame()
allBlocksPrAt15 <- data.frame()
allBlocksPrAt25 <- data.frame()

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
  
  PrAt10 <- read.csv(paste("evaluation_result/input_data/5_10_graphs_", inGro, "g_", btwGro, "ng/precision_at_k_10_link_prediction.csv", sep = ""))
  ggplot(PrAt10, aes(x=embedder, y=pk_ratio)) + 
    geom_boxplot() +
    geom_jitter(width = 0.2)
  ggsave(paste("evaluation_result/input_data/5_10_graphs_", inGro, "g_", btwGro, "ng/precision_at_k_10_link_prediction.pdf", sep = ""), width = 8)
  
  PrAt10$ratio = paste(ratio)
  allBlocksPrAt10 <- rbind(allBlocksPrAt10, PrAt10)

  PrAt15 <- read.csv(paste("evaluation_result/input_data/5_10_graphs_", inGro, "g_", btwGro, "ng/precision_at_k_15_link_prediction.csv", sep = ""))
  ggplot(PrAt15, aes(x=embedder, y=pk_ratio)) + 
    geom_boxplot() +
    geom_jitter(width = 0.2)
  ggsave(paste("evaluation_result/input_data/5_10_graphs_", inGro, "g_", btwGro, "ng/precision_at_k_15_link_prediction.pdf", sep = ""), width = 8)
  
  PrAt15$ratio = paste(ratio)
  allBlocksPrAt15 <- rbind(allBlocksPrAt15, PrAt15)

  PrAt25 <- read.csv(paste("evaluation_result/input_data/5_10_graphs_", inGro, "g_", btwGro, "ng/precision_at_k_25_link_prediction.csv", sep = ""))
  ggplot(PrAt25, aes(x=embedder, y=pk_ratio)) + 
    geom_boxplot() +
    geom_jitter(width = 0.2)
  ggsave(paste("evaluation_result/input_data/5_10_graphs_", inGro, "g_", btwGro, "ng/precision_at_k_25_link_prediction.pdf", sep = ""), width = 8)
  
  PrAt25$ratio = paste(ratio)
  allBlocksPrAt25 <- rbind(allBlocksPrAt25, PrAt25)
}

write.csv(allBlocksAvgErr, file = "evaluation_result/input_data/5_10_graphs_all_avgErr.csv", row.names = FALSE)
ggplot(allBlocksAvgErr, aes(x=embedder, y=f_score)) + 
  geom_boxplot() + 
  geom_jitter(width = 0.3, aes(color=ratio))
ggsave("evaluation_result/input_data/5_10_graphs_all_avgErr.pdf", width = 8)

write.csv(allBlocksPrAt10, file = "evaluation_result/input_data/5_10_graphs_all_PrAt10.csv", row.names = FALSE)
ggplot(allBlocksPrAt10, aes(x=embedder, y=pk_ratio)) + 
  geom_boxplot() +
  geom_jitter(width = 0.3, aes(color=ratio))
ggsave("evaluation_result/input_data/5_10_graphs_all_PrAt10.pdf", width = 8)

write.csv(allBlocksPrAt15, file = "evaluation_result/input_data/5_10_graphs_all_PrAt15.csv", row.names = FALSE)
ggplot(allBlocksPrAt15, aes(x=embedder, y=pk_ratio)) + 
  geom_boxplot() +
  geom_jitter(width = 0.3, aes(color=ratio))
ggsave("evaluation_result/input_data/5_10_graphs_all_PrAt15.pdf", width = 8)

write.csv(allBlocksPrAt25, file = "evaluation_result/input_data/5_10_graphs_all_PrAt25.csv", row.names = FALSE)
ggplot(allBlocksPrAt25, aes(x=embedder, y=pk_ratio)) + 
  geom_boxplot() +
  geom_jitter(width = 0.3, aes(color=ratio))
ggsave("evaluation_result/input_data/5_10_graphs_all_PrAt25.pdf", width = 8)