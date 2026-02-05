## Analysis of Training and Practice Load in Division I Collegiate Football

**Project Description:**  
This project analyzed training and practice load data from Division I collegiate football to identify the primary drivers of both total player load and player load per minute across positional groups. The objective was to better understand how different movement- and intensity-based variables contribute to workload accumulation, and how these contributions vary by position.

Using GPS-derived metrics collected during training sessions and practices, the analysis focused on isolating which features most strongly influenced workload outcomes. Emphasis was placed on distinguishing between volume-driven load (total player load) and intensity-driven load (player load per minute) to provide a more nuanced view of training demands.

---

### 1. Data Description

The primary dataset consisted of external workload data collected via Catapult GPS devices worn by players during training sessions and practices. Metrics captured key aspects of movement volume, speed, and intensity commonly used in football performance monitoring.

An initial feature selection process was conducted to identify variables most relevant to player load outcomes. This step was informed by football-specific research and practical relevance, allowing the analysis to focus on a targeted subset of metrics from the broader Catapult variable set.

---

### 2. Analytical Approach

Analyses were conducted at the positional-group level to account for the distinct movement profiles and physical demands associated with different roles. Separate modeling approaches were applied for total player load and player load per minute to differentiate between cumulative workload and intensity-based stress.

Feature importance techniques were used to evaluate which GPS-derived variables most strongly contributed to workload outcomes within each positional group. This enabled direct comparison of workload drivers across groups such as skill positions, bigs, and linemen, highlighting position-specific patterns in training demands.

---

### 3. Results and Interpretation

Results demonstrated that the variables most strongly associated with workload differed meaningfully by position. Metrics related to movement intensity and high-load activity played a larger role in explaining player load per minute, while volume-related metrics contributed more heavily to total player load.

These differences emphasize the importance of position-specific perspectives when evaluating training load, as identical training sessions can impose substantially different stress profiles depending on positional role.

---

### 4. Visualization and Reporting

Findings were communicated through a combination of statistical summaries and interactive visualizations. Feature importance plots were used to clearly illustrate how workload drivers varied across positional groups, supporting interpretation and practical application.

![Feature importance by position](images/CFB-training-load/dashboard.jpg?raw=true)
*Figure: Relative importance of GPS-derived features for predicting player load per minute across positional groups.*

---

### 5. Practical Implications

- Training load is driven by different factors depending on positional role, reinforcing the need for position-specific monitoring and interpretation.
- Evaluating player load per minute provides additional insight beyond total workload by isolating intensity-driven stress.
- Feature-based modeling offers a transparent framework for understanding how training design influences workload accumulation.

---

*Tools used: R (tidyverse, randomForest), Power BI, Catapult GPS exports*
