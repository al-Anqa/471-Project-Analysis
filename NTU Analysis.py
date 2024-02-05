import pyromat as pm
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.interpolate import *


air = pm.get('ig.air')

# Hot stream properties
T_hi = 475.95 # K, taken from T_16a on EEs
T_ho = 303 # K
m_dot_hot = 9.68 # kg/s, taken from m_dot_brayton on EES
P_hot = 4.531 # Bar, taken from P_16a on EES
c_p_hot = air.cp(T=T_hi, p=P_hot)
print(c_p_hot)
C_h = m_dot_hot * c_p_hot

# Cold stream properties
T_ci = 293 # K
# We set this as an array of values to find which when we hit dimishing returns
m_dot_cold = np.arange(11, 50, 0.1) # kg/s
P_cold = 1.01325 # Bar
c_p_cold = air.cp(T=T_ci, p=P_cold)
print(c_p_cold)


arr = np.zeros((len(m_dot_cold), 6))
i=0

# We do the NTU analysis for all the mass flow rates.
for mfr in m_dot_cold:
    # print(f'The mass flow rate is {mfr}')
    C_c = mfr * c_p_cold
    C_min = min(C_c, C_h)
    C_max = max(C_c, C_h)
    q_max = C_min * (T_hi - T_ci)
    C_r = C_min / C_max
    # print(f'C_r is {C_r}')
    # print(c_p_cold, c_p_hot)

    epsilon = (C_h * (T_hi - T_ho)) / (C_min * (T_hi - T_ci))
    # print(f'For this flow rate, epsilon is {epsilon}')

    if C_r < 1:
        NTU = (1 / (C_r - 1)) * np.log((epsilon - 1) / (epsilon * C_r - 1))
    elif C_r == 1:
        NTU = (epsilon) / (1 - epsilon)

    # print(f'For this flow rate, the NTU is {NTU} and the C_r is {C_r}')
    R_tot = (NTU * C_min) ** -1
    # print(f'For this flow rate, the R_total is {R_tot}')

    T_co = ((epsilon * (C_min * (T_hi - T_ci))) / C_c) + T_ci
    # print(f'For this flow rate, the cold stream outlet is {T_co}')


    arr[i, 0] = mfr
    arr[i, 1] = T_co
    arr[i, 2] = R_tot
    arr[i, 3] = epsilon
    arr[i, 4] = NTU
    arr[i, 5] = C_r

    i += 1

# print(arr)
df = pd.DataFrame(arr)
df.columns = ['Mass Flow Rate', 'Cold-Stream Outlet', 'Total Resistance', 'Epsilon/Effectiveness', 'NTU', 'C_r']
df.to_csv('NTU Analysis.csv', index=False)

plt.figure(figsize=(8,5))
plt.plot(arr[:, 0], arr[:, 1], label='Cold-flow Outlet Temperature')
plt.legend()
plt.xlabel('Cold-flow Mass Flow Rate [kg/s]')
plt.ylabel('Cold-flow Outlet Temperature, [K]')
plt.title('Cold-flow Outlet Temperature vs. Mass Flow Rate')
plt.grid(axis='x', linestyle='--')

sig_mfr = np.arange(10, 50, 5)
for flow in sig_mfr:
    interp = np.interp(flow, arr[:, 0], arr[:, 1])
    print(f'For a flow of {flow}, we have a T_co of {interp}')

plt.savefig('Figures\\T_co vs m_dot_cold.png')
plt.show()
