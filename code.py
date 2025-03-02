import pandas as pd

data = pd.read_csv('WA_Fn-UseC_-HR-Employee-Attrition.csv')

# %%
print(data.head())

# %%
data.info()

# %%
print(data.columns)

# %%
#checking cells that have only 1 value (not useful for analysis)
print(data['EmployeeCount'].unique())
print(data['Over18'].unique())
print(data['StandardHours'].unique())


# %%
data=data.drop(['EmployeeCount','Over18','StandardHours'], axis=1, errors='ignore')
# %%
#removing duplicate rows 
data=data.drop_duplicates()
print(data.duplicated().sum())

# %%
#No need to fix structural errors because we only have int and Categorical columns, 
#we dont have columns like dates where we would need to fix 

# %%
#missing data:
missing_data=data.isnull().sum()
print(missing_data)

# %%
#Target= Attrition column 
#features= all the other columns that we didnt delete from the data frame


# %%
#taking out outliers from salary:

for column in ['MonthlyIncome']:
    Q1 = data[column].quantile(0.25)
    Q3 = data[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    
    data = data[(data[column] >= lower_bound) & (data[column] <= upper_bound)]

for column in ['MonthlyRate']:
    Q1 = data[column].quantile(0.25)
    Q3 = data[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    
    data = data[(data[column] >= lower_bound) & (data[column] <= upper_bound)]



# %%
#checking how many values in each column I have after I delete the outliers:
data.info()

# %%
import scipy.stats as stats
numerical_data = data.select_dtypes(include=['int64'])
skewness = stats.skew(numerical_data)
kurtosis = stats.kurtosis(numerical_data)
print(kurtosis)
print(skewness)
# %%

#kurtosis there are no values <>3 so I dont modify columns because of kurtosis
#skewness we have some big values like in YearsSinceLastPromotion (skewness of 2). 
#I decided to transform it so will have more normal distribuition and check again:
skewness = stats.skew(data['YearsSinceLastPromotion'])
print(skewness)
data['YearsSinceLastPromotion'], _ = stats.boxcox(data['YearsSinceLastPromotion'] + 1)
skewness = stats.skew(data['YearsSinceLastPromotion'])
print(skewness)


# %%
