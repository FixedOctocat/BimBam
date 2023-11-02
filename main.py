"""Import classes"""
from classes.apk import Apk
from classes.settings import Settings
from classes.analyzer import Analyzer
from classes.graph import Graph

if __name__ == "__main__":
    ProgramSettings = Settings()
    ProgramSettings.init_argparser()
    ProgramSettings.print_settings()

    ApkFile = Apk(ProgramSettings.apk_path)

    AnalyzerTool = Analyzer(ApkFile, ProgramSettings)
    AnalyzerTool.start()
    if ProgramSettings.pyvis:
        MainGraph = Graph(f"{ProgramSettings.output}.json")
        MainGraph.draw()
        MainGraph.show()
