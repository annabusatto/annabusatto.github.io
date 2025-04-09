## Collegiate Athletes Force Plate Analysis

**Project Description:** This study analyzed changes in asymmetries over time among male and female Division I collegiate athletes from various sports, focusing on those who have been in the program for three or more years. The goal was to identify significant deviations from baseline measurements and assess the associated risk of injury by evaluating several asymmetry and performance metrics.

### 1. Data Description

The data for this project includes:

**Force Plate Data:** Collected from countermovement jumps and single-leg jumps performed by Division I athletes from multiple sports between 2020 and 2025. Key metrics associated with asymmetry and performance were identified, focusing on variables such as Concentric Peak Force Asymmetry, Eccentric Peak Force Asymmetry, Force at Zero Velocity Asymmetry, and Landing Impulse Asymmetry. These metrics were used to investigate asymmetry changes within individual athletes across seasons to predict and prevent injury risks.

### 2. Project Process

1. **Data Cleaning:**
   - Extract information, change date formats, and remove unnecessary columns.
   - Add athletes' gender and player position.
   - Create different data frames for individual sports as needed.
   - Sort athletes who have been in the program for 3+ years.
   - Remove outliers using the IQR (interquartile range) method.

2. **Exploratory Data Analysis:**
   - Analyze performance metrics (Concentric Peak Force / BM, Eccentric Peak Force / BM, Peak Power / BM, RSI-modified) and asymmetry metrics (Concentric Peak Force Asymmetry, Eccentric Peak Force Asymmetry, Force at Zero Velocity Asymmetry, Landing Impulse Asymmetry).
   - Generate descriptive statistics and visualize histograms of differences between male and female athletes.
   - Analyze differences between sports using ANOVA.
   - Visualize asymmetries within each sport using boxplots.
   - Perform cluster analysis based on sport and gender.
   - Determine the optimal number of clusters using the elbow method.
   - Perform KMeans clustering with the optimal number of clusters and visualize the clusters using pair plots.

3. **Data Analysis in Python:**
   - Focus on asymmetry metrics and examine changes over time for individual athletes from football, gymnastics, and men's and women's basketball.
   - Identify when asymmetry changes cross a threshold that could be linked to an increased risk of injury.
   - Calculate correlation coefficients between asymmetry and performance metrics to identify linear relationships.
   - Create correlation heatmaps of asymmetry and performance metrics.
   - Create scatter plots to visually inspect relationships between each pair of asymmetry and performance metrics.
   - Perform regression analysis to quantify relationships between asymmetry and performance metrics.
   - Extend pair plots to include both asymmetry and performance metrics.

4. **Focused Analysis:**
   - Investigate metrics focusing on smaller and different groups to see if trends remain consistent or reveal new insights.
   - Conduct correlation and scatter plot analyses for specific groups such as female or male athletes, football athletes, and lacrosse athletes.



   
<!--
```javascript
if (isAwesome){
  return true
}
```

### 2. Assess assumptions on which statistical inference will be based

```javascript
if (isAwesome){
  return true
}
```

### 3. Support the selection of appropriate statistical tools and techniques

<img src="images/dummy_thumbnail.jpg?raw=true"/>

### 4. Provide a basis for further data collection through surveys or experiments

Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. 

For more details see [GitHub Flavored Markdown](https://guides.github.com/features/mastering-markdown/). -->
