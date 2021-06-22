# Install Pandas, Numpy and Matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Read population_by_country.csv
population_by_country=pd.read_csv("population_by_country_2020.csv")
print(population_by_country)
# Create a numpy array for population_by_country
np_population_by_country=np.array(population_by_country)
# Select the columns Population (2020) and Land Area (KmÂ²)
np_pop_2020=np_population_by_country[:,1]
print(np_pop_2020)
np_area_2020=np_population_by_country[:,5]
print(np_area_2020)
print(np_pop_2020+np_area_2020)

GDP_by_country_WB=pd.read_csv("API_NY.GDP.MKTP.CD_DS2_en_csv_v2_2445719.csv",skiprows=4)
print(GDP_by_country_WB.head())
print(GDP_by_country_WB.info())
Country_by_region_WB=pd.read_csv("Metadata_Country_API_NY.GDP.MKTP.CD_DS2_en_csv_v2_2445719.csv")
print(Country_by_region_WB.head())
print(Country_by_region_WB.info())
GDP_by_region_and_country_WB_merge = pd.merge(Country_by_region_WB,GDP_by_country_WB, left_on='TableName', right_on='Country Name')
print(GDP_by_region_and_country_WB_merge.shape)
GDP_by_region_and_country_WB_merge.to_csv("merged_WB.csv")
# Check individual values for missing values
print((GDP_by_region_and_country_WB_merge.isna))
print(GDP_by_region_and_country_WB_merge.isna().any)
print(GDP_by_region_and_country_WB_merge.isna().sum())
# Delete rows on IncomeGroup & Region with NaN values (Aggregate Columns)
GDP_by_region_and_country_WB_merge_cl1=GDP_by_region_and_country_WB_merge.dropna(subset=["Region"])
print(GDP_by_region_and_country_WB_merge_cl1.isna().sum())
# Delete dupliates or unnecessary columns:
GDP_by_region_and_country_WB_merge_cl2= GDP_by_region_and_country_WB_merge_cl1.drop(['SpecialNotes', 'TableName',"Indicator Code","Unnamed: 5","Country Code_y","2020","Unnamed: 65"], axis=1)
print(GDP_by_region_and_country_WB_merge_cl2.info())
print(GDP_by_region_and_country_WB_merge_cl2.isna().any())
# Extract to csv and review:
GDP_by_region_and_country_WB_merge_cl2.to_csv("merged_WB_v2.csv")
# Rename column Country Code_x to Country Code:
GDP_by_region_and_country_WB_merge_cl3=GDP_by_region_and_country_WB_merge_cl2.rename({"Country Code_x":"Country Code"},axis=1)
print(GDP_by_region_and_country_WB_merge_cl3.info())
# Insert a column "Baseline_GDP" after Indicator Name with value 0 for all rows.
GDP_by_region_and_country_WB_merge_cl3["Baseline_GDP"] = 0
print(GDP_by_region_and_country_WB_merge_cl3.head())
# Move "Baseline_GDP" column position to after "Indicator Name" and before GBP data
col_list = GDP_by_region_and_country_WB_merge_cl3.columns.tolist()
col_list.insert(5, col_list.pop(col_list.index('Baseline_GDP')))
print(col_list)
GDP_by_region_and_country_WB_merge_cl3 = GDP_by_region_and_country_WB_merge_cl3.reindex(columns=col_list)
# Forward fill by row across all columns
GDP_by_region_and_country_WB_merge_clean=GDP_by_region_and_country_WB_merge_cl3.ffill(axis=1)
print(GDP_by_region_and_country_WB_merge_clean.info())
print(GDP_by_region_and_country_WB_merge_clean.head())
GDP_by_region_and_country_WB_merge_clean.to_csv("merged_WB_v4.csv")
# Set the Indexs to Region and IncomeGroup
GDP_by_region_and_country_WB_merge_clean=GDP_by_region_and_country_WB_merge_clean.set_index("Region","IncomeGroup")
print(GDP_by_region_and_country_WB_merge_clean.head())
# Groupby region and GDP 2000 v 2019
GDP_by_region_2000v2019 = GDP_by_region_and_country_WB_merge_clean.groupby("Region")[["2000","2019"]].sum()
print(GDP_by_region_2000v2019)
GDP_by_region_2000v2019.plot(kind="bar", title="GDP by Region 2000 V 2019")
plt.show()
plt.clf()
# GDP pie chart summary years 1960, 2000 & 2019
GDP_Years = ["1960","2000","2019"]
GDP_by_region = GDP_by_region_and_country_WB_merge_clean.groupby("Region")[GDP_Years].sum()
GDP_by_region[GDP_Years].plot(kind="pie", subplots=True, title="GDP by Region 1960, 2000, 2019")
plt.show()
# Slice for sub saharan Africa
# Slice for sub saharan Africa
