from flask import Flask, jsonify, request
from flask_restful import Resource, Api, reqparse
from add_queries import add_item

app = Flask("BuffSniper")
api = Api(app)

parser = reqparse.RequestParser()


@app.route('/add-item', methods=['POST'])
def post():
        json_response = request.get_json()
        print(json_response)
        add_item(json_response['mode'], json_response['arg'],
                 json_response['float'], json_response['pattern'],
                 json_response['discord_id'], json_response['margin'])
        return json_response, 201


if __name__ == "__main__":
  app.run(debug=True)