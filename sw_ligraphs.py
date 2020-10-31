'''
Plot graphics
'''

import glob
import csv
import matplotlib.pyplot as plt
import os
import re

GRAPH_SHIFT = 1

def read_file_data(filepath):
    '''
    Read data in [[val,time],[val, time]] format
    '''

    data = None

    with open(filepath, 'r') as dest_f:
        data_iter = csv.reader(dest_f,delimiter="\t")
        data = [data for data in data_iter]

    timemarks = data[0][1:]
    data = data[1:]
    data.reverse()

    return (data, timemarks)

def plot_graph(data, timemarks, out_filepath, to_display=False, save_to_disk=True):
    '''
    Plot grapth
    '''

    graphics = list()
    levels = list()
    y = list()

    # Populate list
    for idx in range(0, len(data[0]) - 1):
        graphics.append([])

    for measure_idx, measure in enumerate(data):
        level = int(measure[0])
        if level != 0:
            levels.append(level)
        else:
            levels.append(1)

        values = measure[1:]
        for idx_val in range(0, len(values)):
            graphics[idx_val].append(float(values[idx_val]) + GRAPH_SHIFT * idx_val)
        
    # Main magic of the graph
    fig, ax = plt.subplots()
   
    for y in graphics: 
        plt.plot(y, levels, color='black')

    ax.invert_yaxis()

    fig.canvas.draw()

    x_labels = [tick.get_text() for tick in ax.get_xticklabels()]
    for idx, _ in enumerate(x_labels):
        if int(re.sub(u"\u2212", "-", x_labels[idx])) < 0:
            continue
        if int(x_labels[idx]) > (len(timemarks) - 1):
            continue
        x_labels[idx] = timemarks[int(x_labels[idx])][:-10]
    ax.set_xticklabels(x_labels)

    y_labels = [tick.get_text() for tick in ax.get_yticklabels()]
    for idx, _ in enumerate(y_labels):
        if y_labels[idx] == '0':
            y_labels[idx] = '1'
    ax.set_yticklabels(y_labels)

    if to_display:
        plt.show()

    if save_to_disk:
        plt.tight_layout()
        fig.set_figheight(6)
        fig.set_figwidth(18)
        plt.savefig(out_filepath, dpi=300)

    return None

def main():
    print("Script is started")

    files = glob.glob("./input/*.txt")    

    for filepath in files:
        print("Process >> " + filepath)

        try:
            read_data, read_timemarks = read_file_data(filepath)

            out_png_filepath = "./output/" + os.path.basename(filepath) + ".png"

            output_data = plot_graph(read_data, read_timemarks, out_png_filepath)
            print("Saved PNG to >> " + out_png_filepath)
    
        except Exception as e:
            print("Cannot process >> ", filepath)
            print("Reason >> " + str(e))
            
        finally:
            print()

    print("Script is finished")

if __name__ == "__main__":
    main()