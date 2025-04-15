# %% [markdown]
# # Deflection Curve for Thesis

# %% [markdown]
# ## Packages

# %%
import sys
sys.path.append("./")
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize

# %% [markdown]
# ## Table Overview

# %%

defl_torque = pd.read_csv("./2in1 Springs/150Nm+150Nm/defl_torque.csv", header=None)
defl = defl_torque.iloc[:, 0]
torque = defl_torque.iloc[:, 1]

Shift = pd.read_csv("./2in1 Springs/150Nm+150Nm/Shift_2in1_150_150.csv", header=None)
Shift
x0_val = Shift.iloc[0, 0]
y0_val = Shift.iloc[0, 1]

Logit_Params = pd.read_csv("./2in1 Springs/150Nm+150Nm/Logit_2in1_150_150.csv", header=None)
K = Logit_Params.iloc[0, 0]
h = Logit_Params.iloc[0, 1]/2
L_star = Logit_Params.iloc[0, 2]
c = Logit_Params.iloc[0, 3]

Logit_Model = pd.read_csv("./2in1 Springs/150Nm+150Nm/Model_2in1_150_150.csv", header=None)
tau = Logit_Model.iloc[:, 0]

# %%
def calc_torque_smooth(L, ang_err, K, h, c):
    # # Set up logit function
    # c_0 = 30

    # def c_obj_func(c, h, L):
    #     return abs((1/(4*c) - c*(h+L)**2)*np.log((1/2 + c*(h+L))/(1/2 - c*(h+L))) - L)

    # # Optimization to find c
    # result = minimize(lambda c: c_obj_func(c, h, L), c_0, bounds=[(0, None)])
    # c = result.x[0]

    b = 1/4/c - c*(h+L)**2

    def y_logit(x):
        return b * np.log((0.5 + c*x) / (0.5 - c*x))

    # Calculate deflection
    defl = np.where(ang_err > 0, ang_err - h, ang_err + h)
    defl[np.abs(ang_err) < (h + L)] = 0
    defl += (np.abs(ang_err) < (h + L)) * y_logit(ang_err)

    # Calculate torque
    tau = K * defl

    return tau

# %%
fig = plt.figure(figsize=(9, 6), dpi=200)
ax = fig.add_subplot(111)
plt.plot(defl - x0_val, torque - y0_val, label="Raw Curve")

# tau = calc_torque_smooth(L_star, defl, K, h, c)
plt.plot(defl, tau, label="Logit Fit")


plt.rc('text', usetex=True)
plt.rc('font', family='serif')
plt.xlabel(r'Deflection (degrees)', fontsize=14)
plt.ylabel(r'Torque (Nm)',fontsize=14)
plt.legend(loc='lower right', fontsize=12)

# # Axis Ticks
# ax.spines['top'].set_visible(False)
# ax.spines['right'].set_visible(False)
# ax.spines['bottom'].set_visible(True)
# ax.spines['left'].set_visible(True)
# plt.savefig("../figs/RAW/Test.png")

# %%



