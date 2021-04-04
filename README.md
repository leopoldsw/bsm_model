# BSM Model

This simple Python package calculates some basic stats for options using the Black–Scholes–Merton (BSM) model. 

It can be used to estimate implied volatility, greeks (delta, gemma, theta, vega, rho) and the price of the option. 

## Install

`pip install bsm-model`

## Import

`from bsm_model import BSM`

## Create an option

We can create an instance of the BSM class:

`random_option = BSM(S, K, r, T, P, option_type)`

Available arguments include

- S is the price of the underlying asset. 
- K is the strike price.
- r is the risk free interest rate.
- T is the number of **days** till expiration. 
- calculation_date is the date when you want the calculations to represent. You can't use this concurrently with T.
- expiration_date is the option expiration date. You can't use this concurrently with T.
- P is the price of the option.
- q is the continuous dividend yield.
- option_type is the type of option, either call or put. Default is call.
- optimization_method is the optimization method used to estimate implied volatility. Default is newton.
- trading_days is a boolean to indicate whether you want consider only trading days. Default is False. If False, 365 is used as the number of days in a year. If True, 252 is used as the number of days in a year. 

## Calculations

Then, calling different methods. For example, the following method gives the delta of the option:

`random_option.delta()`
