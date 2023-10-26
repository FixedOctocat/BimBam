import json
import re
from subprocess import DEVNULL, STDOUT, check_call
from glob import glob
import os


class Apk:
    def __init__(self, apkFilepath):
        self.LoadApk(apkFilepath)
        self.apkFilepath = apkFilepath

        self.PackageName = None
        self.MainActivityName = None
        self.SetInfo()

    def GetPackageName(self):
        return self.PackageName

    def GetMainActivityName(self):
        return self.MainActivityName

    def LoadApk(self, apkFilepath):
        if os.path.isdir("apktoolFolder"):
            c = input("apktoolFolder wil be deleted\nA you sure? [Y/n] ")
            if c.lower() != "y":
                print("Analyzing file in apktoolFolder")
                return 0

            check_call(["rm", "-r", "apktoolFolder"])

        try:
            check_call(
                ["apktool", "d", apkFilepath, "-o", "apktoolFolder"],
                stdout=DEVNULL,
                stderr=STDOUT,
            )
        except Exception as e:
            print(e)

    def SetInfo(self):
        AndroidManifest = open("apktoolFolder/AndroidManifest.xml").read()
        PackageName = re.search('package="([a-zA-Z0-9.]*)"', AndroidManifest)
        MainActivityName = re.search(
            'android:name="([a-zA-Z0-9.]*MainActivity)"', AndroidManifest
        )

        self.PackageName = PackageName.group(1) if PackageName else None
        self.MainActivityName = MainActivityName.group(1) if PackageName else None

    def DrawClassGraph(self, GraphSettings):
        def GetEntryPoints(
            StartPoint=None, DepthNumber=0, AnalyzedClass=[], PreviousFunctionCalls=[]
        ):
            result = {
                "Name": "",
                "members": "",
            }

            if not GraphSettings.Recursive:
                if StartPoint in AnalyzedClass:
                    return []
                AnalyzedClass.append(StartPoint)

            if DepthNumber == GraphSettings.Depth:
                return []

            if GraphSettings.Details:

                def MakeDetailedView(SmaliCode):
                    return f"{SmaliCode[1]}({SmaliCode[2]}){SmaliCode[3]}"

                Detailed = list(
                    set(
                        [
                            FunctionCallFromFP
                            for FunctionCallFromFP in PreviousFunctionCalls
                            if StartPoint.split(".")[-1] in FunctionCallFromFP[0]
                        ]
                    )
                )

                if not GraphSettings.InitFunctions:
                    Detailed = [
                        MakeDetailedView(FunctionCallFromFP)
                        for FunctionCallFromFP in Detailed
                        if FunctionCallFromFP[1] != "<init>"
                    ]

                if Detailed:
                    for i in range(len(Detailed)):
                        result[f"Function {i}"] = Detailed[i]

            def ClassCheck(ClassName, FuncName, StartPoint=StartPoint):
                if not GraphSettings.PackageNameCheck:
                    for i in self.GetPackageName().split("."):
                        if i not in ClassName:
                            return False

                if "android" in ClassName:
                    return False

                if "java" in ClassName:
                    return False

                if not GraphSettings.InitFunctions:
                    if FuncName == "<init>":
                        return False

                if StartPoint.split(".")[-1] in ClassName:
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
                    EP = GetEntryPoints(
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

        data = GetEntryPoints(
            GraphSettings.MainPoint
            if GraphSettings.MainPoint
            else self.GetMainActivityName()
        )

        with open(f"{GraphSettings.Output}.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
