class UnionFind:
    """Union-Find (Disjoint-Set) implementation for clustering."""
    def __init__(self):
        self.parent = {}
        self.rank = {}

    def find(self, node):
        """Find the root of the node with path compression."""
        if self.parent[node] != node:
            self.parent[node] = self.find(self.parent[node])
        return self.parent[node]

    def union(self, node1, node2):
        """Union two nodes by rank."""
        root1 = self.find(node1)
        root2 = self.find(node2)
        if root1 != root2:
            if self.rank[root1] > self.rank[root2]:
                self.parent[root2] = root1
            elif self.rank[root1] < self.rank[root2]:
                self.parent[root1] = root2
            else:
                self.parent[root2] = root1
                self.rank[root1] += 1

    def add(self, node):
        """Add a new node."""
        if node not in self.parent:
            self.parent[node] = node
            self.rank[node] = 0

    def get_all(self):
        """Get all sets as a list of lists."""
        clusters = {}
        for node in self.parent:
            root = self.find(node)
            if root not in clusters:
                clusters[root] = []
            clusters[root].append(node)
        return list(clusters.values())

def cluster_elements_optimized(elements, status_map, min_cluster_size=100):
    """
    Optimized clustering of elements using Union-Find.
    
    Args:
        elements (list): List of elements with attributes `label` and `connectivity`.
        status_map (dict): A map of element labels to their status (e.g., active/inactive).
        min_cluster_size (int): Minimum number of elements in a cluster to keep.

    Returns:
        tuple: (node_clusters, element_clusters) after filtering.
    """
    # Initialize Union-Find structure
    uf = UnionFind()

    # Step 1: Union all nodes that belong to the same element
    for ele in elements:
        label = ele.label
        if not status_map[label]:
            continue  # Skip inactive elements
        conn = ele.connectivity
        for node in conn:
            uf.add(node)  # Ensure all nodes are in Union-Find
        for i in range(len(conn) - 1):
            uf.union(conn[i], conn[i + 1])

    # Step 2: Group nodes by their connected component root
    clusters = {}
    for node in uf.parent:
        root = uf.find(node)
        if root not in clusters:
            clusters[root] = set()
        clusters[root].add(node)

    # Step 3: Map nodes back to elements
    node_to_cluster = {node: root for root, nodes in clusters.items() for node in nodes}
    element_clusters = {}
    for ele in elements:
        label = ele.label
        if not status_map[label]:
            continue
        cluster_id = node_to_cluster[ele.connectivity[0]]  # Assume connectivity is non-empty
        if cluster_id not in element_clusters:
            element_clusters[cluster_id] = []
        element_clusters[cluster_id].append(label)

    # Step 4: Filter clusters by size
    element_clusters = [cluster for cluster in element_clusters.values() if len(cluster) > min_cluster_size]
    node_clusters = [list(nodes) for nodes in clusters.values() if len(nodes) > min_cluster_size]

    return node_clusters, element_clusters

def cluster_elements(elements):
    """
    Optimized clustering of elements using Union-Find.
    
    Args:
        elements (list): List of elements with attributes `label` and `connectivity`.
        status_map (dict): A map of element labels to their status (e.g., active/inactive).
        min_cluster_size (int): Minimum number of elements in a cluster to keep.

    Returns:
        tuple: (node_clusters, element_clusters) after filtering.
    """
    # Initialize Union-Find structure
    uf = UnionFind()

    # Step 1: Union all nodes that belong to the same element
    for ele in elements:
        label = ele[0]
        conn = ele[1:]
        for node in conn:
            uf.add(node)  # Ensure all nodes are in Union-Find
        for i in range(len(conn) - 1):
            uf.union(conn[i], conn[i + 1])

    # Step 2: Group nodes by their connected component root
    clusters = {}
    for node in uf.parent:
        root = uf.find(node)
        if root not in clusters:
            clusters[root] = set()
        clusters[root].add(node)

    # Step 3: Map nodes back to elements
    node_to_cluster = {node: root for root, nodes in clusters.items() for node in nodes}
    element_clusters = {}
    for ele in elements:
        label = ele.label
        cluster_id = node_to_cluster[ele[0]]  # Assume connectivity is non-empty
        if cluster_id not in element_clusters:
            element_clusters[cluster_id] = []
        element_clusters[cluster_id].append(label)

    # Step 4: Filter clusters by size
    element_clusters = [cluster for cluster in element_clusters.values()]
    node_clusters = [list(nodes) for nodes in clusters.values()]
    return node_clusters, element_clusters