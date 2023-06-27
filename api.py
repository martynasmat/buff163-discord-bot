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
            return {"message": "kazkas blogai su mode arg"}, 406

        if str(json_response['arg']) == '':
            return {"message":"kazkas blogai su arg arg"}, 406

        # if str(json_response['float']) == '':
        #     return 'kazkas blogai su float arg', 406
        #
        # if str(json_response['pattern']) == '':
        #     return 'kazkas blogai su pattern arg', 406

        if str(json_response['discord_id']) == '':
            return {"message":"kazkas blogai su discord_id arg"}, 406

        # if str(json_response['margin']) == '':
        #     return {"message":"kazkas blogai su margin arg"}, 406

        for item in json_response['arg']:
            print(item)
            add_item(json_response['mode'], item['url'],
                     item['float'], item['pattern'],
                     json_response['discord_id'], item['margin'])

        return json_response, 201


if __name__ == "__main__":
  app.run(debug=True)