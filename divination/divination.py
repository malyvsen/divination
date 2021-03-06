import numpy as np
from sklearn.linear_model import Ridge



class Divination:
    def __init__(self, regression=None, periods=4):
        self.regression = Ridge() if regression is None else regression
        if isinstance(periods, int):
            periods = [2 ** idx for idx in range(periods)]
        self.periods = periods


    def fit(self, data):
        num_last = len(data) - max(self.periods) - 1
        self.regression.fit(
            X=self.factors(data.iloc[:-1], num_last),
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