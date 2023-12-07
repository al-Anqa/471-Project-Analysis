import numpy as np
import CoolProp.CoolProp as CP
import pandas as pd

fluid_name = "Air"
temperature =  351.55 # Temperature in K
pressure = 101325  # Pressure in Pa
thickness = 0.01
d_i = 0.10 + 2 * thickness

cp = CP.PropsSI("Cpmass", "T", temperature, "P", pressure, fluid_name)
print(f'cp = {cp}')


#Obtain dynamic viscosity (mu) for air
viscosity = CP.PropsSI("V", "T", temperature, "P", pressure, fluid_name)
print(f'mu = {viscosity}')

m_dot_cold = 25
Re = m_dot_cold / (4 * np.pi * viscosity)
print(f'Re = {Re}')

Pr = CP.PropsSI("Prandtl", "T", temperature, "P", pressure, fluid_name)
print(f'Pr = {Pr}')
Nu = 0.023 * (Re)**0.8 * Pr**0.4

k = CP.PropsSI("conductivity", "T", temperature, "P", pressure, fluid_name)
print(f'k = {k}')

h_coefficient = (Nu * k) 
print(f'h_coef = {h_coefficient}')

length = 10
area = (np.pi * 0.22 * length)
print(f'area = {area}')

new_coeff = h_coefficient * area
print(f'new_coeff = {new_coeff}')

R_cv2 = 0.02
d_o = (new_coeff / R_cv2)**(1/1.8)+d_i
print(f'd_o = {d_o}')