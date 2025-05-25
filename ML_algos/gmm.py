import numpy as np
from typing import NamedTuple, Union, Literal
from scipy.stats import multivariate_normal


def hello():
    print('Hello from gmm.py!')


class GMMState(NamedTuple):
    """Parameters to a GMM Model."""
    pi: np.ndarray  # [K]
    mu: np.ndarray  # [K, d]
    sigma: np.ndarray  # [K, d, d]


def train_gmm(train_data: np.ndarray,
              init_pi: np.ndarray,
              init_mu: np.ndarray,
              init_sigma: np.ndarray,
              *,
              num_iterations: int = 50,
              ) -> GMMState:
  
    # Sanity check
    N, d = train_data.shape
    K, = init_pi.shape
    assert init_mu.shape == (K, d)
    assert init_sigma.shape == (K, d, d)


    
    pi, mu, sigma = init_pi.copy(), init_mu.copy(), init_sigma.copy()

    for iteration in range(num_iterations):

        responsibilities = np.zeros((N, K))  

        for k in range(K):

            responsibilities[:, k] = pi[k] * multivariate_normal.pdf(train_data, mean=mu[k], cov=sigma[k])

        responsibilities /= responsibilities.sum(axis=1, keepdims=True)
        N_k = responsibilities.sum(axis=0)  
        pi = N_k / N

        mu = np.dot(responsibilities.T, train_data) / N_k[:, np.newaxis]  

        for k in range(K):
            diff = train_data - mu[k]  
            weighted_diff = responsibilities[:, k, np.newaxis] * diff  
            sigma[k] = np.dot(weighted_diff.T, diff) / N_k[k]  

        log_likelihood = np.sum(np.log(np.sum(responsibilities, axis=1)))
        print(log_likelihood)

    return GMMState(pi, mu, sigma)


def compress_image(image: np.ndarray, gmm_model: GMMState) -> np.ndarray:
    """Compress image by mapping each pixel to the mean value of a
    Gaussian component (hard assignment).

    Arguments:
        image: A numpy array of shape (H, W, 3) and dtype uint8.
        gmm_model: type GMMState. A GMM model parameters.
    Returns:
        compressed_image: A numpy array of (H, W, 3) and dtype uint8.
            Be sure to round off to the nearest integer.
    """
    H, W, C = image.shape
    K = gmm_model.mu.shape[0]

    pixels = image.reshape(-1, C).astype(float)  

    responsibities = np.zeros((H * W, K))  

    for k in range(K):
        responsibities[:, k] = gmm_model.pi[k] * multivariate_normal.pdf(
            pixels, mean=gmm_model.mu[k], cov=gmm_model.sigma[k]
        )

    assigned_components = np.argmax(responsibities, axis=1)  

    compressed_pixels1 = gmm_model.mu[assigned_components]  

    compressed_pixels2 = np.round(compressed_pixels1).astype(np.uint8)

    compressed_image = compressed_pixels2.reshape(H, W, C)

    assert compressed_image.dtype == np.uint8
    assert compressed_image.shape == (H, W, C)
    return compressed_image


