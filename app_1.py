# pip install flask
from flask import Flask, jsonify, request , make_response
import uuid

app= Flask(__name__)

businesses = [
    {
        "id":1,
        "name":"costa",
        "town":"London",
        "rating":4,
        "review":[]  
    },

    {
        "id":2,
        "name":"Pret",
        "town":"Brum",
        "rating":3,
        "review":[]  
    },

    {
        "id":3,
        "name":"YSP",
        "town":"Milton Keynes",
        "rating":5,
        "review":[]  
    },

]

@app.route('/business', methods=['Get'])
def welcome():
    return jsonify({"message":"Welcome to Businesses."})

@app.route('/all', methods=['Get'])
def getAllbusinesses():
    return jsonify({"Businesses": businesses})

@app.route('/api/get/one/business/<int:biz_id>', methods=['Get'])
def getOneBusiness(biz_id):
    for biz in businesses:
        if biz["id"] == biz_id:
            return make_response (jsonify(biz), 200)
        else:
            return make_response (jsonify({"Error":"No Business Found"}), 404)
        
@app.route('/business', methods=['POST'])
def addBusiness():
    data = request.get_json()

    new_business = {

        "id":str(uuid.uuid4()),
        "name":data["name"],
        "town":data["town"],
        "rating":data.get("rating",5),
        "review":[]

    }
    businesses.append(new_business)
    return make_response(jsonify(new_business),200)

@app.route('/business/<int:biz_id>', methods=['DELETE'])
def deleteBusiness(biz_id):
    for biz in businesses:
        if biz["id"] == biz_id:
            businesses.remove(biz)
        return make_response(jsonify({"error":"Business removed"}),200)
    return make_response(jsonify({"error":"business not found"}),404)
    

if __name__ == '__main__':
     app.run(debug=True)
