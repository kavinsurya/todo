import helper
from flask import Flask, request, Response, render_template
import json

app = Flask(__name__)

@app.route('/')
def hello_world():
   return render_template("index.html")

@app.route('/item/new', methods = ['POST'])
def add_item():
   #Get item from the POST body
#    print(request.data)
   req_data = request.form
   item = req_data['item']
   
   #Add item to the list
   res_data = helper.add_to_list(item)

   #Return error if item not added
   if res_data is None:
      response = Response("{'error': 'Item not added - '}"  + item, status=400 , mimetype='application/json')
      return response
   
   #Return response
   response = Response(json.dumps(res_data), mimetype='application/json')
   
   return response

@app.route('/items/all')
def get_all_items():
   # Get items from the helper
   res_data = helper.get_all_items()
   #Return response
   response = Response(json.dumps(res_data), mimetype='application/json')
   return response

@app.route('/item/status', methods=['GET'])
def get_item():
   #Get parameter from the URL
   item_name = request.args.get('name')
   
   # Get items from the helper
   status = helper.get_item(item_name)
   
   #Return 404 if item not found
   if status is None:
      response = Response("{'error': 'Item Not Found - '}"  + item_name, status=404 , mimetype='application/json')
      return response

   #Return status
   res_data = {
      'status': status
   }

   response = Response(json.dumps(res_data), status=200, mimetype='application/json')
   return response

@app.route('/item/update', methods = ['PUT'])
def update_status():
   #Get item from the POST body
   req_data = request.get_json()
   item = req_data['item']
   status = req_data['status']
   
   #Update item in the list
   res_data = helper.update_status(item, status)
   if res_data is None:
      response = Response("{'error': 'Error updating item - '" + item + ", " + status   +  "}", status=400 , mimetype='application/json')
      return response
   
   #Return response
   response = Response(json.dumps(res_data), mimetype='application/json')
   
   return response

@app.route('/item/remove', methods = ['POST'])
def delete_item():
   #Get item from the POST body
   req_data = request.form
   item = req_data['item']
   
   #Delete item from the list
   res_data = helper.delete_item(item)
   if res_data is None:
      response = Response("{'error': 'Error deleting item - '" + item +  "}", status=400 , mimetype='application/json')
      return response
   
   #Return response
   response = Response(json.dumps(res_data), mimetype='application/json')
   
   return response

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)