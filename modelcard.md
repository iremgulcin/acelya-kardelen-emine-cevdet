---
# MODEL CARD

# Histogram-based Gradient Boost Regression Model
<!-- Provide a quick summary of what the model is/does. -->
The model predicts the number of usage of a given line, in a given date and hour.
<!--{{ model_summary | default("", true) }}-->

## Model Details

### Model Description

<!-- Provide a longer summary of what this model is. -->
Our model uses its training features like date, hour and transfer_type etc. to predict the number of usage for a specified route. 
<!--{{ model_description | default("", true) }}-->

- **Developed by:** Scikit-learn (finetuned by: Açelyanur Şen, Cevdet Eren Özbozkurt)
- **Model date:** 07/02/2024
- **Model type:** Regression model
- **Language(s):** Python, scikit-learn
- **Finetuned from model:** Scikit-learn's Histogram-based gradient boost regression model 

### Model Sources 

<!-- Provide the basic links for the model. -->

- Model creation code can be found [here](https://github.com/iremgulcin/acelya-kardelen-emine-cevdet/blob/main/h_gbr_model.ipynb)


## Uses

<!-- Address questions around how the model is intended to be used, including the foreseeable users of the model and those affected by the model. -->

### Direct Use
Predicting the number of usages for a specific route on a specific date and hour
<!-- This section is for the model use without fine-tuning or plugging into a larger ecosystem/app. 
{{ direct_use | default("[More Information Needed]", true)}}-->

### Downstream Use 

<!-- This section is for the model use when fine-tuned for a task, or when plugged into a larger ecosystem/app -->
The predictions of the model can be used to plan better schedules for transportation routes or better resource management.


### Out-of-Scope Use

<!-- This section addresses misuse, malicious use, and uses that the model will not work well for. -->
Using the model for purposes other than predicting usage, such as pricing. Since the model's predictions are route-level, passenger flow cannot be calculated.


## Bias, Risks, and Limitations

<!-- This section is meant to convey both technical and sociotechnical limitations. -->
- The model only handles categorical features with a maximum cardinality of 255, potentially limiting its applicability to datasets with larger categories.
- The model may struggle with predicting very large or very low usage numbers due to the inherent differences between high and low usage lines in the training data.
- As with any machine learning model, there is a risk of bias based on the training data. Consider the representatives of your training data to potential biases.
<!--{{ bias_risks_limitations | default("[More Information Needed]", true)}}-->

### Recommendations

<!-- This section is meant to convey recommendations with respect to the bias, risk, and technical limitations. -->
- Be aware of the limitations of the model and its potential biases.
- Be mindful of the model's performance on data with different temporal dynamics, considering that it was initially trained using time series cross-validation. Shifts in temporal patterns or changes in the underlying data distribution over time may impact the model's accuracy and reliability. Regularly assess the model's suitability for the current temporal context and be prepared to adapt or update it accordingly.
<!--{{ bias_recommendations | default("Users (both direct and downstream) should be made aware of the risks, biases and limitations of the model. More information needed for further recommendations.", true)}}-->

## How to Get Started with the Model

Use the code below to get started with the model.

Install streamlit first:
```console
pip install streamlit
```
Run the [streamlit UI file](model_ui.py):
```console
streamlit model_ui.py
```
 

## Training Details

### Training Data

<!-- This should link to a Dataset Card, perhaps with a short stub of information on what the training data is all about as well as documentation related to data pre-processing or additional filtering. -->
Training features were: `'transition_hour', 'transport_type_id', 'day', 'line_encoded', 'transfer_type_b', 'number_of_passenger', 'month', 'dayofyear', 'day_of_month', 'top_lines_indicator'`

Target was `'number_of_passenger'`, i.e. number of usage. `'top_lines_indicator'` created to help the model identifying higher numbers easier. 

Training data was mostly categorical features. Histogram-based gradient boost regression model supports categorical features, therefore these features below were tagged as one:
```python
categorical_features = ['transition_hour', 'transport_type_id', 'day',
                  'transfer_type_b','month','top_lines_indicator']
```

All the explanation about these features can be found in the [dataset card](https://github.com/iremgulcin/acelya-kardelen-emine-cevdet/blob/main/datasetcard.md).
<!--{{ training_data | default("[More Information Needed]", true)}}-->

### Training Procedure

<!-- This relates heavily to the Technical Specifications. Content here should link to that section when it is relevant to the training procedure. -->

#### Preprocessing 

We tried normalizing and standardizing the set for the model but none of the methods helped with the model's performance.
- All the date related features were created before training.
- Transfer type and transport type were change into binary columns.
- Top 15 lines were picked from the dataset and binary `top_lines_indicator` was created.


#### Training Hyperparameters

- **Training regime:**

	- **Algorithm:** Histogram-Based Gradient Boosting Regressor
	- **Training Data:** Time series cross-validation with 10 folds
	- **Hyperparameters:**
	  - Maximum number of iterations: 400
	  - Random state: 42
	  - Minimum samples per leaf: 5
	  - L2 regularization: 0.5
	  - Maximum depth: 7
	  - Categorical features: ['transition_hour', 'transport_type_id', 'day', 'transfer_type_b', 'month', 'top_lines_indicator']
	  - Learning rate: 0.1


#### Speeds, Sizes, Times [optional]

<!-- This section provides information about throughput, start/end time, checkpoint size if relevant, etc. -->
With using time series cross validation of 10 splits, the process took 19 minutes.
The model has early stopping integrated if the data has more than 10k samples, therefore this feature was utilized as well.


## Evaluation

<!-- This section describes the evaluation protocols and provides the results. -->

### Testing Data, Factors & Metrics

#### Testing Data

<!-- This should link to a Dataset Card if possible. -->
The model evaluation was performed using time series cross-validation (tscv) with 10 folds. This means the full dataset was split into 10 non-overlapping folds, with each fold used for testing while the remaining 9 folds were used for training. This ensures the evaluation covers various temporal segments and avoids overfitting to specific data points.
The testing data included a designated set for out-of-sample testing, notably [February 2023 data](https://www.kaggle.com/datasets/acelyasn/ibb-february-2023-transportation-dataset), which was not part of the model's training dataset.
More information on the data can be found [here](https://github.com/iremgulcin/acelya-kardelen-emine-cevdet/blob/main/datasetcard.md).
#### Factors

<!-- These are the things the evaluation is disaggregating by, e.g., subpopulations or domains. -->
Due to the tscv approach, specific factors like time periods or routes weren't explicitly considered during evaluation. However, the cross-validation inherently accounts for temporal variations and captures performance across diverse data subsets.

<!--{{ testing_factors | default("[More Information Needed]", true)}}-->

#### Metrics

<!-- These are the evaluation metrics being used, ideally with a description of why. Decision tresholds, model performance measures -->
Since we are using regression in order to predict the usage amount, the metrics we checked were mean absolute error, root mean squared error and r-squared. 
-   **Mean Absolute Error (MAE):**  Measures the average absolute difference between predicted and actual values.
-   **Root Mean Squared Error (RMSE):** Measures the average squared difference between predicted and actual values, penalizing larger errors more heavily.
-   **R-squared (R²):** Represents the proportion of variance in the target variable explained by the model.

<!--{{ testing_metrics | default("[More Information Needed]", true)}}-->

### Results
Overall training results (with 10 splits using Timeseries cross validation), calculated by getting the mean values of each fold:
- **Overall Mean Absolute Error (MAE):** 102.38 (+/- 8.59)
- **Overall Root Mean Squared Error (RMSE):** 348.41 (+/- 88.67)
- **Overall R-squared (R²):** 0.961 (+/- 0.024)

The model achieved a high R² of 0.961, indicating a strong overall fit to the data. Relatively high MAE and RMSE scores might indicate that the model can have harder time predicting larger values, most probably due to the distribution of the dataset. 

Results after predicting the training set i.e. our initial set:
- **MAE:**  91.0318043397631
- **RMSE:**  246.08508949745288
- **R2:**  0.9822519097537541

<img src="https://github.com/iremgulcin/acelya-kardelen-emine-cevdet/assets/122313795/bb979799-38fe-4963-9153-1b19bbbdf837" width="850" height="360">

February part of the graph:

<img src="https://github.com/iremgulcin/acelya-kardelen-emine-cevdet/assets/122313795/cf303b41-5b5f-4595-9dd0-78f4f1c1c67e" width="850" height="360">

Result of predicting February 2023 set which the model never seen:
- **MAE:**  98.55941068384743
- **RMSE**:  323.4147218899902
- **R2**:  0.9667258127868387

<!--  ![resim](https://github.com/iremgulcin/acelya-kardelen-emine-cevdet/assets/122313795/0035ba95-96be-452d-ba11-fea7e67a5735) -->
<img src="https://github.com/iremgulcin/acelya-kardelen-emine-cevdet/assets/122313795/0035ba95-96be-452d-ba11-fea7e67a5735" width="850" height="360">

#### Summary

The model exhibited good performance on the training set but showed some generalization error on the separate test set, with slightly higher MAE and RMSE values. Interestingly, it **performed surprisingly well on the February 2023 data**, achieving similar MAE, RMSE scores as the inital training process.

