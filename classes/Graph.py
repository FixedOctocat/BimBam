from pyvis.network import Network
import json


class Graph:
    __slots__ = ["net", "data"]

    def __init__(self, json_file: str):
        self.net = Network(directed=True, select_menu=True, layout=True)
        f = open(json_file)
        self.data = json.load(f)
        f.close()

    def AddConnection(self, node1: str, node2: str):
        if [node1, node2] not in [[i["from"], i["to"]] for i in self.net.get_edges()]:
            self.net.add_edge(node1, node2)

    def AddNode(self, node: str, level: int):
        if node not in self.net.get_nodes():
            self.net.add_node(node, shape="ellipse", physics=False, level=level)

    def Show(self):
        self.net.force_atlas_2based()
        self.net.show("nodes.html", notebook=False)

    def Draw(self, StartPoint: json = None, level: int = 0):
        if StartPoint is None:
            StartPoint = self.data

        self.AddNode(StartPoint["Name"], level=level)
        for ActivityName in StartPoint["members"]:
            self.AddNode(ActivityName["Name"], level=level + 1)
            self.AddConnection(StartPoint["Name"], ActivityName["Name"])

        if StartPoint["members"]:
            for member in StartPoint["members"]:
                self.Draw(member, level + 1)
