## Drive-Foot Force-Plate Profiling and Pitch Velocity

**Project Description:**  
This project analyzes high-frequency drive-foot force plate data to characterize how lower-body force production and timing relate to pitch velocity. The objective was to translate raw time-series force and torque data into interpretable biomechanical features that explain why some pitchers throw harder than others.

The analysis emphasizes feature extraction, timing alignment, and interpretable modeling, with a focus on producing coach-facing outputs that connect mechanical traits to velocity outcomes.

---

## 1. Data Description

### 1.1 Force Plate Data  
Force plate signals were recorded at high frequency (300 Hz) during pitching deliveries. The dataset includes:

- Ground reaction forces (horizontal and vertical components)  
- Rotational torque about the vertical axis  
- Pitch velocity  
- Pitcher body weight (for normalization)  
- Ball release frame for temporal alignment  

All forces were normalized by body weight to allow comparison across pitchers of different sizes.

---

## 2. Analytical Approach

### 2.1 Temporal Alignment

All force signals were aligned relative to ball release (t = 0).  
A −1.00 s to 0.00 s window was used to capture the full:

- loading phase  
- propulsion phase  
- momentum transfer into release  

This ensured that comparisons reflected mechanically meaningful phases of the delivery rather than arbitrary time windows.

---

### 2.2 Feature Engineering

Per-pitch mechanical features were extracted from the drive-foot force and torque profiles:

- **Peak Forward Force (FY/BW)**  
- **Peak Vertical Force (FZ/BW)**  
- **Peak Rotational Torque (|TZ|)**  
- **Rate of Force Development (RFD)**  
- **Forward and Vertical Impulse**  
- **Time to Peak Forward Force**

These features were designed to quantify:

- magnitude of force production  
- explosiveness (how quickly force is generated)  
- total momentum contribution  
- timing relative to release  

Pitch-level features were then aggregated to the pitcher level to produce stable mechanical profiles.

---

## 3. Results and Interpretation

### 3.1 Drive-Force Characteristics and Velocity

Linear modeling revealed moderate but meaningful relationships between drive-foot mechanics and pitch velocity.

Key findings:

- Higher **Rate of Force Development (RFD)** was positively associated with velocity  
- Peak forward force showed directional association with velocity  
- Total forward impulse was less predictive than timing and explosiveness  
- Rotational torque contributed modestly, suggesting lower-body rotation plays a complementary role  

Overall, the timing and explosiveness of force production appeared more important than magnitude alone.

---

### 3.2 Force–Time Profile Comparisons

Average force-time curves were generated for pitchers and aligned to ball release.

<img src="images/Baseball/force_profile_example.png?raw=true"/>
*Example drive-foot forward force profile aligned to ball release (anonymized).*

Higher-velocity pitchers tended to exhibit:

- smoother, coordinated force buildup  
- forward-force peaks occurring closer to release  
- more synchronized force and torque patterns  

Lower-velocity pitchers often showed:

- earlier or irregular torque peaks  
- less coordinated timing between force and rotation  
- greater variability across pitches  

These profile differences emphasize sequencing and coordination rather than raw force magnitude.

---

## 4. Practical Implications

- **Explosiveness over volume:** Rapid force development is more influential than total impulse accumulation  
- **Timing matters:** Synchronizing force peaks closer to release improves energy transfer  
- **Coordination is critical:** Forward force and rotational torque must align temporally  

These findings support development strategies focused on:

- lead-leg blocking mechanics  
- lower-body rate of force development  
- proximal-to-distal sequencing drills  

---

## 5. Tools Used

*Python (pandas, numpy, matplotlib), linear regression (OLS), time-series feature engineering*

---

## 6. Sample Code

**[➡️ Sample Python Script (Force Plate Feature Engineering + Modeling)](https://github.com/annabusatto/annabusatto.github.io/blob/master/code/force_plate_velocity_sample.py)**
