# Retail Price Optimization & Discount Analysis
![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![SciPy](https://img.shields.io/badge/Optimisation-SciPy-orange)
![Status](https://img.shields.io/badge/Status-Complete-brightgreen)
> Measure price elasticity per customer segment and find the revenue-maximising discount rate using Brent's optimisation method.
Project Structure
```
DS4_RetailPrice__config.py      ← Segments, elasticity params, discount range
DS4_RetailPrice__data_gen.py    ← Synthetic 2K transaction dataset
DS4_RetailPrice__elasticity.py  ← Log-log OLS elasticity estimation per segment
DS4_RetailPrice__optimizer.py   ← Revenue-maximising discount (SciPy minimize_scalar)
DS4_RetailPrice__dashboard.py   ← EDA + optimisation curve charts
DS4_RetailPrice__main.py        ← Entry point
DS4_RetailPrice__requirements.txt
```
Run
```bash
pip install -r DS4_RetailPrice__requirements.txt
python DS4_RetailPrice__main.py
```
## Key Results

Segment	Elasticity	Optimal Discount

Budget	~−2.0 (highly elastic)	~33%

Mid-Market	~−1.3 (moderate)	~28%

Premium	~−0.7 (inelastic)	~18%

Premium customers barely respond to discounts — over-discounting erodes margin without meaningful volume gain.
