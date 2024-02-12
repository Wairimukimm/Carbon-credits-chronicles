![image](https://github.com/Wairimukimm/Carbon-credits-chronicles/assets/122815372/3052af54-8494-461f-b00a-96353357c0a2)



## CARBON CREDITS CHRONICLES 
## Overview
In the race against climate change, businesses are embracing carbon credit projects to mitigate their environmental footprint. This study delves into time series analysis, comparing pre and post-implementation periods of carbon credit projects, aiming to unveil the transformative impact on emission patterns over time.


## Business and Data Understanding
As the global community grapples with the urgent challenge of climate change, there is a pressing need for comprehensive understanding and effective strategies to mitigate its impacts. Carbon credits, a key instrument in climate change mitigation efforts, represent a mechanism through which organizations can offset their carbon emissions by investing in emissions reduction projects elsewhere. These credits not only facilitate emission reductions but also drive investments in sustainable development initiatives worldwide
## Problem Statement
As the global business landscape shifts towards sustainability, there is a growing need to comprehensively evaluate the effectiveness of carbon credit initiatives in curbing emissions. This study addresses the challenge of systematically assessing the impact of these projects on emission patterns through a rigorous time series analysis. The question at the forefront is: Do carbon credit initiatives significantly influence and contribute to the reduction of emissions over time?
## Components
* The [Jupyter Notebook](https://github.com/Wairimukimm/Carbon-credits-chronicles/blob/main/Notebook.ipynb) is the main deliverable. It contains the details of the approach taken and the methodology. It contains data cleaning, exploratory data analysis, data preparation for modelling and building the recommendation system.

* The [Presentation](https://github.com/randellmwania/Movie-Recommendation-System/blob/main/presentation.pdf) is the non technical Presentation of the project. It contains the objectives, problem statment, model evaluation, findings and recommendations.

* The dataset used for this project can be found in [Kaggle](https://ourworldindata.org/co2-emissions) and [2](https://gspp.berkeley.edu/research-and-impact/centers/cepp/projects/berkeley-carbon-trading-project/offsets-database)




## Technologies
* Python version: 3.6.9
* Matplotlib version: 3.1.3
* Seaborn version: 0.9.0
* Pandas version: 0.25.1
* Numpy version: 1.16.5

    
## To begin

* Clone this [repository](https://github.com/Wairimukimm/Carbon-credits-chronicles/blob/main/Notebook.ipynb)
* Download the [Dataset](https://gspp.berkeley.edu/research-and-impact/centers/cepp/projects/berkeley-carbon-trading-project/offsets-database) used and install any technologies if necessary


## Data Wrangling
In this section, we did data preparation which invloved:
* Checking for missing values, removing duplicates, renaming columns and dropping unnecessary columns to ensure the data is clean and suitable for analysis and modelling.



## Explaratory Data Analysis(EDA)
We perfomed both univariate and bivariate analysis to uncover patterns in the dataset. 
* The top 5 genres were drama, comedy, thriller, action and romance
* The most viewed movies were pulp fiction, fight club, star wars and inception

## ARIMA MODEL

* ARIMA is a time series forecasting method used to model and forecast future values based on past observations. It's suitable for data exhibiting trend and/or seasonality.

* ARIMA models decompose a time series into three components: auto-regressive (AR), differencing (I), and moving average (MA). It accounts for linear dependencies between observations and aims to make predictions based on these dependencies.

## SIMPLE EXPONENTIAL SMOOTHING
* SES is a straightforward time series forecasting method used to generate short-term forecasts, especially when data lacks clear trend or seasonality.


* SES assigns exponentially decreasing weights to past observations, assuming that more recent observations are more relevant for forecasting future value


## EVALUATION
Evaluating RMSE and MAE

RMSE:0.024251388344712705
MAE:0.0005881298366460672

The RMSE measures the average magnitude of errors between predicted and actual ratings. A lower RMSE indicates better predictive performance.The MAE represents the average absolute errors between predicted and actual ratings. Similar to RMSE, a lower MAE indicates better accuracy
## CONCLUSIONS

Data scientist are not fortune tellers and hence cannot predict the future but the data shows that though Carbon Credits s relatively new. If implemented well it has the potential to incentivise companies into reducing carbon emission. This paired with government policies aimed at reducing CO2 emissions can prove to be a powerful combination as entities that fail to reduce their emissions will be forced into buying Carbon Credits to offset their emissions or pay fines. The effectiveness demonstrated by the U.S cap-and-trade model in reducing sulphur dioxide emissions during the 1990s provides compelling evidence for its application in addressing the current climate change crisis. By adopting carbon pricing and emissions trading programs, we can establish a market-driven mechanism for reducing greenhouse gas emissions. Through concerted efforts involving stakeholders and knowledge-sharing initiatives, we can expedite the shift towards a low-carbon economy. This collaborative approach holds promise for fostering a sustainable future that benefits present and future generations alike.
 
