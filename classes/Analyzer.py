import re
import json
from glob import glob


class Analyzer:
    def __init__(self, Apk, Settings):
        self.Apk = Apk
        self.Settings = Settings

    def ClassCheck(self, ClassName, FuncName=None, StartPoint=None):
        if not self.Settings.InitFunctions:
            if FuncName == "<init>":
                return False

        if not self.Settings.PackageNameCheck:
            for i in self.Apk.GetPackageName().split("."):
                if i not in ClassName:
                    return False

        for nameCheck in ["android", "java", StartPoint.split(".")[-1]]:
            if nameCheck in ClassName:
                return False

        return True

    # EntryPoints Search
    def FunctionSearch(
        self, StartPoint=None, DepthNumber=0, AnalyzedClass=[], PreviousFunctionCalls=[]
    ):
        result = {
            "Name": "",
            "members": "",
        }

        if not self.Settings.Recursive:
            if StartPoint in AnalyzedClass:
                return []
            AnalyzedClass.append(StartPoint)

        if DepthNumber == self.Settings.Depth:
            return []

        if self.Settings.Details:
            Detailed = list(
                set(
                    [
                        FunctionCallFromFP
                        for FunctionCallFromFP in PreviousFunctionCalls
                        if StartPoint.split(".")[-1] in FunctionCallFromFP[0]
                    ]
                )
            )

            if not self.Settings.InitFunctions:
                Detailed = [
                    f"{FunctionCallFromFP[1]}({FunctionCallFromFP[2]}){FunctionCallFromFP[3]}"
                    for FunctionCallFromFP in Detailed
                    if FunctionCallFromFP[1] != "<init>"
                ]

            if Detailed:
                for i in range(len(Detailed)):
                    result[f"Function {i}"] = Detailed[i]

        ActivityFolder = [
            dir
            for dir in glob(
                f"apktoolFolder/smali*/{'/'.join(StartPoint.split('.')[:-1])}"
            )
        ][0]

        FirstPoint = open(
            f"{ActivityFolder}/{StartPoint.split('.')[-1]}.smali", "r"
        ).read()

        FunctionCallsFromFP = re.findall(
            "L([a-zA-Z0-9$\/<>]*);->([a-zA-Z0-9$\/<>]*)\(([a-zA-Z0-9$\/<>;\[\]]*)\)([a-zA-Z0-9$\/<>]*)",
            FirstPoint,
        )

        AfterEntryPoints = list(
            set(
                [
                    i[0].replace("/", ".")
                    for i in FunctionCallsFromFP
                    if self.ClassCheck(
                        ClassName=i[0], FuncName=i[1], StartPoint=StartPoint
                    )
                ]
            )
        )

        MembersOfEP = []
        if len(AfterEntryPoints):
            for i in AfterEntryPoints:
                EP = self.FunctionSearch(
                    i,
                    DepthNumber=DepthNumber + 1,
                    AnalyzedClass=AnalyzedClass,
                    PreviousFunctionCalls=FunctionCallsFromFP,
                )

                if EP:
                    MembersOfEP.append(EP)

        result["Name"] = f"{StartPoint.split('.')[-1]}"
        result["members"] = MembersOfEP

        return result

    # Search for intents
    def IntentSearch(
        self, StartPoint=None, DepthNumber=0, AnalyzedClass=[], PreviousFunctionCalls=[]
    ):
        result = {
            "Name": "",
            "members": "",
        }

        if not self.Settings.Recursive:
            if StartPoint in AnalyzedClass:
                return []
            AnalyzedClass.append(StartPoint)

        if DepthNumber == self.Settings.Depth:
            return []

        ActivityFolder = [
            dir
            for dir in glob(
                f"apktoolFolder/smali*/{'/'.join(StartPoint.split('.')[:-1])}"
            )
        ][0]

        FirstPoint = open(
            f"{ActivityFolder}/{StartPoint.split('.')[-1]}.smali", "r"
        ).read()

        FunctionCallsFromFP = re.findall(
            """const-class .*, L(.*);\n\n    invoke-direct {.*}, Landroid\/content\/Intent;-><init>\(Landroid\/content\/Context;Ljava\/lang\/Class;\)V""",
            FirstPoint,
        )

        AfterEntryPoints = [
            i.replace("/", ".")
            for i in FunctionCallsFromFP
            if self.ClassCheck(ClassName=i, StartPoint=StartPoint)
        ]

        MembersOfEP = []
        if len(AfterEntryPoints):
            for i in AfterEntryPoints:
                EP = self.IntentSearch(
                    i,
                    DepthNumber=DepthNumber + 1,
                    AnalyzedClass=AnalyzedClass,
                    PreviousFunctionCalls=FunctionCallsFromFP,
                )

                if EP:
                    MembersOfEP.append(EP)

        result["Name"] = f"{StartPoint.split('.')[-1]}"
        result["members"] = MembersOfEP

        return result

    def DrawClassGraph(self):
        data = self.IntentSearch(
            self.Settings.MainPoint
            if self.Settings.MainPoint
            else self.Apk.GetMainActivityName()
        )

        return data

    def Start(self):
        if self.Settings.FunctionsGraph:
            data = self.FunctionSearch(
                self.Settings.MainPoint
                if self.Settings.MainPoint
                else self.Apk.GetMainActivityName()
            )

        if self.Settings.IntentsGraph:
            data = self.IntentSearch(
                self.Settings.MainPoint
                if self.Settings.MainPoint
                else self.Apk.GetMainActivityName()
            )

        with open(f"{self.Settings.Output}.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
