from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from joblib import load

model = load_model('./sentiment/SENTIMENTAL_LSTM.keras')
tokenizer = load('./sentiment/tokenizer.joblib')
encoder = load('./sentiment/encoder.joblib')

def predict_sentiment(text):
    seq = tokenizer.texts_to_sequences([text])
    padded = pad_sequences(seq, maxlen=100)
    pred = model.predict(padded)
    label_index = pred.argmax()
    label = encoder.inverse_transform([label_index])[0]
    
    sentiment_labels = {
        -1: 'Negative',
        0: 'Neutral',
        1: 'Positive'
    }
    return sentiment_labels[label]
