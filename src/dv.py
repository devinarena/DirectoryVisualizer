import os
import sys
import pandas as pd
import plotly.express as px
import re
import random

random.seed()

# customizables
MIN_FILE_SIZE = 1000000  # 1 MB
Y_AXIS = "File Size (B)"  
Y_AXIS_DOWNSCALE = 1  # keep this at 1 unless you want to downscale the y axis (e.g. 1000 to show in KB)
BAR_COLOR = random.choice([
    "#1e90ff", "#ff6347", "#32cd32", "#ff69b4", "#ffd700", "#ff8c00",
    "#4b0082", "#00ffff", "#ff00ff", "#000000"
]) # random color from a list of colors if none is specified
GRAPH_TITLE = "Directory Visualizer: "
SORTED = False


def print_splash() -> None:
    """
    Prints the splash screen for the program
    """
    print("DirectoryVisualizer by Devin Arena")
    print("Usage: python main.py <directory> <graph-type> [options]")
    print("Required arguments:")
    print("  <directory>\t\tPath to the directory to visualize")
    print("  <graph-type>\t\tType of graph to show (pie, bar, scatter)")
    print("Optional arguments:")
    print("  -h, --help\t\tShow this help message and exit")
    print("  -m, --size\t\tMinimum file size to show (in KB)")
    print("  -kb\t\t\tShow file sizes in KB instead of B")
    print("  -mb\t\t\tShow file sizes in MB instead of B")
    print("  -gb\t\t\tShow file sizes in GB instead of B")
    print("  -c, --color\t\tColor of the bars in the graph (hex code)")
    print("  -s, --sorted\t\tSort the graph by file size")


def main() -> None:
    """
    Main function
    """
    global GRAPH_TITLE, MIN_FILE_SIZE, Y_AXIS, Y_AXIS_DOWNSCALE, BAR_COLOR, SORTED

    if len(sys.argv) < 3:
        print_splash()
        return

    if sys.argv[1] == "-h" or sys.argv[1] == "--help" or sys.argv[
            2] == "-h" or sys.argv[2] == "--help":
        print_splash()
        return

    path = sys.argv[1]
    GRAPH_TITLE += path
    graph_type = sys.argv[2]

    if graph_type != "pie" and graph_type != "bar" and graph_type != "scatter":
        print("Error: invalid graph type, use -h or --help for help")
        return

    if not os.path.exists(path):
        print("Error: path does not exist")
        return

    if not os.path.isdir(path):
        print("Error: path is not a directory")
        return

    # parse optional arguments
    for i in range(2, len(sys.argv)):
        if sys.argv[i] == "-h" or sys.argv[i] == "--help":
            print_splash()
            exit(0)
        if sys.argv[i] == "-m" or sys.argv[i] == "--size":
            try:
                MIN_FILE_SIZE = int(sys.argv[i + 1]) * 1000
            except:
                print(
                    "Error: invalid minimum file size, use -h or --help for help"
                )
                return
        elif sys.argv[i] == "-c" or sys.argv[i] == "--color":
            BAR_COLOR = sys.argv[i + 1]

            if not BAR_COLOR.startswith("#"):
                BAR_COLOR = "#" + BAR_COLOR

            # check if valid hex code with regex
            if not re.match(r"^#(?:[0-9a-fA-F]{3}){1,2}$", BAR_COLOR):
                print("Error: invalid hex code, use -h or --help for help")
                return
        elif sys.argv[i] == "-s" or sys.argv[i] == "--sorted":
            SORTED = True
        elif sys.argv[i] == "-kb":
            Y_AXIS = "File Size (KB)"
            Y_AXIS_DOWNSCALE = 1000 # 1000 bytes in 1 KB
        elif sys.argv[i] == "-mb":
            Y_AXIS = "File Size (MB)"
            Y_AXIS_DOWNSCALE = 1000000 # 1000000 bytes in 1 MB
        elif sys.argv[i] == "-gb":
            Y_AXIS = "File Size (GB)"
            Y_AXIS_DOWNSCALE = 1000000000 # 1000000000 bytes in 1 GB

    files = os.listdir(path)
    file_sizes = {}

    # get file sizes
    for file in files:
        file_ext = os.path.splitext(file)[1]
        file_size = os.path.getsize(os.path.join(path, file))

        if file_ext in file_sizes:
            file_sizes[file_ext] += file_size
        else:
            file_sizes[file_ext] = file_size

    # remove extensions with file size less than MIN_FILE_SIZE
    file_sizes = {
        k: v / Y_AXIS_DOWNSCALE
        for k, v in file_sizes.items() if v >= MIN_FILE_SIZE
    }

    # Sort the dictionary by value in descending order if SORTED is True
    if not SORTED:
        df = pd.DataFrame(file_sizes.items(), columns=["Extension", Y_AXIS])
    else:
        df = pd.DataFrame(sorted(file_sizes.items(),
                                 key=lambda x: x[1],
                                 reverse=True),
                          columns=["Extension", Y_AXIS])
    
    # create graph based on graph_type
    if graph_type == "pie":
        fig = px.pie(df,
                     title=GRAPH_TITLE,
                     names="Extension",
                     values=Y_AXIS,
                     color="Extension",
                     color_discrete_sequence=px.colors.sequential.RdBu)
        fig.show()
    elif graph_type == "bar":
        fig = px.bar(df,
                     title=GRAPH_TITLE,
                     x="Extension",
                     y=Y_AXIS,
                     color="Extension",
                     color_discrete_sequence=[BAR_COLOR])
        fig.show()
    elif graph_type == "scatter":
        fig = px.scatter(df,
                         title=GRAPH_TITLE,
                         x="Extension",
                         y=Y_AXIS,
                         color="Extension",
                         color_discrete_sequence=[BAR_COLOR])
        fig.show()


if __name__ == "__main__":
    main()