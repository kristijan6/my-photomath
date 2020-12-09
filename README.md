# my-photomath
Task required for the Machine Learning Intern position @ Photomath

Modules:
1. postfix_calc.py 
    - Postfix based calculator for calculating the expression
2. data_loader.py 
    - handles all data, from preprocessing to reading the input for the neural network
3. model.py
    - neural network model. If not stated otherwise, it will not train new model but rather load the latest model available in the **saved_model**

Folders:
1. data
    - data used to test how the model works 
2. recognized_data
    - cropped characters (not preprocessed) from the character detector
3. saved_model
    - saved pretrained models. By default it's loaded when initializing the Model
4. test_data, train_data
    - data used for training adn testing the model

Use **my-photomath.ipynb** for examples on how to use different modules.
