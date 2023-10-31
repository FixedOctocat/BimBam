import re
import json
from glob import glob


class Analyzer:
    def __init__(self, Apk, Settings):
        self.Apk = Apk
        self.Settings = Settings

    def GetEntryPoints(
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

        def ClassCheck(ClassName, FuncName, StartPoint=StartPoint):
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
                    if ClassCheck(i[0], i[1])
                ]
            )
        )

        DetaildEP = []
        if len(AfterEntryPoints):
            for i in AfterEntryPoints:
                EP = self.GetEntryPoints(
                    i,
                    DepthNumber=DepthNumber + 1,
                    AnalyzedClass=AnalyzedClass,
                    PreviousFunctionCalls=FunctionCallsFromFP,
                )

                if EP:
                    DetaildEP.append(EP)

        result["Name"] = f"{StartPoint.split('.')[-1]}"
        result["members"] = DetaildEP

        return result

    def DrawClassGraph(self):
        data = self.GetEntryPoints(
            self.Settings.MainPoint
            if self.Settings.MainPoint
            else self.Apk.GetMainActivityName()
        )

        with open(f"{self.Settings.Output}.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
