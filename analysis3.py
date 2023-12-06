import numpy as np
import CoolProp.CoolProp as CP
import pandas as pd

fluid_name = "Air"
temperature =  (476.03321731 + 293)/2  # Temperature in K
pressure = 101325  # Pressure in Pa

#Obtain dynamic viscosity (mu) for air
viscosity = CP.PropsSI("V", "T", temperature, "P", pressure, fluid_name)
density = CP.PropsSI("D", "T", temperature, "P", pressure, fluid_name)


m_dot = 3

diameters = np.linspace(0.01, 0.5, 100)
length = np.linspace(0.1, 10, 100)

solution = np.zeros((len(diameters), len(length)))

i=0

for d in diameters:
    j=0
    for l in length:
        delta_P = (128 * m_dot * viscosity * l) / (np.pi * density * d)
        solution[i, j] = delta_P
        j += 1
    i += 1  

df = pd.DataFrame(solution)
df.to_excel('output.xlsx', index=False)
print(solution)
