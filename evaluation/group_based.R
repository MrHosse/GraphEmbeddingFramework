#!/usr/bin/env Rscript

#install.packages("tidyverse")
#install.packages("dplyr")

library(tidyverse)
library(dplyr)

args <- commandArgs()
path <- args[6]
metric <- args[7]
metric_split <- strsplit(metric, "#")[[1]]
eval_type <- metric_split[2]

if (file.exists(path)) {
  data <- read.csv(path)
  data <- subset(data, type == eval_type)

  data <- data %>% mutate(Embedder_SimMetric = paste(embedder, similarity_metric, sep = "#"))

  ggplot(data, aes(x = group, y = value, fill = Embedder_SimMetric)) +
    geom_boxplot() + 
    labs(y = eval_type)
  ggsave(file.path("output", paste(metric, ".pdf", sep = "")), width = 16)
}