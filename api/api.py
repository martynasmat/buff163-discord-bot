from flask import Flask, jsonify, request
from flask_restful import Resource, Api, reqparse
from add_queries import add_item
from flask_cors import CORS

app = Flask("BuffSniper")
api = Api(app)

parser = reqparse.RequestParser()
CORS(app, support_credentials=True)


@app.route('/add-item', methods=['POST'])
def post():
        json_response = request.get_json()
        print(json_response)

        if str(json_response['mode']) == '':
            return 'kazkas blogai su mode arg', 406

        if str(json_response['arg']) == '':
            return 'kazkas blogai su arg arg', 406

        # if str(json_response['float']) == '':
        #     return 'kazkas blogai su float arg', 406
        #
        # if str(json_response['pattern']) == '':
        #     return 'kazkas blogai su pattern arg', 406

        if str(json_response['discord_id']) == '':
            return 'kazkas blogai su discord_id arg', 406

        if str(json_response['margin']) == '':
            return 'kazkas blogai su margin arg', 406

        add_item(json_response['mode'], json_response['arg'],
                 json_response['float'], json_response['pattern'],
                 json_response['discord_id'], json_response['margin'])
        return json_response, 201


if __name__ == "__main__":
  app.run(debug=True)