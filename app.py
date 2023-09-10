from flask import Flask, render_template, request, redirect, url_for
import predictor  # Assuming predictor.py is in the same directory

app = Flask(__name__)

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
        return render_template('analysis.html', results=predictions)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
