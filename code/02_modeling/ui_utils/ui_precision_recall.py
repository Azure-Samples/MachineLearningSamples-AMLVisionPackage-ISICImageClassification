import sys
import numpy as np
import bqplot
from bqplot import pyplot as bqPyplot
from ipywidgets import widgets, Layout


# ----------------------------------------------------------------------------------------------------------------------
# Precision/recall curve UI
# ----------------------------------------------------------------------------------------------------------------------
class PrecisionRecallUI(object):
    def __init__(self, precisions, recalls, thres):
        assert(len(recalls) == len(precisions) == len(thres))

        # Callback
        def index_change_callback(change):
            selected_recall = int(np.round(change.new[0]))
            index = np.abs(recalls - selected_recall).argmin()
            w_precision.value = "{:2.2f}".format(precisions[index])
            w_recall.value    = "{:2.2f}".format(recalls[index])
            w_threshold.value = "{:2.2f}".format(thres[index])

        # Set up bqplot UI
        ls_x = bqplot.LinearScale(min=0, max=100)  # reverse=True)
        ls_y = bqplot.LinearScale(min=0, max=100)
        axis_y = bqplot.Axis(label='Recall', scale=ls_x)
        axis_x = bqplot.Axis(label='Precision', scale=ls_y, orientation='vertical')
        lines = bqplot.Lines(x=recalls, y=precisions, scales={'x': ls_x, 'y': ls_y}, colors=['orange'])
        index_sel = bqplot.interacts.IndexSelector(scale=ls_x, marks=[lines], color = "blue",  colors = ["green"])
        index_sel.observe(index_change_callback, names=['selected'])
        fig = bqplot.Figure(marks=[lines], axes=[axis_x, axis_y], title='Precision-recall curve', interaction=index_sel)

        # Set up p/r/threshold text fields UI
        w_precision = widgets.Text(value="CLICK ON PLOT", description="Precision:")
        w_recall    = widgets.Text(value="CLICK ON PLOT", description="Recall:")
        w_threshold = widgets.Text(value="CLICK ON PLOT", description="Threshold:")
        w_texts = widgets.HBox(children=[w_precision, w_recall, w_threshold])

        # Create final UI
        self.ui = widgets.VBox([fig, w_texts])