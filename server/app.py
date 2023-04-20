# flask app
import os
import json
from flask import Flask, request, jsonify, send_from_directory
import datetime


app = Flask(__name__)

@app.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = "Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With"
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    return response


# route to get all conversationss name and id
@app.route('/conversations', methods=['GET'])
def get_conversations():
    res = []
    # go through all json files in the data folder
    for file in os.listdir("data"):
        # open the file
        with open("data/" + file, "r") as f:
            # convert the json to a python dictionary
            data = json.load(f)
            # get the conversation id and name
            conversation_id = data["conversation_id"]
            conversation_name = data["conversation_name"]
            # append the conversation id and name to the response
            res.append({"id": conversation_id, "name": conversation_name})
    # sort the response by the conversation id
    res.sort(key=lambda x: x["id"])
    # return the response
    return jsonify(res), 200


# route to get conversation by id
@app.route('/conversation/<id>', methods=['GET'])
def get_conversation(id):
    # go through all json files in the data folder
    for file in os.listdir("data"):
        # if the file name matches the id
        if file == id + ".json":
            # open the file
            with open("data/" + file, "r") as f:
                # convert the json to a python dictionary
                data = json.load(f)
                conversation = data["conversation"]
                conversation_name = data["conversation_name"]
                # return the conversation
                return jsonify({
                    "id": id,
                    "conversation": conversation,
                    "name": conversation_name
                }), 200
    # if the id is not found
    return jsonify({"error": "conversation not found"}), 404


# route to create a new conversation
@app.route('/conversation', methods=['POST'])
def create_conversation():
    # get the conversation from the request
    conversation_name = request.get_json()
    # create a new id
    id = len(os.listdir("data"))
    # create a new file with the id
    with open("data/" + str(id) + ".json", "w") as f:
        # write the conversation to the file
        json.dump({"conversation_id": id,
                   "conversation_name": conversation_name,
                   "conversation": []}, f, indent=4, ensure_ascii=False)
    # return the id
    return jsonify({"id": id}), 201


# route to update conversation by id
@app.route('/conversation/<id>', methods=['PUT'])
def update_conversation(id):
    # get the conversation from the request
    conversation = request.get_json()
    # go through all json files in the data folder
    for file in os.listdir("data"):
        # if the file name matches the id
        if file == id + ".json":
            # open the file
            with open("data/" + file, "r") as f:
                # get the data
                data = json.load(f)
                # update the conversation
                data["conversation"] = conversation
            with open("data/" + file, "w") as f:
                # write the data to the file
                json.dump(data, f, indent=4, ensure_ascii=False)
            # return the id
            return jsonify({"id": id}), 200
    # if the id is not found
    return jsonify({"error": "conversation not found"}), 404


# route to change the name of a conversation by id
@app.route('/conversation/<id>/name', methods=['PUT'])
def update_conversation_name(id):
    # get the conversation name from the request
    conversation_name = request.get_json()
    # go through all json files in the data folder
    for file in os.listdir("data"):
        # if the file name matches the id
        if file == id + ".json":
            # open the file
            with open("data/" + file, "w") as f:
                # get the data
                data = json.load(f)
                # update the conversation name
                data["conversation_name"] = conversation_name
                # write the data to the file
                json.dump(data, f, indent=4, ensure_ascii=False)
            # return the id
            return jsonify({"id": id}), 200
    # if the id is not found
    return jsonify({"error": "conversation not found"}), 404


# route to delete conversation by id
@app.route('/conversation/<id>', methods=['DELETE'])
def delete_conversation(id):
    # go through all json files in the data folder
    for file in os.listdir("data"):
        # if the file name matches the id
        if file == id + ".json":
            # delete the file
            os.remove("data/" + file)
            # rename all files after the deleted file
            for file in os.listdir("data"):
                # get the file name
                file_name = file.split(".")[0]
                # if the file name is greater than the id
                if int(file_name) > int(id):
                    # rename the file
                    os.rename("data/" + file, "data/" + str(int(file_name) - 1) + ".json")
            # return the id
            return jsonify({"id": id}), 200
    # if the id is not found
    return jsonify({"error": "conversation not found"}), 404


# route to download conversation by id
@app.route('/conversation/<id>/download', methods=['GET'])
def download_conversation(id):
    # go through all json files in the data folder
    for file in os.listdir("data"):
        # if the file name matches the id
        if file == id + ".json":
            # send the file
            return send_from_directory("data", file, as_attachment=True)
    # if the id is not found
    return jsonify({"error": "conversation not found"}), 404

if __name__ == "__main__":
    app.run(port=5000, debug=True)