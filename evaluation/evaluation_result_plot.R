install.packages("tidyverse")

library(tidyverse)

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
  name <- group[3]
  
  AvgErr <- read.csv(paste("evaluation_result/input_data/5_10_graphs_", inGro, "g_", btwGro, "ng/average_error_link_prediction.csv", sep = ""))
  
  AvgErr$name = paste(name)
  allBlocksAvgErr <- rbind(allBlocksAvgErr, AvgErr)
  
  PrAt10 <- read.csv(paste("evaluation_result/input_data/5_10_graphs_", inGro, "g_", btwGro, "ng/precision_at_k_10_link_prediction.csv", sep = ""))
  
  PrAt10$name = paste(name)
  allBlocksPrAt10 <- rbind(allBlocksPrAt10, PrAt10)

  PrAt15 <- read.csv(paste("evaluation_result/input_data/5_10_graphs_", inGro, "g_", btwGro, "ng/precision_at_k_15_link_prediction.csv", sep = ""))
  
  PrAt15$name = paste(name)
  allBlocksPrAt15 <- rbind(allBlocksPrAt15, PrAt15)

  PrAt25 <- read.csv(paste("evaluation_result/input_data/5_10_graphs_", inGro, "g_", btwGro, "ng/precision_at_k_25_link_prediction.csv", sep = ""))
  
  PrAt25$name = paste(name)
  allBlocksPrAt25 <- rbind(allBlocksPrAt25, PrAt25)
}

randomGeoAvgErr <- read.csv("evaluation_result/input_data/geometric_graphs/average_error_link_prediction.csv")
randomGeoAvgErr$name = paste("random geometric")
allBlocksAvgErr <- rbind(allBlocksAvgErr, randomGeoAvgErr)

randomGeoPreAt10 <- read.csv("evaluation_result/input_data/geometric_graphs/precision_at_k_10_link_prediction.csv")
randomGeoPreAt10$name = paste("random geometric")
allBlocksPrAt10 <- rbind(allBlocksPrAt10, randomGeoPreAt10)

randomGeoPreAt15 <- read.csv("evaluation_result/input_data/geometric_graphs/precision_at_k_15_link_prediction.csv")
randomGeoPreAt15$name = paste("random geometric")
allBlocksPrAt15 <- rbind(allBlocksPrAt15, randomGeoPreAt15)

randomGeoPreAt25 <- read.csv("evaluation_result/input_data/geometric_graphs/precision_at_k_25_link_prediction.csv")
randomGeoPreAt25$name = paste("random geometric")
allBlocksPrAt25 <- rbind(allBlocksPrAt10, randomGeoPreAt25)

write.csv(allBlocksAvgErr, file = "evaluation_result/input_data/5_10_graphs_all_avgErr.csv", row.names = FALSE)
write.csv(allBlocksPrAt10, file = "evaluation_result/input_data/5_10_graphs_all_PrAt10.csv", row.names = FALSE)
write.csv(allBlocksPrAt15, file = "evaluation_result/input_data/5_10_graphs_all_PrAt15.csv", row.names = FALSE)
write.csv(allBlocksPrAt25, file = "evaluation_result/input_data/5_10_graphs_all_PrAt25.csv", row.names = FALSE)

ggplot() + 
  geom_boxplot(data = allBlocksAvgErr, mapping = aes(name, f_score, fill=embedder))  + 
  theme( axis.text.x = element_blank()) 