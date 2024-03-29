from dataset import data_load
from model import train
import numpy as np

import tensorflow as tf
from keras.preprocessing.sequence import pad_sequences

from all_graph import forecast_graph, obvious_graph, target_graph, comparison_graph

# Train model
train_url = "https://www.youtube.com/watch?v=X7158uQk1yI"
model, tokenizer = train(train_url)

# Load test datasets
test_url = "https://www.youtube.com/watch?v=L6sbfskaTDQ"
test_sets = data_load(test_url)
num_examples = len(test_sets)

print('Dataset')
print(test_sets)
print(f'There are {num_examples} examples')

test_sentences = test_sets['text'].tolist()
test_labels = test_sets['score'].tolist()

# Preprocessing
max_len = 30
trunc_type = 'post'
padding = 'post'

test_sequences = tokenizer.texts_to_sequences(test_sentences)
test_padded = pad_sequences(test_sequences, maxlen=max_len, truncating=trunc_type, padding=padding)
test_labels = np.array(test_labels)

# Predict
forecast = model.predict(test_padded)
forecast = forecast.squeeze()
mse = tf.keras.metrics.mean_squared_error(test_labels, forecast).numpy()

print(mse)

# Most-replayed section graphs
forecast_graph(forecast)
obvious_graph(forecast)
target_graph(test_labels)
comparison_graph(forecast, test_labels)
