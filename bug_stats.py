from bokeh.plotting import figure, output_file, show, ColumnDataSource
from bokeh.models import HoverTool, ColorBar, LinearColorMapper, Ticker
import pandas as pd

output_file("bug_stats.html")
df = pd.read_csv('test.csv')
#source = ColumnDataSource(data=dict(
#    x=[1, 2, 3, 4, 5],
#    y=[2, 5, 8, 2, 7],
#    desc=['A', 'b', 'C', 'd', 'E'],
#))

palette = ["#5e4fa2", "#3288bd", "#66c2a5", "#abdda4", "#e6f598", "#ffffbf", "#fee08b", "#fdae61", "#f46d43", "#d53e4f", "#9e0142"]

melting_points = df["HP"]
low = min(melting_points)
high= max(melting_points)
melting_point_inds = [int(10.0*(x-low)/(high-low)) for x in melting_points] #gives items in colors a value from 0-10
df["hp_colors"] = [palette[i] for i in melting_point_inds]

color_mapper = LinearColorMapper(palette=palette,low=low, high=high)


#colors = [
#    "#%02x%02x%02x" % (int(r), 150, 150) for r in zip(50+2*df["SPEED"])
#]

source = ColumnDataSource(df)
hover = HoverTool(tooltips=[
    ("Name", "@NAME"),
    ("Attack", "@ATTACK"),
    ("Defense", "@DEFENSE"),
    ("HP","@HP"),
    ("Speed","@SPEED"),
    ("Sp. Attack", "@SP_ATTACK"),
    ("Sp. Defense", "@SP_DEFENSE")
])

TOOLS = "crosshair,pan,wheel_zoom,zoom_in,zoom_out,box_zoom,undo,redo,reset,tap,save"

p = figure(plot_width=600, plot_height=600, tools=TOOLS,title="Relative Size = Total Stats, Color = HP")
p.add_tools(hover)
p.xaxis.axis_label = "Attack"
p.yaxis.axis_label = "Defense"
color_bar = ColorBar(color_mapper=color_mapper,
                     label_standoff=12, border_line_color=None,location=(-65, 0), orientation='horizontal')

p.circle('ATTACK', 'DEFENSE', size="TOTAL_10", fill_alpha = 0.6,fill_color="hp_colors",line_color=None,source=source)
p.add_layout(color_bar, 'above')

show(p)