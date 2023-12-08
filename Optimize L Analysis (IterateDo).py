import numpy as np
import CoolProp.CoolProp as CP
import pandas as pd
import matplotlib.pyplot as plt

def Haaland(epsilon, D, Re_D):
    f = (-1.8 * np.log10(((epsilon / D) / 3.7) ** 1.11 + (6.9 / Re_D)) )
    return f

def DittusBoelter(Re_D, Pr, n):
    Nu_D = 0.023 * Re_D ** (4/5) * Pr ** n
    return Nu_D

def Reynolds(m_dot, viscosity, d_h):
    Re = (4* m_dot) / (np.pi * viscosity * d_h)
    return Re


d_o = np.arange(1, 0.34, -0.01)
arr = np.zeros((len(d_o), 4))

df = pd.DataFrame(arr)
df.columns = ['External Flow Diameter', 'Length', 'Pressure Drop', 'Outer Flow Reynolds']

i=0

for out_dim in d_o:
    d_i = 0.32
    thickness = 0.01
    d_thickness = d_i + 2 * thickness

    epsilon = 0.015

    # Fixed Parameters
    m_dot_hot = 9.68
    m_dot_cold = 25

    t_hot_avg = 389.475
    t_cold_avg = 332.264

    p_hot = 450000 # Pa
    p_cold = 101325 # Pa

    # Hot Stream Flow

    visc_i = CP.PropsSI("V", "T", t_hot_avg, "P", p_hot, 'Air')
    k_i = CP.PropsSI("conductivity", "T", t_hot_avg, "P", p_hot, 'Air')
    Pr_i = CP.PropsSI("Prandtl", "T", t_hot_avg, "P", p_hot, 'Air')
    rho_i = CP.PropsSI("Dmass", "T", t_hot_avg, "P", p_hot, 'Air')
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

    d_ho = out_dim - d_thickness
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

    R_total = 0.024973983029638967 # Taken from NTU Analysis.py

    length = (1 / R_total) * ((1 / (h_conv_i * np.pi * d_i)) + (R_cond) + (1 / (h_conv_o * np.pi * d_thickness)))
    print(length)

    P_drop = (8 * Haaland(epsilon, d_i, Re_i) * m_dot_hot ** 2) / (np.pi ** 2 * d_i ** 5 * rho_i)

    df['External Flow Diameter'].iloc[i] = out_dim
    df['Length'].iloc[i] = length
    df['Pressure Drop'].iloc[i] = P_drop
    df['Outer Flow Reynolds'].iloc[i] = Re_o    

    i += 1

df.to_csv('Optimized L Analysis (Do).csv', index=False)

# plt.figure(1)
# plt.plot(df['Internal Flow Diameter'], df['Length'], label='Hot-flow Pipe Diameter, [m]')
# plt.legend()
# plt.xlabel('Hot-flow Pipe Diameter, [m]')
# plt.ylabel('Heat Exhanger Length [m]')
# plt.title('Heat Exhanger Length vs. Hot-flow Pipe Diameter')
# plt.grid(axis='x', linestyle='--')

# plt.show()

# plt.figure(2)
# plt.plot(df['Internal Flow Diameter'], df['Pressure Drop'], label='Pressure Drop [Pa]')
# plt.legend()
# plt.xlabel('Hot-flow Pipe Diameter, [m]')
# plt.ylabel('Pressure Drop, [Pa]')
# plt.title('Pressure Drop [kPa] vs. Hot-flow Pipe Diameter')
# plt.grid(axis='x', linestyle='--')

# plt.show()
