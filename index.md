<a id="top"></a>
# Portfolio

Applied sports analytics and biomechanics projects alongside doctoral research in uncertainty quantification, inverse modeling, and machine learning for physiological systems.

**Explore:**
<br>
[🏈 Sports Data Science & Analytics](#sports)
<br>
[🎓 PhD Research & Publications](#phd)

---

<a id="sports"></a>
## Sports Data Science & Analytics

---

### Football

[Closing the Window: A position-aware metric that quantifies how defenders reduce a receiver’s space and opportunity while the ball is in the air](https://kaggle.com/competitions/nfl-big-data-bowl-2026-analytics/writeups/closing-the-window)

<small>Developed for the NFL Big Data Bowl 2026 (Analytics Track), this project uses player-tracking data to measure defensive influence during the ball’s flight, capturing how coverage players restrict receiver options before the ball arrives. By modeling space, angles, and reachability frame-by-frame, it surfaces hidden defensive impact that traditional outcome-based metrics miss and connects late-window disruption to reduced completion rates.
</small>

<img src="images/BDB/defenders_distribution.png?raw=true"/>

---

[Collegiate Football Training and Practice Loads](/FB_PlayerLoadProject)

<small>
Applied analysis of training and practice load in Division I collegiate football, focused on identifying the primary drivers of total player load and player load per minute across positions. The project examines how different movement and intensity variables contribute to workload profiles, with the goal of supporting more efficient and sustainable training design.
</small>
<br><br>
<img src="images/CFB-training-load/dashboard.jpg?raw=true"/>

---

[Case Studies of Asymmetry, Performance, and Injury in Collegiate Football Players](/FB_CaseStudies)

<small>
Longitudinal case studies of two Division I collegiate football players examining relationships between movement asymmetry, performance metrics, and injury events across multiple competitive seasons. Using force plate, GPS, NordBord, hydration, and injury data, the project explores how athlete-specific asymmetry and workload patterns evolve over time and highlights the value of individualized monitoring over population-level thresholds.
</small>

<img src="images/AthleteProfiling/playerLoad.jpg?raw=true"/>

---

### Basketball

[NBA Schedule Intensity & Recovery Stress Modeling (R Shiny App)](/ScheduleIntensity_Project)

<small>
Analysis of NBA schedules focused on quantifying how game density, travel, and recovery windows contribute to cumulative workload stress across a season. The project introduces a schedule intensity framework and an interactive R Shiny app that allows users to explore schedule-driven stress patterns for any NBA team over time.
</small>
<br><br>
<img src="images/ScheduleIntensity/dashboard_overview.png?raw=true"/>

---

### Baseball

[Context-Neutral Vertical Bat Angle Modeling from Swing-Level Tracking Data](/VerticalBatAngle_Project)

<small>
This project develops a context-neutral estimate of hitters’ intrinsic vertical bat angle by separating swing mechanics from pitch-level context such as location, velocity, movement, count, and pitch type. A mixed-effects modeling framework is used to stabilize estimates across uneven sample sizes and produce interpretable batter-side benchmarks that are robust to situational noise. The resulting adjusted bat-angle estimates are explored in relation to batted-ball and plate-discipline metrics to inform player evaluation, development, and advance scouting.
</small>

<img src="images/Baseball/VBA_distribution.png?raw=true"/>

---

[Drive-Foot Force-Plate Profiling and Pitch Velocity](/Pitching_ForcePlate_Project)

<small>
Analysis of high-frequency force-plate data focused on characterizing how drive-foot force and torque profiles relate to pitch velocity. The project extracts interpretable biomechanical features including peak forces, rate of force development, impulses, and timing relative to ball release, with all forces normalized by body weight and aligned to a common mechanical reference point. Results highlight the importance of force timing and explosiveness over magnitude alone and demonstrate how complex time-series biomechanics can be translated into coach-facing, actionable insights.
</small>

<img src="images/Baseball/force_profile_example.png?raw=true"/>

---

### Other Sports

[Longitudinal Force Plate Profiling of Asymmetry and Performance in Collegiate Athletes](/AthleteProfiling_ForcePlate)

<small>
Longitudinal analysis of force plate–derived asymmetry and performance metrics in male and female Division I collegiate athletes across multiple sports. Using countermovement and single-leg jump data collected between 2020–2025, the project examines how asymmetry evolves over time, compares trends across sports and sex, and evaluates relationships between asymmetry and performance outputs. Results highlight consistent structure in asymmetry metrics, weak group-level associations with performance, and the importance of individual athlete monitoring for applied decision-making.
</small>

<img src="images/AthleteProfiling/asymmetry.jpg?raw=true"/>


---


[End-of-Year Performance Analysis for Collegiate Gymnastics](/Gymnastics_Report)

<small>Project completed for a Division I collegiate gymnastics team, integrating competition scores, force plate metrics, injury logs, treatments, DEXA scans, and mental health data to highlight key performance trends and support planning around athlete health and readiness.</small>

<img src="images/Gymnastics/overview-figure.png?raw=true"/>
*Figure 1: Injury percentage by phase and weekly treatment frequency for the season.*
<br>

<div style="text-align:right; margin-top: 20px;">
  <a href="#top" style="font-size: 0.85em; text-decoration: none; color: #666;">
    Back to top ↑
  </a>
</div>

---

<a id="phd"></a>
## PhD Research & Publications

---

My doctoral research focused on cardiovascular electrophysiology and the mechanisms underlying sudden cardiac death. Through controlled experimental models, I investigated how conduction system abnormalities and ischemic trigger events contribute to arrhythmogenesis.

This work required rigorous experimental design, high-fidelity physiological data collection, quantitative analysis, and reproducible validation practices.

🔗 [Google Scholar](https://scholar.google.com/citations?user=2RCONMQAAAAJ&hl=en)

---

### Dissertation  

**The Role of the Conduction System and Trigger Events Leading to Sudden Cardiac Death**

My dissertation examined how ischemic stress and conduction system dynamics interact to produce arrhythmic events. Using structured experimental protocols, I evaluated how graded physiological stress influences conduction patterns and cardiac instability.

**Core Contributions:**

- Designed and executed IACUC-approved experimental protocols for controlled myocardial ischemia  
- Developed structured ischemic stress and recovery paradigms  
- Analyzed high-resolution physiological recordings to quantify conduction and arrhythmic behavior  
- Implemented rigorous statistical evaluation and reproducibility standards  
- Ensured compliance with institutional regulatory oversight for preclinical research  

This work emphasized mechanistic clarity, controlled experimentation, and careful interpretation of complex biological signals.

---

### First-Author Publications  

---

#### Predicting Ventricular Arrhythmia in Myocardial Ischemia Using Deep Learning  

**Busatto, A.**, et al.  
*Heart Rhythm O2* (Accepted)

🔗 [Project Repository (SkipAlert)](https://github.com/annabusatto/SkipAlert)

Developed an LSTM-based time-to-event prediction framework for premature ventricular contractions (PVCs) during acute ischemia.

- Stacked LSTM architecture for temporal modeling  
- Continuous time-to-event regression formulation  
- Pooled cross-validation with subject-specific fine-tuning  
- MAE ≈ 4–6 seconds  
- Integrated physiological interpretation with ML outputs  

---

#### Reconstructing Ventricular Activation Sequences from Epicardial Data: Insights from Geodesic Back-Propagation Optimization in Porcine Models  

**Busatto, A.**, et al.  
*Computers in Biology and Medicine*  

🔗 [Published Article](https://www.sciencedirect.com/science/article/pii/S0010482525015318)

*Co-First Author*

Evaluated inverse reconstruction of volumetric ventricular activation using modified geodesic back-propagation and eikonal propagation models.

- Inferred earliest activation sites from epicardial surface data  
- Validated against intramural recordings  
- Quantified instability and ill-posedness of inverse solutions  
- Identified need for physiological priors in digital twin reconstruction  

---

#### Uncertainty Quantification of Conduction Velocity in Models of Cardiac Spread of Activation  

**Busatto, A.**, et al.  
*Medical & Biological Engineering & Computing* (Under Review)

Developed a polynomial chaos expansion (PCE)–based uncertainty quantification framework for ventricular activation modeling.

- Sobol global sensitivity analysis  
- Large-scale eikonal simulations  
- Characterized spatial heterogeneity in activation-time variance  
- Established CV parameter-prioritization strategies

<div style="text-align:right; margin-top: 20px;">
  <a href="#top" style="font-size: 0.85em; text-decoration: none; color: #666;">
    Back to top ↑
  </a>
</div>

<!-- ### Category Name 2

- [Project 1 Title](http://example.com/)
- [Project 2 Title](http://example.com/)
- [Project 3 Title](http://example.com/)
- [Project 4 Title](http://example.com/)
- [Project 5 Title](http://example.com/)

---
-->


<!--
---
<p style="font-size:11px">Page template forked from <a href="https://github.com/evanca/quick-portfolio">evanca</a></p> -->
<!-- Remove above link if you don't want to attibute -->
