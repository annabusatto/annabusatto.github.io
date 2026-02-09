## Longitudinal Force Plate Profiling of Asymmetry and Performance  
*Collegiate athletes across sports, sex, and competitive seasons*

### Project Overview

This project examined longitudinal changes in force-plate–derived asymmetry and performance metrics in Division I collegiate athletes across multiple sports. Using countermovement jump (CMJ) and single-leg jump data collected between 2020–2025, the analysis focused on athletes with three or more years in the program, allowing for within-athlete comparisons across seasons rather than single time-point evaluations.

The primary goals were to:
- Characterize how asymmetry metrics behave over time  
- Evaluate whether asymmetry meaningfully relates to performance outputs  
- Identify where group-level analysis is limited and individual monitoring becomes most informative

---

## Data Summary

**Population**
- 473 athletes with ≥3 years in the program  
- 227 athletes with ≥4 years  
- Sports included football, basketball, lacrosse, gymnastics, swim & dive, and others  
- Male and female athletes analyzed separately and jointly  

**Testing Modality**
- Dual force plates  
- Countermovement jumps and single-leg jumps  

**Performance Metrics**
- Concentric Peak Force / BM  
- Eccentric Peak Force / BM  
- Peak Power / BM  
- RSI-modified  

**Asymmetry Metrics**
- Concentric Mean Force Asymmetry [% L,R]  
- Eccentric Mean Force Asymmetry [% L,R]  
- Eccentric:Concentric Mean Force Ratio Asymmetry [% L,R]  
- Concentric Peak Force Asymmetry [% L,R]  
- Eccentric Peak Force Asymmetry [% L,R]  
- Force at Zero Velocity Asymmetry [% L,R]  
- CMJ Stiffness Asymmetry [% L,R]  
- Impulse-based asymmetries (braking, takeoff, landing, concentric impulse – 100 ms)

---

## Analysis Workflow

### 1. Data Cleaning & Cohort Construction

- Standardized athlete identifiers and testing dates  
- Removed incomplete records  
- Assigned missing sport labels, substantially increasing usable sample size  
- Added sex classification for subgroup analyses  
- Filtered athletes to those with ≥3 years of testing history  
- Removed extreme outliers using an IQR-based approach  

---

### 2. Exploratory Performance Analysis

Baseline performance metrics were examined prior to asymmetry analysis to establish context.

Key observations:
- Male athletes demonstrated significantly higher normalized force, power, and RSI-modified values compared to female athletes  
- Differences persisted despite normalization by body mass  
- Performance distributions aligned with expected sport-specific demands  

<img src="images/AthleteProfiling/Concentric_Peak_Force___BM_N_kg_comparison_histogram.png?raw=true"/>
<img src="images/AthleteProfiling/Eccentric_Peak_Force___BM_N_kg_comparison_histogram.png?raw=true"/>
<img src="images/AthleteProfiling/Peak_Power___BM_W_kg_comparison_histogram.png?raw=true"/>
<img src="images/AthleteProfiling/RSI-modified_m_s_comparison_histogram.png?raw=true"/>

---

### 3. Asymmetry Structure & Group Differences

To examine how asymmetry metrics behaved across populations:

- One-way ANOVA revealed significant differences between sports for all asymmetry metrics analyzed  
- K-means clustering (k = 6, selected via the elbow method) revealed consistent structure across:
  - Sports  
  - Sex  
  - Testing years  

Notable linear relationships emerged between:
- Concentric Mean Force Asymmetry and Concentric Peak Force Asymmetry  
- Eccentric Mean Force Asymmetry and Eccentric:Concentric Mean Force Ratio Asymmetry  
- Concentric Peak Force Asymmetry and CMJ Stiffness Asymmetry  
- Eccentric Peak Force Asymmetry and Force at Zero Velocity Asymmetry  

Male athletes tended to display more extreme asymmetry outliers, while female athletes showed tighter clustering around the mean.

<img src="images/AthleteProfiling/asymmetry_clusters_pairplot.png?raw=true"/>
<img src="images/AthleteProfiling/sports_asymmetry_clusters_pairplot_fixed.png?raw=true"/>
<img src="images/AthleteProfiling/gender_asymmetry_clusters_pairplot.png?raw=true"/>

---

### 4. Asymmetry vs Performance Relationships

The relationship between asymmetry metrics and performance outputs was assessed using correlation and regression analyses.

Findings:
- Correlations between asymmetry and performance metrics were generally low and slightly negative
- Results were consistent across:
  - The full cohort  
  - Male vs female athletes  
  - Individual sports with the largest samples (football, lacrosse, swim & dive)  

Overall, higher asymmetry did not reliably correspond to reduced performance at the group level.

<img src="images/AthleteProfiling/asymmetry-performace-metrics-correlation_heatmap.png?raw=true"/>
<img src="images/AthleteProfiling/scatter_Concentric_Mean_Force_Asymmetry_vs_RSI-modified.png?raw=true"/>

---

### 5. Individual-Level Longitudinal Analysis

As group-level trends flattened, the most informative insights emerged from individual athlete monitoring.

Key observations:
- Athletes within the same sport often exhibited very different asymmetry trajectories  
- Stable performance could coexist with persistent asymmetry  
- Sudden deviations from an athlete’s own baseline were more meaningful than absolute asymmetry magnitude  

To improve interpretability:
- Metrics were averaged per athlete per year
- Individual trajectories were visualized within specific sports (e.g., men’s and women’s basketball)

<img src="images/AthleteProfiling/individual_basketball.png?raw=true"/>
<img src="images/AthleteProfiling/basketball_avg_example.png?raw=true"/>

---

## Key Takeaways

- Asymmetry metrics show strong internal structure but weak relationships with performance at the group level  
- Sex and sport differences exist, but overall trends remain consistent  
- Individual longitudinal analysis provides the clearest signal for applied monitoring  
- Asymmetry is best interpreted as a contextual monitoring variable, not a standalone risk or performance indicator  

---

## Practical Implications

- Population-based asymmetry thresholds may be misleading  
- Athlete-specific baselines are more informative than cross-sectional comparisons  
- Force plate data is most valuable when used for trend monitoring and decision support, not binary screening  

---

## Limitations & Future Work

- Injury data was unavailable, limiting direct injury-risk modeling  
- Future extensions could integrate:
  - Injury logs  
  - Training load metrics  
  - Shorter rolling analysis windows (2–3 years)  
  - Expanded single-leg jump analysis  

These additions would allow for stronger applied inference and more actionable athlete management strategies.

