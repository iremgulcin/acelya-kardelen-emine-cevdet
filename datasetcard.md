---
# Dataset Card
---

# Dataset Card for Annual Transportation Usage in Istanbul, 2022

<!-- Provide a quick summary of the dataset. -->
The dataset we created consists of merged datasets of 12 months, all shared by Istanbul Metropolitan Municipality.
<!--{{ dataset_summary | default("", true) }}-->

## Dataset Details

### Dataset Description

<!-- Provide a longer summary of what this dataset is. -->
Istanbul Metropolitan Municipality shares transportation usage monthly. All 12 months of 2022 were merged into this final one. The set has nearly 7.5 million rows and consists of hourly usage of 877 transportation lines (highway and rail type) in a year. The information of football matches that were played in Istanbul of the teams Beşiktaş, Galatasaray, and Fenerbahçe was added but didn't help the performance of the model and therefore dropped from the final set. Temperature was also added and used to train our models but it also didn't affect the models' performance. Both initial set and training set will be shared. 



<!--{{ dataset_description | default("", true) }}-->

- **Curated by:** Istanbul Metropolitan Municipality and Açelyanur Şen
<!--{{ curators | default("[More Information Needed]", true)}}-->
<!-- **License:** {{ license | default("[More Information Needed]", true)}}-->

### Dataset Sources 

<!-- Provide the basic links for the dataset. -->
- [Initial annual set](https://www.kaggle.com/datasets/acelyasn/annual-istanbul-transport-data-2022-wout-marine)
- [Istanbul Metropolitan Municipality Data Portal](https://data.ibb.gov.tr/dataset/hourly-public-transport-data-set)


## Uses

<!-- Address questions around how the dataset is intended to be used. -->
Can be used to understand the trends overtime

### Direct Use

<!-- This section describes suitable use cases for the dataset. -->
- **Prediction of Route Usage:** The dataset can be employed to train models aimed at predicting the usage of transportation routes over time. This predictive capability can be valuable for optimizing various aspects of transportation planning, such as determining optimal departure times, adjusting the frequency of vehicles, and even informing the creation of new routes.

- **Planning and Optimization:** The predictions derived from the trained models can be utilized for strategic planning and optimization of transportation services. By gaining insights into usage patterns, transportation authorities and companies can make informed decisions regarding resource allocation, scheduling, and route planning.

- **Performance Monitoring:** The dataset can also serve as a valuable tool for monitoring the performance of transportation routes. By analyzing historical data, one can identify trends, peak usage periods, and areas that may require additional attention or adjustments in service.

- **Research and Analysis:** Researchers and analysts can leverage the dataset to conduct studies and analyses on various aspects of public transportation, contributing to a deeper understanding of travel patterns, user behavior, and the factors influencing transportation demand.

<!--{{ direct_use | default("[More Information Needed]", true)}}-->


## Dataset Structure

<!-- This section provides a description of the dataset fields, and additional information about the dataset structure such as criteria used to create the splits, relationships between data points, etc. -->
The features we used are as below:
| feature              | feature info                                                      | type     |
|----------------------|-------------------------------------------------------------------|----------|
| transition_hour      | From 0 to 23. Indicates the hour in the day.                      | int      |
| transition_date      | Our index value. The date of the transition.                      | datetime |
| day *[^*]                | From the index. 0 to 6, day of the week                           | int      |
| day_of_month*        | From the date index. 1 to 28/31, day of the month                 | int      |
| day_of_year*         | From the date index. 1 to 365, day of the year                    | int      |
| line                 | Names of the lines                                                | string   |
| line_encoded*        | Factorized values of the line names                               | int      |
| transport_type_id    | Binary column for transport types. Rail = 1, Highway = 0          | int      |
| transfer_type        | Binary column for journey types. Normal = 1, Transfer = 0         | int      |
| number_of_passenger  | Individual passengers traveling in the given hour                 | int      |
| top_lines_indicator* | Binary column to check if given line is in the most used 15 lines | int      |
---------------------------------
Features that weren't used but are in the initial set:
| feature   | feature info                                              |  type |
|-----------|-----------------------------------------------------------|---|
| TEMP*      | Hourly temperature data.                                  | float  |
| team_1*    | The home team of the match.                               | string  |
| match_day* | Binary column for match days. Match day = 1, no match = 0 | int  |

[^*]: *marked features are created by us. 
<!--{{ dataset_structure | default("[More Information Needed]", true)}}-->
Since we have a time series data, instead of normal cross validation methods "Time series cross validation" was utilized while splitting the dataset. Time series cross validation is a technique that splits the data in such a way that test set is always the future compared to the train set; keeping the meaning of the corresponding dates of the datapoints. This way we made sure there were no data leakage and the model used "past" data and predicted the next one.  
## Dataset Creation

### Source Data

<!-- This section describes the source data (e.g. news text and headlines, social media posts, translated sentences, ...). -->
Individual passengers traveling in the given hour is calculated by Istanbul Metropolitan Municipality. 
#### Data Collection and Processing

<!-- This section describes the data collection and processing process such as data selection criteria, filtering and normalization methods, tools and libraries used, etc. -->
12 months of hourly data was merged into one using OS command lines. 
For the temperature data, we utilized [meteoblue](meteoblue.com/) and for the match data, [wikipedia](https://tr.wikipedia.org/wiki/2021-22_S%C3%BCper_Lig_ma%C3%A7lar%C4%B1) was used. Initial dataset had marine routes as well but only railway and highway data was used due to errors in the tags of marine lines.
<!--{{ data_collection_and_processing_section | default("[More Information Needed]", true)}}-->

#### Features and the target

<!-- This section describes the features of the dataset and the target of the project -->
Features that are used: *'transition_hour',  'transport_type_id',  'day',  'line_encoded', 'transfer_type_b', 'number_of_passenger', 'month', 'dayofyear', 'day_of_month', 'top_lines_indicator'*

Target: *'number_of_passenger'*. 

Their respected explanation can be found in the [Dataset Structure](#dataset-structure) section. 

<!--### Annotations [optional]

<!-- If the dataset contains annotations which are not part of the initial data collection, use this section to describe them. -->

<!--#### Annotation process-->

<!-- This section describes the annotation process such as annotation tools used in the process, the amount of data annotated, annotation guidelines provided to the annotators, interannotator statistics, annotation validation, etc. -->

<!--{{ annotation_process_section | default("[More Information Needed]", true)}}-->

<!--#### Who are the annotators?

<!-- This section describes the people or systems who created the annotations. -->

<!--{{ who_are_annotators_section | default("[More Information Needed]", true)}}-->


## Bias, Risks, and Limitations

<!-- This section is meant to convey both technical and sociotechnical limitations. -->
For better analysis and a better demand planning system, usage information for each stop of the routes is needed. However, in order to track each stop, cameras or other sensors must be utilized since citizens don't have to use their transport cards while leaving transportation vehicles. 
Since individual stop data is not available, popular locations can't be extracted from the dataset. If the routes also had locational data at least for their first and last stops, more in-depth analysis could've been made as well. Moreover, dataset is not balanced at all. Most used 15 lines have over millions of passengers while the rest have very less usage, meaning that unpopular routes contribute more to the dataset with more data points. The models might have a hard time predicting large values because of this.
<!--{{ bias_risks_limitations | default("[More Information Needed]", true)}}-->


<!--## Citation [optional]

<!-- If there is a paper or blog post introducing the dataset, the APA and Bibtex information for that should go in this section. -->

