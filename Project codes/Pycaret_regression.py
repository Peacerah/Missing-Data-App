# Load dataset
import pandas as pd
train = pd.read_csv("train.csv")
test = pd.read_csv("test.csv")

# init setup
from pycaret.regression import *
s = setup(train, target = "target")

#model training and selection
best = compare_models()

#analyze best model
evaluate_model(best)

#predict on new data
predictions = predict_model(best, data = test)

# save bestt pipeline
save_model(best, "my_best_pipeline")
