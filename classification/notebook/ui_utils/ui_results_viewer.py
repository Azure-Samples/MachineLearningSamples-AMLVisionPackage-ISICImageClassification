import sys
import numpy as np
from ipywidgets import widgets, Layout, IntSlider
import bqplot
from bqplot import pyplot as bqPyplot


def wImread(img_obj, context):
    imgBytes = open(img_obj.storage_path, "rb").read()
    return imgBytes


# Init
class ResultsUI(object):
    # Init object and define instance variables
    def __init__(self, dataset, context, pred_scores, pred_labels):
        self.dataset = dataset
        self.context = context
        self.pred_scores = pred_scores
        self.pred_labels = pred_labels
        assert (pred_scores.shape[1] == len(dataset.labels))
        assert (len(pred_labels) == pred_scores.shape[0] == len(dataset.images))

        # Init
        self.vis_image_index = 0
        self.labels = [l.name for l in dataset.labels]
        self.label_to_id = {s: i for i, s in enumerate(self.labels)}

        # Create UI
        self.ui = self.create_ui()

    # Update / redraw all UI elements
    def update_ui(self):
        pred_label = self.pred_labels[self.vis_image_index]
        img_obj = self.dataset.images[self.vis_image_index]
        scores = self.pred_scores[self.vis_image_index]

        self.w_image_header.value = "Image index: {}".format(self.vis_image_index)
        self.w_img.value = wImread(img_obj, self.context)
        self.w_gt_label.value = self.dataset.get_labels_for_image(img_obj)[0].name
        self.w_pred_label.value = str(pred_label)
        self.w_pred_score.value = str(self.pred_scores[self.vis_image_index, self.label_to_id[pred_label]])
        self.w_index.value = str(self.vis_image_index)
        self.w_filename.value = img_obj.name
        self.w_path.value = img_obj.storage_path
        bqPyplot.clear()
        bqPyplot.bar(self.labels, scores, align='center', alpha=1.0, color=np.abs(scores),
                     scales={'color': bqplot.ColorScale(scheme='Blues', min=0)})

    # Create all UI elements
    def create_ui(self):

        # ------------
        # Callbacks + logic
        # ------------
        # Return if image should be shown
        def image_passes_filters(image_index):
            actual_label = self.dataset.get_labels_for_image(self.dataset.images[image_index])[0]
            bo_pred_correct = actual_label.name == self.pred_labels[image_index]
            if (bo_pred_correct and self.w_filter_correct.value) or (not bo_pred_correct and self.w_filter_wrong.value):
                return True
            return False

        # Next / previous image button callback
        def button_pressed(obj):
            step = int(obj.value)
            self.vis_image_index += step
            self.vis_image_index = min(max(0, self.vis_image_index), int(len(self.pred_labels)) - 1)
            while not image_passes_filters(self.vis_image_index):
                self.vis_image_index += step
                if self.vis_image_index <= 0 or self.vis_image_index >= int(len(self.pred_labels)) - 1:
                    break
            self.vis_image_index = min(max(0, self.vis_image_index), int(len(self.pred_labels)) - 1)
            self.w_image_slider.value = self.vis_image_index
            self.update_ui()

        # Image slider callback. Need to wrap in try statement to avoid errors when slider value is not a number.
        def slider_changed(obj):
            try:
                self.vis_image_index = int(obj['new']['value'])
                self.update_ui()
            except Exception as e:
                pass

        # ------------
        # UI - image + controls (left side)
        # ------------
        w_next_image_button = widgets.Button(description="Image +1")
        w_next_image_button.value = "1"
        w_next_image_button.layout = Layout(width='80px')
        w_next_image_button.on_click(button_pressed)
        w_previous_image_button = widgets.Button(description="Image -1")
        w_previous_image_button.value = "-1"
        w_previous_image_button.layout = Layout(width='80px')
        w_previous_image_button.on_click(button_pressed)

        self.w_image_slider = IntSlider(min=0, max=len(self.pred_labels) - 1, step=1,
                                      value=self.vis_image_index, continuous_update=False)
        self.w_image_slider.observe(slider_changed)
        self.w_image_header = widgets.Text("", layout=Layout(width="130px"))
        self.w_img = widgets.Image()
        self.w_img.layout.width = '500px'
        w_image_with_header = widgets.VBox(children=[widgets.HBox(children=[w_previous_image_button, w_next_image_button, self.w_image_slider]),
                                                  self.w_img], width=520)

        # ------------
        # UI - info (right side)
        # ------------
        w_filter_header = widgets.HTML(value="Filters (use Image +1/-1 buttons for navigation):")
        self.w_filter_correct = widgets.Checkbox(value=True, description='Correct classifications')
        self.w_filter_wrong = widgets.Checkbox(value=True, description='Incorrect classifications')

        w_gt_header = widgets.HTML(value="Ground truth:")
        self.w_gt_label = widgets.Text(value="", description="Label:")

        w_pred_header = widgets.HTML(value="Prediction:")
        self.w_pred_label = widgets.Text(value="", description="Label:")
        self.w_pred_score = widgets.Text(value="", description="Score:")

        w_info_header = widgets.HTML(value="Image info:")
        self.w_index = widgets.Text(value="", description="Index:")
        self.w_filename = widgets.Text(value="", description="Name:")
        self.w_path = widgets.Text(value="", description="StoragePath:")

        w_scores_header = widgets.HTML(value="Classification scores:")
        self.w_scores = bqPyplot.figure()
        self.w_scores.layout.height = '250px'
        self.w_scores.layout.width = '370px'
        self.w_scores.fig_margin = {"top": 5, "bottom": 80, "left": 30, "right": 5}

        # Combine UIs into tab widget
        w_info_HBox = widgets.VBox(children=[w_filter_header, self.w_filter_correct, self.w_filter_wrong, w_gt_header,
                                           self.w_gt_label, w_pred_header, self.w_pred_label, self.w_pred_score,
                                           w_info_header, self.w_index, self.w_filename, self.w_path, w_scores_header,
                                           self.w_scores])
        w_info_HBox.layout.padding = '20px'
        vis_tabs_ui = widgets.Tab(children=[widgets.HBox(children=[w_image_with_header, w_info_HBox])])  # ,
        vis_tabs_ui.set_title(0, 'Results viewer')

        # Fill UI with content
        self.update_ui()

        return (vis_tabs_ui)
