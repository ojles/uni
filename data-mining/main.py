from scipy.io import arff
import FLAME as flm
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans
from sklearn import datasets

def plot_result(x, y, labels, cluster_labels, title, colors=None):
    if colors is None:
        colors = ['red', 'green', 'blue', 'purple', 'yellow', 'cyan', 'magenta', 'black'][:len(cluster_labels)]
        fig = plt.figure(figsize=(8, 8))
        plt.scatter(x, y, c=labels, cmap=matplotlib.colors.ListedColormap(colors))
    else:
        fig = plt.figure(figsize=(8, 8))
        plt.scatter(x, y, c=colors, edgecolors='none')
    cb = plt.colorbar()
    loc = np.arange(0, max(labels), max(labels) / float(len(cluster_labels)))
    cb.set_ticks(loc)
    cb.set_ticklabels(cluster_labels)
    cb.ax.set_ylabel('Clusters', rotation=270)
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title(title)
    plt.show()


def calc_colors(flame):
    color_map = plt.get_cmap('jet')(np.linspace(0, 1, len(flame.labels)))
    alphas = [np.max(el) for el in flame.fuzzy_memberships]
    min_alpha = np.min(alphas)
    max_alpha = np.max(alphas)
    minus_alpha = min_alpha * 0.7
    min_alpha = min_alpha - minus_alpha
    max_alpha = max_alpha - minus_alpha
    alpha_scaler = 1 / (max_alpha - min_alpha)
    colors = []
    for i, el in enumerate(flame.fuzzy_memberships):
        j = flame_prediction[i]
        a = (alphas[i] - minus_alpha) * alpha_scaler
        if a > 1.0:
            a = 1
    colors.append([color_map[j][0], color_map[j][1], color_map[j][2], a])


#
# generate/load dataset
#
n_samples=1500
noisy_moons = datasets.make_moons(n_samples=n_samples, noise=.04, random_state=1)
X = noisy_moons[0]
y_true = noisy_moons[1]
for i in X:
    i[0] = i[0] * 100
    i[1] = i[1] * 100

print('Min:', np.array(X).min())
print('Max:', np.array(X).max())


#
# start clustering
#
flame = flm.FLAME(k_neighbors=220)
flame.cluster(X)
flame_prediction = flame.single_memberships
flame_labels = flame.labels

#
# create color map with alpha
#
color_map = plt.get_cmap('jet')(np.linspace(0, 1, len(flame_labels)))
alphas = [np.max(el) for el in flame.fuzzy_memberships]
min_alpha = np.min(alphas)
max_alpha = np.max(alphas)
minus_alpha = min_alpha * 0.7
min_alpha = min_alpha - minus_alpha
max_alpha = max_alpha - minus_alpha
alpha_scaler = 1 / (max_alpha - min_alpha)

colors = []
for i, el in enumerate(flame.fuzzy_memberships):
    j = flame_prediction[i]
    a = (alphas[i] - minus_alpha) * alpha_scaler
    if a > 1.0:
        a = 1
    colors.append([color_map[j][0], color_map[j][1], color_map[j][2], a])

#
# plot results
#
#plot_result(X[:, 0], X[:, 1], y_true, list(set(y_true)), 'Plot with true labels')
plot_result(X[:, 0], X[:, 1], flame_prediction, flame_labels, 'Plot with predicted FLAME labels', colors=colors)

#
# compare to k-means
#
kmeans = KMeans(n_clusters=len(flame_labels), random_state=0).fit(X)
y_pred_kmeans1 = kmeans.labels_
#plot_result(X[:, 0], X[:, 1], y_pred_kmeans1, list(set(y_pred_kmeans1)), 'Scatter plot with predicted k-means labels')
