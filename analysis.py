import pyromat as pm

air = pm.get('ig.air')

m_doth = 3 # kg/s
T_hi = 595 # K
T_ho = 303 # K
P_h = 13 # Bar

T_hf = (T_hi + T_ho) / 2
rho_hf = air.d(T=T_hf, p=P_h)
c_ph =  air.cp(T=T_hf, p=P_h)
print(rho_hf)

q = m_doth * c_ph * (T_hi - T_ho)
print(q)