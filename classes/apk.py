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

        self.activities = {
            "MainActivities": [],
            "ExportedActivities": [],
            "OtherActivities": [],
        }
        self.providers = {"Exported": [], "NotExported": []}
        self.receivers = {"Exported": [], "NotExported": []}
        self.services = {"Exported": [], "NotExported": []}
        self.__load_components()

        self.permissions = self.get_permissions()

    def __load_components(self):
        """Save all activities"""

        application = self.manifest_file.find("application")
        for activity in application.find_all("activity"):
            try:
                exported = "True" if activity["android:exported"] == "true" else "False"
            except KeyError:
                exported = False

            if exported:
                intent_filters = activity.find_all("intent-filter")

                try:
                    if "android.intent.action.MAIN" in [
                        intent.find("action").get("android:name")
                        for intent in intent_filters
                    ] and "android.intent.category.LAUNCHER" in [
                        intent.find("category").get("android:name")
                        for intent in intent_filters
                    ]:
                        self.activities["MainActivities"].append(
                            activity["android:name"]
                        )
                    else:
                        self.activities["ExportedActivities"].append(
                            activity["android:name"]
                        )
                except AttributeError:
                    self.activities["ExportedActivities"].append(
                        activity["android:name"]
                    )
            else:
                self.activities["OtherActivities"].append(activity["android:name"])

        for provider in application.find_all("provider"):
            exported = provider.get("android:exported", False) == "true"

            if exported:
                self.providers["Exported"].append(provider.get("android:name"))
            else:
                self.providers["NotExported"].append(provider.get("android:name"))

        for receiver in application.find_all("receiver"):
            exported = receiver.get("android:exported", False) == "true"

            if exported:
                self.receivers["Exported"].append(receiver.get("android:name"))
            else:
                self.receivers["NotExported"].append(receiver.get("android:name"))

        for service in application.find_all("service"):
            exported = service.get("android:exported", False) == "true"

            if exported:
                self.services["Exported"].append(service.get("android:name"))
            else:
                self.services["NotExported"].append(service.get("android:name"))

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
