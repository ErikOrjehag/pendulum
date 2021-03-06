
import matplotlib.pyplot as plt
from casadi import *

T = 10.
N = 20

x1 = MX.sym('x1')
x2 = MX.sym('x2')
x = vertcat(x1, x2)
u = MX.sym('u')

xdot = vertcat((1-x2**2)*x1 - x2 + u, x1)

L = x1**2 + x2**2 + u**2

dae = { 'x': x, 'p': u, 'ode': xdot, 'quad': L }
opts = { 'tf': T/N }
F = integrator('F', 'cvodes', dae, opts)

Fk = F(x0=[0.2, 0.3], p=0.4)
print Fk['xf']
print Fk['qf']

w = []
w0 = []
lbw = []
ubw = []
J = 0
g = []
lbg = []
ubg = []

X0 = MX.sym('X0', 2)
w += [X0]
lbw += [0, 1]
ubw += [0, 1]
w0 += [0, 1]

Xk = MX([0, 1])
for k in range(N):
    # New NLP variable for the control
    Uk = MX.sym('U_' + str(k))
    w += [Uk]
    lbw += [-1]
    ubw += [1]
    w0 += [0]

    # Integrate till the end of the interval
    Fk = F(x0=Xk, p=Uk)
    Xk_end = Fk['xf']
    J = J + Fk['qf']

    # New NLP variable for state at end of interval
    Xk = MX.sym('X_' + str(k+1), 2)
    w += [Xk]
    lbw += [-0.25, -inf]
    ubw += [inf, inf]
    w0 += [0, 0]

    # Add equality contraint
    g += [Xk_end - Xk]
    lbg += [0, 0]
    ubg += [0, 0]

prob = { 'f': J, 'x': vertcat(*w), 'g': vertcat(*g) }
opts = { 'ipopt.print_level': 5, 'ipopt.sb': 'yes', 'print_time': 0 }
solver = nlpsol('solver', 'ipopt', prob, opts)

sol = solver(x0=w0, lbx=lbw, ubx=ubw, lbg=lbg, ubg=ubg)

w_opt = sol['x'].full().flatten()

x1_opt = w_opt[0::3]
x2_opt = w_opt[1::3]
u_opt = w_opt[2::3]

tgrid = [T/N*k for k in range(N+1)]

plt.figure(1)
plt.clf()
plt.plot(tgrid, x1_opt, '--')
plt.plot(tgrid, x2_opt, '-')
plt.step(tgrid, vertcat(DM.nan(1), u_opt), '-.')
plt.xlabel('t')
plt.legend(['x1','x2','u'])
plt.grid()
plt.show()
