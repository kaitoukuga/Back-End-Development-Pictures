from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    return data, 200

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    for pic in data:
        if pic["id"] == int(id):
            return pic, 200
    return {"message":"Picture not Found"}, 404


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    new_pic = request.json
    # Validate new_pic is not duplicate
    for pic in data:
        if new_pic["id"] == pic["id"]:
            return {"Message":f"picture with id {new_pic['id']} already present"}, 302
    
    data.append(new_pic)
    return new_pic, 201


######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    new_info = request.json
    # Validate new_pic is exist
    for pic in data:
        if pic.get("id") == id:
            pic.update(new_info)
            return pic, 200
    else:
        return {"message": "picture not found"}, 404

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    for pic in data:
        if pic["id"] == id:
            data.remove(pic)
            return {"message":f"Picture of id {pic['id']} deleted"}, 204
    return {"message":"Picture not Found"}, 404
