from flask import Flask, render_template, request, redirect, url_for
import predictor  # Assuming predictor.py is in the same directory
from metaphor_python import Metaphor  # Import the Metaphor class

app = Flask(__name__)

# Initialize the Metaphor API
metaphor = Metaphor("144e6f1d-4b0d-4b8c-ac9b-cc77c89975bc")

@app.route('/', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        uploaded_files = request.files.getlist("file[]")
        if not uploaded_files:
            return "No files uploaded!", 400

        # Save the images temporarily
        paths = []
        for file in uploaded_files:
            path = "img/" + file.filename
            file.save(path)
            paths.append(path)

        predictions = predictor.predict_images(paths)

        # Get the highest-ranking disease
        top_disease = predictions[0][0] if predictions else None

        # Use the metaphor API to get more information about the top disease
        metaphor_results = []
        if top_disease:
            search_response = metaphor.search("more information about psoriasis", type="neural")
            for result in search_response.results:
                metaphor_results.append({
                    "title": result.title,
                    "url": result.url,
                    "published_date": result.published_date
                })

        return render_template('analysis.html', results=predictions, metaphor_results=metaphor_results)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
