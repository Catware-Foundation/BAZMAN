
import sys, os, time

import pickle
from flask import Flask, Request, redirect, send_from_directory, request
from flask_cors import CORS
import markovify
import json

Ff = open("catenv.py", 'r', encoding='UTF-8')
__catenv__ = Ff.read()
exec(__catenv__)
Ff.close()
del Ff

syslog = []
syscolors = {
"lightgray": "37",
"default": "39",
"blue": "34",
"green": "32",
"cyan": "36",
"yellow": "93"
}

l(" >>> Initalizing Flask...")
app = Flask(__name__)
l(" >>> Initializing CORS...")
CORS(app)

configuration = {}
l("Loading configuration...")
for x in os.listdir("conf"):
    configuration = {**configuration, **json.loads(readff(f"conf/{x}"))}
    l(f" * Loaded: {x}")

bases = []
l("Loading bases...")
for x in configuration["bases"]:
    l(
f""" Loading: {x["name"]}
 ---------------------------------->
 {x["description"]}
 ---------------------------------->
 Author: {x['author']}
 Path: {x['path']}
 Detecting serialized shot...
"""
    )
    if os.listdir(f"{x['path']}/serial") != []:
        l("Found Pickle Shot. Deserializing...")
        bases.append(
  {**x,
  "object": deserialize(f"{x['path']}/serial/base.pickle")}
)
    else:
        buff = ''
        l("NO PICKLES?\nGenerating the base...")
        for y in os.listdir(f"{x['path']}/source"):
             buff += readff(f"{x['path']}/source/{y}")
        base = markovify.Text(buff)
        del buff
        serialize(f"{x['path']}/serial/base.pickle", base)
        bases.append(
        {**x,
        "object": base}
        )
        del base

@app.route("/<path:path>")
def index(path):
    print(f"path = [{path}]", file=sys.stdout)
    if path == "":
        path = "index.html"
        return send_from_directory('web', "index.html")
    else:
        return send_from_directory('web', path)

@app.route("/")
def index_np():
    return send_from_directory('web', "index.html")

@app.route("/bases")
def getbases():
    return json.dumps(configuration["bases"])

@app.route("/gen")
def gener():
    try:
        num = int(request.args.get('num'))
    except:
        return "No ?num=index provided."
    while True:
        text = bases[num]["object"].make_sentence()
        if text != None:
            return text

@app.route("/bmd")
def bmd():
    return 'BAZMAN SERVER #1211'

def main():
    l("Running server...")
    app.run("0.0.0.0", port=1211)

if __name__ == "__main__":
    main()
