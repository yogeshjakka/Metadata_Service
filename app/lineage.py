from sqlalchemy.orm import Session
from .models import Lineage

def build_graph(db: Session):
    graph = {}
    edges = db.query(Lineage).all()
    for e in edges:
        graph.setdefault(e.upstream_fqn, []).append(e.downstream_fqn)
    return graph

def has_cycle(graph, start, target):
    visited = set()

    def dfs(node):
        if node == start:
            return True
        if node in visited:
            return False
        visited.add(node)
        for neigh in graph.get(node, []):
            if dfs(neigh):
                return True
        return False

    return dfs(target)
