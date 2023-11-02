"""
re for finding patterns (package_name and mainactivity_name)
os for dir checking
subprocess for apktool usage
"""
import re
import os
from subprocess import DEVNULL, STDOUT, check_call


class Apk:
    """Class representing a apk file and it's structure"""

    def __init__(self, apk_filepath: str):
        self.apk_filepath = apk_filepath
        self.load_apk()

        self.package_name = None
        self.mainactivity_name = None
        self.exported_activities = []
        self.other_activities = []
        self.set_info()

    def load_apk(self):
        """Load apk file with apktool"""
        if os.path.isdir("apktoolFolder"):
            c = input("apktoolFolder wil be deleted\nAre you sure? [Y/n] ")
            if c.lower() != "y":
                print("Analyzing file in apktoolFolder")
                return 0

            check_call(["rm", "-r", "apktoolFolder"])
            return 0
        try:
            check_call(
                ["apktool", "d", self.apk_filepath, "-o", "apktoolFolder"],
                stdout=DEVNULL,
                stderr=STDOUT,
            )
        except Exception as e:
            print(e)

    def set_info(self):
        """Get informations from unpacked apk file"""
        android_manifest = open(
            "apktoolFolder/AndroidManifest.xml", encoding="utf-8"
        ).read()

        package_name = re.search(r'package="([a-zA-Z0-9.]*)"', android_manifest)
        self.package_name = package_name.group(1) if package_name else None

        mainactivity_name = re.search(
            rf'android:name="({self.package_name}[a-zA-Z0-9_$.]*MainActivity)"',
            android_manifest,
        )
        self.mainactivity_name = mainactivity_name.group(1) if package_name else None

        all_activities = re.findall(r"<activity.*>", android_manifest)
        for activity in all_activities:
            activity_name = re.search(
                r'android:name="([a-zA-Z0-9_$.]*)"', activity
            ).group(1)
            if 'android:exported="true"' in activity:
                self.exported_activities.append(activity_name)
            else:
                self.other_activities.append(activity_name)
