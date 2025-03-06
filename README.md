# Introduction

This project leverages innovative deep learning models and the Django framework for symptom-based disease prediction. It also provides detailed information about the top predicted diseases, including a chat feature with a doctor. The model that performed best was the Sequential Model with a SoftMax Activation Function, achieving an accuracy of 97.66%. We built the prediction model on this architecture for further usage in the Django framework for UI integration.

We're aiming to predict a wide range of diseases, including Fungal infections, Allergies, Diabetes, etc. By analyzing various symptoms such as Itching, Skin rash, Nodal skin eruptions, and more, our model learns how to predict disease possibilities. This system is designed to be accessible and useful even to individuals with limited medical knowledge. It can assist in early disease detection and diagnosis, giving users an initial understanding of the severity of their condition.


# Background

In healthcare, early disease detection is crucial. This project applies machine learning to predict diseases based on symptoms. We used CSV files containing a dataset with numerous symptoms and corresponding diseases.

Our model, a Convolutional Neural Network (CNN) Sequential Model with SoftMax activation function, examines these symptoms to find patterns and identify diseases early. After extensive training and testing, our model achieves an impressive accuracy of 97.66%.

Beyond just predicting diseases, we have designed a user-friendly interface (UI) to simplify interaction with the model. Users can input their symptoms, and the model provides predictions about potential diseases. Moreover, users can connect with healthcare professionals for further guidance and treatment.

This project advances disease prediction by leveraging symptom-based data, allowing for earlier diagnosis and improved healthcare accessibility. Through the integration of advanced technology, comprehensive symptom data, and a user-friendly interface, our goal is to enhance healthcare outcomes for all.


# Dataset Used

For that we have used the Kaggle dataset which is publicly available for the usage.
Dataset Line:- https://www.kaggle.com/datasets/kaushil268/disease-prediction-using-machine-learning/data


# Results

We utilized various Deep learning models in our project, including Sequential Model with SoftMax Activation Function, Sequential Model Using Dense and Dropout Layers, Decision Tree, Random Forest, SVM, and Gradient Boosting. The accuracies for these models are as follows:
1. Sequential Model with SoftMax Activation Function: 97.66%
2. Sequential Model Using Dense and Dropout Layers: 95.15%
3. Decision Tree: 94.37%
4. Random Forest: 90.6%
5. SVM: 89.87%
6. Gradient Boosting: 86.57%


# Research Paper

Our work has also been published as a research paper and presented at 2024 4th Asian Conference on Innovation in Technology (ASIANCON). You can access the paper using the link below:
🔗 Research Paper: Symptom-Based Disease Prediction Framework Integrated with Django and Deep Learning Models
The paper contains further details about our methodology, experiments, and results, along with information about the conference where our work was presented.

