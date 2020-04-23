import numpy as np
from sklearn.neighbors import NearestNeighbors

class FLAME:
    def __init__(self, metric='euclidean', k_neighbors=20, max_iterations=None,
                 converge_threshold=1e-5, min_member_threshold=0.3):
        self.metric = metric
        self.k_neighbors = k_neighbors
        self.n_samples = 0
        self.csos = None
        self.outliers = None
        self.num_clusters = 0
        self.max_iterations = max_iterations
        self.converge_threshold = converge_threshold
        self.min_member_threshold = min_member_threshold
        self.fixed = {}
        self.fuzzy_memberships = None
        self.single_memberships = None
        self.multiple_memberships = None

    def cluster(self, X):
        self.n_samples = len(X)
        knn_distances, knn_indices = self._find_knearest(X)
        densities = self._compute_densities(knn_distances)
        weight_vector = self._compute_weight_vector(knn_distances)
        objects = self._define_object_types(densities, knn_indices)
        initial_memberships = self._initialize_memberships(objects)
        self.fuzzy_memberships = self._approximate_membership(initial_memberships, weight_vector, knn_indices)
        # self.multiple_memberships = self._assign_multiple_membership(self.fuzzy_memberships)
        self.single_memberships = self._assign_single_membership(self.fuzzy_memberships)
        self.labels = sorted(list(set(self.single_memberships)))
        if len(self.outliers) > 0:
            self.labels[-1] = 'Outliers'

    def _find_knearest(self, X):
        nbrs = NearestNeighbors(n_neighbors=self.k_neighbors + 1, metric=self.metric).fit(X)
        distances, indices = nbrs.kneighbors(X)
        # kneigbors also includes the object itself with distance 0,
        # we need to remove that
        distances = distances.T[1:].T
        indices = indices.T[1:].T
        return distances, indices

    def _compute_densities(self, knn_distances):
        nearest_dist_sums = np.sum(knn_distances, axis=1)
        max_distance = np.max(nearest_dist_sums)
        densities = np.divide(max_distance, nearest_dist_sums)
        return densities

    def _compute_weight_vector(self, knn_distances):
        weight_vector = []
        for d in knn_distances:
            s = np.sum(d)
            weights = [1 / di for di in d]
            weights_sum = np.sum(weights)
            weights = [w / weights_sum for w in weights]
            weight_vector.append(weights)
        return np.array(weight_vector)

    def _define_object_types(self, densities, knn_indices):
        csos, outliers, others = [], [], []
        outlier_threshold = np.mean(densities) - 2 * np.std(densities)  # Threshold obtained from FLAME paper
        for i, d in enumerate(densities):
            if np.max(densities[knn_indices[i]]) < d:
                csos.append(i)  # Cluster Supporting Object
                self.fixed[i] = 1
            elif np.min(densities[knn_indices[i]]) > d + outlier_threshold:
                outliers.append(i)  # Outlier
                self.fixed[i] = 1
            else:
                others.append(i)
        return csos, outliers, others

    def _initialize_memberships(self, objects):
        csos, outliers, others = objects
        # +1 for the outlier 'cluster'
        M = len(csos) + 1
        self.num_clusters = M
        memberships = np.zeros([self.n_samples, M])
        # Begin with equal membership to each cluster
        starting_membership = 0.1
        for i, cso in enumerate(csos):
            memberships[cso, i] = 1
        for i, outlier in enumerate(outliers):
            memberships[outlier, M - 1] = 1
        for i, other in enumerate(others):
            memberships[other].fill(starting_membership)
        self.csos = csos
        self.outliers = outliers
        return memberships

    def _approximate_membership(self, memberships, weight_vector, knn_indices):
        iterations = 0
        error = 0
        while self.max_iterations is None or iterations < self.max_iterations:  # Iterative minimization of error function
            iterations += 1
            prev_memberships = memberships.copy()
            for l, knn in enumerate(knn_indices):
                if self.fixed.get(l):
                    continue
                memberships[l] = weight_vector[l].dot(prev_memberships[knn])

            error = np.square(memberships - prev_memberships).sum()
            if error < self.converge_threshold:
                return memberships
        return memberships

    def _assign_single_membership(self, memberships):
        outliers = np.where(memberships[:, -1] == 1)[0]
        membership_indices = memberships[:, :-1].argmax(axis=1)
        membership_indices[outliers] = len(self.csos)
        return membership_indices

    def _assign_multiple_membership(self, memberships):
        multiple_memberships = []
        for i, x in enumerate(memberships[:, :-1]):
            multiple_memberships.append([(j, z) for j, z in enumerate(x) if z > self.min_member_threshold])
        return multiple_memberships
