import numpy as np
import matplotlib.pyplot as plt

# PARAMETERS
L = 99
N = 20

p = 0.4
q = 1 - p 

# INITIAL VALUE FUNCTION
def V0(x): return (1 - (q/p)**x) / (1 - (q/p)**L)

def W0(x): return (1 - (q/p)**x) / (1 - (q/p)**L)

initial_wealth = np.arange(1, L+1)

def u_span(x): 
    max_u = min(x, L - x)
    
    if max_u <= 1:
        return [1]
    
    return np.arange(1, max_u)

# APPROXIMATION IN VALUE SPACE 
def value_space(): 
    bet = [1 for x in initial_wealth]

    V = [V0(x) for x in initial_wealth]

    for _ in range(N):
        for x in initial_wealth[1:-1]:
            maximize = max([(p * V[x -1 + u] + q * V[x -1 - u], u) for u in u_span(x)], 
                           key = lambda x: x[0])   

            bet[x-1] = maximize[1]
            V[x-1] = maximize[0]

    return (V, bet)

# APPROXIMATION IN POLICY SPACE
def policy_space():
    bet = [1 for x in initial_wealth] # Arbitrary initial betting strategy

    W_vals = [W0(x) for x in initial_wealth]

    for _ in range(N):
        # Want to solve W(x) - pW(x + u) - qW(x - u) = 0
        A = np.eye(L)
        for x in initial_wealth[1:-1]:
            A[x - 1, x - 1 + bet[x-1]] = -p
            A[x - 1, x - 1 - bet[x-1]] = -q

        b = np.concat((np.zeros(L-1), np.ones(1)), axis=None)

        W = np.linalg.solve(A, b)

        for x in initial_wealth[1:-1]:
            maximize = max([(p*W[x-1 + u] + q*W[x-1 - u], u) for u in u_span(x)],
                    key = lambda x: x[0])
            
            bet[x - 1] = maximize[1]
            W_vals[x - 1] = maximize[0]
            
    return (W_vals, bet)

# PLOTTING 
value_space_fn, value_space_bet = value_space()

fig = plt.figure(constrained_layout=True)
subfig1, subfig2 = fig.subfigures(nrows=2, ncols=1)

subfig1.suptitle('Approximation in Value Space')
subfig2.suptitle('Approximation in Policy Space')

axs1 = subfig1.subplots(nrows=1, ncols=2)
axs2 = subfig2.subplots(nrows=1, ncols=2)

# Plot value space function
ax1 = axs1[0]
ax1.plot(initial_wealth, value_space_fn, label='Value Function')
ax1.set_title('Value Function')
ax1.set_xlabel('Initial Wealth')
ax1.set_ylabel('Value')
ax1.legend()

# Plot value space betting strategy
ax2 = axs1[1]
ax2.plot(initial_wealth, value_space_bet, label='Betting Strategy')
ax2.set_title('Betting Strategy')
ax2.set_xlabel('Wealth')
ax2.set_ylabel('Bet')
ax2.legend()

policy_space_fn, policy_space_bet = policy_space()

# Plot policy space function
ax3 = axs2[0]
ax3.plot(initial_wealth, policy_space_fn, label='Value Function')
ax3.set_title('Value Function')
ax3.set_xlabel('Initial Wealth')
ax3.set_ylabel('Value')
ax3.legend()

# Plot policy space betting strategy
ax4 = axs2[1]
ax4.plot(initial_wealth, policy_space_bet, label='Betting Strategy')
ax4.set_title('Betting Strategy')
ax4.set_xlabel('Wealth')
ax4.set_ylabel('Bet')
ax4.legend()

plt.show()





