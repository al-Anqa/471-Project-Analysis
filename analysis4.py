import pyromat as pm

air = pm.get('ig.air')

den = air.d(T=477.05, p=4.5)
print(den)