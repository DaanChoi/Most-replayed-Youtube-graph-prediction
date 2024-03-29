# data
import keras.layers
import nltk
from nltk.corpus import stopwords
from dataset import data_load

# preprocessing
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
import numpy as np

# modeling
import tensorflow as tf

# visualize
import matplotlib.pyplot as plt


def dataset(url):
    dataset = data_load(url)
    num_examples = len(dataset)

    print('Dataset')
    print(dataset)
    print(f'There are {num_examples} examples')
    dataset = dataset.sample(frac=1, random_state=1004)

    sentences = dataset['text'].tolist()
    labels = dataset['score'].tolist()

    # nltk.download('stopwords')
    # print(stopwords.words('english'))

    training_split = 0.9
    train_sentences = sentences[:int(training_split * num_examples)]
    train_labels = labels[:int(training_split * num_examples)]

    val_sentences = sentences[int(training_split * num_examples):]
    val_labels = labels[int(training_split * num_examples):]

    print(f'Training dataset has {len(train_sentences)} examples')
    print(f'Validation dataset has {len(val_sentences)} examples')

    return train_sentences, train_labels, val_sentences, val_labels


def preprocessing(train_sentences, train_labels, val_sentences, val_labels):
    max_len = 30
    trunc_type = 'post'
    padding = 'post'
    oov_token = '<OOV>'

    tokenizer = Tokenizer(oov_token=oov_token)
    tokenizer.fit_on_texts(train_sentences)

    train_sequences = tokenizer.texts_to_sequences(train_sentences)
    train_padded = pad_sequences(train_sequences, maxlen=max_len, truncating=trunc_type, padding=padding)
    train_labels = np.array(train_labels)

    val_sequences = tokenizer.texts_to_sequences(val_sentences)
    val_padded = pad_sequences(val_sequences, maxlen=max_len, truncating=trunc_type, padding=padding)
    val_labels = np.array(val_labels)

    return train_padded, train_labels, val_padded, val_labels, tokenizer


def visualize(history):
    train_acc = history.history['mse']
    val_acc = history.history['val_mse']

    plt.plot(train_acc)
    plt.plot(val_acc)

    plt.xlabel('epochs')
    plt.ylabel('mse')

    plt.legend(['mse', 'val_mse'])

    plt.savefig('mse.jpg')
    # plt.show()

# Callback
class myCallback(tf.keras.callbacks.Callback):
    # Define the correct function signature for on_epoch_end
    def on_epoch_end(self, epoch, logs={}):
        if logs.get('mse') is not None and logs.get('mse') < 0.0113:
            print("\nMAE is lower than 0.113 so cancelling training!")

            # Stop training once the above condition is met
            self.model.stop_training = True


callbacks = myCallback()


def train(train_url):
    # Load data
    train_sentences, train_labels, val_sentences, val_labels = dataset(train_url)

    # Preprocessing
    train_padded, train_labels, val_padded, val_labels, tokenizer = preprocessing(train_sentences, train_labels, val_sentences, val_labels)
    word_index = tokenizer.word_index
    total_words = len(word_index) + 1  # add 1 due to padding_token
    print('word_index vocabulary\n', word_index)

    # Model
    embedding_dim = 64
    epoch = 50
    max_len = 30
    batch_size = 128
    # Small batches can offer a regularizing effect (Wilson and Martinez, 2003),
    # perhaps due to the noise they add to the learning process.

    model = tf.keras.Sequential([
        keras.layers.Embedding(total_words, embedding_dim, input_length=max_len),
        keras.layers.Bidirectional(keras.layers.LSTM(64)),
        keras.layers.Dropout(0.5),
        keras.layers.Dense(1)
    ])

    print(model.summary())

    # Learning rate tuning => mse 값과 val_mse 값이 낮은 구간을 고려하여 lr을 선택했습니다.
    lr_scheduler = tf.keras.callbacks.LearningRateScheduler(
        lambda epoch: 1e-4 * 10**(epoch / 20)
    )

    model.compile(optimizer=keras.optimizers.Adam(learning_rate=4e-4),
                  loss=keras.losses.Huber(),
                  metrics=['mse'])

    history = model.fit(train_padded, train_labels, epochs=epoch,
                        batch_size=batch_size,
                        validation_data=(val_padded, val_labels),
                        callbacks=[callbacks]
                        )

    # Visualize result
    visualize(history)

    return model, tokenizer

