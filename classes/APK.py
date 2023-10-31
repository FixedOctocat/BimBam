import re
import os
from subprocess import DEVNULL, STDOUT, check_call


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
            c = input("apktoolFolder wil be deleted\nAre you sure? [Y/n] ")
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
