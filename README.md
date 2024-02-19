# Short-term Route-level Demand Forecasting for Istanbul’s Transportation Routes

This project aims to predict the number of passengers using public transportation lines in Istanbul at specified time intervals. This facilitates end-users, citizens, to plan their travels accordingly, and enables the municipality to adjust the frequency of routes during peak hours.

## Dataset
The dataset used in the project was downloaded from the Istanbul Metropolitan Municipality's open data portal. It contains hourly passenger counts of public transportation lines in Istanbul for the year 2022. The columns in the dataset are as follows:

- **Date**: The date when the passenger count was recorded.
- **Time**: The time when the passenger count was recorded.
- **Route**: The name of the public transportation route.
- **Passenger_Count**: The number of passengers boarding the route at that time.

The dataset size is 242 MB, consisting of 7.4 million rows and 19 columns.

## Models
In the project, 6 different models were trained to predict the passenger counts of public transportation routes using the dataset. These models are as follows:

1. **Prophet**: Developed by Facebook, Prophet is a model that performs well for time series data. However, due to the large number of columns in our dataset, we achieved an r^2 score of 13% on the test data. After experimenting with parameters and modifying the dataset, we achieved an r^2 score of 53% on some routes when trained with multithread learning. However, we ultimately decided that the model was not suitable for our project.
  
2. **LSTM**: Long Short-Term Memory (LSTM) is a deep learning model suitable for sequential data. After preprocessing the dataset and training the model, we achieved an r^2 score ranging from 23% to 26%. We experimented with different parameters similar to Prophet but could only achieve an r^2 score of 53% to 56%.
  
3. **XGBoost**: XGBoost is a high-performance machine learning model using gradient boosting. By optimizing parameters with gradient boosting, we achieved an r^2 score of 83%.
  
4. **Gradient Boosting Regressor**: This model, utilizing the gradient boosting method, achieved an r^2 score of 98% after preprocessing and training. However, due to high MAE and RMSE scores, indicating potential overfitting, we adjusted parameters and obtained an r^2 score of 93%.
  
5. **MLP**: Multi-Layer Perceptron (MLP) is a deep learning model. After preprocessing and training, we achieved an r^2 score of 56%.
  
6. **Hist Gradient Boosting Regressor**: This model, which utilizes histogram-based gradient boosting, outperformed other models. After preparing the data and training the model, we obtained an r^2 score of 98.83%. However, upon scrutinizing some graphical representations of the model's results, we are deliberating whether the accuracy of the model is genuine or potentially misleading.

## Application
In the application phase of the model, there will be a front-end where users can select the route, date, time, and transfer type. After making selections, the model's prediction will be displayed on the screen.


https://github.com/iremgulcin/acelya-kardelen-emine-cevdet/assets/122313795/f3039432-4744-4b55-9757-c531bb971a31


## Future Plans
One future plan would be to use real-time data in order to predict *user flow* and to calculate importance of each stop of the routes. This would deflinitely improve the predictions of the model.

## License
This project is licensed under the MIT License.

