"""Import classes"""
from classes.apk import Apk
from classes.settings import Settings
from classes.analyzer import CallSearch
from classes.graph import Graph

if __name__ == "__main__":
    ProgramSettings = Settings()
    ProgramSettings.init_argparser()

    ProgramSettings.print_settings()

    ApkFile = Apk(ProgramSettings.apk_path)

    if ProgramSettings.functions_graph or ProgramSettings.intents_graph:
        AnalyzerTool = CallSearch(ApkFile, ProgramSettings)
        AnalyzerTool.start()
        if ProgramSettings.pyvis:
            MainGraph = Graph(f"{ProgramSettings.output}.json")
            MainGraph.start()
            MainGraph.show()
