import numpy as np


def hello():
    print('Hello from ica.py!')


def sigmoid(x: np.ndarray) -> np.ndarray:
    
    pos_mask = (x >= 0)
    neg_mask = (x < 0)

    # specify dtype! otherwise, it may all becomes zero, this could have different
    # behaviors depending on numpy version
    z = np.zeros_like(x, dtype=float)
    z[pos_mask] = np.exp(-x[pos_mask])
    z[neg_mask] = np.exp(x[neg_mask])

    top = np.ones_like(x, dtype=float)
    top[neg_mask] = z[neg_mask]
    s = top / (1 + z)
    return s


def unmixer(X: np.ndarray) -> np.ndarray:
   
    M, N = X.shape
    W = np.eye(N)
    losses = []

    anneal = [0.1, 0.1, 0.1, 0.05, 0.05, 0.05, 0.02, 0.02, 0.01, 0.01,
              0.005, 0.005, 0.002, 0.002, 0.001, 0.001]
    print('Separating tracks ...')
    for alpha in anneal:
        print('working on alpha = {0}'.format(alpha))
        for xi in X:
            W += alpha * filter_grad(xi, W)
    return W


def filter_grad(x: np.ndarray, W: np.ndarray) -> np.ndarray:
   

    s = W @ x
    
    g = 1 / (1 + np.exp(-s))
    
    phi = 1 - 2 * g
    grad_part1 = phi.reshape(-1, 1) * x
    
    inv_W = np.linalg.inv(W)
    grad_part2 = inv_W.T
    
    grad = grad_part1 + grad_part2

    
    return grad

    

def unmix(X: np.ndarray, W: np.ndarray):
    
    return X@W

   