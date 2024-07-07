import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

#parameters
rho_al = 2.7e3
R = 55e-3
r = 40e-3
H = 50e-3
h = 40e-3

I = np.pi/2*(R**4*H-r**4*h)*rho_al

m1 = 1e-2
m2 = 2
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

I0 = 1/3*m1*l1**2 + 1/12*m2*l2**2 + m2*d2**2 + 1/12*m3*l3**2 + m3*d3**2 + m41*(3*(R**2+r**2)+h**2) + m41*d41**2 + 1/12*m42*R**2 + m42*d42**2 + 1/6*m7*a**2 + m7*d7**2

w = 15

m_tot = 6
g = 9.81
l_cm = 130e-3

#motor
V_nominal = 12
Speed_no_load = 628.32
Torque_stall = 0.1722

# Differential equations
def system(t, y):
    theta, theta_dot, phi, phi_dot, psi, psi_dot = y
    
    #Mx = F * d * np.cos(theta)
    V_input = 4.5+0.5*t
    #w_max = Speed_no_load*V_input/V_nominal
    #Torque_max = Toeque_stall*V_input/V_nominal
    M_tot = I*0.5*Speed_no_load/V_nominal
    #Mx = m_tot * g * l_cm * np.sin(theta)
    #Mx = M_tot*np.sin(theta)*np.cos(phi)+m_tot * g * l_cm * np.sin(theta)
    #My = M_tot*np.sin(theta)*np.sin(phi)
    Mx = 0
    My = 0
    Mz = M_tot
    
    derivs = np.zeros_like(y)

    derivs[0] = theta_dot

    derivs[1] = (Mx - I * phi_dot * np.sin(theta) * (phi_dot * np.cos(theta) + psi_dot))/I0 + phi_dot**2 * np.sin(theta) * np.cos(theta)
    
    derivs[2] = phi_dot
   
    derivs[3] = ((My + I * theta_dot * (phi_dot * np.cos(theta) + psi_dot))/I0 - 2 * phi_dot * theta_dot * np.cos(theta))/np.sin(theta)
    
    derivs[4] = Speed_no_load*V_input/V_nominal - Speed_no_load*I/Torque_stall
    #derivs[4] = w
    #derivs[4] = psi_dot

    #derivs[5] = Mz/I + phi_dot * theta_dot * np.sin(theta) - derivs[3] * np.cos(theta)
    derivs[5] = 0.5*Speed_no_load/V_nominal

    return derivs

# Initial conditions
y0 = np.array([2*np.pi-0.5, 0, 0, 0, 0, Speed_no_load*4.5/V_nominal - Speed_no_load*I/Torque_stall])  # [θ, θ˙, φ, φ˙, ψ, ψ˙]

t_span = (0, 10)

sol = solve_ivp(system, t_span, y0, method='RK45', atol=1e-6, rtol=1e-3, max_step=0.01)

# Plot the solution
plt.plot(sol.t, sol.y[3]) 
plt.xlabel('Time')
plt.ylabel('Theta')
plt.show()





