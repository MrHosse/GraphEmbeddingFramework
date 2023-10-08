#!/usr/bin/env -S Rscript --vanilla

# install.packages("tidyverse")

library(tidyverse)

graph_groups <- list(
  list("1.0", "0.0", "reg 100-0"),
  list("0.75", "0.25", "reg 75-25"),
  list("0.5", "0.5", "reg 50-50")
)

allBlocksAvgErr <- data.frame()
allBlocksPrAt10 <- data.frame()
allBlocksPrAt15 <- data.frame()
allBlocksPrAt25 <- data.frame()

for (group in graph_groups) {
  inGro <- group[1]
  btwGro <- group[2]
  name <- group[3]
  
  AvgErr <- read.csv(paste("evaluation_result/input_data/5_10_graphs_", inGro, "g_", btwGro, "ng/average_error_link_prediction.csv", sep = ""))
  
  AvgErr$graph_group = paste(name)
  allBlocksAvgErr <- rbind(allBlocksAvgErr, AvgErr)
  
  PrAt10 <- read.csv(paste("evaluation_result/input_data/5_10_graphs_", inGro, "g_", btwGro, "ng/precision_at_k_10_link_prediction.csv", sep = ""))
  
  PrAt10$graph_group = paste(name)
  allBlocksPrAt10 <- rbind(allBlocksPrAt10, PrAt10)

  PrAt15 <- read.csv(paste("evaluation_result/input_data/5_10_graphs_", inGro, "g_", btwGro, "ng/precision_at_k_15_link_prediction.csv", sep = ""))
  
  PrAt15$graph_group = paste(name)
  allBlocksPrAt15 <- rbind(allBlocksPrAt15, PrAt15)

  PrAt25 <- read.csv(paste("evaluation_result/input_data/5_10_graphs_", inGro, "g_", btwGro, "ng/precision_at_k_25_link_prediction.csv", sep = ""))
  
  PrAt25$graph_group = paste(name)
  allBlocksPrAt25 <- rbind(allBlocksPrAt25, PrAt25)
}

graph_groups <- list(
  list("1.0", "0.0", "irreg 100-0"),
  list("0.75", "0.25", "irreg 75-25")
)

for (group in graph_groups) {
  inGro <- group[1]
  btwGro <- group[2]
  name <- group[3]
  
  AvgErr <- read.csv(paste("evaluation_result/input_data/irreg_block_graphs_", inGro, "g_", btwGro, "ng/average_error_link_prediction.csv", sep = ""))
  
  AvgErr$graph_group = paste(name)
  allBlocksAvgErr <- rbind(allBlocksAvgErr, AvgErr)
  
  PrAt10 <- read.csv(paste("evaluation_result/input_data/irreg_block_graphs_", inGro, "g_", btwGro, "ng/precision_at_k_10_link_prediction.csv", sep = ""))
  
  PrAt10$graph_group = paste(name)
  allBlocksPrAt10 <- rbind(allBlocksPrAt10, PrAt10)

  PrAt15 <- read.csv(paste("evaluation_result/input_data/irreg_block_graphs_", inGro, "g_", btwGro, "ng/precision_at_k_15_link_prediction.csv", sep = ""))
  
  PrAt15$graph_group = paste(name)
  allBlocksPrAt15 <- rbind(allBlocksPrAt15, PrAt15)

  PrAt25 <- read.csv(paste("evaluation_result/input_data/irreg_block_graphs_", inGro, "g_", btwGro, "ng/precision_at_k_25_link_prediction.csv", sep = ""))
  
  PrAt25$graph_group = paste(name)
  allBlocksPrAt25 <- rbind(allBlocksPrAt25, PrAt25)
}

randomGeoAvgErr <- read.csv("evaluation_result/input_data/geometric_graphs/average_error_link_prediction.csv")
randomGeoAvgErr$graph_group = paste("random geometric")
allBlocksAvgErr <- rbind(allBlocksAvgErr, randomGeoAvgErr)

randomGeoPreAt10 <- read.csv("evaluation_result/input_data/geometric_graphs/precision_at_k_10_link_prediction.csv")
randomGeoPreAt10$graph_group = paste("random geometric")
allBlocksPrAt10 <- rbind(allBlocksPrAt10, randomGeoPreAt10)

randomGeoPreAt15 <- read.csv("evaluation_result/input_data/geometric_graphs/precision_at_k_15_link_prediction.csv")
randomGeoPreAt15$graph_group = paste("random geometric")
allBlocksPrAt15 <- rbind(allBlocksPrAt15, randomGeoPreAt15)

randomGeoPreAt25 <- read.csv("evaluation_result/input_data/geometric_graphs/precision_at_k_25_link_prediction.csv")
randomGeoPreAt25$graph_group = paste("random geometric")
allBlocksPrAt25 <- rbind(allBlocksPrAt10, randomGeoPreAt25)

#write.csv(allBlocksAvgErr, file = "evaluation_result/input_data/all_graphs_avgErr.csv", row.names = FALSE)
#write.csv(allBlocksPrAt10, file = "evaluation_result/input_data/all_graphs_PrAt10.csv", row.names = FALSE)
#write.csv(allBlocksPrAt15, file = "evaluation_result/input_data/all_graphs_PrAt15.csv", row.names = FALSE)
#write.csv(allBlocksPrAt25, file = "evaluation_result/input_data/all_graphs_PrAt25.csv", row.names = FALSE)

ggplot(allBlocksAvgErr, aes(x=graph_group, y=f_score, fill=embedder)) + 
  geom_boxplot()
ggsave("evaluation_result/all_graphs_avgErr.pdf", width = 16)
ggplot(allBlocksPrAt10, aes(x=graph_group, y=pk_ratio, fill=embedder)) + 
  geom_boxplot()
ggsave("evaluation_result/all_graphs_PrAt10.pdf", width = 16)
ggplot(allBlocksPrAt15, aes(x=graph_group, y=pk_ratio, fill=embedder)) + 
  geom_boxplot()
ggsave("evaluation_result/all_graphs_PrAt15.pdf", width = 16)
ggplot(allBlocksPrAt25, aes(x=graph_group, y=pk_ratio, fill=embedder)) + 
  geom_boxplot()
ggsave("evaluation_result/all_graphs_PrAt25.pdf", width = 16)

dev.off()