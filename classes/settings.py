"""
os for file checking
argparse for parsing arguments
"""
import os
import argparse


class Settings:
    """Class representing a settings from argparse"""

    def __init__(self):
        self.apk_path = None
        self.functions_graph = False
        self.intents_graph = False
        self.main_point = None
        self.depth = 6
        self.recursive = False
        self.init_functions = False
        self.details = False
        self.package_name_check = False
        self.output = "graph"
        self.output_dir = "apktoolFolder"
        self.pyvis = False

    def parse_args(self, args: argparse.Namespace):
        """Save passed arguments from argparse to Settings class"""
        if not args.apk:
            print("Provide path to APK")
            os._exit(1)

        if not os.path.isfile(args.apk):
            print(f"Can't get file, check path: {args.apk}")
            os._exit(1)

        self.apk_path = args.apk

        if args.fgraph:
            self.functions_graph = args.fgraph

        if args.igraph:
            self.intents_graph = True

        if args.startp:
            self.main_point = args.startp

        if args.depth:
            self.depth = args.depth

        if args.rec:
            self.recursive = args.rec

        if args.initfunc:
            self.init_functions = args.initfunc

        if args.details:
            self.details = args.details

        if args.pnc:
            self.package_name_check = args.pnc

        if args.output:
            self.output = args.output

        if args.output_dir:
            self.output_dir = args.output_dir

        if args.pyvis:
            self.pyvis = args.pyvis

    def init_argparser(self):
        """Init argparser"""
        parser = argparse.ArgumentParser()
        parser.add_argument("apk", type=str, help="Path to APK")
        parser.add_argument(
            "-fg",
            "--fgraph",
            action="store_true",
            help="Function graph view by provided APK",
        )
        parser.add_argument(
            "-ig",
            "--igraph",
            action="store_true",
            help="Intent graph view by provided APK",
        )
        parser.add_argument("-sp", "--startp", type=str, help="Starting point")
        parser.add_argument("-d", "--depth", type=int, help="depth of search")
        parser.add_argument(
            "-r", "--rec", action="store_true", help="output function recursively"
        )
        parser.add_argument(
            "-if",
            "--initfunc",
            action="store_true",
            help="output <init> functions",
        )
        parser.add_argument(
            "-det", "--details", action="store_true", help="Get detailed view"
        )
        parser.add_argument(
            "-pnc",
            action="store_true",
            help="Do package name check for all calls",
        )
        parser.add_argument(
            "-o",
            "--output",
            type=str,
            help="output file",
        )
        parser.add_argument(
            "-od",
            "--output_dir",
            type=str,
            help="Directory for apktool",
        )
        parser.add_argument(
            "--pyvis",
            action="store_true",
            help="Generate interactive graph",
        )

        self.parse_args(parser.parse_args())

    def print_settings(self):
        """Print settings in table format"""
        d = {
            "APK": self.apk_path if self.apk_path else "Not specified",
            "Draw Functions Graph": "True" if self.functions_graph else "False",
            "Draw Intents Graph": "True" if self.intents_graph else "False",
            "Main Point": self.main_point if self.main_point else "Not specified",
            "depth": self.depth,
            "recursive search": "True" if self.recursive else "False",
            "Filter <init> functions": "False" if self.init_functions else "True",
            "Get detailed information": "True" if self.details else "False",
            "Do package name check": "True" if self.package_name_check else "False",
            "Directory for apktool": self.output_dir,
        }

        print("{:<30} {:<15}".format("Argument", "Value"))
        for k, v in d.items():
            print("{:<30} {:<15}".format(k, v))
