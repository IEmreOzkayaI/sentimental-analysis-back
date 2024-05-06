from flask import Flask, request, jsonify
from joblib import load
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pandas as pd

# Kaydedilmiş modeli yükle
model = load_model('./SENTIMENTAL_LSTM.keras')
tokenizer = load('./tokenizer.joblib')
encoder = load('./encoder.joblib')

print("Model yüklendi.")

app = Flask(__name__)

def predict_sentiment(text):
    # Process the text
    seq = tokenizer.texts_to_sequences([text])
    padded = pad_sequences(seq, maxlen=100)
    
    # Get prediction from the model
    pred = model.predict(padded)
    
    # Find the label with the highest probability
    label_index = pred.argmax()
    label = encoder.inverse_transform([label_index])[0]  # Find sentiment label using label encoding
    sentiment_labels = {
        -1: 'Negative',
        0: 'Neutral',
        1: 'Positive'
    }  # Map -1, 0, 1 to labels
    return sentiment_labels[label]

# API endpoint'i ve request method'u tanımlama
@app.route('/predict', methods=['POST'])
def predict():
    text = request.json['text']
    prediction = predict_sentiment(text)
    return jsonify({'prediction': prediction})

if __name__ == '__main__':
    app.run(debug=False, port=3000, use_reloader=False, use_debugger=False)


