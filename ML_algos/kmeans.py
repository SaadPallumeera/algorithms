"""EECS545 HW5 Q1. K-means"""

import numpy as np
import sklearn.metrics


def hello():
    print('Hello from kmeans.py!')


def euclidean_distance(x: np.ndarray, y: np.ndarray) -> np.ndarray:
    """Compute the pixel error between the data and compressed data.

    Please do not change this function!

    Arguments:
        x: A numpy array of shape (N*, d), where d is the data dimension.
        y: A numpy array of shape (N*, d), where d is the data dimension.
    Return:
        errors: A numpy array of shape (N*). Euclidean distances.
    """
    assert x.shape == y.shape
    error = np.sqrt(np.sum(np.power(x - y, 2), axis=-1))
    return error


def train_kmeans(train_data: np.ndarray, initial_centroids, *,
                 num_iterations: int = 50):
    """K-means clustering.

    Arguments:
        train_data: A numpy array of shape (N, d), where
            N is the number of data points
            d is the dimension of each data point. Note: you should NOT assume
              d is always 3; rather, try to implement a general K-means.
        initial_centroids: A numpy array of shape (K, d), where
            K is the number of clusters. Each data point means the initial
            centroid of cluster. You should NOT assume K = 16.
        num_iterations: Run K-means algorithm for this number of iterations.

    Returns:
        centroids: A numpy array of (K, d), the centroid of K-means clusters
            after convergence.
    """
    # Sanity check
    N, d = train_data.shape
    K, d2 = initial_centroids.shape
    if d != d2:
        raise ValueError(f"Invalid dimension: {d} != {d2}")

    # We assume train_data contains a real-valued vector, not integers.
    assert train_data.dtype.kind == 'f'

    centroids = initial_centroids.copy()
    for i in range(num_iterations):
        distances = np.sqrt(((train_data[:, np.newaxis, :] - centroids) ** 2).sum(axis=2))
        
        # Assign each point to nearest cluster
        clustr_assignments = np.argmin(distances, axis=1)

        # Update centroids while handling empty clusters
        new_centroids = []
        for k in range(K):
            cluster_points = train_data[clustr_assignments == k]
            if len(cluster_points) > 0:
                new_centroid = cluster_points.mean(axis=0)
            else:
                # Keep previous centroid if cluster is empty
                new_centroid = centroids[k]
            new_centroids.append(new_centroid)
        new_centroids = np.array(new_centroids)

        # Calculate SSD using original assignments
        ssd = np.sum((train_data - new_centroids[clustr_assignments]) ** 2)
        
        # Update centroids for next iteration
        centroids = new_centroids

        print(f'Iteration {i:2d}: SSD = {ssd:2.2f}')

    assert centroids.shape == (K, d)
    return centroids


def compress_image(image: np.ndarray, centroids: np.ndarray) -> np.ndarray:
    """Compress image by mapping each pixel to the closest centroid.

    Arguments:
        image: A numpy array of shape (H, W, 3) and dtype uint8.
        centroids: A numpy array of shape (K, 3), each row being the centroid
            of a cluster.
    Returns:
        compressed_image: A numpy array of (H, W, 3) and dtype uint8.
            Be sure to round off to the nearest integer.
    """
    H, W, C = image.shape
    K, C2 = centroids.shape
    assert C == C2 == 3, "Invalid number of channels."
    assert image.dtype == np.uint8

    ###########################################################################
    # Implement K-means algorithm.
    ###########################################################################
    
    pixels = image.reshape(-1, C).astype(float)  # Convert to float for distance calculation

    distances = np.sqrt(((pixels[:, np.newaxis, :] - centroids) ** 2).sum(axis=2))

    closest_centroid_indices = np.argmin(distances, axis=1)

    compressed_pixels = centroids[closest_centroid_indices]

    compressed_pixels2 = np.round(compressed_pixels).astype(np.uint8)

    compressed_image = compressed_pixels2.reshape(H, W, C)

    #######################################################################

    assert compressed_image.dtype == np.uint8
    assert compressed_image.shape == (H, W, C)
    return compressed_image
