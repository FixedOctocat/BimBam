# BimBam
Tool for drawing function/intent graphs

```
python3 main.py --help
usage: main.py [-h] [-fg] [-ig] [-sp STARTP] [-e] [-a] [-d DEPTH] [-r] [-if] [-det] [-pnc] [-snc] [-o OUTPUT]
               [-od OUTPUT_DIR] [--pyvis]
               apk

positional arguments:
  apk                   Path to APK

options:
  -h, --help            show this help message and exit
  -fg, --fgraph         Function graph view by provided APK
  -ig, --igraph         Intent graph view by provided APK
  -sp STARTP, --startp STARTP
                        Starting point
  -e, --exported        Analyze exported activities
  -a, --allactivities   Analyze all activities
  -d DEPTH, --depth DEPTH
                        Depth of search
  -r, --rec             Output function recursively
  -if, --initfunc       output <init> functions
  -det, --details       Get detailed view
  -pnc                  Do package name check for all calls
  -snc                  Filter all system classes for calls
  -o OUTPUT, --output OUTPUT
                        Output file
  -od OUTPUT_DIR, --output_dir OUTPUT_DIR
                        Directory for apktool
  --pyvis               Generate interactive graph
```