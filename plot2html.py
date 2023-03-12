#!/usr/bin/env python3
import pandas as pd
from bokeh.plotting import output_file, save, show
from bokeh.layouts import row, column, gridplot
import datetime
import numpy as np
import os

def boke_history(time, y, xlabe='tempo', ylabel='', title='', legend='', notebook=False):
    from bokeh.plotting import figure, output_notebook
    from bokeh.models import DatetimeTickFormatter
    if notebook: output_notebook()

    p = figure(title=title, x_axis_type='datetime', 
               y_axis_label=ylabel, 
               x_axis_label=xlabe,
               plot_width=750, plot_height=350)
    p.xaxis.major_label_orientation = 3.14/4
    # add a line renderer with legend and line thickness
    p.line(time, y, legend_label=legend, line_width=2)
    p.xgrid.band_hatch_pattern = "/"
    p.xgrid.band_hatch_alpha = 0.6
    p.xgrid.band_hatch_color = "lightgrey"
    p.xgrid.band_hatch_weight = 0.5
    p.xgrid.band_hatch_scale = 10
    p.xaxis.formatter=DatetimeTickFormatter(
            hours=["%d %B %Y"],
            days=["%d %B %Y"],
            months=["%d %B %Y"],
            years=["%d %B %Y"],
        )
    return p

def main():
    
    lastdata = [x for x in os.listdir('./') if "data_sensors_" in x][-1]
    columns=['timestamp', 'day', 'hour', 'P_in [hP]', 'H_in [%]', 'T_in [C]',  'P_out [hP]', 'H_out [%]', 'T_out [C]', 'T_room [C]', 'H_room [%]', 'D_room [C]', 'P_room [hP]']
    dtp = pd.read_csv(lastdata, delimiter=' ', skiprows = 1, header = None)
    print
    date = [datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S') for x in (dtp[1].values+' '+dtp[2].values)]

    p = []
    for i in range(3, len(dtp.columns)):
        p.append(boke_history(time=date, y=np.array(dtp[i]), notebook=True, ylabel=columns[i], legend=columns[i]))
    grid_layout = column([p[i] for i in range(len(p))])
    output_file("./plots.html")
    save(grid_layout)
    
if __name__ == "__main__":
    main()
