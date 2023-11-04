"""
re for pattern searching in smali code (intents, functions)
json for dict dumping
glob for directory recursive search
"""

import re
import json
from glob import glob


class Analyzer:
    """Class for smali code analyze"""

    def __init__(self, apk, settings):
        self.apk = apk
        self.settings = settings

    def class_check(
        self, class_name: str, func_name: str = None, start_point: str = None
    ):
        """Funtion for class name (and function name) checks"""
        if not self.settings.init_functions:
            if func_name == "<init>":
                return False

        if self.settings.package_name_check:
            for i in self.apk.package_name.split("."):
                if i not in class_name:
                    return False

        if self.settings.system_name_check:
            for name_check in ["android", "java"]:
                if name_check in class_name:
                    return False

        if start_point.split(".")[-1] in class_name:
            return False

        return True

    # EntryPoints Search
    def function_search(
        self,
        start_point: str = None,
        depth_number: int = 0,
        analyzed_class: list = None,
        previous_function_calls: list = None,
        color: str = "#97c2fc",
    ) -> dict:
        """Search function calls"""
        result = {
            "Name": f"{start_point.split('.')[-1]}",
            "members": "",
        }

        if self.settings.pyvis:
            result["color"] = color

        if not self.settings.recursive:
            if start_point in analyzed_class:
                return []
            analyzed_class.append(start_point)

        if depth_number == self.settings.depth:
            return []

        if self.settings.details:
            detailed = list(
                set(
                    [
                        FunctionCallFromFP
                        for FunctionCallFromFP in previous_function_calls
                        if start_point.split(".")[-1] in FunctionCallFromFP[0]
                    ]
                )
            )

            if not self.settings.init_functions:
                detailed = [
                    f"{FunctionCallFromFP[1]}({FunctionCallFromFP[2]}){FunctionCallFromFP[3]}"
                    for FunctionCallFromFP in detailed
                    if FunctionCallFromFP[1] != "<init>"
                ]

            if detailed:
                for i, details in enumerate(detailed):
                    result[f"Function {i}"] = details

        activity_folder = [
            dir
            for dir in glob(
                f"apktoolFolder/smali*/{'/'.join(start_point.split('.')[:-1])}"
            )
        ]

        members_of_ep = []
        if activity_folder:
            activity_folder = activity_folder[0]
            try:
                first_point = open(
                    f"{activity_folder}/{start_point.split('.')[-1]}.smali",
                    "r",
                    encoding="utf-8",
                ).read()
            except FileNotFoundError:
                print(f"Can't find class: {start_point}")
                result["members"] = members_of_ep
                return result

            function_calls_from_fp = re.findall(
                r"L([a-zA-Z0-9$\/<>]*);->([a-zA-Z0-9$\/<>]*)\(([a-zA-Z0-9$\/<>;\[\]]*)\)([a-zA-Z0-9$\/<>]*)",
                first_point,
            )

            after_entry_points = list(
                set(
                    [
                        i[0].replace("/", ".")
                        for i in function_calls_from_fp
                        if self.class_check(
                            class_name=i[0], func_name=i[1], start_point=start_point
                        )
                    ]
                )
            )

            if after_entry_points:
                for i in after_entry_points:
                    ep = self.function_search(
                        i,
                        depth_number=depth_number + 1,
                        analyzed_class=analyzed_class,
                        previous_function_calls=previous_function_calls,
                    )

                    if ep:
                        members_of_ep.append(ep)

        result["members"] = members_of_ep

        return result

    # Search for intents
    def intent_search(
        self,
        start_point: str = None,
        depth_number: int = 0,
        analyzed_class: list = None,
        color: str = "#97c2fc",
    ) -> dict:
        """Intent search in activities"""
        result = {
            "Name": "",
            "members": "",
        }

        if self.settings.pyvis:
            result["color"] = color

        if not self.settings.recursive:
            if start_point in analyzed_class:
                return []
            analyzed_class.append(start_point)

        if depth_number == self.settings.depth:
            return []

        activity_folder = [
            dir
            for dir in glob(
                f"apktoolFolder/smali*/{'/'.join(start_point.split('.')[:-1])}"
            )
        ][0]

        first_point = open(
            f"{activity_folder}/{start_point.split('.')[-1]}.smali",
            "r",
            encoding="utf-8",
        ).read()

        function_calls_from_fp = re.findall(
            r"""const-class .*, L(.*);\n\n    invoke-direct {.*}, Landroid\/content\/Intent;-><init>\(Landroid\/content\/Context;Ljava\/lang\/Class;\)V""",
            first_point,
        )

        after_entry_points = [
            i.replace("/", ".")
            for i in function_calls_from_fp
            if self.class_check(class_name=i, start_point=start_point)
        ]

        members_of_ep = []
        if after_entry_points:
            for i in after_entry_points:
                ep = self.intent_search(
                    i,
                    depth_number=depth_number + 1,
                    analyzed_class=analyzed_class,
                )

                if ep:
                    members_of_ep.append(ep)

        result["Name"] = f"{start_point.split('.')[-1]}"
        result["members"] = members_of_ep

        return result

    def draw_class_graph(self) -> dict:
        """Return dict graph"""
        data = self.intent_search(
            self.settings.main_point
            if self.settings.main_point
            else self.apk.get_main_activity_name()
        )

        return data

    def start(self, data: dict = None):
        """Start analyzing apk"""
        activities = {}
        activities["MainActivity"] = [self.apk.mainactivity_name]
        if self.settings.all_activities:
            activities["Exported"] = self.apk.exported_activities
            activities["Other"] = self.apk.other_activities
        elif self.settings.exported:
            activities["Exported"] = self.apk.exported_activities

        colors = {
            "MainActivity": "#fc97bc",
            "Exported": "#fcc897",
            "Other": "#97c2fc",
        }

        data = []
        if self.settings.functions_graph:
            for activity_type, activity_names in activities.items():
                for activity in activity_names:
                    data.append(
                        self.function_search(
                            activity,
                            depth_number=0,
                            analyzed_class=[],
                            previous_function_calls=[],
                            color=colors[activity_type],
                        )
                    )

        if self.settings.intents_graph:
            for activity_type, activity_names in activities.items():
                for activity in activity_names:
                    data.append(
                        self.intent_search(
                            activity,
                            depth_number=0,
                            analyzed_class=[],
                            color=colors[activity_type],
                        )
                    )

        if data:
            with open(f"{self.settings.output}.json", "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
