import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

#parameters
rho_al = 2.7e3
R = 55e-3
r = 40e-3
H = 50e-3
h = 40e-3

Iz = np.pi/2*(R**4*H-r**4*h)*rho_al

m1 = 1e-2
m2 = 0.32
m3 = 1e-2
m41 = rho_al*np.pi*(R**2-r**2)*h
m42 = rho_al*np.pi*R**2*(H-h)
m7 = 2

d2 = 70e-3
d3 = 110e-3
d41 = 90e-3
d42 = 115e-3
d7 = 190e-3

l1 = 30e-3
l2 = 80e-3
l3 = 60
a = 140e-3

Ix = 1/3*m1*l1**2 + 1/12*m2*l2**2 + m2*d2**2 + 1/12*m3*l3**2 + m3*d3**2 + m41*(3*(R**2+r**2)+h**2) + m41*d41**2 + 1/12*m42*R**2 + m42*d42**2 + 1/6*m7*a**2 + m7*d7**2

w = 15

m_tot = 6
g = 9.81
l_cm = 130e-3

V_nominal = 12
Speed_no_load = 628.32
Torque_stall = 0.1722

def gyropendulum (t,y):
    theta, theta_dot, phi, phi_dot, psi, psi_dot = y
    M_theta = 0
    M_phi = 0
    M_psi = 1
    #M_psi = Iz*0.5*Speed_no_load/V_nominal
    
    derivs = np.zeros_like(y)
    derivs[0] = theta_dot
    derivs[1] = (M_theta + phi_dot**2*np.sin(theta)*np.cos(theta)*(Ix-Iz) - Iz*psi_dot*phi_dot*np.sin(theta) - m_tot*g*l_cm)/Ix
    derivs[2] = phi_dot
    derivs[3] = (M_phi + 2*np.sin(theta)*np.cos(theta)*theta_dot*phi_dot*(Iz-Ix)-Iz*(np.cos(theta)*derivs[5]-theta_dot*psi_dot*np.sin(theta)))/(Ix*np.sin(theta)**2+Iz*np.cos(theta)**2)
    derivs[4] = psi_dot
    derivs[5] = M_psi/Iz - derivs[3]*np.cos(theta) + phi_dot*theta_dot*np.sin(theta)
    return derivs

# Initial conditions
y0 = np.array([1e-6, 1, 0, 0, 0, w])  # [θ, θ˙, φ, φ˙]

t_span = (0, 10)

sol = solve_ivp(gyropendulum, t_span, y0, method='RK45', atol=1e-6, rtol=1e-3, max_step=0.01)

# Plot the solution
plt.plot(sol.t, sol.y[0])
plt.grid()
plt.xlabel('Time,s')
plt.ylabel('Nutation,rad')
plt.show()

#%%
#def theta (t,y):
    