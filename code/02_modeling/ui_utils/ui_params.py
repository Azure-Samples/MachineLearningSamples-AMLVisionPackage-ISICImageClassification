from ipywidgets import widgets, Layout
import IPython




class ParamsUI():

    def __init__(self):

        # Callback for the info button, opens up a dialog
        def info_button_pressed(obj):
            dialog_javascript_pattern = """
                require(
                    ["base/js/dialog"],
                    function(dialog) {
                        dialog.modal({
                            title: 'TITLE',
                            body: 'BODY',
                            buttons: {
                                'close': {}
                            }
                        });
                    });
            """

            title = "Learning rate"
            body = obj.tooltip
            msg_js = dialog_javascript_pattern.replace('TITLE', title).replace('BODY', body)
            IPython.display.display(IPython.display.Javascript(msg_js))


        # Mockup parameters
        label_layout = Layout(width='200px')
        info_button = widgets.Button(description='info', icon='info', value="learningRate",
                                    tooltip='A value used by the learning algorithm to determine how quickly the weights are adjusted. It determines the acquisition time for neurons with weights that are trained using the algorithm.')
        info_button.on_click(info_button_pressed)
        w1 = widgets.Text(value="0.01")
        w2 = widgets.Dropdown(options=['ResNet18.dnn', 'AlexNet.dnn'])
        w3 = widgets.Checkbox(value=False)
        w4 = widgets.FloatSlider(value=0.5, min=0, max=1.0, step=0.05)
        w_box = widgets.VBox(children=[
            widgets.HBox(children=[
                widgets.HTML(layout=label_layout, value='<div align = "right"> learningRate: </div>', tooltip='tooltip'),
                w1, info_button]),
            widgets.HBox(children=[
                widgets.HTML(layout=label_layout, value='<p style="text-align:right"> pretrainedModelFileName'), w2,
                info_button]),
            widgets.HBox(children=[widgets.Label(layout=label_layout, value="boVerbose:"), w3, info_button]),
            widgets.HBox(children=[widgets.Label(layout=label_layout, value="dropoutRate:"), w4, info_button])])

        # Tab widget
        page1 = widgets.Box(children=[w_box], padding=4)
        page2 = widgets.Box(children=[], padding=4)
        page3 = widgets.Box(children=[], padding=4)
        page4 = widgets.Box(children=[], padding=4)
        page5 = widgets.Box(children=[], padding=4)
        tabs = widgets.Tab(children=[page1, page2, page3, page4, page5])
        tabs.set_title(0, 'Trainer')
        tabs.set_title(1, 'Model')
        tabs.set_title(2, 'Dataset and Splitter')
        tabs.set_title(3, 'Evaluation')
        tabs.set_title(4, 'Deployment')
        params_ui = widgets.Tab(children=[tabs])
        params_ui.set_title(0, 'PARAMETERS')

        self.ui = params_ui