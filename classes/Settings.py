import os
import argparse


class Settings:
    def __init__(self):
        self.apkPath = None
        self.Graph = False
        self.MainPoint = None
        self.Depth = 6
        self.Recursive = False
        self.InitFunctions = False
        self.Details = False
        self.PackageNameCheck = False
        self.Output = "graph"

    def ParseArgs(self, args: argparse.Namespace):
        if not args.apk:
            print("Provide path to APK")
            return 1
        elif not os.path.isfile(args.apk):
            print(f"Can't get file, check path: {args.apk}")
            return 1
        else:
            self.apkPath = args.apk

        if args.graph:
            self.Graph = True

        if args.startp:
            self.MainPoint = args.startp

        if args.depth:
            self.Depth = args.depth

        if args.rec:
            self.Recursive = args.rec

        if args.initfunc:
            self.InitFunctions = args.initfunc

        if args.details:
            self.Details = args.details

        if args.pnc:
            self.PackageNameCheck = args.pnc

        if args.output:
            self.Output = args.output

    def InitArgparser(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("apk", type=str, help="Path to APK")
        parser.add_argument(
            "-g", "--graph", action="store_true", help="Graph view by provided APK"
        )
        parser.add_argument("-sp", "--startp", type=str, help="Starting point")
        parser.add_argument("-d", "--depth", type=int, help="Depth of search")
        parser.add_argument(
            "-r", "--rec", action="store_true", help="Output function recursively"
        )
        parser.add_argument(
            "-if",
            "--initfunc",
            action="store_true",
            help="Output <init> functions",
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
            help="Output file",
        )

        self.ParseArgs(parser.parse_args())

    def PrintSettings(self):
        print()
        d = {
            "APK": self.apkPath if self.apkPath else "Not specified",
            "Draw Graph": self.Graph,
            "Main Point": self.MainPoint if self.MainPoint else "Not specified",
            "Depth": self.Depth,
            "Recursive search": self.Recursive,
            "Filter <init> functions": self.InitFunctions,
            "Ouput detailed information": self.Details,
            "Do package name check": self.PackageNameCheck,
        }

        print("{:<30} {:<15}".format("Argument", "Value"))
        for k, v in d.items():
            print("{:<30} {:<15}".format(k, v))
