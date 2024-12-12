import numpy as np

tests = [(100, 1), (40, 1)]
eval_questions = [
    (40, 0.8), # Code below returns max_prob = 0.33451, first_offer = 14
    (40, 0.5), # Code below returns max_prob = 0.25471, first_offer = 11
    (60, 0.5)] # Code below returns max_prob = 0.25313, first_offer = 16

def secretary(N: int, p: float) -> tuple:
    """
    Return the optimal probability of hiring the best candidate and the first offer to make. The optimal strategy is to make an offer to the first candidate that is better than the best candidate seen so far (after n_opt candidates have been interviewed) until such an offer is accepted or no candidate is left. 

    Args:
        N (int): Number of candidates
        p (float): Probability of each candidate accepting an offer if given one

    Returns:
        tuple: (max_prob, first_offer) where max_prob is the optimal probability of hiring the best candidate and first_offer is the first offer to make
    """    

    V = np.zeros((2, N+1)) # max prob of hiring best candidate given xn = x
    A = np.zeros((2, N+1))

    #terminal conditions
    V[0][N] = 0 
    V[1][N] = p
    A[1][N] = 1


    for i in range(N-2, -1, -1):
        n = i + 1
        # If not best candidate yet, reject and V = E[V(n+1)]
        V[0][n] = 1/(n+1)*V[1][n+1] + n/(n+1)*V[0][n+1]

        # If best candidate yet
        V[1][n] = max(p*n/N + (1-p)*V[0][n], V[0][n])

        if V[1][n] == p*n/N + (1-p)*V[0][n]:
            A[1][n] = 1
       
    for i, An in enumerate(A[1]):
        if An == 1:
            first_offer = i
            break

    return V[1][1], first_offer

def secretary_runner(test):
    N, p = test

    max_prob, first_offer = secretary(N, p)
    print(f"Optimal prob for N = {N}, p = {p}: {round(max_prob, 5)}, First offer: {first_offer}/{N}")

print("TEST CASES")
for t in tests:
    secretary_runner(t)

print("\nHOMEWORK QUESTIONS")
for q in eval_questions:
    secretary_runner(q)