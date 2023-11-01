from classes.APK import Apk
from classes.Settings import Settings
from classes.Analyzer import Analyzer
from classes.Graph import Graph

if __name__ == "__main__":
    ProgramSettings = Settings()
    ProgramSettings.InitArgparser()
    ProgramSettings.PrintSettings()

    ApkFile = Apk(ProgramSettings.apkPath)

    AnalyzerTool = Analyzer(ApkFile, ProgramSettings)
    AnalyzerTool.Start()

    MainGraph = Graph("graph.json")
    MainGraph.Draw()
    MainGraph.Show()
