from flask import Flask, request, redirect, url_for, render_template
import os
import json
import glob
import sys
import zipfile
from uuid import uuid4
import carlookup
import constants
from imgurpython import ImgurClient

app = Flask(__name__)
imgur_client = ImgurClient("9838eb2e63fe84d","d5d86cfcb9cf55a60c59cf989085892918d674a7")
@app.route("/")
def index():
    brands  = []
    for key in constants.EMISSIONS:
        brands.append(key.title())
    return render_template("index.html", brands = brands)


@app.route("/upload", methods=["POST"])
def upload():
    """Handle the upload of a file."""
    form = request.form

    # Create a unique "session ID" for this particular batch of uploads.
    upload_key = str(uuid4())

    # Target folder for these uploads.
    target = "static/uploads/{}".format(upload_key)
    try:
        os.mkdir(target)
    except  Exception as e:
        print(e)
        return "Couldn't create upload directory: {}".format(target)

    print("=== Form Data ===")
    for key, value in list(form.items()):
        print(key, "=>", value)
    try:
        car_file = request.files['car']
        destination = "/".join([target, car_file.filename])
        print("accept incoming file:", car_file.filename)
        print("save it to:", destination)
        car_file.save(destination)
        print('Saved Car File')
    except KeyError:
        print('Did not get car file')

    try:
        zip_file = request.files['zip']
        destination = "/".join([target, zip_file.filename])
        print("accept incoming file:", zip_file.filename)
        print("save it to:", destination)
        zip_file.save(destination)
    except KeyError:
        print('Did not get zip file')

    return redirect(url_for("upload_complete", uuid=upload_key))


@app.route("/files/<uuid>")
def upload_complete(uuid):
    """The location we send them to at the end of the upload."""

    # Get their files.
    root = "static/uploads/{}".format(uuid)
    if not os.path.isdir(root):
        return "Error: UUID not found!"


    zip_file = None
    carfile = None
    car_results = None
    timeline = None
    emissions = 1

    for file in glob.glob("{}/*.*".format(root)):
        fname = file.split(os.sep)[-1]
        ext = os.path.splitext(fname)[1]
        if ext == ".zip":
            zip_file = root+"/"+fname
        elif ext in [".jpg", ".jpeg", ".bmp", ".gif", ".png", ".svg", ".psd", ".raw"]:
            carfile = root+"/"+fname

    if carfile is not None:
        try:
            upload_results = imgur_client.upload_from_path(carfile, anon=True)
            print(upload_results)
            car_results = carlookup.search(upload_results["link"])
            print(car_results)
        except Exception as e:
            print("EXCEPTION : " + str(e))
            car_results = {'name' : '', 'average' : '118.1 g/km', 'range' : '118.1 g/km'}
        emissions = float(car_results['average'][:-5])

    if zip_file is not None:
        zip_ref = zipfile.ZipFile(zip_file)
        zip_ref.extractall(root)

        json_path = root +  "/Takeout/Location\ History/Location\ History.json"
        out_path = root + "/data.json"

        command = "./json-parser" + " " + json_path + " > " + out_path
        os.system(command)

        with open(root+"/data.json") as json_data:
            data = json_data.read().replace('\n', '')

        data = data[:-2] + "}"

        with open(root+"/data.json", "w") as json_data:
            json_data.write(data)

        with open(root+"/data.json") as json_data:
            timeline = json.load(json_data)
            for k, val in timeline.items():
                timeline[k]["emissions"] = int(timeline[k]["drove"]) * emissions

            timeline = [(v,k) for v,k in timeline.items()]
            timeline.sort(key=lambda x: int(x[0]))
        

    return render_template("files.html",
        uuid=uuid,
        car_results = car_results,
        timeline = timeline
    )

if __name__ == '__main__':
    flask_options = dict(
        host='0.0.0.0',
        debug=True,
        port=80,
        threaded=True,
    )

    app.run(**flask_options)

