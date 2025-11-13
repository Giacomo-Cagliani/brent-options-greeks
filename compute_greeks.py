import math
from math import log, sqrt, exp
from statistics import NormalDist

def bs_call_price(S, K, T, r, sigma):
    if T<=0 or sigma<=0:
        return max(S-K,0.0)
    d1 = (math.log(S/K) + (r + 0.5*sigma*sigma)*T) / (sigma*math.sqrt(T))
    d2 = d1 - sigma*math.sqrt(T)
    N = NormalDist().cdf
    return S*N(d1) - K*math.exp(-r*T)*N(d2)

def bs_call_delta(S, K, T, r, sigma):
    d1 = (math.log(S/K) + (r + 0.5*sigma*sigma)*T) / (sigma*math.sqrt(T))
    N = NormalDist().cdf
    return N(d1)

def bs_call_gamma(S, K, T, r, sigma):
    d1 = (math.log(S/K) + (r + 0.5*sigma*sigma)*T) / (sigma*math.sqrt(T))
    n = lambda x: math.exp(-0.5*x*x)/math.sqrt(2*math.pi)
    return n(d1) / (S*sigma*math.sqrt(T))

def bs_call_vega(S, K, T, r, sigma):
    d1 = (math.log(S/K) + (r + 0.5*sigma*sigma)*T) / (sigma*math.sqrt(T))
    n = lambda x: math.exp(-0.5*x*x)/math.sqrt(2*math.pi)
    return S * n(d1) * math.sqrt(T)

def bs_call_theta(S, K, T, r, sigma):
    # Theta per year
    d1 = (math.log(S/K) + (r + 0.5*sigma*sigma)*T) / (sigma*math.sqrt(T))
    d2 = d1 - sigma*math.sqrt(T)
    n = lambda x: math.exp(-0.5*x*x)/math.sqrt(2*math.pi)
    N = NormalDist().cdf
    term1 = - (S * n(d1) * sigma) / (2*math.sqrt(T))
    term2 = - r * K * math.exp(-r*T) * N(d2)
    return term1 + term2

# Parameters
S = 60.0
K = 60.0
T_days = 30
T = T_days/365.0
sigma = 0.20
r = 0.0
contract_size = 1000

price_per_bbl = bs_call_price(S,K,T,r,sigma)
delta_per_bbl = bs_call_delta(S,K,T,r,sigma)
gamma_per_bbl = bs_call_gamma(S,K,T,r,sigma)
vega_per_bbl = bs_call_vega(S,K,T,r,sigma)
theta_per_year_per_bbl = bs_call_theta(S,K,T,r,sigma)

# Convert to requested units
# user expects Delta in bbl (i.e., delta * contract_size), Gamma maybe quoted as per USD (per $ move) scaled to contract
price_per_contract = price_per_bbl * contract_size
delta_per_contract = delta_per_bbl * contract_size
gamma_per_contract = gamma_per_bbl * contract_size  # per USD
vega_per_contract = vega_per_bbl * contract_size  # per 1 vol-point (i.e., 0.01)
# Theta returned is per year; convert to per day
theta_per_year_per_contract = theta_per_year_per_bbl * contract_size
theta_per_day_per_contract = theta_per_year_per_contract/365.0

print(f"S={S}, K={K}, T={T_days} days ({T:.6f} yr), sigma={sigma*100:.2f}%, r={r*100:.2f}%")
print('---')
print(f"Price per bbl: {price_per_bbl:.6f} USD")
print(f"Price per contract (1,000 bbl): {price_per_contract:.2f} USD")
print(f"Delta per bbl: {delta_per_bbl:.6f} (unitless)")
print(f"Delta per contract (bbl): {delta_per_contract:.1f} bbl")
print(f"Gamma per bbl: {gamma_per_bbl:.6f} per USD")
print(f"Gamma per contract: {gamma_per_contract:.3f} per USD")
print(f"Vega per bbl: {vega_per_bbl:.6f} USD per 1 vol (i.e., per 100% = unlikely)")
print(f"Vega per contract: {vega_per_contract:.3f} USD per 1 vol (i.e., per 100 vol pts)")
print(f"Vega per contract per 1 vol-point (0.01): {vega_per_contract*0.01:.3f} USD per 1 vol-point (1%)")
print(f"Theta per year per bbl: {theta_per_year_per_bbl:.6f} USD/yr")
print(f"Theta per day per contract: {theta_per_day_per_contract:.3f} USD/day")

# Also print d1,d2 and n(d1)
from math import log, sqrt
d1 = (math.log(S/K) + (r + 0.5*sigma*sigma)*T) / (sigma*math.sqrt(T))
d2 = d1 - sigma*math.sqrt(T)
nd1 = math.exp(-0.5*d1*d1)/math.sqrt(2*math.pi)
print('---')
print(f"d1={d1:.6f}, d2={d2:.6f}, n(d1)={nd1:.6f}")

# Scenario calculations
deltaS_A = 0.02 * S  # +2% move
S_A = S + deltaS_A
price_A = bs_call_price(S_A, K, T, r, sigma)
deltaV_A_exact = (price_A - price_per_bbl) * contract_size
delta_term_A = delta_per_bbl * deltaS_A * contract_size
gamma_term_A = 0.5 * gamma_per_contract * (deltaS_A ** 2)

print('\nScenario A (S +2%):')
print(f"  S -> {S_A:.2f}, ΔV exact per contract: {deltaV_A_exact:.3f} USD")
print(f"  Taylor Δ term: {delta_term_A:.3f} USD, 0.5·Γ·(ΔS)^2: {gamma_term_A:.3f} USD, sum: {delta_term_A+gamma_term_A:.3f} USD")

# Scenario B: vol +5pp
sigma_B = sigma + 0.05
price_B = bs_call_price(S, K, T, r, sigma_B)
deltaV_B_exact = (price_B - price_per_bbl) * contract_size
vega_term_B = (vega_per_contract * 0.01) * 5  # vega per 1% times 5
print('\nScenario B (vol +5pp):')
print(f"  sigma -> {sigma_B:.2%}, ΔV exact per contract: {deltaV_B_exact:.3f} USD")
print(f"  Vega term (approx): {vega_term_B:.3f} USD")

# Scenario C: 5 days decay
T_C = (T_days - 5)/365.0
price_C = bs_call_price(S, K, T_C, r, sigma)
deltaV_C_exact = (price_C - price_per_bbl) * contract_size
theta_term_C = theta_per_day_per_contract * 5
print('\nScenario C (5 days elapsed):')
print(f"  ΔV exact per contract: {deltaV_C_exact:.3f} USD")
print(f"  Theta term (approx): {theta_term_C:.3f} USD")

# 60-day (T=60) Greeks for comparison
T60_days = 60
T60 = T60_days/365.0
price60_bbl = bs_call_price(S, K, T60, r, sigma)
delta60_bbl = bs_call_delta(S, K, T60, r, sigma)
gamma60_bbl = bs_call_gamma(S, K, T60, r, sigma)
vega60_bbl = bs_call_vega(S, K, T60, r, sigma)
theta60_year_bbl = bs_call_theta(S, K, T60, r, sigma)

print('\n60-day option (per contract):')
print(f"  Price per contract: {price60_bbl*contract_size:.2f} USD")
print(f"  Delta per contract: {delta60_bbl*contract_size:.3f} bbl")
print(f"  Gamma per contract: {gamma60_bbl*contract_size:.3f} per USD")
print(f"  Vega per 1% per contract: {vega60_bbl*contract_size*0.01:.3f} USD per 1%")
print(f"  Theta per day per contract: {(theta60_year_bbl*contract_size)/365.0:.3f} USD/day")

# --- Portfolio construction and stress tests ---
# Portfolio: physical short 100 contracts (100,000 bbl)
# We choose a Delta- and Vega-neutral option mix: long 20 x 30-day calls, short 14 x 60-day calls
# Futures are used to neutralise the remaining Delta; we choose 97 futures long (1,000 bbl each) to achieve near-zero Delta.

phys_short = 100  # contracts
futures_long = 97  # contracts
call30_long = 20   # contracts (30-day)
call60_short = 14  # contracts (60-day, short)

# Greeks per contract
delta30 = delta_per_contract
vega30 = vega_per_contract * 0.01  # per 1% vol
theta30 = theta_per_day_per_contract

delta60 = delta60_bbl * contract_size
vega60 = vega60_bbl * contract_size * 0.01
theta60 = (theta60_year_bbl * contract_size) / 365.0

# Portfolio Greeks
total_delta = -phys_short*contract_size + futures_long*contract_size + call30_long*delta30 - call60_short*delta60
total_vega = call30_long*vega30 - call60_short*vega60
total_theta = call30_long*theta30 - call60_short*theta60

print('\n--- Portfolio (delta & vega neutral target) ---')
print(f"Positions: physical short {phys_short}, futures long {futures_long}, 30d calls long {call30_long}, 60d calls short {call60_short}")
print(f"Total Delta (bbl): {total_delta:.1f}")
print(f"Total Vega (USD per 1%): {total_vega:.1f}")
print(f"Total Theta (USD/day): {total_theta:.1f}")

# Stress tests: Case A S -> 65 ( +8.33% ), Case B vol +5pp
S_caseA = 65.0
price30_caseA = bs_call_price(S_caseA, K, T, r, sigma)
price60_caseA = bs_call_price(S_caseA, K, T60, r, sigma)

delta30_caseA = bs_call_delta(S_caseA, K, T, r, sigma) * contract_size
delta60_caseA = bs_call_delta(S_caseA, K, T60, r, sigma) * contract_size

# P&L from revaluation (exact) for options
pv30_before = price_per_contract * call30_long
pv60_before = price60_bbl*contract_size * call60_short * -1  # short
pv30_after = price30_caseA * contract_size * call30_long
pv60_after = price60_caseA * contract_size * call60_short * -1

pv_before_total = pv30_before + pv60_before
pv_after_total = pv30_after + pv60_after
deltaV_portfolio_A = pv_after_total - pv_before_total

print('\nCase A: Spot -> 65 USD/bbl (price move)')
print(f" Option P&L exact (USD): {deltaV_portfolio_A:.2f}")
print(f" Delta before: { (call30_long*delta30 - call60_short*delta60):.1f} bbl")
print(f" Delta after: { (call30_long*delta30_caseA - call60_short*delta60_caseA):.1f} bbl")
print(f" Delta change from options: { (call30_long*delta30_caseA - call60_short*delta60_caseA) - (call30_long*delta30 - call60_short*delta60):.1f} bbl")

# Case B: vol +5pp
sigma_B = sigma + 0.05
price30_B = bs_call_price(S, K, T, r, sigma_B)
price60_B = bs_call_price(S, K, T60, r, sigma_B)
pv30_B = price30_B * contract_size * call30_long
pv60_B = price60_B * contract_size * call60_short * -1
deltaV_portfolio_B = (pv30_B + pv60_B) - (pv30_before + pv60_before)

print('\nCase B: Vol +5pp (20% -> 25%)')
print(f" Option P&L exact (USD): {deltaV_portfolio_B:.2f}")
print(f" Approx Vega P&L (USD): { (call30_long*vega30 - call60_short*vega60) * 5:.2f}")

