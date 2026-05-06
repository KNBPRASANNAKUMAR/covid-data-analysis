import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

if not os.path.exists("visuals"):
    os.makedirs("visuals")

if not os.path.exists("output"):
    os.makedirs("output")

print("Files in data folder:")
print(os.listdir("data"))

covid = pd.read_csv("data/covid_19_clean_complete.csv")
day_wise = pd.read_csv("data/day_wise.csv")
full_grouped = pd.read_csv("data/full_grouped.csv")
worldometer = pd.read_csv("data/worldometer_data.csv")

usa_file = None

if "usa_country_wise.csv" in os.listdir("data"):
    usa_file = "data/usa_country_wise.csv"

if "usa_county_wise.csv" in os.listdir("data"):
    usa_file = "data/usa_county_wise.csv"

if usa_file:
    usa = pd.read_csv(usa_file)
    print("USA dataset loaded from:", usa_file)
else:
    print("USA dataset not found")

print(covid.head())
print(worldometer.head())

covid["Date"] = pd.to_datetime(covid["Date"])

print(covid.info())

covid["death_rate"] = (covid["Deaths"] / covid["Confirmed"]) * 100

print(covid[["Country/Region","Confirmed","Deaths","death_rate"]].head())

plt.figure(figsize=(10,5))
sns.lineplot(data=covid, x="Date", y="Confirmed")
plt.title("Global COVID Confirmed Cases Over Time")
plt.savefig("visuals/global_cases_trend.png")
plt.close()

top_countries = covid.groupby("Country/Region")["Confirmed"].max().sort_values(ascending=False).head(10)

print(top_countries)

plt.figure(figsize=(10,5))
top_countries.plot(kind="bar")
plt.title("Top 10 Countries by COVID Cases")
plt.savefig("visuals/top_countries_cases.png")
plt.close()

corr = covid[["Confirmed","Deaths","Recovered"]].corr()

plt.figure(figsize=(8,6))
sns.heatmap(corr, annot=True)
plt.title("Correlation Matrix")
plt.savefig("visuals/correlation_matrix.png")
plt.close()

top_world = worldometer.sort_values("TotalCases", ascending=False).head(10)

print(top_world)

plt.figure(figsize=(10,5))
sns.barplot(data=top_world, x="Country/Region", y="TotalCases")
plt.xticks(rotation=45)
plt.title("Top Countries by Total Cases")
plt.savefig("visuals/worldometer_top_cases.png")
plt.close()

try:
    covid.to_csv("output/cleaned_covid_data.csv", index=False)
    top_countries.to_csv("output/top_countries.csv")
except PermissionError:
    covid.to_csv("cleaned_covid_data.csv", index=False)
    top_countries.to_csv("top_countries.csv")

print("Analysis completed successfully")