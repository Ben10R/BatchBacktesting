
from backtesting import Backtest, Strategy
from backtesting.lib import crossover
import numpy as np
import pandas_ta as taPanda


class AbstractStrategy(Strategy):
    def init(self):
        pass

    def next(self):
        pass

    def optimize_parameters(self):
        pass

    def optimize_func(self):
        pass

    def optimize_run(self):
        pass


class EMA(Strategy):
    n1 = 20
    n2 = 80
    n3 = 150

    def init(self):
        close = self.data.Close
        self.ema20 = self.I(taPanda.ema, close.s, self.n1)
        self.ema80 = self.I(taPanda.ema, close.s, self.n2)
        self.ema150 = self.I(taPanda.ema, close.s, self.n3)

    def next(self):
        price = self.data.Close
        if crossover(self.ema20, self.ema80):
            self.position.close()
            self.buy(sl=0.90 * price, tp=1.25 * price)

        elif crossover(self.ema80, self.ema20):
            self.position.close()
            self.sell(sl=1.10 * price, tp=0.75 * price)

    def optimize_parameters(self):
        self.n1 = self.I(taPanda.ema, self.data.Close.s, self.n1)
        self.n2 = self.I(taPanda.ema, self.data.Close.s, self.n2)
        self.n3 = self.I(taPanda.ema, self.data.Close.s, self.n3)

    def optimize_func(self):
        self.optimize(
            n1=range(10, 30, 5),
            n2=range(10, 30, 5),
            n3=range(10, 30, 5),
            maximize="Equity Final [$]",
        )

    def optimize_run(self, instrument):
        self.optimize_parameters(instrument)
        self.run()

class RSI(Strategy):
    n1 = 14
    n2 = 30
    n3 = 70

    def init(self):
        close = self.data.Close
        self.rsi = self.I(taPanda.rsi, close.s, self.n1)
        self.rsi30 = self.I(taPanda.rsi, close.s, self.n2)
        self.rsi70 = self.I(taPanda.rsi, close.s, self.n3)

    def next(self):
        price = self.data.Close
        if crossover(self.rsi, self.rsi30):
            self.position.close()
            self.buy(sl=0.90 * price, tp=1.25 * price)

        elif crossover(self.rsi70, self.rsi):
            self.position.close()
            self.sell(sl=1.10 * price, tp=0.75 * price)

    def optimize_parameters(self):
        self.n1 = self.I(taPanda.rsi, self.data.Close.s, self.n1)
        self.n2 = self.I(taPanda.rsi, self.data.Close.s, self.n2)
        self.n3 = self.I(taPanda.rsi, self.data.Close.s, self.n3)

    def optimize_func(self):
        self.optimize(
            n1=range(10, 30, 5),
            n2=range(10, 30, 5),
            n3=range(10, 30, 5),
            maximize="Equity Final [$]",
        )

    def optimize_run(self):
        self.optimize_parameters()
        self.run()

class BollingerBands(Strategy):
    n1 = 20
    n2 = 2

    def init(self):
        close = self.data.Close
        self.bbands = self.I(taPanda.bbands, close.s, self.n1, self.n2)

    def next(self):
        price = self.data.Close
        if crossover(price, self.bbands[0]):
            self.position.close()
            self.buy(sl=0.90 * price, tp=1.25 * price)

        elif crossover(self.bbands[0], price):
            self.position.close()
            self.sell(sl=1.10 * price, tp=0.75 * price)

class MACD(Strategy):
    n1 = 12
    n2 = 26
    n3 = 9

    def init(self):
        close = self.data.Close
        self.macd = self.I(taPanda.macd , close.s, self.n1, self.n2, self.n3)

    def next(self):
        price = self.data.Close
        if crossover(self.macd[0], self.macd[1]):
            self.position.close()
            self.buy(sl=0.90 * price, tp=1.25 * price)

        elif crossover(self.macd[1], self.macd[0]):
            self.position.close()
            self.sell(sl=1.10 * price, tp=0.75 * price)

class LinearRegression(Strategy):
    n1 = 20
    n2 = 2

    def init(self):
        close = self.data.Close
        self.lreg = self.I(taPanda.linreg, close.s, self.n1, self.n2)

    def next(self):
        price = self.data.Close
        if crossover(price, self.lreg):
            self.position.close()
            self.buy(sl=0.90 * price, tp=1.25 * price)

        elif crossover(self.lreg, price):
            self.position.close()
            self.sell(sl=1.10 * price, tp=0.75 * price)


class StandardDeviation(Strategy):
    n1 = 20

    def init(self):
        close = self.data.Close
        self.std = self.I(taPanda.stdev, close.s, self.n1)

    def next(self):
        price = self.data.Close
        if crossover(price, self.std):
            self.position.close()
            self.buy(sl=0.90 * price, tp=1.25 * price)

        elif crossover(self.std, price):
            self.position.close()
            self.sell(sl=1.10 * price, tp=0.75 * price)


class EBSW(Strategy):
    def init(self):
        close = self.data.Close
        self.ebsw = self.I(taPanda.ebsw, close.s)

    def next(self):
        price = self.data.Close
        if crossover(price, self.ebsw):
            self.position.close()
            self.buy(sl=0.90 * price, tp=1.25 * price)

        elif crossover(self.ebsw, price):
            self.position.close()
            self.sell(sl=1.10 * price, tp=0.75 * price)

class ADX(Strategy):
    def init(self):
        close = self.data.Close
        self.adx = self.I(taPanda.adx, self.data.High.s, self.data.Low.s, close.s)

    def next(self):
        price = self.data.Close
        if self.adx[-1] > 25:
            self.buy()
        elif self.adx[-1] < 25:
            self.sell()

class AD(Strategy):
    def init(self):
        close = self.data.Close
        self.ad = self.I(taPanda.ad, self.data.High.s, self.data.Low.s, close.s, self.data.Volume.s)

    def next(self):
        price = self.data.Close
        if self.ad[-1] > self.ad[-2]:
            self.buy()
        elif self.ad[-1] < self.ad[-2]:
            self.sell()

class TRIX(Strategy):
    def init(self):
        close = self.data.Close
        self.trix = self.I(taPanda.trix, close.s)

    def next(self):
        price = self.data.Close
        if self.trix[-1] > self.trix[-2]:
            self.buy()
        elif self.trix[-1] < self.trix[-2]:
            self.sell()

class Aberration(Strategy):
    def init(self):
        close = self.data.Close
        self.aberration = self.I(taPanda.aberration, self.data.High.s, self.data.Low.s, close.s)

    def next(self):
        price = self.data.Close
        if self.aberration[-1] > self.aberration[-2]:
            self.buy()
        elif self.aberration[-1] < self.aberration[-2]:
            self.sell()

class OBV(Strategy):
    def init(self):
        close = self.data.Close
        self.obv = self.I(taPanda.obv, close.s, self.data.Volume.s)

    def next(self):
        price = self.data.Close
        if self.obv[-1] > self.obv[-2]:
            self.buy()
        elif self.obv[-1] < self.obv[-2]:
            self.sell()

class StochasticOscillator(Strategy):
    def init(self):
        close = self.data.Close
        self.stoch = self.I(taPanda.stoch, self.data.High.s, self.data.Low.s, close.s)

    def next(self):
        price = self.data.Close
        if crossover(self.stoch[0], self.stoch[1]):
            self.position.close()
            self.buy(sl=0.90 * price, tp=1.25 * price)

        elif crossover(self.stoch[1], self.stoch[0]):
            self.position.close()
            self.sell(sl=1.10 * price, tp=0.75 * price)

class PercentageReturn(Strategy):
    def init(self):
        close = self.data.Close
        self.pr = self.I(taPanda.percent_return, close.s)

    def next(self):
        price = self.data.Close
        if self.pr[-1] > self.pr[-2]:
            self.buy()
        elif self.pr[-1] < self.pr[-2]:
            self.sell()

class AroonOscillator(Strategy):
    def init(self):
        close = self.data.Close
        self.aroon = self.I(taPanda.aroon, high=self.data.High.s, low=self.data.Low.s)

    def next(self):
        # aroon up self.aroon[0]
        # aroon down self.aroon[1]
        # aroon oscillator self.aroon[2]
        price = self.data.Close
        if crossover(price, self.aroon[0]):
            self.position.close()
            self.buy(sl=0.90 * price, tp=1.25 * price)

        elif crossover(self.aroon[1], price):
            self.position.close()
            self.sell(sl=1.10 * price, tp=0.75 * price)

class SimpleMeanReversion(Strategy):
    def init(self):
        close = self.data.Close
        self.sma = self.I(taPanda.sma, close.s, 20)
        self.std = self.I(taPanda.stdev, close.s, 20)

    def next(self):
        price = self.data.Close
        if crossover(price, self.sma):
            self.position.close()
            self.buy(sl=0.90 * price, tp=1.25 * price)

        elif crossover(self.sma, price):
            self.position.close()
            self.sell(sl=1.10 * price, tp=0.75 * price)

class MAD(Strategy):
    def init(self):
        close = self.data.Close
        self.mad = self.I(taPanda.mad, close.s)

    def next(self):
        price = self.data.Close
        if self.mad[-1] > self.mad[-2]:
            self.buy()
        elif self.mad[-1] < self.mad[-2]:
            self.sell()

# class FourierTransform(Strategy):
#     def FFT(self, x):
#         """
#         A recursive implementation of
#         the 1D Cooley-Tukey FFT, the
#         input should have a length of
#         power of 2.
#         """
#         N = len(x)
#         if N == 1:
#             return x
#         X_even = self.FFT(x[::2])
#         X_odd = self.FFT(x[1::2])
#         factor = \
#             np.exp(-2j*np.pi*np.arange(N)/ N)
#         return np.concatenate(
#             [
#                 X_even + factor[: int(N / 2)] * X_odd,
#                 X_even + factor[int(N / 2) :] * X_odd,
#             ]
#         )

#     def init(self):
#         close = self.data.Close
#         self.ft = self.I(self.FFT, close.s)

#     def next(self):
#         price = self.data.Close
#         if self.ft[-1] > self.ft[-2]:
#             self.buy()
#         elif self.ft[-1] < self.ft[-2]:
#             self.sell()

class CDLZ(Strategy):
    def init(self):
        close = self.data.Close
        self.zigzag = self.I(taPanda.cdl_z, self.data.Open.s, self.data.High.s, self.data.Low.s, close.s)

    def next(self):
        price = self.data.Close
        if self.zigzag[-1] > self.zigzag[-2]:
            self.buy()
        elif self.zigzag[-1] < self.zigzag[-2]:
            self.sell()

class MOM(Strategy):
    def init(self):
        close = self.data.Close
        self.mom = self.I(taPanda.mom, close.s)

    def next(self):
        price = self.data.Close
        if self.mom[-1] > self.mom[-2]:
            self.buy()
        elif self.mom[-1] < self.mom[-2]:
            self.sell()

STRATEGIES = [
    EMA,
    RSI,
    BollingerBands,
    MACD,
    LinearRegression,
    OBV,
    AD,
    ADX,
    StochasticOscillator,
    StandardDeviation,
    EBSW,
    TRIX,
    Aberration,
    AroonOscillator,
    SimpleMeanReversion,
    MAD,
    # FourierTransform,
    CDLZ,
    MOM,
]

STRATEGIES_STR = [
    "EMA",
    "RSI",
    "BollingerBands",
    "MACD",
    "LinearRegression",
    "OBV",
    "AD",
    "ADX",
    "StochasticOscillator",
    "StandardDeviation",
    "EBSW",
    "TRIX",
    "Aberration",
    "AroonOscillator",
    "SimpleMeanReversion",
    "MAD",
    # "FourierTransform",
    "CDLZ",
    "MOM",
]