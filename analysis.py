import pyromat as pm
import numpy as np

air = pm.get('ig.air')

# Hot stream properties
T_hi = 595 # K
T_ho = 303 # K
m_dot_hot = 3 # kg/s
P_hot = 13 # Bar
c_p_hot = air.cp(T=T_hi, p=P_hot)
C_h = m_dot_hot * c_p_hot

# Cold stream properties
T_ci = 293 # K
m_dot_cold = 5 # kg/s
P_cold = 1.01325 # Bar
c_p_cold = air.cp(T=T_ci, p=P_cold)
C_c = m_dot_cold * c_p_cold

C_min = min(C_c, C_h)
C_max = max(C_c, C_h)
q_max = C_min * (T_hi - T_ci)
C_r = C_min / C_max

print(c_p_cold, c_p_hot)
epsilon = (C_h * (T_hi - T_ho)) / (C_min * (T_hi - T_ci))

if C_r < 1:
    NTU = (1 / (C_r - 1)) * np.log((epsilon - 1) / (epsilon * C_r - 1))
elif C_r == 1:
    NTU = (epsilon) / (1 - epsilon)

R_tot = (NTU * C_min) ** -1
print(R_tot)