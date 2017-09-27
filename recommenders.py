import numpy as np
import pandas


# Class for Popularity Recommender System 
class popular_recommendation():
    def __init__(self):
        self.user_id = None
        self.train_data = None
        self.article_id = None
        self.popularity_recommendations = None       
    

# Create the popularity recommender system
    def create(self, train_data, user_id, article_id):
        self.train_data = train_data
        self.user_id = user_id
        self.article_id = article_id
        # find a count of user_ids for each unique article as recommendation score
        train_data_grouped = train_data.groupby([self.article_id]).agg({self.user_id: 'count'}).reset_index()
        train_data_grouped.rename(columns = {'users_name': 'Ratings'},inplace=True)
        # Sort the articles based upon recommendation score
        train_data_sort = train_data_grouped.sort_values(['Ratings', self.article_id], ascending = [0,1])
        # finding a recommendation rank based upon score
        train_data_sort['Rank'] = train_data_sort['Ratings'].rank(ascending=0, method='first')
        # find the top 10 recommendations
        self.popularity_recommendations = train_data_sort.head(10)
    
# Use the popularity based recommender system model to make recommendations
    def recommend(self, user_id):   
        user_recommendations = self.popularity_recommendations
        # Add user_id column for which the recommendations are being findingd
        user_recommendations['user_id'] = user_id
        # Bring user_id column to the front    
        cols = user_recommendations.columns.tolist()
        cols = cols[-1:] + cols[:-1]
        user_recommendations = user_recommendations[cols]
        return user_recommendations
