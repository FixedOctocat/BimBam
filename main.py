"""Import classes"""
from classes.apk import Apk
from classes.settings import Settings
from classes.analyzer import CallSearch, BaseInformation
from classes.graph import Graph

if __name__ == "__main__":
    ProgramSettings = Settings()
    ProgramSettings.init_argparser()

    ProgramSettings.print_settings()

    ApkFile = Apk(ProgramSettings.apk_path)
    ApkInfo = BaseInformation(ApkFile, ProgramSettings)
    ApkInfo.get_attack_surface()

    if ProgramSettings.functions_graph or ProgramSettings.intents_graph:
        AnalyzerTool = CallSearch(ApkFile, ProgramSettings)
        AnalyzerTool.start()
        if ProgramSettings.pyvis:
            MainGraph = Graph(f"{ProgramSettings.output}.json")
            MainGraph.start()
            MainGraph.show()
