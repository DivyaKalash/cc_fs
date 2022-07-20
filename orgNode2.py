import datetime
import hashlib
import json
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin

import requests
from urllib.parse import urlparse


class BlockVote:
    def __init__(self):
        self.hashList = [None]*100
        # self.data = []
        self.credit = 1000
        self.calculated_credit = 0
        self.credit_used = 0
        self.create_file()
        # self.nodes = set()


    def create_file(self):
        # block = {
        #     "index": len(self.chain) + 1,
        #     "timestamp": str(datetime.datetime.now()),
        #     "proof": proof,
        #     "alloted_credit": self.credit,
        #     "calculated_credit": self.calculated_credit,
        #     "credit_used": self.credit_used,
        #     "available_credit": self.credit - self.credit_used,
        #     "previous_hash": previous_hash,
        #     "data": self.data
        # }
        f = open("org.txt", "w")
        for i in range(100):
            f.write("None\n")
        # self.data = []
        self.calculated_credit = 0
        # self.chain.append(block)
        # return block

    def hash(self, x):
        return x % 10
    def quad_hash(self,x):

        for i in range(100):
            if(self.hashList[(hash(x) + i*i)%100] == None):
                return ((hash(x) + i*i)%100)



    def add_data(self, org_id, co2, ch4, n2o, hfc, pfc, sf6, date):

        self.calculated_credit = (float(co2) + (25 * float(ch4)) + (298 * float(n2o)) + (1430 * float(hfc)) + (7390 * float(pfc)) + (22800 * float(sf6)))/1000
        self.credit_used += self.calculated_credit
        # self.data.append(
        #     {
        #         "org_id": org_id,
        #         "c02": co2,
        #         "ch4": ch4,
        #         "n20": n2o,
        #         "hfc": hfc,
        #         "pfc": pfc,
        #         "sf6": sf6,
        #         "alloted_credit": self.credit,
        #         "calculated_credit": self.calculated_credit,
        #         "credit_used": self.credit_used,
        #         "available_credit": self.credit - self.credit_used,
        #         "date": date
        #
        #     }
        # )
        # previous_block = self.get_previous_block()
        # return previous_block["index"] + 1

        id = int(org_id,16)
        index = self.quad_hash(id)
        # lines = [None]*100;
        b = org_id+"|"+co2+"|"+ch4+"|"+n2o+"|"+hfc+"|"+pfc+"|"+sf6+"|"+date+"|\n"
        # lines[index] = b
        with open("org.txt", "r") as file:
            lines = file.readlines()
        lines[index] = b
        with open("org.txt","w")as file:
            file.writelines(lines)
        self.hashList[index]="occupied"
        return index;













    def org_transaction(self, org_id):
        org_trans = []
        with open("org.txt", "r") as file:
            lines = file.readlines()
        print(lines[0])
        for i in range(len(lines)-1):
            line = lines[i].split("|")
            print(lines[i])
            org_idd = line[0]

            if(org_id == org_idd):
                co2 = line[1]
                ch4 = line[2]
                n2o = line[3]
                hfc = line[4]
                pfc = line[5]
                sf6 = line[6]
                date = line[7]
                temp = {"org_id": org_idd,"co2":co2,"ch4": ch4, "n2o": n2o, "hfc": hfc, "pfc": pfc, "sf6": sf6,"date": date}
                org_trans.append(temp)
        return org_trans



        # for block in range(len(self.chain)-1):
        #     if (self.chain[block+1]["data"][0]["org_id"]) == org_id:
        #         org_trans.append(self.chain[block+1]["data"][0])
        # return org_trans



app = Flask(__name__)
CORS(app)
# node_address = str(uuid4()).replace("-", "")

blockvote = BlockVote()





@app.route("/get_creditData", methods=["GET"])
def get_creditData():
    response = {
        "alloted_credit": blockvote.credit,
        "credit_used": blockvote.credit_used,
        "available_credit": blockvote.credit - blockvote.credit_used
    }
    return jsonify(response), 200







@app.route("/add_data", methods=["POST"])
def add_data():
    json = request.get_json()
    data_keys = ["org_id", "co2", "ch4", "n2o", "hfc", "pfc", "sf6", "date"]
    if not all(key in json for key in data_keys):
        return "Elements are missing", 400
    index = blockvote.add_data(json["org_id"], json["co2"], json["ch4"], json["n2o"], json["hfc"], json["pfc"], json["sf6"], json["date"])
    response = {"message": f"This data is added to file at line {index}"}
    return jsonify(response), 201


@app.route("/get_orgTrans", methods=["POST"])
def get_orgTrans():
    json = request.get_json()
    transactions = blockvote.org_transaction(json["org_id"])
    response = {"transactions": transactions}
    return jsonify(response), 201









app.run(host="0.0.0.0", port=2708)