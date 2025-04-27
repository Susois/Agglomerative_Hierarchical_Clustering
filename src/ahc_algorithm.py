import numpy as np

def agglomerative_clustering(points, step_callback, linkage='single'):
    n = len(points)
    clusters = [[point] for point in points]

    # Ban đầu khoảng cách giữa các điểm
    distances = np.full((n, n), np.inf)
    for i in range(n):
        for j in range(i + 1, n):
            distances[i, j] = compute_linkage([points[i]], [points[j]], linkage)
            distances[j, i] = distances[i, j]

    dendrogram_boxes = [(50 + i * 50, 180) for i in range(n)]
    dendrogram_lines = []

    step_callback(clusters.copy(), {"boxes": dendrogram_boxes.copy(), "lines": dendrogram_lines.copy()})

    active_indices = list(range(n))  # Chỉ số các cluster còn hoạt động

    while len(active_indices) > 1:
        # Tìm 2 cluster gần nhất
        min_dist = np.inf
        min_pair = (None, None)

        for i in active_indices:
            for j in active_indices:
                if i != j and distances[i, j] < min_dist:
                    min_dist = distances[i, j]
                    min_pair = (i, j)

        i, j = min_pair

        # Gộp 2 cụm
        new_cluster = clusters[i] + clusters[j]
        clusters.append(new_cluster)

        # Thêm cluster mới
        new_idx = len(clusters) - 1

        # Cập nhật khoảng cách cho cluster mới
        distances = expand_distances(distances, clusters, new_idx, linkage)

        # Xóa cluster cũ
        active_indices.remove(i)
        active_indices.remove(j)
        active_indices.append(new_idx)

        # Cập nhật dữ liệu dendrogram
        xi, yi = dendrogram_boxes[i]
        xj, yj = dendrogram_boxes[j]
        new_x = (xi + xj) / 2
        new_y = min(yi, yj) - 30
        dendrogram_lines.append((xi, yi, new_x, new_y))
        dendrogram_lines.append((xj, yj, new_x, new_y))
        dendrogram_boxes.append((new_x, new_y))

        step_callback([clusters[idx] for idx in active_indices],
                      {"boxes": [dendrogram_boxes[idx] for idx in active_indices],
                       "lines": dendrogram_lines.copy()})

def expand_distances(old_distances, clusters, new_idx, linkage):
    """Cấp phát ma trận khoảng cách mới khi thêm 1 cluster."""
    n_old = old_distances.shape[0]
    n_new = len(clusters)

    new_distances = np.full((n_new, n_new), np.inf)
    new_distances[:n_old, :n_old] = old_distances

    for i in range(n_new - 1):
        d = compute_linkage(clusters[i], clusters[new_idx], linkage)
        new_distances[i, new_idx] = new_distances[new_idx, i] = d

    return new_distances

def compute_center(cluster):
    """Tính tâm cụm."""
    xs, ys = zip(*cluster)
    return (sum(xs) / len(xs), sum(ys) / len(ys))

def compute_linkage(cluster1, cluster2, linkage):
    """Tính khoảng cách giữa hai cụm theo loại liên kết."""
    if linkage == 'single':
        return min(euclidean(p1, p2) for p1 in cluster1 for p2 in cluster2)
    elif linkage == 'complete':
        return max(euclidean(p1, p2) for p1 in cluster1 for p2 in cluster2)
    elif linkage == 'average':
        distances = [euclidean(p1, p2) for p1 in cluster1 for p2 in cluster2]
        return sum(distances) / len(distances)
    else:
        raise ValueError(f"Unknown linkage method: {linkage}")

def euclidean(p1, p2):
    """Tính khoảng cách Euclid giữa 2 điểm."""
    return ((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2) ** 0.5
