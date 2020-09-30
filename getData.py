import pandas as pd

urlConfirmed = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
urlDeaths = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv"
urlRecovered = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv"

# Read the dataset from github
globalConfirmed = pd.read_csv(urlConfirmed)
globalDeaths = pd.read_csv(urlDeaths)
globalRecovered = pd.read_csv(urlRecovered)

# Drop unuseful columns in this analysis
globalConfirmed.drop(columns=["Lat", "Long", "Province/State"], inplace=True)
globalDeaths.drop(columns=["Lat", "Long", "Province/State"], inplace=True)
globalRecovered.drop(columns=["Lat", "Long", "Province/State"], inplace=True)

# Group data by country and sum the total case (because there are some country data with different regions).
# Transpose it so that the countries become columns
globalConfirmedByCountries = globalConfirmed.groupby("Country/Region").sum().transpose()
globalDeathsByCountries = globalDeaths.groupby("Country/Region").sum().transpose()
globalRecoveredByCountries = globalRecovered.groupby("Country/Region").sum().transpose()

globalConfirmedByCountriesDateIncluded = (
    globalConfirmedByCountries.reset_index().rename(columns={"index": "Date"})
)
globalDeathsByCountriesDateIncluded = globalDeathsByCountries.reset_index().rename(
    columns={"index": "Date"}
)
globalRecoveredByCountriesDateIncluded = (
    globalRecoveredByCountries.reset_index().rename(columns={"index": "Date"})
)

# create global confirmed dataframe


globalConfirmedByCountriesDateIncluded.to_csv("confirmed.csv")
globalDeathsByCountriesDateIncluded.to_csv("deaths.csv")
globalRecoveredByCountriesDateIncluded.to_csv("recovered.csv")

dfConfirmed = pd.read_csv("confirmed.csv").drop("Unnamed: 0", axis=1)

globalActiveCases = (
    globalConfirmedByCountries - globalDeathsByCountries - globalRecoveredByCountries
)
globalActiveCases = globalActiveCases.reset_index().rename(columns={"index": "Date"})
globalActiveCases.to_csv("active.csv")

dftd = (
    pd.read_csv("confirmed.csv")
    .drop(columns=["Unnamed: 0", "Date"])
    .iloc[1:][:]
    .reset_index(drop=True)
)
dfyst = (
    pd.read_csv("confirmed.csv")
    .drop(columns=["Unnamed: 0", "Date"])
    .iloc[:-1][:]
    .reset_index(drop=True)
)

dailyGlobalNewCases = dftd - dfyst
date = pd.DataFrame({"Date": dfConfirmed.Date[1:]}).reset_index(drop=True)
frames = [date, dailyGlobalNewCases]
dailyGlobalNewCases = pd.concat(frames, axis=1)
dailyGlobalNewCases.to_csv("dailyGlobalNewCases.csv")


def globalTotalConfirmed(date):
    dateIndex = int(dfConfirmed.loc[dfConfirmed.Date == date].index.values)
    print(dateIndex)
    temp = dfConfirmed.loc[dfConfirmed.Date == date].copy()
    ttlCases = temp.drop("Date", axis=1).transpose().sum()
    return ttlCases


# print(globalTotalConfirmed('9/24/20'))

# create total cases dataframe
def createGlobalTotal():
    df = pd.read_csv("confirmed.csv").drop("Unnamed: 0", axis=1)
    ttlList = []
    for ix in range(df.shape[0]):
        ttlList.append(df.iloc[ix, 1:189].sum())
    #     print(len(ttlList),len(df.Date.tolist()))
    newDf = pd.DataFrame()
    newDf["Date"] = df.Date.tolist()
    newDf["Global Total"] = ttlList

    return newDf


createGlobalTotal().to_csv("globalTtl.csv")
# print(df.tail())
