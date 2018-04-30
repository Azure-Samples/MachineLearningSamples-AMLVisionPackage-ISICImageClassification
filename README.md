# Azure Machine Learning for Computer Vision

A large number of problems in the computer vision domain can be solved using image classification approaches. These include building models which answer questions such as, "Is an OBJECT present in the image?" (where OBJECT could for example be "dog", "car", "ship", etc.) as well as more complex questions, like "What class of eye disease severity is evinced by this patient's retinal scan?"

This document shows how the Azure Machine Learning for Computer Vision Package (CVTK) can be used to train, test, and deploy an **image classification** model. Currently, [CNTK](https://www.microsoft.com/en-us/cognitive-toolkit/) is used as the deep learning framework, training is performed locally on a GPU powered machine such as the ([Data Science VM](https://azuremarketplace.microsoft.com/en-us/marketplace/apps/microsoft-ads.dsvm-deep-learning?tab=Overview)), and deployment uses the Azure ML Operationalization CLI.

In this tuturial, the following steps are performed:

1. [Data acquision](code/01\_data\_acquisition\_and\_understanding/data\_acquisition.ipynb)

We chose ISIC dataset for the image classification task. ISIC (The International Skin Imaging Collaboration) is a partership between academia and industry to faciliate the application of digital skin imaging to study and help reduce melanoam mortality. The [ISIC archive](https://isic-archive.com/#images) contains over 13,000 skin lesion images with labels either benign or malignant. We download a sample of the images from ISIC archive.

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

This step operationalizes the model produced from the modeling step. It introduces the operationalization prequisites and setup. Finally, the consumption of the web service is also explained. Through this tutorial, you can learn to build deep learning models with CVTK and operationalize the model in Azure.
For more details, please check the CVTK API docs. 

# Contributing

This project welcomes contributions and suggestions.  Most contributions require you to agree to a
Contributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us
the rights to use your contribution. For details, visit https://cla.microsoft.com.

When you submit a pull request, a CLA-bot will automatically determine whether you need to provide
a CLA and decorate the PR appropriately (e.g., label, comment). Simply follow the instructions
provided by the bot. You will only need to do this once across all repos using our CLA.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or
contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.

# Legal Notices

Microsoft and any contributors grant you a license to the Microsoft documentation and other content
in this repository under the [Creative Commons Attribution 4.0 International Public License](https://creativecommons.org/licenses/by/4.0/legalcode),
see the [LICENSE](LICENSE) file, and grant you a license to any code in the repository under the [MIT License](https://opensource.org/licenses/MIT), see the
[LICENSE-CODE](LICENSE-CODE) file.

Microsoft, Windows, Microsoft Azure and/or other Microsoft products and services referenced in the documentation
may be either trademarks or registered trademarks of Microsoft in the United States and/or other countries.
The licenses for this project do not grant you rights to use any Microsoft names, logos, or trademarks.
Microsoft's general trademark guidelines can be found at http://go.microsoft.com/fwlink/?LinkID=254653.

Privacy information can be found at https://privacy.microsoft.com/en-us/

Microsoft and any contributors reserve all others rights, whether under their respective copyrights, patents,
or trademarks, whether by implication, estoppel or otherwise.
