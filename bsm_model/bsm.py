import numpy as np
from scipy.optimize import brentq, newton
from scipy.stats import norm
from datetime import date

class BSM:
    """A option modelled using Black–Scholes–Merton Option Pricing Model
    """

    def __init__(self, S=None, K=None, r=None, T=None, calculation_date=None, expiration_date=None, P=None, q=0,
                 option_type='call', optimization_method='newton', trading_days=False):
        """Initialize Option Class

        Args:
            S (float): Current price of the underlying asset.
            K (float): Strike price of the option.
            r (float): Risk-free interest rate most appropriate for this option.
            T (float): Number of days till the expiration date.
            P (float, optional): Market price of the option
            q (int, optional): Continuous dividend yield. Defaults to 0.
            type (str): Type of the option. Either 'call' or 'put'. Defaults to 'call'.
            method (str): Optimization method to find iv.
        Returns:
            [type]: [description]
        """

        # Check variables and inputs
        if option_type.lower() not in ['call', 'put']:
            raise ValueError("Option can only be either a call or put.")

        if all([T, any([calculation_date, expiration_date])]):
            raise ValueError("You can either use T or (calculation_date & expiration_date)")
        
        # if date arguments are used, convert string to date
        if all([calculation_date, expiration_date]):
            calculation_date = date(int(calculation_date[0:4]), int(calculation_date[5:7]), int(calculation_date[8:10]))
            expiration_date = date(int(expiration_date[0:4]), int(expiration_date[5:7]), int(expiration_date[8:10]))

        # for the trading_days argument
        _days_in_year = 252 if trading_days else 365

        # Assign values to the class
        self.S = S
        self.K = K
        self.r = r
        self.T = T / _days_in_year if T else (expiration_date - calculation_date).days / _days_in_year
        self.P = P
        self.q = q
        self.type = option_type.lower()
        self.method = optimization_method.lower()

    def d1(self, iv):
        _d1 = (np.log(self.S / self.K) + (self.r + iv ** 2 / 2) * self.T) / (iv * np.sqrt(self.T))
        return _d1

    def d2(self, iv):
        _d2 = (np.log(self.S / self.K) + (self.r - iv ** 2 / 2) * self.T) / (
                iv * np.sqrt(self.T))  # same as d1 - iv*np.sqrt(self.T)
        return _d2

    def price(self, iv):
        _d1 = self.d1(iv)
        _d2 = self.d2(iv)

        if self.type == 'call':
            _price = np.exp(-self.q * self.T) * self.S * norm.cdf(_d1) - self.K * np.exp(-self.r * self.T) * norm.cdf(
                _d2)
        else:
            _price = self.K * np.exp(-self.r * self.T) * norm.cdf(-_d2) - np.exp(-self.q * self.T) * self.S * norm.cdf(
                -_d1)

        return _price

    def iv(self):
        if self.method == 'newton':
            # Brenner, M., & Subrahmanyam, M. (1988).
            # A Simple Formula to Compute the Implied Standard Deviation.
            # Financial Analysts Journal, 44(5), 80-83.
            # Retrieved April 3, 2021, from http://www.jstor.org/stable/4479152
            # Maybe use this link to improve: https://www.sciencedirect.com/science/article/abs/pii/0378426695000143
            _init_value = np.sqrt(2 * np.pi / self.T) * (self.P / self.S)
            _iv = newton(lambda sigma: self.P - self.price(sigma), _init_value, maxiter=50)
        elif self.method == 'brent':
            _iv = brentq(lambda sigma: self.P - self.price(sigma), -1e-6, 1)
        return _iv

    def delta(self):
        _sigma = self.iv()
        _d1 = self.d1(_sigma)
        _delta = norm.cdf(_d1) if self.type == 'call' else norm.cdf(_d1) - 1
        # if self.type == 'call':
        #     _delta = norm.cdf(_d1)
        # elif self.type == 'put':
        #     _delta = norm.cdf(_d1) - 1
        return _delta

    def theta(self):
        _sigma = self.iv()
        _d1, _d2 = self.d1(_sigma), self.d2(_sigma)
        if self.type == 'call':
            _theta = -(self.S * norm.pdf(_d1) * _sigma) / (2 * np.sqrt(self.T)) - self.r * self.K * np.exp(
                -self.r * self.T) * norm.cdf(_d2)
        else:
            _theta = -(self.S * norm.pdf(_d1) * _sigma) / (2 * np.sqrt(self.T)) + self.r * self.K * np.exp(
                -self.r * self.T) * norm.cdf(-_d2)
        return _theta / 365

    def gamma(self):
        _sigma = self.iv()
        _d1, _d2 = self.d1(_sigma), self.d2(_sigma)
        _gamma = norm.pdf(_d1) / (self.S * _sigma * np.sqrt(self.T))
        return _gamma

    def vega(self):
        _sigma = self.iv()
        _d1, _d2 = self.d1(_sigma), self.d2(_sigma)

        _vega = self.S * np.sqrt(self.T) * norm.pdf(_d1)

        return _vega / 100

    def rho(self):
        _sigma = self.iv()
        _d1, _d2 = self.d1(_sigma), self.d2(_sigma)

        if self.type == 'call':
            _rho = self.K * self.T * np.exp(-self.r * self.T) * norm.cdf(_d2)
        else:
            _rho = -self.K * self.T * np.exp(-self.r * self.T) * norm.cdf(-_d2)
        return _rho / 100
