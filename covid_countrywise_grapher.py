# Colab Link: https://colab.research.google.com/drive/1sg7NX_B8eT0OgzKkEj3BHgUEmrTT61TS

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

data = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')
pop = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/UID_ISO_FIPS_LookUp_Table.csv')

by_population_percentage = False
logarithmic = False

def get_pop(country):
    c_pop = pop[pop['Country_Region'] == country]['Population'].values.tolist()[0]
    return int(c_pop)

def get_country_data(country):
    c_data = data[data['Country/Region'] == country]
    c_int = c_data.iloc[:, 4:].values.tolist()[0]
    return np.array(c_int)

countries = input("Enter countries to graph for: ").split(', ')

for c in countries:
    c_data = get_country_data(c)/get_pop(c) if by_population_percentage else get_country_data(c)
    days = [i+1 for i in range(len(c_data))]
    plt.plot(days, c_data, label=c)
    plt.xlabel('Days', color='r'), plt.ylabel('Confirmed Cases', color='r'), plt.title('COVID-19 Confirmed Cases', color='b')
  
if logarithmic: plt.yscale('log')
plt.legend(loc='upper left' if not logarithmic else 'lower right')
plt.show()