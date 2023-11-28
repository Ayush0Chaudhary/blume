from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app, support_credentials=True)

@app.route('/optimize', methods = ['POST','OPTIONS'])
@cross_origin(supports_credentials=True)
def optimize():
    if(request.method == 'POST'):
        data = request.get_json()
        print(data)
        return jsonify({'data': data})
    

  
  
if __name__ == '__main__': 
    app.run(debug = True)   
    # step 1 noice 