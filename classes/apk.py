"""
re for finding patterns (package_name and mainactivity_name)
os for dir checking
subprocess for apktool usage
bs4 for AndroidManifest.xml parsing
"""

import os
from subprocess import DEVNULL, STDOUT, check_call
from bs4 import BeautifulSoup


class Apk:
    """Class representing a apk file and it's structure"""

    def __init__(self, path_to_apk: str):
        self.path_to_apk = path_to_apk
        self.__use_apktool()

        self.manifest = AndroidManifest("apktoolFolder/AndroidManifest.xml")
        self.package_name = self.manifest.get_package_name()

    def __use_apktool(self):
        """Load apk file with apktool"""

        if os.path.isdir("apktoolFolder"):
            c = input("apktoolFolder wil be deleted\nAre you sure? [Y/n] ")
            if c.lower() != "y":
                print("Analyzing file in apktoolFolder")
                return 0

            check_call(["rm", "-r", "apktoolFolder"])

        check_call(
            ["apktool", "d", self.path_to_apk, "-o", "apktoolFolder"],
            stdout=DEVNULL,
            stderr=STDOUT,
        )
        return 1


class AndroidManifest:
    """Class to read AndroidManifest.xml file"""

    def __init__(self, path_to_manifest: str):
        # AndroidManifest.xml file
        self.path_to_manifest = path_to_manifest

        with open(self.path_to_manifest, "r", encoding="utf-8") as f:
            data = f.read()

        self.manifest_file = BeautifulSoup(data, "xml")

        self.mainactivities = []
        self.exported_activities = []
        self.other_activities = []
        self.__set_activities()

        self.permissions = self.get_permissions()

        # Other useful staff
        self.services = None
        self.receivers = None
        self.providers = None

    def __set_activities(self):
        """Save all activities"""

        application = self.manifest_file.find("application")
        for activity in application.find_all("activity"):
            try:
                exported = "True" if activity["android:exported"] == "true" else "False"
            except KeyError:
                exported = False

            if exported:
                intent_filters = activity.find_all("intent-filter")

                if "android.intent.action.MAIN" in [
                    intent.find("action")["android:name"] for intent in intent_filters
                ] and "android.intent.category.LAUNCHER" in [
                    intent.find("category")["android:name"] for intent in intent_filters
                ]:
                    self.mainactivities.append(activity["android:name"])
                else:
                    self.exported_activities.append(activity["android:name"])
            else:
                self.other_activities.append(activity["android:name"])

    def get_permissions(self) -> list:
        """Grab permissions from AndroidManifest.xml"""

        premissions = []
        for permission in self.manifest_file.find_all("uses-permission"):
            premissions.append(permission["android:name"])
        return premissions

    def get_package_name(self) -> str:
        "Get package name from manifest"

        package_name = self.manifest_file.find("manifest")["package"]
        return package_name
