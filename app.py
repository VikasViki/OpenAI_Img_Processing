import os
import shutil
from flask import Flask, jsonify, request, send_file
from pymongo import MongoClient
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib import cm
from matplotlib.colors import Normalize

app = Flask(__name__)

# MongoDB connection details
mongo_host = "localhost"  
mongo_port = 27017       
db_name = "img_database" 
collection_name = "img_collection"

# Initialize MongoDB client
client = MongoClient(mongo_host, mongo_port)
db = client[db_name]
collection = db[collection_name]

colors = ["blue", "green", "yellow", "red"]
custom_cmap = ListedColormap(colors)

count = 0

IMAGE_RESULTS_DIR = "img_results"

def clear_directory(directory):
    if os.path.exists(directory):
        shutil.rmtree(directory)
    os.makedirs(directory)

clear_directory(IMAGE_RESULTS_DIR)

def create_numpy_array(results):
    numpy_array = []
    for image_info in results:
        numpy_array.append(list(map(int, image_info.values()))[1:])
    return np.array(numpy_array)

@app.route('/get_frames_between_depth', methods=['GET'])
def get_frames_between_depth():
    """
    Fetch records from MongoDB where depth is between min_depth and max_depth.
    """
    try:
        # Get query parameters
        min_depth = request.args.get('min_depth', type=float)
        max_depth = request.args.get('max_depth', type=float)
        
        # Validate query parameters
        if min_depth is None or max_depth is None:
            return jsonify({"error": "Both 'min_depth' and 'max_depth' parameters are required"}), 400
        
        if min_depth > max_depth:
            return jsonify({"error": "'min_depth' cannot be greater than 'max_depth'"}), 400

        # Query MongoDB for records within the depth range
        query = {
            "depth": {
                "$gte": min_depth, 
                "$lte": max_depth
                }
            }
        results = list(collection.find(query, {"_id": 0}))

        image_data_as_numpy_array = create_numpy_array(results)
        print("image_data", image_data_as_numpy_array)

        norm = Normalize(vmin=np.min(image_data_as_numpy_array), vmax=np.max(image_data_as_numpy_array))
        normalized_data = norm(image_data_as_numpy_array)

        colored_data = custom_cmap(normalized_data)
        print(image_data_as_numpy_array.shape)

        global count
        colored_image_path = f"img_results/colored_frames_{min_depth}_to_{max_depth}_{count}.png"
        plt.imsave(colored_image_path, image_data_as_numpy_array, cmap=custom_cmap)
        count += 1

        print("Image saved to results directory")

        return send_file(colored_image_path, mimetype='image/png')
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
