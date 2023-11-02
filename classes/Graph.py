"""
json for reading file
pyvis for visualizasion
"""
import json
from pyvis.network import Network


class Graph:
    """Graph class for storing and drawing graphs"""

    def __init__(self, json_file: str):
        self.net = Network(directed=True, select_menu=True, layout=True)
        with open(json_file, "r", encoding="utf8") as file:
            self.data = json.load(file)

    def add_connection(self, node1: str, node2: str):
        """Create connection between two nodes"""
        if [node1, node2] not in [[i["from"], i["to"]] for i in self.net.get_edges()]:
            self.net.add_edge(node1, node2)

    def add_node(self, node: str, level: int):
        """Create node"""
        if node not in self.net.get_nodes():
            self.net.add_node(node, shape="box", physics=False, level=level)

    def show(self):
        """Show graph"""
        self.net.force_atlas_2based()
        self.net.show("nodes.html", notebook=False)

    def draw(self, start_point: json = None, level: int = 0):
        """Start to analyze json file"""
        if start_point is None:
            start_point = self.data

        self.add_node(start_point["Name"], level=level)
        for activity_name in start_point["members"]:
            self.add_node(activity_name["Name"], level=level + 1)
            self.add_connection(start_point["Name"], activity_name["Name"])

        if start_point["members"]:
            for member in start_point["members"]:
                self.draw(member, level + 1)
