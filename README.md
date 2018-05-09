# Introduction

This article shows how to use the [Azure Machine Learning Package for Computer Vision (AMLPCV)](https://docs.microsoft.com/en-us/python/api/overview/azure-machine-learning/computer-vision?view=azure-ml-py-latest) to train, test, and deploy an **image classification** model. The sample uses the TDSP structure and templates in [Azure Machine Learning Workbench](https://docs.microsoft.com/en-us/azure/machine-learning/service/quickstart-installation). The complete sample is provided in this walkthrough. It uses [CNTK](https://www.microsoft.com/en-us/cognitive-toolkit/) as the deep learning framework, and training is performed on a [Data Science VM](https://azuremarketplace.microsoft.com/en-us/marketplace/apps/microsoft-ads.dsvm-deep-learning?tab=Overview) GPU machine. Deployment uses the Azure ML Operationalization CLI.

Many applications in the computer vision domain can be framed as image classification problems. These include building models that answer questions such as "Is an object present in the image?" (object could be *dog*, *car*, or *ship*) and more complex questions such as "What class of eye disease severity is evinced by this patient's retinal scan?" AMLPCV streamline image classification data processing and modeling pipeline. 

# Link to GitHub repository
We provide summary documentation here about the sample. More extensive documentation can be found on the [GitHub site](https://github.com/Azure/MachineLearningSamples-AMLVisionPackage-ISICImageClassification).

# TDSP Walkthrough with AMLPCV

The walkthrough covers the following tasks:

1. [Data acquision](code/01\_data\_acquisition\_and\_understanding/data\_acquisition.ipynb)

ISIC dataset is used for the image classification task. ISIC (The International Skin Imaging Collaboration) is a partership between academia and industry to facilitate the application of digital skin imaging to study and help reduce melanoma mortality. The [ISIC archive](https://isic-archive.com/#images) contains over 13,000 skin lesion images with labels either benign or malignant. We download a sample of the images from ISIC archive.

2. [Modeling](code/02_modeling/modeling.ipynb)

In modeling step, the following substeps are performed. 

* Dataset Creation

In order to generate a Dataset object in AMLPCV, provide a root directory of images on the local disk.

* Image Visualization and annotation

Visualize the images in the dataset object, and correct some of the labels if necessary.

* Image Augmentation

Augment a dataset object using the transformations described in the [imgaug](https://github.com/aleju/imgaug) library.

* DNN Model Definition

Define the model architecture used in the training step. Six different per-trained deep neural network models are supported in AMLPCV: AlexNet, Resnet-18, Resnet-34, and Resnet-50, Resnet-101, and Resnet-152.

* Classifier Training

Train the neural networks with default or custom parameters.

* Evaluation and Visualization

The substep provides functionality to evaluate the performance of the trained model on an independent test dataset. The evaluation metrics include accuracy, precision and recall, and ROC curve.

Those substeps are explained in detail in the corresponding Jupyter Notebook. We also provided guidelines for turning the parameters such as learning rate, mini batch size, and dropout rate to further improve the model performance.

3. [Deployment](code/03\_deployment/deployment.ipynb)

This step operationalizes the model produced from the modeling step. It introduces the operationalization prerequisites and setup. Finally, the consumption of the web service is also explained. Through this tutorial, you can learn to build deep learning models with AMLPCV and operationalize the model in Azure.

# References

* [Azure Machine Learning Package for Computer Vision (AMLPCV)](https://docs.microsoft.com/en-us/python/api/overview/azure-machine-learning/computer-vision?view=azure-ml-py-latest)
* [Azure Machine Learning Workbench](https://docs.microsoft.com/en-us/azure/machine-learning/service/quickstart-installation)
* [Data Science VM](https://azuremarketplace.microsoft.com/en-us/marketplace/apps/microsoft-ads.dsvm-deep-learning?tab=Overview)

