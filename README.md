# Azure Machine Learning for Computer Vision

Many applications in the computer vision domain can be framed as image classification. These include building models that answer questions such as "Is an OBJECT present in the image?" (OBJECT could be *dog*, *car*, or *ship*) as well as more complex questions such as "What class of eye disease severity is evinced by this patient's retinal scan?"

This document shows how the Azure Machine Learning Package for Computer Vision (AMLPCV) can be used to train, test, and deploy an **image classification** model. Currently, [CNTK](https://www.microsoft.com/en-us/cognitive-toolkit/) is used as the deep learning framework, training is performed locally on a GPU powered machine such as the ([Data Science VM](https://azuremarketplace.microsoft.com/en-us/marketplace/apps/microsoft-ads.dsvm-deep-learning?tab=Overview), and deployment uses the Azure ML Operationalization CLI.

In this tutorial, the following steps are performed:

1. [Data acquision](code/01\_data\_acquisition\_and\_understanding/data\_acquisition.ipynb)

We choose ISIC dataset for the image classification task. ISIC (The International Skin Imaging Collaboration) is a partership between academia and industry to facilitate the application of digital skin imaging to study and help reduce melanoma mortality. The [ISIC archive](https://isic-archive.com/#images) contains over 13,000 skin lesion images with labels either benign or malignant. We download a sample of the images from ISIC archive.

2. [Model](code/02_modeling/modeling.ipynb)

Within modeling step, the following steps are performed. 

* Dataset Creation
* Image Visualization and annotation
* Image Augmentation
* DNN Model Definition
* Classifier Training
* Evaluation and Visualization

Those steps are further explained in the corresponding Jupyter Notebook. We also provided guidelines for turning the parameters such as learning rate, mini batch size, and dropout rate to further improve the model performance.

3. [Deployment](code/03\_deployment/deployment.ipynb)

This step operationalizes the model produced from the modeling step. It introduces the operationalization prerequisites and setup. Finally, the consumption of the web service is also explained. Through this tutorial, you can learn to build deep learning models with AMLPCV and operationalize the model in Azure.

References
[Azure Machine Learning Package for Computer Vision (AMLPCV)](https://docs.microsoft.com/en-us/python/api/overview/azure-machine-learning/computer-vision?view=azure-python)



