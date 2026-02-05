# playerload.R
# ------------------------------------------------------------
# Feature importance modeling for external load (Catapult GPS)
# - Trains a Random Forest within each positional group
# - Predicts Total.Player.Load using workload features
# - Outputs a clean variable-importance table + plot
#
# Notes:
# - This script is intentionally "portfolio-safe":
#   - no team identifiers
#   - no athlete identifiers
#   - no local file paths
# ------------------------------------------------------------

suppressPackageStartupMessages({
  library(dplyr)
  library(ggplot2)
  library(randomForest)
})

# -----------------------------
# 1) Load data
# -----------------------------
# Expecting a flat table with at least:
# - Position.Group
# - Total.Player.Load
# - Player.Load.Per.Minute (optional, can be excluded)
#
# Example:
# df <- read.csv("data/catapult_full_sessions.csv")

df <- read.csv("path/to/your/catapult_full_sessions.csv")

# -----------------------------
# 2) Helper functions
# -----------------------------

# Keep only numeric features + required columns
prep_group_data <- function(data, group_name, target = "Total.Player.Load",
                            drop_vars = c("Total.Player.Load")) {
  d <- data %>%
    filter(Position.Group == group_name) %>%
    # keep target + numeric predictors
    select(Position.Group, all_of(target), where(is.numeric))

  # Remove rows with missing values in any remaining columns
  d <- d %>% tidyr::drop_na()

  # Remove leakage / redundant vars
  # NOTE: add or remove items here depending on what columns exist in your export
  drop_exact <- c(
    # player-load-derived metrics 
    "Average.Player.Load..Session.",
    "Average.Player.Load..1D.Fwd...Session.",
    "Average.Player.Load..1D.Side...Session.",
    "Average.Player.Load..1D.Up...Session.",
    "Average.Player.Load..2D...Session.",
    "Player.Load..1D.Fwd.",
    "Player.Load..1D.Side.",
    "Player.Load..1D.Up.",
    "Player.Load..2D.",
    "Peak.Player.Load",
    "Equivalent.Distance",
    "Period.Count",
    "Period.Number",
    # exertion / ratio metrics
    "Exertion.Index",
    "Exertion.Index.Per.Minute",
    "Work.Rest.Ratio"
  )

  # Remove columns explicitly dropped in analysis
  drop_all <- unique(c(drop_exact, drop_vars))

  d <- d %>%
    select(-any_of(drop_all))

  # Remove bands / low / slow columns
  d <- d %>%
    select(-matches("Band\\.1|Band\\.2|Band\\.3|Low|Slow", ignore.case = TRUE))

  d
}

fit_rf_importance <- function(d, target = "Total.Player.Load", ntree = 500, seed = 123) {
  set.seed(seed)

  # Build design matrix
  x <- d %>% select(-all_of(target))
  y <- d[[target]]

  rf <- randomForest(x = x, y = y, importance = TRUE, ntree = ntree)

  imp <- importance(rf)
  imp_df <- as.data.frame(imp) %>%
    tibble::rownames_to_column("feature") %>%
    arrange(desc(`%IncMSE`))

  list(model = rf, importance = imp_df)
}

plot_importance <- function(imp_df, group_name, top_n = 20) {
  p <- imp_df %>%
    slice_head(n = top_n) %>%
    ggplot(aes(x = reorder(feature, `%IncMSE`), y = `%IncMSE`)) +
    geom_col() +
    coord_flip() +
    labs(
      title = paste0("Top Features Driving Total Player Load (", group_name, ")"),
      x = NULL,
      y = "% Increase in MSE (Random Forest Importance)"
    ) +
    theme_minimal()

  p
}

# -----------------------------
# 3) Run by positional group
# -----------------------------
groups <- sort(unique(df$Position.Group))

results <- lapply(groups, function(g) {
  d_g <- prep_group_data(
    data = df,
    group_name = g,
    target = "Total.Player.Load",
    drop_vars = c("Total.Player.Load", "Player.Load.Per.Minute")
  )

  fit <- fit_rf_importance(d_g, target = "Total.Player.Load", ntree = 500)

  list(
    group = g,
    importance = fit$importance,
    plot = plot_importance(fit$importance, g, top_n = 20)
  )
})

# -----------------------------
# 4) Output (example)
# -----------------------------
# Print top 10 features per group
for (r in results) {
  cat("\n----------------------------\n")
  cat("Group:", r$group, "\n")
  print(r$importance %>% select(feature, `%IncMSE`, IncNodePurity) %>% head(10))
}

# Save plots (optional)
# dir.create("outputs", showWarnings = FALSE)
# for (r in results) {
#   ggsave(
#     filename = file.path("outputs", paste0("importance_", r$group, ".png")),
#     plot = r$plot, width = 8, height = 6, dpi = 300
#   )
# }
