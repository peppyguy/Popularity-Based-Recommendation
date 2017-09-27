from flask.ext.api import FlaskAPI
from flask import request, current_app, abort
from functools import wraps
from flask_pymongo import PyMongo
app = FlaskAPI(__name__)
from bson import ObjectId
import json
import pandas as pd
from bson import json_util
from operator import itemgetter
import operator
import numpy as np
from flask import Flask,abort,jsonify,request
import cPickle as pickle
from flask import Flask

popularity_recommendation=pickle.load(open("pm.pkl","rb"))

app=Flask(__name__)


@app.route('/popular',methods=['POST'])
def make_predict():
    # all kind of error should go error
    data=request.get_json(force=True)
    # convert our json to numpy array
    predict_request= data['user_id']
    #item = request.data.get('')
    #if not item:
    #    return []
    #predict_request=np.array(item)
    # np aaray goes into popularity_recommendation and prediction comes out
    recom=popularity_recommendation.recommend(predict_request)
    df=pd.DataFrame(recom)
    ff=df.article_id.values
    #Gettting list of article values
    hh=[]
    for i in ff:
       hh.append(i)
    #removing the "article-" from the article list and decide the num range when the number of recommendation increases
    num=range(0,9)
    h=[]
    for i in num:
        h.append(hh[i][8:])
    #Getting the article details from mongo 
    gg=[]
    feed=mongo.db.feeds
    for u in feed.find({'feedEntity.entityId':{'$in':h}}).sort("publishDate",-1):
        gg.append(u)

    # return our prediction 
    return json.dumps({'results':gg})



app.config['MONGO_DBNAME'] = 'sodelhi'
app.config['MONGO_URI'] = 'mongodb://139.59.66.172:27017/sodelhi'

mongo = PyMongo(app)





@app.route('/')
def index():
    return "Hello World"

if __name__ == "__main__":
    app.run()
