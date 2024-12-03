import joblib
import sys
from pathlib import Path

# Add scripts directory to Python path
scripts_dir = Path(__file__).parent.parent / 'scripts'
sys.path.append(str(scripts_dir))

# Import functions from notebook files
import nbformat
from nbformat import read
from IPython import get_ipython

def load_notebook_functions(notebook_path):
    with open(notebook_path) as f:
        nb = read(f, as_version=4)
    for cell in nb.cells:
        if cell.cell_type == 'code':
            exec(cell.source, globals())

# Load functions from notebooks
load_notebook_functions(str(scripts_dir / 'preprocess.ipynb'))
load_notebook_functions(str(scripts_dir / 'train_model.ipynb'))

model = None
vectorizer = None

async def load_model():
    global model, vectorizer
    model = joblib.load('data/nearest_neighbors_model.joblib')
    vectorizer = joblib.load('data/tfidf_vectorizer.joblib')

def get_recommendations(user_input):
    if not model or not vectorizer:
        raise ValueError('Model not initialized')

    input_vector = vectorizer.transform([' '.join(user_input['preferences'])])
    distances, indices = model.kneighbors(input_vector)
    return {'recommendations': indices.flatten().tolist()}
