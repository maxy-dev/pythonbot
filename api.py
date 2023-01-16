import disnake as discord
import os
import datetime, time
from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from utils import RdictManager
from disnake.ext import commands

def main():
  app = Flask(__name__)
  api = Api(app)

  @app.errorhandler(404)
  def page_not_found(e):
      return "<h1>404</h1><p>The resource could not be found.</p>", 404

  class Balance(Resource):
    def get(self):
      query_parameters = request.args
      userid = query_parameters.get("userid")
      
      with RdictManager(str("./database")) as db:
        if userid:
          return db["balance"][str(userid)] if str(userid) in db["balance"] else ({"message": "The user could not be found.", "status": 404}, 404)
        else:
          return db["balance"]
        
  class Inventory(Resource):
    def get(self):
      query_parameters = request.args
      userid = query_parameters.get("userid")
      with RdictManager(str("./database")) as db:
        if userid:
          return db["inventory"][str(userid)] if str(userid) in db["inventory"] else ({"message": "The user could not be found.", "status": 404}, 404)
        else:
          return db["inventory"]

  api.add_resource(Balance, "/api/balance")
  api.add_resource(Inventory, "/api/inventory")
  
  app.run()

if __name__ == "__main__":
  main()