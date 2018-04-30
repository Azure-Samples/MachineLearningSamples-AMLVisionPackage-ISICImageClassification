from ipywidgets import widgets, Layout, IntSlider
import io
from cvtk import ClassificationDataset, Label

#import sys
#import bqplot, IPython, random
#from IPython.display import display
#from bqplot import pyplot as bqPyplot
#sys.path.append("C:\\Users\\pabuehle\\Desktop\\PROJECTS\\pythonLibrary")
#from pabuehle_utilities_general_v2 import randomizeList




# ------------
# Helpers
# ------------
def w_imread(img_obj, context):
    img_bytes = open(img_obj.storage_path, "rb").read()
    return img_bytes

def list_split(list_1D, n, method):
    if method.lower() == 'fillFirst'.lower():
        list_2D = [list_1D[i:i + n] for i in range(0, len(list_1D), n)]
    else:
        raise Exception('Unknown list split method')
    return list_2D


# ------------------------------------------------
# Class - Image annotation UI
# -------------------------------------------------
class AnnotationUI(object):

    # Init object and define instance variables
    def __init__(self, dataset, context, grid_size=(3, 2), img_indices=[]):
        self.dataset  = dataset
        self.context  = context
        self.grid_size = grid_size

        # Set images to be shown (in that order)
        if img_indices == []:
            img_indices = list(range(len(dataset.images)))
            #random.shuffle(img_indices)

        ##############self.labels = sorted([l.name for l in dataset.labels])
        self.labels = self.dataset.labels
        self.label_options = {}
        for l in self.labels:
            self.label_options[l.name] = l

        # Initialize what images are on what image page
        # (page == grid of images on the right side of the UI)
        self.page_index = 0
        self.page_img_indices = list_split(img_indices, grid_size[0] * grid_size[1], method='fillFirst')

        # Create UI
        self.ui = self.create_ui()


    # Update / redraw the zoom UI elements
    def update_zoom_ui(self, img_obj, img_index):
        self.w_zoom_img.value      = w_imread(img_obj, self.context)
        self.w_zoom_header.value   = "Image #: {}".format(img_index)
        self.w_zoom_text_area.value = str(img_obj).replace(', ', '\n')
        self.w_page_slider.value   = str(self.page_index)


    # Update / redraw all UI elements
    def update_ui(self):
        self.bo_updating_ui = True # indicate code is in updating-UI state

        # Update image grid UI
        img_indices = self.page_img_indices[self.page_index]
        for i in range(self.grid_size[0] * self.grid_size[1]):
            w_img    = self.w_imgs[i]
            w_label  = self.w_labels[i]
            w_button = self.w_buttons[i]

            if i < len(img_indices):
                img_index = img_indices[i]
                img_obj = self.dataset.images[img_index]
                w_img.layout.visibility    = 'visible'
                w_button.layout.visibility = 'visible'
                w_label.layout.visibility  = 'visible'
                w_img.value = w_imread(img_obj, self.context)
                w_img.description = str(img_index)
                w_label.value = self.dataset.get_labels_for_image(img_obj)[0]
                #w_label.text = str(img_index)  # this property is ignored and not accessible later in code
                w_label.description  = "Image " + str(img_index)
                w_button.description = "Zoom"
                w_button.value = str(img_index)
            else:
                w_img.layout.visibility    = 'hidden'
                w_button.layout.visibility = 'hidden'
                w_label.layout.visibility  = 'hidden'

        # Update zoom image UI
        self.update_zoom_ui(self.dataset.images[img_indices[0]], img_indices[0])
        self.bo_updating_ui = False


    # Create all UI elements
    def create_ui(self):

        # ------------
        # Callbacks
        # ------------
        # Callback for image label dropdown menu
        def dropdown_changed(obj):
            # Note that updating the dropdown label in code (e.g. in the update_ui() function)
            # also triggers this change event. Hence need to check if self.bo_updating_ui is False.
            if obj['type'] == 'change' and obj['name'] == 'value' and not self.bo_updating_ui:
                img_index = int(obj['owner'].description[6:])
                new_label = obj['owner'].value
                self.dataset.change_label_for_image(self.dataset.images[img_index], new_label)

        # Callback for "zoom" button
        def img_button_pressed(obj):
            img_index = int(obj.value)
            img_obj = self.dataset.images[img_index]
            self.update_zoom_ui(img_obj, img_index)

        # Callback for "next images" or "previous images" buttons
        def page_button_pressed(obj):
            self.page_index += int(obj.value)
            self.page_index = max(0, self.page_index)
            self.page_index = min(self.page_index, len(self.page_img_indices) - 1)
            self.update_ui()

        # Callback for "image page" slider
        def page_slider_changed(obj):
            try:
                self.page_index = int(obj['new']['value'])
                self.update_ui()
            except Exception as e:
                pass

        # Init
        self.bo_updating_ui = False

        # ------------
        # UI - image grid
        # ------------
        self.w_imgs    = []
        self.w_labels  = []
        self.w_buttons = []
        w_img_label_buttons = []

        for i in range(self.grid_size[0] * self.grid_size[1]):
            # Initialize images
            w_img = widgets.Image(width=200, description="")
            self.w_imgs.append(w_img)

            # Initialize dropdown menus
            w_label = widgets.Dropdown(options=self.label_options, value=self.label_options[self.labels[0].name], text="Image 0", description="Image 0")
            w_label.layout.width = '200px'
            w_label.observe(dropdown_changed, names='value')
            self.w_labels.append(w_label)

            # Initialize zoom buttons
            w_button = widgets.Button(description="Image id: ", value="")
            w_button.layout.width = "100px"
            w_button.button_style = 'warning'
            w_button.on_click(img_button_pressed)
            self.w_buttons.append(w_button)

            # combine into image grid widget
            w_img_label_button = widgets.VBox(children=[w_button, w_img, w_label])
            w_img_label_button.width = '230px'
            w_img_label_buttons.append(w_img_label_button)

        # Image grid widget
        w_grid_HBoxes = []
        for r in range(self.grid_size[0]):
            hbox = widgets.HBox(children=[w_img_label_buttons[r * self.grid_size[1] + c] for c in range(self.grid_size[1])])
            hbox.layout.padding = '10px'
            w_grid_HBoxes.append(hbox)
        w_img_grid = widgets.VBox(w_grid_HBoxes)

        # ------------
        # UI - zoom window
        # ------------
        w_next_page_button = widgets.Button(description="Next images", value="1")
        w_next_page_button.value = "1"  # should not be necessary but bug on some jupyter versions otherwise
        w_next_page_button.layout.width = '120px'
        w_next_page_button.button_style = 'primary'
        w_next_page_button.on_click(page_button_pressed)

        w_previous_page_button = widgets.Button(description="Previous images", value="-1",
                                             layout=Layout(color='white', background_color='lightblue'))
        w_previous_page_button.value = "-1"
        w_previous_page_button.layout.width = '120px'
        w_previous_page_button.button_style = 'primary'
        w_previous_page_button.on_click(page_button_pressed)

        self.w_page_slider = IntSlider(min=0, max=len(self.page_img_indices) - 1, step=1, value=self.page_index,
                                     continuous_update=False, description='Image page:')
        self.w_page_slider.observe(page_slider_changed)

        self.w_zoom_header = widgets.Text("")
        self.w_zoom_header.layout.width = "100px"
        self.w_zoom_header.layout.color = 'white'
        self.w_zoom_header.layout.background_color = 'orange'
        self.w_zoom_img = widgets.Image()
        self.w_zoom_img.layout.width = '500px'
        self.w_zoom_text_area = widgets.Textarea()
        self.w_zoom_text_area.layout.width  = '500px'
        self.w_zoom_text_area.layout.height = '100px'

        w_zoom_button_slider = widgets.HBox([widgets.VBox([w_next_page_button, w_previous_page_button]),
                                          self.w_page_slider])  # self.w_zoom_header
        w_zoom_button_slider.layout.width = '420px'


        # ------------
        # UI - final
        # ------------
        annotation_ui = widgets.HBox(children=[widgets.VBox(children=[w_zoom_button_slider, self.w_zoom_img, self.w_zoom_text_area], width=520),
                                              w_img_grid])
        annotation_ui.layout.border_color = 'black'
        annotation_ui.layout.border_style = 'solid'
        tabs_ui = widgets.Tab(children=[annotation_ui])
        tabs_ui.set_title(0, 'Image Annotation')

        # Update UI with actual images
        self.update_ui()
        return (tabs_ui)