import numpy as np
import CoolProp.CoolProp as CP
import pandas as pd

def Haaland(epsilon, D, Re_D):
    f = (-1.8 * np.log10 * (((epsilon / D) / 3.7) ** 1.11 + (6.9 / Re_D)) )
    return f

d_i = 
d_o =
thickness = 

R_total = 
