from flask import request, jsonify, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.service.photo_service import PhotosService

photos_Blueprint = Blueprint("photos_Blueprint", __name__)


@photos_Blueprint.record
def init_photos_blueprint(state):

    photos_Blueprint.photos = PhotosService()


@photos_Blueprint.route("/add", methods=["POST"])
@jwt_required()
def add_photo():
    """
    Add Photo
    ---
    tags:
      - Photos
    summary: "Add a new photo for the authenticated user"
    description: "Allows an authenticated user to upload a new photo with optional description."
    parameters:
      - name: user_id
        in: query
        type: string
        required: true
        description: ID of the user (JWT token)
      - name: photo_url
        in: query
        type: string
        required: true
        description: Photo url
      - name: description
        in: query
        type: string
        required: false
        description: Photo description
    responses:
      200:
        description: "Photo added successfully"
        content:
          application/json:
            schema:
              type: object
              properties:
                msg:
                  type: string
                  example: "Photo added successfully"
                photo_id:
                  type: string
                  description: "The ID of the newly created photo."
      400:
        description: "Invalid request data"
        content:
          application/json:
            schema:
              type: object
              properties:
                msg:
                  type: string
                  example: "Missing data"
      401:
        description: "Unauthorized, JWT required"
    """
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    user_id = get_jwt_identity()
    photo_url = request.json.get("photo_url")
    description = request.json.get("description")

    if not photo_url:
        return jsonify({"msg": "Missing data"}), 400

    if type(photo_url) != str or (type(description) != str and description != None):
        return jsonify({"msg": "Incorrect data type detected"}), 400

    photo_id = photos_Blueprint.photos.insert_photo(user_id, photo_url, description)
    if not photo_id:
        return jsonify({"msg": "Error, try later"}), 400

    return (
        jsonify({"msg": "Photo added successfully", "photo_id": photo_id}),
        200,
    )


@photos_Blueprint.route("/delete/<string:photo_id>", methods=["DELETE"])
@jwt_required()
def delete_photo(photo_id):
    """
    Delete Photo
    ---
    tags:
      - Photos
    summary: "Delete a photo by ID"
    description: "Deletes a photo owned by the authenticated user, based on the provided photo ID."
    parameters:
      - name: user_id
        in: query
        type: string
        required: true
        description: ID of the user to be deleted (JWT token)
      - name: photo_id
        in: path
        type: string
        required: true
        description: Photo id
    responses:
      200:
        description: "Photo deleted successfully"
        content:
          application/json:
            schema:
              type: object
              properties:
                msg:
                  type: string
                  example: "Delete successful"
      400:
        description: "Photo could not be deleted"
        content:
          application/json:
            schema:
              type: object
              properties:
                msg:
                  type: string
                  example: "Delete not successful"
      404:
        description: "Photo not found"
        content:
          application/json:
            schema:
              type: object
              properties:
                msg:
                  type: string
                  example: "Photo not found"
      401:
        description: "Unauthorized, JWT required"
    """
    photo = photos_Blueprint.photos.get_photo_by_id(photo_id)
    if not photo:
        return jsonify({"msg": "Photo not found"}), 404

    if photos_Blueprint.photos.delete_photo(photo):
        return jsonify({"msg": "Delete successful"}), 200
    else:
        return jsonify({"msg": "Delete not successful"}), 400
