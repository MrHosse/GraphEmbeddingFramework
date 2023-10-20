#!/usr/bin/env Rscript

#install.packages("tidyverse")
#install.packages("dplyr")

library(tidyverse)
library(dplyr)

args <- commandArgs()
path <- args[6]
metrics <- args[7:length(args)]

if (file.exists(path)) {
  for (metric in metrics) {
    metric_split <- strsplit(metric, "#")[[1]]
    eval_name <- metric_split[1]
    eval_type <- metric_split[2]

    data <- read.csv(path)
    data <- subset(data, type == eval_type)

    data <- data %>% mutate(Embedder_SimMetric = paste(embedder, similarity_metric, sep = "#"))

    ggplot(data, aes(x = group, y = value, fill = Embedder_SimMetric)) +
      geom_boxplot() + 
      labs(y = eval_type)
    ggsave(file.path("output", paste(eval_name, ".pdf", sep = "")), width = 16)
  }
}