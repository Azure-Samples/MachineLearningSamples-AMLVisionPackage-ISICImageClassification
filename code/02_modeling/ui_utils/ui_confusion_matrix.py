import numpy as np
from bokeh.plotting import figure
from bokeh.models import HoverTool, ColumnDataSource, LinearColorMapper, LogTicker, ColorBar


# ----------------------------------------------------------------------------------------------------------------------
# Confusion matrix UI
# ----------------------------------------------------------------------------------------------------------------------
class ConfusionMatrixUI(object):

    def __init__(self, conf_mat, labels):
        conf_mat = np.array(conf_mat)
        assert(conf_mat.shape[0] == conf_mat.shape[1] == len(labels))

        # Prepare plot data
        xname = []
        yname = []
        color = []
        alpha = []
        for i, name1 in enumerate(labels):
            for j, name2 in enumerate(labels):
                xname.append(name1)
                yname.append(name2)
                alpha.append(conf_mat[i, j] / (1.0 * conf_mat.max()))  # min(counts[i,j]/4.0, 0.9) + 0.1)
                color.append('orange')
        source = ColumnDataSource(data=dict(xname=xname, yname=yname, colors=color,
                                            alphas=alpha, count=conf_mat.flatten()))

        # Initialize UI
        cm_fig = figure(title="", x_axis_location="above", tools="hover,save",
                       toolbar_location="below", x_range=list(reversed(labels)), y_range=labels)
        cm_fig.plot_width  = min(100 * len(labels), 600)
        cm_fig.plot_height = cm_fig.plot_width
        cm_fig.grid.grid_line_color = None
        cm_fig.axis.axis_line_color = None
        cm_fig.axis.major_label_standoff = 0
        cm_fig.axis.major_tick_line_color = None
        cm_fig.axis.major_label_text_font_size = "20pt"
        cm_fig.xaxis.major_label_orientation = np.pi/3 # np.pi/2 for vertical
        cm_fig.xaxis.axis_label = "Prediction"
        cm_fig.yaxis.axis_label = "Ground Truth"

        # Set plot data
        cm_fig.rect('xname', 'yname', 0.9, 0.9, source=source, color='colors', alpha='alphas', line_color=None,
                   hover_line_color='black', hover_color='colors')
        cm_fig.select_one(HoverTool).tooltips = [('names', '@yname, @xname'),
                                                ('count', '@count')]

        # Set final UI
        self.ui = cm_fig