import numpy as np
from sklearn.linear_model import LinearRegression



class Divination:
    def __init__(self, periods=4):
        if isinstance(periods, int):
            periods = [2 ** idx for idx in range(periods)]
        self.periods = periods


    def fit(self, data):
        num_last = len(data) - max(self.periods)
        self.regression = LinearRegression().fit(
            X=self.factors(data, num_last),
            y=data.values[-num_last:, :]
        )
        return self
    

    def predict(self, data, num_steps):
        result = data.copy()
        for step in range(num_steps):
            new_index = result.index[-1] + (result.index[-1] - result.index[-2])
            new_row = self.regression.predict(self.factors(result, num_last=1))[0]
            result.loc[new_index] = new_row
        return result
    

    def factors(self, data, num_last):
        return np.array([
            data[var][-period - num_last:].rolling(window=period).mean()[-num_last:] for var in data.columns for period in self.periods
        ]).transpose()