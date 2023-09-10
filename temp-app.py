from flask import Flask, render_template, request, redirect, url_for
from rf_crossval_severness import get_severeness

app = Flask(__name__)

from werkzeug.utils import secure_filename

# Set up an upload folder within your project directory
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    if request.method == 'POST':
        # Extract the data from the form into the dictionary
        data = {
            'erythema': request.form['erythema'],
            'scaling': request.form['scaling'],
            'definite_borders': request.form['definite_borders'],
            'itching': request.form['itching'],
            'koebner_phenomenon': request.form['koebner_phenomenon'],
            'polygonal_papules': request.form['polygonal_papules'],
            'follicular_papules': request.form['follicular_papules'],
            'oral_mucosal_involvement': request.form['oral_mucosal_involvement'],
            'knee_and_elbow_involvement': request.form['knee_and_elbow_involvement'],
            'scalp_involvement': request.form['scalp_involvement'],
            'family_history': request.form['family_history'],
            'melanin_incontinence': request.form['melanin_incontinence'],
            'eosinophils_infiltrate': request.form['eosinophils_infiltrate'],
            'PNL_infiltrate': request.form['PNL_infiltrate'],
            'fibrosis_papillary_dermis': request.form['fibrosis_papillary_dermis'],
            'exocytosis': request.form['exocytosis'],
            'acanthosis': request.form['acanthosis'],
            'hyperkeratosis': request.form['hyperkeratosis'],
            'parakeratosis': request.form['parakeratosis'],
            'clubbing_rete_ridges': request.form['clubbing_rete_ridges'],
            'elongation_rete_ridges': request.form['elongation_rete_ridges'],
            'thinning_suprapapillary_epidermis': request.form['thinning_suprapapillary_epidermis'],
            'spongiform_pustule': request.form['spongiform_pustule'],
            'munro_microabcess': request.form['munro_microabcess'],
            'focal_hypergranulosis': request.form['focal_hypergranulosis'],
            'disappearance_granular_layer': request.form['disappearance_granular_layer'],
            'vacuolisation_damage_basal_layer': request.form['vacuolisation_damage_basal_layer'],
            'spongiosis': request.form['spongiosis'],
            'saw_tooth_appearance_retes': request.form['saw_tooth_appearance_retes'],
            'follicular_horn_plug': request.form['follicular_horn_plug'],
            'perifollicular_parakeratosis': request.form['perifollicular_parakeratosis'],
            'inflammatory_mononuclear_infiltrate': request.form['inflammatory_mononuclear_infiltrate'],
            'band_like_infiltrate': request.form['band_like_infiltrate'],
            'age': request.form['age']
        }
        
        # Convert string inputs to integers
        for key, value in data.items():
            data[key] = int(value)

        # Get prediction using the model
        pred = get_severeness(data)

        return render_template('result.html', prediction=pred[0])
    return redirect(url_for('severity.html'))

if __name__ == '__main__':
    app.run(debug=True)