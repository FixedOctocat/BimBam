from classes.APK import Apk
from classes.Settings import Settings

if __name__ == "__main__":
    ProgramSettings = Settings()
    ProgramSettings.InitArgparser()
    apk = Apk(ProgramSettings.apkPath)
    ProgramSettings.PrintSettings()

    if ProgramSettings.Graph:
        apk.DrawClassGraph(ProgramSettings)
