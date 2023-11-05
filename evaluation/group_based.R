#!/usr/bin/env Rscript

library(tidyverse)
library(dplyr)

args <- commandArgs()
data_path <- args[6]
path <- file.path(data_path, "output/all_graphs.csv")
metrics <- args[7:length(args)]

if (file.exists(path)) {
  for (metric in metrics) {
    data <- read.csv(path)
    data <- subset(data, type == metric)

    data <- data %>% mutate(Embedder_SimMetric = paste(embedder, similarity_metric, sep = "#"))

    ggplot(data, aes(x = group, y = value, fill = Embedder_SimMetric)) +
      geom_boxplot() + 
      labs(y = metric)
    ggsave(file.path("data/output", paste(metric, ".pdf", sep = "")), width = 16)
  }
}