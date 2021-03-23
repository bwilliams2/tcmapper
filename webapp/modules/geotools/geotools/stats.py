import pandas as pd
import numpy as np


def growth_rates(data: pd.DataFrame):
    def calc_cumsums(df: pd.DataFrame):
        d = df.groupby("YEAR_BUILT").size()
        d.name = "New"
        cumsums = d.cumsum()
        cumsums.name = "Total"
        d = d.to_frame().join(cumsums)
        vals = d.values
        rates = np.insert(vals[1:, 0]/vals[:-1,1], 0, 0)
        d["Rates"] = rates
        diffs = 6
        return d
    year_class_sums = data.groupby("USECLASS1").apply(calc_cumsums).reset_index()
    plot_data = []
    for useclass, df in year_class_sums.groupby("USECLASS1"):
        points = df.to_dict(orient="records")
        plot_data.append({"id": useclass, "points":points})
    
    return plot_data
    
    