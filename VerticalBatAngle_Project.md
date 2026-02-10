## Context-Neutral Vertical Bat Angle Modeling from Swing-Level Tracking Data

**Project Description:**  
This project estimates a context-neutral (intrinsic) Vertical Bat Angle (VBA) for each batter-side by separating swing-plane tendencies from pitch-level factors that influence observed bat angle. The objective is to produce stable, interpretable batter-side benchmarks that are not overly sensitive to pitch location, pitch type, velocity, or count context.

The adjusted VBA estimates are then explored in relation to batter-side performance metrics to assess whether certain swing-plane tendencies are associated with consistent differences in batted-ball outcomes or approach metrics, and how these insights could be applied in player evaluation, development, or advance scouting.

---

## 1. Data Description

### 1.1 Swing-Level Tracking Information  
The analysis leverages swing-level tracking information describing bat-path behavior and pitch context. Rather than treating observed bat angle as a static trait, this information allows swing-plane variation to be evaluated in the context of pitch location, pitch characteristics, and game situation.

### 1.2 Batter-Side Performance Metrics  
To contextualize intrinsic swing-plane tendencies, batter-side performance summaries were used to examine how adjusted VBA relates to batted-ball behavior and plate approach. Metrics capture aspects of contact quality, launch-angle behavior, and approach tendencies at the batter-side level.

---

## 2. Analytical Approach

### 2.1 Why Context-Neutral VBA?  
Observed VBA reflects both a hitter’s underlying swing plane and situational adjustments driven by pitch characteristics. Without adjustment, simple averages can be biased by differences in pitch mix, zone distribution, and count context.

This analysis aims to isolate the batter-side component of VBA by explicitly modeling pitch-level effects.

### 2.2 Mixed-Effects Modeling  
A mixed-effects framework was used to estimate intrinsic VBA while stabilizing estimates for batter-sides with uneven swing counts.

- **Fixed effects:** pitch location, velocity, movement, count, and pitch type  
- **Random intercept:** batter-side (batter × stance)

This approach pools information across swings and shrinks small-sample batter-sides toward the population mean, reducing noise-driven extremes.

---

## 3. Results and Interpretation

### 3.1 Pitch-Context Drivers of Observed VBA 
Pitch location, particularly vertical location, along with pitch type and velocity explains a substantial portion of swing-to-swing variation in VBA. Once these factors are controlled for, remaining between–batter-side differences are smaller and more stable.

### 3.2 Intrinsic VBA and Performance Metrics  
Adjusted VBA estimates were evaluated against batter-side performance metrics to examine whether intrinsic swing-plane tendencies align with consistent differences in on-field outcomes.

Most relationships were modest, reinforcing that VBA functions primarily as a mechanical trait rather than a direct performance driver. However, directional tendencies provide useful context for:

- identifying swing-plane profiles associated with greater launch-angle consistency or variability  
- pairing hitter swing characteristics with opposing pitch environments  
- framing individualized development targets  

<img src="images/Baseball/VBA_distribution.png?raw=true"/>

*Relationship between intrinsic vertical bat angle and launch-angle variability.*

---

## 4. Practical Implications

- **Player Evaluation:** Context-neutral VBA enables fairer comparison across hitters by reducing pitch-environment bias  
- **Player Development:** Intrinsic VBA provides a stable mechanical reference for monitoring swing changes over time  
- **Advance Scouting:** Pairing intrinsic VBA with opponent pitch profiles can help contextualize matchup advantages  

---

*Tools used: Python (pandas, numpy, statsmodels, matplotlib)*

**[➡️ Sample Python Script (Mixed-Effects VBA Modeling)](https://github.com/annabusatto/annabusatto.github.io/blob/master/code/vba_mixed_effects_sample.py)**
