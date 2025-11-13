# Brent Options – Delta Hedging Limitations and Greek-Based Risk Management

Delta hedging is often treated as a complete solution to spot risk, but in practice it only neutralizes the first-order exposure. In energy markets, volatility repricing, convexity drift, and time decay can dominate P&L once Delta is flattened.

In this project, based on my recent paper, I apply the Black–Scholes framework to an at-the-money Brent call to quantify how Delta, Gamma, Vega, and Theta interact after hedging. The analysis shows that a pure Delta hedge leaves meaningful Vega and Theta exposure, convexity forces Delta to drift unless rebalanced, and a balanced combination of futures and short-dated options keeps Delta and Vega near zero while treating Theta as a controlled carry. This approach offers a practical hedge playbook for energy desks: measure Greeks in physical units, rebalance frequently, and view Theta as the cost of resilience when volatility spikes.

## Project Structure

### compute_greeks.py

Python script that reproduces all valuations and Greeks used in the study. It includes:

* Black–Scholes pricing for a Brent ATM call
* Analytical Greeks (Delta, Gamma, Vega, Theta)
* Scenario checks for spot, volatility, and time shocks
* Example portfolio scaling from per-barrel to physical units

### Options.pdf

The full paper *“The limitations of delta hedging in option portfolios – An empirical simulation on Brent crude oil”*.
It covers:

* Pricing framework and Greek interpretation
* Taylor-based scenario attribution
* Construction of a delta–vega–theta balanced portfolio
* Stress tests for spot rallies and volatility shocks
* Practical hedging rules for energy desks

### Options.md

Markdown version of the paper, readable directly in GitHub.

### Options.png

3D option value surface showing call price as a function of Brent spot (50–70 USD/bbl) and implied volatility (10–40%) for a 30-day maturity. The curvature and steep volatility gradient highlight why a delta hedge alone is insufficient.

## Key Takeaways

* Delta hedging neutralizes only first-order exposure.
* Residual Vega and Theta risk can dominate P&L.
* Gamma causes Delta to drift unless the hedge is frequently rebalanced.
* Mixing futures and offsetting short-dated options stabilizes Delta and Vega.
* Theta should be treated as a deliberate and transparent cost of maintaining resilience.
