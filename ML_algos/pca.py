from typing import Tuple
import numpy as np


def hello_world():
    print("Hello world from EECS 545 PCA!")


def train_PCA(data: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:

    if len(data.shape) != 2:
        raise ValueError("Invalid shape of data; did you forget flattening?")
    N, d = data.shape

    #######################################################
    ###              START OF YOUR CODE                 ###
    #######################################################
    
    mean = np.mean(data, axis=0)
    data_centered = data - mean

    covariance_matrix_pre = (data_centered.T @ data_centered) 

    covariance_matrix_post = covariance_matrix_pre / N

    eigenvalues_pre, U_pre = np.linalg.eigh(covariance_matrix_post)

    eigenvalues = eigenvalues_pre[::-1]

    U = U_pre[:, ::-1]

    #######################################################
    ###                END OF YOUR CODE                 ###
    #######################################################

    return U, eigenvalues
