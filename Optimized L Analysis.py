import numpy as np
import CoolProp.CoolProp as CP
import pandas as pd
import matplotlib.pyplot as plt

def Haaland(epsilon, D, Re_D):
    f = (-1.8 * np.log10 * (((epsilon / D) / 3.7) ** 1.11 + (6.9 / Re_D)) )
    return f

def DittusBoelter(Re_D, Pr, n):
    Nu_D = 0.023 * Re_D ** (4/5) * Pr ** n
    return Nu_D

def Reynolds(m_dot, viscosity, d_h):
    Re = (4* m_dot) / (np.pi * viscosity * d_h)
    return Re

d_i = np.arange(0.1, 2, 0.02)
arr = np.zeros((len(d_i), 2))
i=0

for d in d_i:
d_o = 2.5
thickness = 0.01
d_thickness = d_i + 2 * thickness


# Fixed Parameters
m_dot_hot = 9.597
m_dot_cold = 25

t_hot_avg = 449
t_cold_avg = 351.55

p_hot = 450000 # Pa
p_cold = 101325 # Pa

# Hot Stream Flow

visc_i = CP.PropsSI("V", "T", t_hot_avg, "P", p_hot, 'Air')
k_i = CP.PropsSI("conductivity", "T", t_hot_avg, "P", p_hot, 'Air')
Pr_i = CP.PropsSI("Prandtl", "T", t_hot_avg, "P", p_hot, 'Air')
# print(f'Pr_i = {Pr_i}')

Re_i = Reynolds(m_dot_hot, visc_i, d_i)
Nu_i = DittusBoelter(Re_i, Pr_i, 0.3)
h_conv_i = (Nu_i * k_i) / (d_i)

# print(f'Re_i = {Re_i}')
# print(f'Nu_i = {Nu_i}')
# print(f'h_conv_i = {h_conv_i}')

# Cold Stream Flow

visc_o = CP.PropsSI("V", "T", t_cold_avg, "P", p_cold, 'Air')
k_o = CP.PropsSI("conductivity", "T", t_cold_avg, "P", p_cold, 'Air')
Pr_o = CP.PropsSI("Prandtl", "T", t_cold_avg, "P", p_cold, 'Air')

d_ho = d_o - d_thickness
Re_o = Reynolds(m_dot_cold, visc_o, d_ho)
Nu_o = DittusBoelter(Re_o, Pr_o, 0.4)
h_conv_o = (Nu_o * k_o) / (d_ho)

# print(f'Re_o = {Re_o}')
# print(f'Nu_o = {Nu_o}')
# print(f'h_conv_o = {h_conv_o}')

# Conduction (Thickness)
# The R_t we calculate here doesn't have an L because we factor it out
k_cond = 237
R_cond = (np.log((d_thickness / 2) / (d_i / 2))) / (2 * np.pi * k_cond)

R_total = 0.02038769

length = (1 / R_total) * ((1 / (h_conv_i * np.pi * d_i)) + (R_cond) + (1 / (h_conv_o * np.pi * d_thickness)))
print(length)

arr[i, 0] = d
arr[i, 1] = length

i += 1

plt.plot(arr[:, 0], arr[:, 1], label='Cold-flow Outlet Temperature')
plt.legend()
plt.xlabel('Cold-flow Mass Flow Rate [kg/s]')
plt.ylabel('Cold-flow Outlet Temperature, [K]')
plt.title('Cold-flow Outlet Temperature vs. Mass Flow Rate')
plt.grid(axis='x', linestyle='--')