
# Regression Project: 

___
___

# <a name="scenario"></a>Scenario
As a junior data scientist on the Zillow data science team, I am tasked to build a model that will predict the values of single unit properties that the tax district assesses (using the property data from those whose last transaction was during May through August of 2017).

Unfortunately, some features of our dataset have been deleted. 
- I must also recover the following features:
    - the state and county information for all of the properties
    - distribution of tax rates for each county
        - tax amounts and tax value of the home

   
   
Memo from the Zillow Data Science Team:
>Note that this is separate from the model you will build, because if you use tax amount in your model, you would be using a future data point to predict a future data point, and that is cheating! In other words, for prediction purposes, we won't know tax amount until we know tax value.

[Jump to Navigation](#navigation)
___

# <a name="project-planning"></a>Project Planning
### Goal:
The goal for this project is to create a model that will accurately predict a home's value determined by the county's Appraisal District. To do so, I will have to identify which of the various features available on Zillow's API affect the accuracy of my model's predictions the most. 

### Initial Hypotheses:

>$Hypothesis_{1}$
>
> There is a relationship between square footage and home value.


>$Hypothesis_{2}$
>
> There is a weak correlation between number of bathrooms and home value.

### Project Planning Initial Thoughts:
- With the missing features I am tasked to reproduce in mind, I want to create some (most likely) dummy features connecting `fips` to county names. 
    - I have a strong feeling that certain counties will have higher home value assessment. 
- On my second iteration, I'd also like to test the importance of 
    - `lotsizesquarefeet` 
    - `regionidcounty`
    - `regionidzip`
    - `regionidneighborhood`
    - `yardbuildingsqft17`
    - 'logerror'
- I'd like to create a new feature:
    - `home_age`: current year - `yearbuilt`
    - 
    
- Although to keep myself on track to reach my goals, I will first focus on my first iteration with my limited features of `calculatedfinishedsquarefeet`, `bedroomcnt` and `bathroomcnt` to predict my target `taxvaluedollarcnt`. 
- If time permits, I'd like to create nice visualizations in Tableau, although I may have to settle with seaborn graphics.

[Jump to Navigation](#navigation)
___
# <a name="key-findings"></a>Key Findings

## Exploration Takeaways
After removing home_value outliers, it seems 'expensive/large' homes are still pulling my data towards the right. The median household looks like 1430 sqft, 3BD/2BA, with a value of $311_000.

Removal of my `home_value` outliers have put a damper on my correlations, most like due to the fact that I have so few features in this first iteration.

A majority of homes are in the bottom 25% of square feet and bottom 45% of home_value.

[Jump to Navigation](#navigation)
___
# <a name="tested-hypotheses"></a>Tested Hypotheses

>$Hypothesis_{1}$
>
> $H_{0}$: There is a relationship between square footage and home value.
>
> $H_{a}$: There IS a correlation between square footage and home value.


>$Hypothesis_{2}$
>
> $H_{0}$: No correlation between number of bathrooms and home value.
>
> $H_{a}$: There IS a correlation between bathrooms and home value.


>$Hypothesis_{3}$
>
> $H_{0}$: No correlation between number of bedrooms and home value.
>
> $H_{a}$: There IS a correlation between bedrooms and home value.


>$Hypothesis_{4}$
>
> $H_{0}$: Three bedroom homes have the same value as the other homes.
>
> $H_{a}$: Home value for 3 bedroom homes differ from the rest.


>$Hypothesis_{5}$
>
> $H_{0}$: No correlation between the size of lot and home value.
>
> $H_{a}$: There IS a correlation between the size of lot and home value.


>$Hypothesis_{6}$
>
> $H_{0}$: No correlation between the year built and home value.
>
> $H_{a}$: There IS a correlation between the year built and home value.

[Jump to Navigation](#navigation)
___
# <a name="take-aways"></a>Take Aways
Relevant features with **minimal** `nulls` matter! The more that is available, the more you are able to test and tweak your model to predict at better rates!


___
# <a name="data-dictionary"></a>Data Dictionary
|                   column_name                   |                                                       description                                                       |                   key                  |       dtype      |
|:-----------------------------------------------:|:-----------------------------------------------------------------------------------------------------------------------:|:--------------------------------------:|:----------------:|
| `bathrooms` / `bathroomcnt`                     |    Number of bathrooms in home including fractional bathrooms                                                           |                                        | float64          |
| `bedrooms` /  `bedroomcnt`                      |    Number of bedrooms in home                                                                                           |                                        | float64          |
| `square_feet` / `calculatedfinishedsquarefeet`  |    Calculated total finished living area of the home                                                                    |                                        | float64          |
|   `fips`                                        |    Federal Information Processing Standard code -  see https://en.wikipedia.org/wiki/FIPS_county_code for more details  |                                        | float64 /  int64 |
|   `lotsizesquarefeet`                           |    Area of the lot in square feet                                                                                       |                                        | float64          |
| `parcelid`                                      | Unique identifier for parcels (lots)                                                                                    |                                        | int64            |
|   `yearbuilt`                                   |    The Year the principal residence was built                                                                           |                                        | float64 /  int64 |
| `home_value` / `taxvaluedollarcnt`              |   The total tax assessed value of the parcel                                                                            |                                        | float64          |
| `taxes` /  `taxamount`                           | The total property tax assessed for that assessment year                                                                |                                        | float64          |
| `county`                                        | The county the property is located.                                                                                     |                                        | object           |
| `state`                                         | The state the property is located.                                                                                      |                                        | object           |
| `bdrm_3`                                        | Identifies if property is a 3 bedroom home.                                                                             | 1: 3 bedroom home 0: not a 3 bdrm home | int64            |
| `tax_rates`                                     | Calculated tax rate = `taxes` / `home_value`                                                                            |                                        | float64          |

[Jump to Navigation](#navigation)
___
# <a name="workflow"></a>Workflow

Please pull my repo first to use the following links to guide you through the data science pipeline. Enjoy!

1. [Prep Your Repo](#prep-your-repo)
1. [Import](#import)
1. [Acquire Data](#acquire-data)
1. [Clean, Prep & Split Data](#clean-prep-and-split-data)
1. [Explore Data](#explore-data)
    - [Hypothesis Testing](#hypothesis-testing)
1. [Evaluate Data](#evaluate-data)
1. [Modeling](#modeling)
    - [Identify Baseline](#identify-baseline)
    - [Train / Validate](#train-validate)
    - [Test](#test)
    
- [Requested Data](#requested-data)

8. [2nd Iteration: Acquire Data](#2nd-iteration-acquire-data)
9. [2nd Iteration: Clean, Prep & Split Data](#2nd-iteration-clean-prep-and-split-data)
10. [2nd Iteration: Explore Data](#2nd-iteration-explore-data)
    - [2nd Iteration: Hypothesis Testing](#2nd-iteration-hypothesis-testing)
11. [2nd Iteration: Modeling](#2nd-iteration-modeling)
    - [2nd Iteration: Identify Baseline](#2nd-iteration-identify-baseline)
    - [2nd Iteration: Train / Validate](#2nd-iteration-train-validate)
    - [2nd Iteration: Test](#2nd-iteration-test)
    

[Jump to Navigation](#navigation)
