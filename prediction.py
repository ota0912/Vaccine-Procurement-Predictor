import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import matplotlib
import numpy as np

def predict(vaccine,state,year):
    df = pd.read_csv("./Web Scraper/compiled_report.csv")
    df = df[(df["VACCINE"]==vaccine) & (df["STATE"]==state)]
    df = df.iloc[initial:final]
    df = df.drop("STATE",axis = 1)
    df = df.drop("VACCINE",axis = 1)
    x = df["YEAR"]
    y = df["APPLICANTS"]
    z = df["VACCINATED"]
    inp = np.copy(x)
    inp = inp.reshape(len(x),1)
    output_cases = np.copy(y)
    output_vaccinated = np.copy(z)
    reg1 = LinearRegression().fit(inp, output_cases)#model for cases
    reg2 = LinearRegression().fit(inp, output_vaccinated)#model for vaccinated
    x=x.to_list()
    y=y.to_list()
    z=z.to_list()
    prediction_data = {}
    last_year = x[-1]
    for i in range (last_year+1,year+1):
        cases = int(np.trunc(reg1.predict([[i]])))
        prediction_data[i] = [cases]
        x.append(i)
        y.append(cases)
    yearly_increase = int((prediction_data[year][0]-z[-1])/(year-last_year))
    itr = z[-1]
    for i in range(last_year+1,year+1):
        itr += yearly_increase
        z.append(itr)
        prediction_data[i].append(itr)
    meet = "Infinity"
    for i in range(last_year+1,3000):
        curr_cases = int(np.trunc(reg1.predict([[i]]))) 
        curr_vacc = int(np.trunc(reg2.predict([[i]])))
        if(curr_vacc>=curr_cases):
            meet = i
    fig,ax = plt.subplots(figsize=(8,5))
    x = np.array(x)
    ax.plot(x,y)
    ax.plot(x,z)
    locator = matplotlib.ticker.MultipleLocator(2)
    plt.gca().xaxis.set_major_locator(locator)
    formatter = matplotlib.ticker.StrMethodFormatter("{x:.0f}")
    plt.gca().xaxis.set_major_formatter(formatter)
    ax.set(title = f"{state} report of {vaccine}",xlabel = "Year",ylabel = "Cases every year")
    plt.savefig('graph.png')
    return {"data":prediction_data,"meet":meet}
