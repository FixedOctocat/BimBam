"""
json for reading file
pyvis for visualizasion
"""
import json
from pyvis.network import Network


class Graph:
    """Graph class for storing and drawing graphs"""

    def __init__(self, json_file: str):
        self.net = Network(directed=True, select_menu=True, layout=False)
        with open(json_file, "r", encoding="utf8") as file:
            self.data = json.load(file)

    def add_connection(self, node1: str, node2: str):
        """Create connection between two nodes"""
        if [node1, node2] not in [[i["from"], i["to"]] for i in self.net.get_edges()]:
            self.net.add_edge(node1, node2)

    def add_node(self, node: str, level: int, color: str = "#97c2fc"):
        """Create node"""
        if node not in self.net.get_nodes():
            self.net.add_node(node, shape="box", level=level, color=color)
        elif color == "#fcc897":
            self.net.nodes[list(map(lambda x: x["id"], self.net.nodes)).index(node)][
                "color"
            ] = "#fcc897"

    def show(self):
        """Show graph"""
        self.net.toggle_physics(True)
        self.net.show("nodes.html", notebook=False)

    def draw(self, start_point: json = None, level: int = 0):
        """Get json to analyze and draw graph"""

        if start_point["members"]:
            self.add_node(start_point["Name"], level=level, color=start_point["color"])
            for activity_name in start_point["members"]:
                self.add_node(
                    activity_name["Name"], level=level + 1, color=activity_name["color"]
                )
                self.add_connection(start_point["Name"], activity_name["Name"])

            if start_point["members"]:
                for member in start_point["members"]:
                    self.draw(member, level + 1)

    def start(self, start_points: json = None):
        """Start analyze json graph"""
        if start_points is None:
            start_points = self.data

        for start_point in start_points:
            self.draw(start_point)
