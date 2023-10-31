from classes.APK import Apk
from classes.Settings import Settings
from classes.Analyzer import Analyzer

if __name__ == "__main__":
    ProgramSettings = Settings()
    ProgramSettings.InitArgparser()
    ProgramSettings.PrintSettings()

    apk = Apk(ProgramSettings.apkPath)

    analyzer = Analyzer(apk, ProgramSettings)

    if ProgramSettings.Graph:
        analyzer.DrawClassGraph()
