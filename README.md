
# Regression Project: Zillow

___
___

# <a name="scenario"></a>Scenario
Utilizing the 2017 Zillow data set, I set out to build a model that would predict the values of single family homes, examining the correlation between the data points and our target variable (home_value). I will identify critical features that can be used in a regression model to predict home value. 
___

# <a name="project-planning"></a>Project Planning
### Goal:
The goal for this project is to create a model that will accurately predict a home's value determined by the county's Appraisal District. To do so, I will have to identify which of the various features are drivers to this end, and implement them into a machine learning regression model. 

### Initial Hypotheses:

>$Hypothesis_{1}$
>
> There is a relationship between square footage and home value.


>$Hypothesis_{2}$
>
> There is a correlation between number of bathrooms and bedrooms and home value.

### Project Planning Initial Thoughts:
- My initial thoughts were that there would be a direct relationship to the total square footage of the property and its appraised value.
- Additionally, I believe there to be a correlation, not just to the number of bedrooms and bathrooms, but also to a ratio of square footage per number of rooms
- To explore this I created a new feature:
    - `sqft_room_ratio`: 'sqft' / ('bedrooms' + 'bathrooms')
___
# <a name="key-findings"></a>Key Findings

## Exploration Takeaways
After removing home_value outliers, especially those homes with more than 6 bedrooms, 6 bathrooms, over a value of $1,500,000, and with a square footage of more than 15,000 sqft. The majority of homes are in the bottom 20% of the overall square footage and bottom 45% of home_value. 

Mean home value = $380,196
Mean square footage = 1774

___
# <a name="tested-hypotheses"></a>Tested Hypotheses

>$Hypothesis_{1}$
>
> $H_{0}$: No correlation between square footage and home value.
>
> $H_{a}$: There is a correlation between square footage and home value.


>$Hypothesis_{2}$
>
> $H_{0}$: No correlation between number of bathrooms and home value.
>
> $H_{a}$: There is a correlation between bathrooms and home value.


>$Hypothesis_{3}$
>
> $H_{0}$: No correlation between number of bedrooms and home value.
>
> $H_{a}$: There is a correlation between bathrooms and home value.


>$Hypothesis_{4}$
>
> $H_{0}$: No correlation between square footage per room ratio and home value.
>
> $H_{a}$: There is a correlation between square footage per room ratio and home value.
___
# <a name="take-aways"></a>Take Aways
A more robust combination of cleaned and wrangeled data/features worked best with the regression models.

Summary¶
Following the evaluation of the different models using my selected features, I found that the best performing model was the Polynomial Regressor with degrees = 2
Looks like it performs best when above the median home value, and much worse below the median value

Mean home value = $380,196
Mean square footage = 1774
Mean Bedrooms = 3
Mean Bathrooms = 2


___
# <a name="data-dictionary"></a>Data Dictionary
|                   column_name                   |                                                       description                                                       |                   key                  |       dtype      |
|:-----------------------------------------------:|:-----------------------------------------------------------------------------------------------------------------------:|:--------------------------------------:|:----------------:|
| `bathrooms` / `bathroomcnt`                     |    Number of bathrooms in home including fractional bathrooms                                                           |                                        | float64          |
| `bedrooms` /  `bedroomcnt`                      |    Number of bedrooms in home                                                                                           |                                        | float64          |
| `sqft` / `calculatedfinishedsquarefeet`  |    Calculated total finished living area of the home                                                                    |                                        | float64          |
|   `fips`        |    Federal Information Processing Standard code  |                                        | float64 /  int64 |
| `cost_per_sqft`                                      | Unique identifier for parcels (lots)                                                                                    |                                        | int64            |
|   `yearbuilt`                                   |    The Year the principal residence was built                                                                           |                                        | float64 /  int64 |
| `home_value` / `taxvaluedollarcnt`              |   The total tax assessed value of the parcel                                                                            |                                        | float64          |
| `taxamount`                           | The total property tax assessed for that assessment year                                                                |                                        | float64          |
| `sqft_room_ratio`                                        | The ratio of sqft to total number of bedrooms and bathrooms.                                                                                     |                                        | int64           |

___
# <a name="workflow"></a>Workflow

1. prep-your-repo (env file and gir ignore to utilize mysql credentials)
1. import all necessary libraries and additional python files (wrangle.py which is available for reference in my repo)
1. acquire-data (wrangle.py)
1. clean-prep-and-split-data (wrangle.py)
1. explore-data
    - hypothesis-testing
1. evaluate-data
1. modeling
    - identify-baseline
    - train-validate
    - test
    

