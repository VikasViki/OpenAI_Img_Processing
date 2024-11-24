**Prerequisites:**
- Make Sure your system has below application installed if not follow the reference.
- docker installed. (Reference: https://docs.docker.com/engine/install/)
- python3.9.15 (Reference: https://www.python.org/downloads/release/python-3915/)


**Follow Below Steps To Run Application** 

- Run `docker run --name mongodb -d -p 27017:27017 mongo` from terminal.
- Run `python3 -m pip install -r requirements.txt` from image_processing directory where requirements.txt is present.
- Run `python3 load_image_data.py`.
- You can validate the image data inside mongo db by following below steps
   -  `docker exec -it mongodb mongosh`
   -  Run `use img_database` and `db.img_collection.find().pretty()`
   -  This should list all records of img.csv data.
- Run `python3 app.py` to run flask application.
- Open a new terminal and run below curl to view the frames between the given depths.
    ```
    curl "http://localhost:5000/get_frames_between_depth?min_depth=9000&max_depth=9001"`
    ```
- You can find the colored frame for the requested query inside `img_results` directory.
- This API also returns the colored image as output.

**NOTE: testing.ipynb is used for experimenting with the image data. Not relevant to solution**
