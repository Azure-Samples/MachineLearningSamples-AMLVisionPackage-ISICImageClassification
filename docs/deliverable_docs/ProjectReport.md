# Data Science Project Report: Skin Cancer Image Classification with Azure Machine Learning (AML) package for Computer Vision (AMLPCV) and Team Data Science Process (TDSP)

This file contains information about the project being executed (in this case, the Skin Cancer Image Classification sample using AMLPCV). It is organized according to the Team Data Science (TDSP) Process [Lifecycle stages](https://github.com/Azure/Microsoft-TDSP/blob/master/Docs/lifecycle-detail.md).

## 1. Business Understanding
### Customer & Business Problem
 *  NOTE: This is a sample for a tutorial, so scope, plan etc., does not necessarily correspond to an actual data science project addressing a specific business question. In an actual project, the problem definition, scope, plan, personnel sections are likely to be much more detailed, based on discussions with the client (or business owner), the structure of the data science team etc.

 * The purpose of this sample is to show how to run image classification with AMLPCV using the TDSP structure and templates.

The dataset for this project is from the [ISIC](https://isic-archive.com/#images), which contains over 13,000 skin lesion images with labels either benign or malignant. We download a sample of the images from ISIC archive.

### Scope
 * The scope of this sample is to create a binary image classification machine learning model which address the above problem.
 * We execute the project in Jupyter Notebooks in AML Workbench. We use the Team Data Science Process template of Azure Machine Learning for this project.
 * We operationalize the solution in Azure Container Services.

## Plan

We follow the stages fo the TDSP lifecycle, and organize documentation and code according to the stages of the lifecycle. Documentation about the work and findings in each of the lifecycle stages is included below. The code is organized into folders that follow the lifecycle stages. Documentation about the code and its execution is provided in .\code folder and subfolders.

### Personnel

The project is executed by one data scientist. Data scientist executes the various data science steps, creates and compares models, and deployes the final model using Azure Machine Learning.

NOTE: In a customer project additional personnel, from both from a data science team as well as the client organization, may be involved (as outlined in the [TDSP documentation](https://github.com/Azure/Microsoft-TDSP/blob/master/Docs/roles-tasks.md))

### Metrics

Accuracy is measured and reported using precision, recall, and AUC.

## 2. Data Acquisition and Understanding

The image classification task uses skin images from the International Skin Imaging Collaboration (ISIC). ISIC is a partership between academia and industry to faciliate the application of digital skin imaging to study and help reduce melanoam mortality. We download a sample of the images from ISIC archive, and the number of samples can be customized.

## 3. Modeling

In modeling step, the following substeps are performed. 

<b>2.1 Dataset Creation</b><br>

<b>2.2 Image Visualization and annotation</b><br>

<b>2.3 Image Augmentation</b><br>

<b>2.4 DNN Model Definition</b><br>

<b>2.5 Classifier Training</b><br>

<b>2.6 Evaluation and Visualization</b><br>

The substep provides functionality to evaluate the performance of the trained model on an independent test dataset. The evaluation metrics include accuracy, precision and recall, and ROC curve.

Those substeps are explained in detail in the corresponding Jupyter Notebook. We also provided guidelines for turning the parameters such as learning rate, mini batch size, and dropout rate to further improve the model performance.

Six different per-trained Deep Neural Network models are supported in AMLPCV: AlexNet, Resnet-18, Resnet-34, and Resnet-50, Resnet-101, and Resnet-152. These DNNs can be used either as classifier, or as featurizer (see step 5). More information about the networks can be found [here](https://github.com/Microsoft/CNTK/blob/master/PretrainedModels/Image.md), and a basic introduction to Transfer Learning is [here](https://blog.slavv.com/a-gentle-intro-to-transfer-learning-2c0b674375a0).

AMLPCV comes with default parametes (224x224 pixel resolution and Resnet-18 DNN) which were selected to work well on a wide variety of tasks. Accuracy can often be improved by eg. increasing the image resolution to 500x500 pixels, and/or selecting a deeper model (Resnet-50), however this comes at a significant increase in training time. See the "How to improve accuracy" section in the Appendix for more detail, and why the minibatch-size and the learning rate need to be updated.

## 4. Deployment

Operationalization is the process of publishing models and code as web services and the consumption of these services to produce business results. Once your model is trained, we can deploy your trained model as a webservice for comsumption with [Azure Machine Learning CLI](https://docs.microsoft.com/en-us/azure/machine-learning/preview/cli-for-azure-machine-learning). The models can be deployed to your local machine or Azure Container Service (ACS) cluster as a webservice. You can scale your webservice with Azure Container Service (ACS) cluster. It also provides some autoscaling functionality for your webservice.

## Code Execution
In this example, we execute code in local compute environment only. Refer to Azure Machine Learning documents for execution details and further options.

IPython notebook files can be double-clicked from the project structure on the left of the Azure Machine Learning UI and run in the Jypyter Notebook Server.

## Reference Documents
 * [Project Repository in GitHub](https://github.com/Azure/MachineLearningSamples-TDSPUCIAdultIncome)
 * [TDSP project template for Azure Machine Learning](https://aka.ms/tdspamlgithubrepo)