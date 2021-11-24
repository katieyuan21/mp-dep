import os
import glob
import argparse


class Node:
    def __init__(self, nid, pid):
        self.node_id = nid
        self.parent_id = pid
        self.children = []


def parse_rsd(path):
    # print(path)
    with open(path) as f:
        data = [(int(line[0]), int(line[6])) for line in [line.split("\t") for line in f.readlines()] if len(line) >= 8]
    nodes = [Node(nid, pid) for nid, pid in data]
    for node in nodes:
        if node.parent_id > 0:
            nodes[node.parent_id - 1].children.append(node)
    return [node for node in nodes if node.parent_id == 0]


def is_partially_independent(node):
    if len(node.children) >= 2:
        try:
            for i, x in enumerate(node.children):
                if x.node_id == node.node_id - 3 and node.children[i + 1].node_id == node.node_id - 1 and x.children[-1].node_id == node.node_id - 2:
                    return True, [node.node_id, x.node_id, node.children[i + 1].node_id, x.children[-1].node_id]
        except IndexError:
            pass
        try:
            for i, x in enumerate(node.children):
                if x.node_id == node.node_id + 1 and node.children[i + 1].node_id == node.node_id + 3 and node.children[i + 1].children[0].node_id == node.node_id + 2:
                    return True, [node.node_id, x.node_id, node.children[i + 1].node_id, node.children[i + 1].children[0].node_id]
        except IndexError:
            pass
    return False, []


def is_fully_embedded(node):
    try:
        for i, x in enumerate(node.children):
            if x.node_id == node.node_id - 2 and node.children[i + 1].node_id == node.node_id - 1 and node.children[i + 2].node_id == node.node_id + 1:
                return True, [node.node_id, x.node_id, node.children[i + 1].node_id, node.children[i + 2].node_id]
    except IndexError:
        pass
    try:
        for i, x in enumerate(node.children):
            if x.node_id == node.node_id - 1 and node.children[i + 1].node_id == node.node_id + 1 and node.children[i + 2].node_id == node.node_id + 2:
                return True, [node.node_id, x.node_id, node.children[i + 1].node_id, node.children[i + 2].node_id]
    except IndexError:
        pass
    try:
        for x in node.children:
            if x.node_id == node.node_id - 2:
                for i, y in enumerate(x.children):
                    if y.node_id == node.node_id - 3 and x.children[i + 1].node_id == node.node_id - 1:
                        return True, [node.node_id, x.node_id, y.node_id, x.children[i + 1].node_id]
    except IndexError:
        pass
    try:
        for x in node.children:
            if x.node_id == node.node_id + 2:
                for i, y in enumerate(x.children):
                    if y.node_id == node.node_id + 1 and x.children[i + 1].node_id == node.node_id + 3:
                        return True, [node.node_id, x.node_id, y.node_id, x.children[i + 1].node_id]
    except IndexError:
        pass
    return False, []


class Statistics:
    def __init__(self, trees):
        self.n_partially_independent = 0
        self.__partially_independent_nodes = set()
        self.n_fully_embedded = 0
        self.__fully_embedded_nodes = set()
        for root in trees:
            self.__travel(root)

    def __travel(self, node):
        if len(node.children) > 0:
            if not node.node_id in self.__partially_independent_nodes:
                result, nodes = is_partially_independent(node)
                if result:
                    # Partially-Independent-Structure
                    # print(nodes)
                    self.n_partially_independent += 1
                    self.__partially_independent_nodes |= set(nodes)
            if not node.node_id in self.__fully_embedded_nodes:
                result, nodes = is_fully_embedded(node)
                if result:
                    # Fully-Embedded-Structure
                    # print(nodes)
                    self.n_fully_embedded += 1
                    self.__fully_embedded_nodes |= set(nodes)
            for child in node.children:
                self.__travel(child)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Start the dependency tree statistics.")
    parser.add_argument("dirs", metavar="DIRS", help="directories of *.rsd files", type=str, nargs="+")
    args = parser.parse_args()

    for directory in args.dirs:
        results = [Statistics(parse_rsd(file)) for file in glob.glob(os.path.join(directory, "*.rsd"))]
        n_partially_independent = sum([r.n_partially_independent for r in results])
        n_fully_embedded = sum([r.n_fully_embedded for r in results])
        print("%s,%d,%d" % (directory, n_partially_independent, n_fully_embedded))
