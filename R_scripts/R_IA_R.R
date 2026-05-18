library(dplyr)
library(arrow)

args <- commandArgs(trailingOnly = TRUE)

origen_dinamico  <- if(length(args) >= 1) args[1] else "JFK"
destino_dinamico <- if(length(args) >= 2) args[2] else "LAX"

# Cargar datos
vuelos <- read_feather("vuelos_2024_sample.feather")

resumen <- vuelos %>%
  filter(origin == origen_dinamico & dest == destino_dinamico) %>%
  filter(!is.na(arr_delay)) %>%
  group_by(aerolinea) %>%
  summarise(
    retraso_medio = round(mean(arr_delay), 1),
    pct_retraso   = round(mean(arr_delay > 0) * 100, 1),
  ) %>%
  arrange(retraso_medio)

write.csv(resumen, "resultado_r.csv", row.names = FALSE)
cat("OK\n")