# import necessary libraries
from flask import Flask, jsonify, render_template
import pymongo

# create instance of Flask app
app = Flask(__name__)

# create connection to server
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)
# connect to/create db
db = client.mars_db

# create a route for my landing page
@app.route("/")
def index():
	data = list(db.scraped_info.find())
	news_title_key = list(data[0].keys())[1]
	news_title_value = list(data[0].values())[1]
	news_p_value = list(data[1].values())[1]
	feat_img_url_value = list(data[2].values())[1]
	latest_tweet_value = list(data[3].values())[1]
	mars_table_facts_value = list(data[4].values())[1]
	mars_stats = []
	st_data = []
	for i in mars_table_facts_value:
	    mars_stats.append(list(mars_table_facts_value[mars_table_facts_value.index(i)].values())[0])
	    st_data.append(list(mars_table_facts_value[mars_table_facts_value.index(i)].values())[1])
	table_data = list(zip(mars_stats, st_data))
	mars_hemispheres_value = list(data[5].values())[1]
	hemi_values_list = []
	for i in mars_hemispheres_value:
	    hemi_values_list.append(i.values())
	hemi_values_list_rf = []
	img_url_src = []
	for i in list(hemi_values_list):
	    hemi_values_list_rf.append(list(hemi_values_list[hemi_values_list.index(i)]))
	for i in hemi_values_list_rf:
	    img_url_src.append(i[1])

	return render_template("index.html", news_title_key=news_title_key, news_title_value=news_title_value, news_p_value=news_p_value, feat_img_url_value=feat_img_url_value, latest_tweet_value=latest_tweet_value, mars_stats=mars_stats, st_data=st_data, table_data=table_data, img_url_src=img_url_src)

# create a route that imports my scrape function
@app.route("/scrape")
def scrape_instance():
	from scrape_mars import scrape
	scraped_data = scrape()
	keys = list(scraped_data.keys())
	values = list(scraped_data.values())
	# delete collection so as to avoid overstacking data 
	db.scraped_info.drop()
	for key in keys:
		db.scraped_info.insert_one(
			{
				key: values[keys.index(key)]
			}
		)
	return "Scrape was successful."

if __name__ == "__main__":
	app.run(debug=True)