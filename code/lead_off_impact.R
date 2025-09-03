

# Lead-off Impact Analysis (R)
# ----------------------------
# This script builds tidy per-routine data, computes athlete baselines,
# and estimates the effect of the lead-off routine on teammates' routines
# later in the lineup (positions 2–6). It also outputs event-specific
# slopes and simple diagnostics.
#
# How to use:
# 1) Install packages if needed:
#    install.packages(c("tidyverse","readxl","lme4","broom.mixed","lubridate"))
# 2) Set your working directory to the folder with the two Excel files or
#    update the paths below.
# 3) Source this file in RStudio (source("lead_off_impact.R")).

suppressPackageStartupMessages({
  library(tidyverse)
  library(readxl)
  library(lubridate)
  library(lme4)
  library(broom.mixed)
})

# ---- Paths ----
path_individual <- "/Users/anna/Desktop/Individual_Consistency.xlsx"
path_team <- "/Users/anna/Desktop/Team_Consistency.xlsx"

# ---- Load ----
idv <- read_excel(path_individual)
team <- read_excel(path_team)

# Coerce dates
idv <- idv %>% mutate(Date = as_date(Date))
team <- team %>% mutate(Date = as_date(Date))

# ---- Tidy individual scores and positions into long format ----
# Scores
scores_long <- idv %>%
  select(Athlete, Date, ends_with("Score")) %>%
  pivot_longer(cols = ends_with("Score"),
               names_to = "Event",
               values_to = "Score") %>%
  mutate(Event = sub(" Score$", "", Event))

# Positions
pos_long <- idv %>%
  select(Athlete, Date, ends_with("Position")) %>%
  pivot_longer(cols = ends_with("Position"),
               names_to = "Event",
               values_to = "Position") %>%
  mutate(Event = sub(" Position$", "", Event))

# Join
df <- scores_long %>%
  left_join(pos_long, by = c("Athlete","Date","Event")) %>%
  filter(!is.na(Score), !is.na(Position)) %>%
  mutate(Position = as.integer(Position))

# Bring in team context (e.g., Home/Away, Win/Loss) by date
team_ctx <- team %>%
  select(Date, `Home/Away`, `Win/Loss`) %>%
  rename(HomeAway = `Home/Away`, WinLoss = `Win/Loss`)

df <- df %>% left_join(team_ctx, by = "Date")

# ---- Athlete-event baselines (expected score) ----
# Option A (default): overall mean per athlete+event
baselines <- df %>%
  group_by(Athlete, Event) %>%
  summarize(mu = mean(Score, na.rm = TRUE),
            sd = sd(Score, na.rm = TRUE),
            n = n(), .groups = "drop")

df <- df %>%
  left_join(baselines, by = c("Athlete","Event")) %>%
  mutate(Resid = Score - mu)

# ---- Build per-routine dataset with lead-off residuals attached ----
df2 <- df %>%
  group_by(Date, Event) %>%
  mutate(leadoff_resid = Resid[which.min(Position)],
         anchor_resid  = Resid[which.max(Position)],
         n_in_event    = n()) %>%
  ungroup()

# Keep only teammates after lead-off for the main effect model
df_follow <- df2 %>% filter(Position >= 2)

# ---- Mixed-effects model: Does lead-off residual predict teammates' residuals? ----
# Residual ~ lead-off residual + random effects for Athlete, Meet(Date), Event
# Interpretation: slope(leadoff_resid) > 0 implies "contagion/boost" from a strong lead-off.
m <- lmer(Resid ~ leadoff_resid + (1|Athlete) + (1|Date) + (1|Event), data = df_follow)

model_summary <- broom.mixed::tidy(m, effects = "fixed", conf.int = TRUE)

# ---- Event-specific slopes (optional) ----
# Fit a model with per-event slope: Resid ~ 0 + leadoff_resid:Event + random effects
m_event <- lmer(Resid ~ 0 + leadoff_resid:Event + (1|Athlete) + (1|Date), data = df_follow)
event_slopes <- broom.mixed::tidy(m_event, effects = "fixed", conf.int = TRUE) %>%
  separate(term, into = c("x","Event"), sep=":") %>%
  select(Event, estimate, conf.low, conf.high, std.error) %>%
  arrange(Event)

# ---- Simple "hit" analysis (binary threshold) ----
# Define a hit threshold (tweak as needed)
hit_thresholds <- c(Vault = 9.80, Bar = 9.80, Beam = 9.80, Floor = 9.85)

df2 <- df2 %>%
  mutate(Hit = Score >= recode(Event,
                               !!!setNames(hit_thresholds, names(hit_thresholds))))

# For each meet+event, compute whether lead-off hit and how teammates did vs baseline
lead_follow <- df2 %>%
  group_by(Date, Event) %>%
  summarize(leadoff_hit = any(Hit & Position==1),
            follow_mean_resid = mean(Resid[Position>=2], na.rm=TRUE),
            .groups="drop")

hit_effect <- lead_follow %>%
  group_by(Event) %>%
  summarize(
    mean_follow_resid_if_leadoff_hit    = mean(follow_mean_resid[leadoff_hit], na.rm=TRUE),
    mean_follow_resid_if_leadoff_miss   = mean(follow_mean_resid[!leadoff_hit], na.rm=TRUE),
    diff = mean_follow_resid_if_leadoff_hit - mean_follow_resid_if_leadoff_miss,
    n_events = n(),
    .groups="drop"
  ) %>% arrange(Event)

# ---- Save outputs ----
out_dir <- "/Users/anna/Desktop/lead_off_outputs"
if (!dir.exists(out_dir)) dir.create(out_dir)

write_csv(df2, file.path(out_dir, "routines_long.csv"))
write_csv(model_summary, file.path(out_dir, "mixed_model_summary.csv"))
write_csv(event_slopes, file.path(out_dir, "event_slopes.csv"))
write_csv(hit_effect, file.path(out_dir, "hit_effect.csv"))

# ---- Console prints ----
cat("\n=== Mixed model: teammates' residual ~ leadoff residual ===\n")
print(model_summary)

cat("\n=== Event-specific slopes (leadoff effect per event) ===\n")
print(event_slopes)

cat("\n=== Hit effect summary (difference in teammates' mean residual when leadoff hits) ===\n")
print(hit_effect)

cat("\nOutputs written to: ", normalizePath(out_dir), "\n")
