# Breat Cancer- Group_A1_43

## Group Members 
| Nome                                      | Up        |
|-------------------------------------------|-----------|
| Francisca Horta Guimarães                 | 202004229 |
| Inês Alexandre Queirós Matos Macedo de Oliveira | 202103343 |
| Miguel Filipe Rodrigues dos Santos  | 202008450 |


## Overview
This project focuses on the application of machine learning models for supervised learning to predict breast cancer. It involves key stages of data analysis, model development, and evaluation using data sourced from Kaggle:

[Breast Cancer Dataset](https://www.kaggle.com/datasets/adhamelkomy/breast-cancer?resource=download)

### Key Components
1. Business Understanding
2. Data Understanding
3. Data Preparation
4. Modeling
5. Evaluation

---

## Related Work

- Consulted the Kaggle dataset and documentation for an in-depth understanding of the data.
- Explored scikit-learn documentation for insights into algorithms and model implementation.
- Reviewed practical guides on feature selection and outlier handling:
  - [Feature Selection Techniques](https://www.geeksforgeeks.org/feature-selection-techniques-in-machine-learning/)
  - [Handling Outliers](https://www.analyticsvidhya.com/blog/2021/05/feature-engineering-how-to-detect-and-remove-outliers-with-python-code/)

---

## Tools and Algorithms

### Libraries
- **Pandas**: Data manipulation and analysis.
- **Seaborn**: Data visualization.
- **Matplotlib**: Visualization and plotting.
- **Scikit-learn**: Machine learning algorithms and utilities.
- **NumPy**: Scientific computing.

### Algorithms
- **Decision Trees**: For classification and regression tasks.
- **Neural Networks**: Inspired by the structure of the human brain.
- **K-Nearest Neighbors (KNN)**: Simple classification and regression model.
- **Support Vector Machines (SVM)**: Finds an optimal hyperplane for classification.
- **Random Forest**: Ensemble of decision trees for robust performance.

---

## Business Understanding & Data Understanding

### Goals
1. Build an accurate model to predict breast cancer.
2. Identify key features for clinical use.

### Dataset Insights
- **Total Entries**: 569
- **Labels**:
  - 62.7% Benign (B)
  - 37.3% Malignant (M)
- **Attributes**: 32
- **Quality**: Clean, no NULL/NaN values.
- **Challenges**:
  - Address potential outliers.
  - Balance the dataset.

### Metrics for Evaluation
- **Accuracy**: Overall correctness.
- **Precision**: Correct identification of malignant cases.
- **Recall**: Capture of all actual malignant cases.
- **F1 Score**: Balance of precision and recall.
- **Confusion Matrix**: Detailed performance analysis.

---

## Data Preparation

### Outlier Detection and Handling
- Methods Used:
  - **Z-Score**
  - **Interquartile Range (IQR)**
- **Results**: 13% identified as outliers, replaced with median values to retain dataset size.

### Recursive Feature Elimination (RFE)
- Selected the top 10 significant features to reduce noise and improve performance.

### Data Balancing
- Techniques Explored:
  - **Undersampling**: Reduced majority class instances.
  - **Oversampling**: Replicated minority class instances.
  - **SMOTE**: Generated synthetic samples for the minority class. Chosen for its balance of data retention and diversity.

---

## Modeling

### Normalization
- Used **StandardScaler** to standardize feature scales and improve consistency.

### Cross-Validation
- **Stratified K-Fold**: Ensured balanced distribution of the target variable.

### Parameter Tuning
- **Grid Search with Cross-Validation**: Explored all parameter combinations for optimal model performance.

---

## Results and Evaluation

### Model Performance
| Model             | Accuracy | Precision | Recall | F1 Score |
|-------------------|----------|-----------|--------|----------|
| Decision Trees    | High     | Moderate  | High   | Moderate |
| Neural Networks   | High     | Moderate  | High   | High     |
| K-Nearest Neighbors (KNN) | Moderate | Low       | High   | Moderate |
| Support Vector Machines (SVM) | High     | High     | High   | High     |
| Random Forest     | Highest  | High      | High   | High     |

### Optimal Models
- **Random Forest**: Best accuracy and recall.
- **Neural Networks**: Strong recall and F1 score.
- **SVM**: High accuracy and balanced metrics.

### Model Time Comparison
| Model             | Training Time | Testing Time |
|-------------------|---------------|--------------|
| Decision Trees    | Low           | Very Low     |
| Neural Networks   | High          | Very Low     |
| KNN               | Very Low      | High         |
| SVM               | Low           | Very Low     |
| Random Forest     | High          | Low          |

---

## Conclusions

1. **Optimal Model**: Random Forest, chosen for high accuracy and reliability.
2. **Alternative Models**:
   - **Neural Networks**: Effective for frequent predictions.
   - **SVM**: Quick training and testing.
3. Dataset size limited generalizability. Larger datasets could improve model robustness.

This project provided hands-on experience in machine learning and its application to breast cancer detection, offering a strong foundation for future research.

