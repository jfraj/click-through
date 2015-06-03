# click-through
Analysis of click-through rate

## Definition of successful

## Discrete questions

* How many distinct ads were shown for the 10 day period in total and per day?
answer and code in `notebook/distinct_ads.ipynb`
* which app_domain is the most successful?
answer and code in `notebooks/successful_app_domain.ipynb`
* which banner position is the most successful?
answer and code in notebooks/successful_banner.ipynb
* Provide the top 10 most successful site_categories for the 10 day period
answer and code in notebooks/top10_site_category.ipynb

## Data insight
As a reference for any successful field, the following plot
shows the overall success of all the adds for each day of the data set.

![alt text](https://raw.githubusercontent.com/jfraj/click-through/master/plots/all_success.png)


Here is a bar chart of the most successful value for each field

![alt text](https://raw.githubusercontent.com/jfraj/click-through/master/plots/most_success.png)

The most successful one, device_id & device_ip, have a small number of clicks, reflected by the larger error bar, but seems to be credible.
The small number of impressions, if true, makes those successful field values less interesting for prediction since they happens so rarely.


## Field values correlations
Relationship between fields can be checked with variation correlations over time.  Here is an example of highly correlated example.

![alt text](https://raw.githubusercontent.com/jfraj/click-through/master/plots/high_corr_ex.png)

This can be use to predict the success of one value when their is only data on a correlated value.

Some field contains more correlations between their values than others, here is the distributions of the 100 most successful paired values of the C20 field:

![alt text](https://raw.githubusercontent.com/jfraj/click-through/master/plots/corr_C20.png)

## A closer look at the most successful app_domain
Here is a plot of the most successful app_domain determined in the discrete questions.

![alt text](https://raw.githubusercontent.com/jfraj/click-through/master/plots/app_domain_success_trend.png)

Clearly, app_domain 99b4c806 is only successful one day, the 28th, but it's the number of impressions are so large that they overwhelm all other days of lower success.  The following plot shows how the distributions of some fields on the 28th and the rest of the data set.

![alt text](https://raw.githubusercontent.com/jfraj/click-through/master/plots/app_domain_28th.png)

(code to produce this plot in `notebooks/app_domain_28th.ipynb`)
There are four fields that are clearly different on the 28th: C14, C17, C18 & C19.  Some of them most likely influence the success.  Indeed, C14 and C17 have values that can have very high success.  This could be investigated by looking at which combinations are successful on the 28th and see if they are still successful (but less frequent) on other days.
