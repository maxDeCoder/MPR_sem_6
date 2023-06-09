from flask import Flask, jsonify, redirect, render_template, request, url_for
from modules import STT, get_summary, annotate, clean_annotations, create_nodes, get_ents
import os
import json
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    print("uploading file")
    print(request.files)
    file = request.files['file']
    file.save("./generated/test.mp3")
    print("uploaded")
    return redirect(url_for("uploaded"))
        # return render_template("summary.html")
 
@app.route("/uploaded")
def uploaded():
    return render_template("summary.html")

@app.route("/process/<filename>")
def process(filename):
    print("processing")
    text = STT(f"./generated/{filename}")
    summary = get_summary(text)
    nodes = create_nodes(clean_annotations(annotate(summary)))
    json_output = open("temp.json", "w")
    json.dump(nodes, json_output, indent=4)
    json_output.close()
    
    print("summary: ", summary)
    
    return jsonify({
        "Summary": summary
    })

@app.route("/tree")
def tree():
    input_file = open("temp.json", "r")
    data = json.load(input_file)

    return jsonify(data)

if __name__=='__main__':
    app.run(debug=False, port=8000)