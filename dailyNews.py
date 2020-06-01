import pickle
import numpy as np
from flask import Flask, request
from simpletransformers.classification import ClassificationModel
from transformers import BartTokenizer, BartForConditionalGeneration, BartConfig

app = Flask(__name__)

sentimentModel = None
summarizerModel = None
tokenizer = None


def load_model():
    global sentimentModel
    global summarizerModel
    global tokenizer
    sentimentModel = ClassificationModel(
        'roberta', 'sentimentAnalysisModel', use_cuda=False)
    summarizerModel = BartForConditionalGeneration.from_pretrained(
        'bart-large-cnn')
    tokenizer = BartTokenizer.from_pretrained('bart-large-cnn')


@app.route('/')
def home_endpoint():
    return 'Hello World!'


@app.route('/predict', methods=['POST'])
def get_prediction():
    # Works only for a single sample
    if request.method == 'POST':
        json_data = request.get_json()  # Get data posted as a json
        data = json_data['article']
        data = [data]
        inputs = tokenizer.batch_encode_plus(
            data, max_length=1024, return_tensors='pt')
        summary_ids = summarizerModel.generate(
            inputs['input_ids'], num_beams=4, max_length=100, early_stopping=True)
        summary = [tokenizer.decode(
            g, skip_special_tokens=True, clean_up_tokenization_spaces=False) for g in summary_ids]
        # runs globally loaded model on the data
        prediction = sentimentModel.predict(data)
        if prediction[0] == 0:
            sentiment = 'Negative'
        else:
            sentiment = 'Positive'
    print(sentiment)
    print('\n \n')
    print(summary)
    return str('Sentiment: ' + sentiment + '\n\nSummary:\n' + summary[0])


if __name__ == '__main__':
    load_model()  # load model at the beginning once only
    app.run(host='0.0.0.0', port=5000)
