import os
import pandas as pd
import numpy as np
import re
import json
from sklearn.linear_model import LinearRegression

pwd = os.getcwd()

df = pd.read_csv('metropop_2010_2019.csv')

def explode_str(df, col='Metro-Area', sep='-'):
    s = df[col]
    i = np.arange(len(s)).repeat(s.str.count(sep) +1)
    return df.iloc[i].assign(**{col: sep.join(s).split(sep)})

new_df = explode_str(df)

def metro_lists_gen(new_df):
    new_df.rename(columns={"Metro-Area": 'metro_area',
                            "State": "state"}, inplace=True)
    new_df['metro_area'] = new_df['metro_area'].apply(lambda row: row.lower())
    lists = new_df[['metro_area', 'state']].unique().tolist()
    with open('metro_list.json', 'w', encoding='utf-8') as f:
        json.dump(lists, f, ensure_ascii=False, indent=4)
    return lists, new_df


def selecting_metro(df, metro):
    df = df.loc[df['metro_area'] == metro]
    df.drop(['metro_area', 'Census', 'Estimate Base'], axis=1, inplace=True)
    df = df.T
    df.dropna(inplace=True)
    df = df.reset_index()
    return df

def prediction_model(df):
    x = df.iloc[:, 0].values.reshape(-1, 1)
    y = df.iloc[:, 1].values.reshape(-1, 1)
    model = LinearRegression().fit(x,y)
    return model

def prediction(model, year):
    return int(model.coef_[0][0] * year + model.intercept_[0])

def main():
    metro = input('Please input the metro area: ').lower()
    year = int(input('Pleae enter the year to predict: '))
    df = new_df
    lists, df = metro_lists_gen(df)
    if metro in lists:
        df = selecting_metro(df, metro)
        model = prediction_model(df)
        result = prediction(model, year)
        print(f'\n Result: {metro.upper()} population in {year} will be {result:,d}')
    else:
        print("Kindly check available metro names and spelling from metro_list.json")

if __name__ == '__main__':
    main()

