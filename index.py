from flask import Flask
from model import filtering,filtering_abb
from flask import jsonify, request,render_template
import json
from database_query import search_for_job_codes
import ast
from database_query import get_connection
print("connection ", get_connection())
app = Flask(__name__)


@app.route('/')
def index():
    
    return render_template('index.html')

@app.route("/job_title/<job_title>")
def input_job_title(job_title): 
    # Call the filtering function with the job_title
    if not job_title:
        return jsonify([])
    if len(job_title)<3:

        job_titles=filtering_abb(job_title)
    else:
        job_titles = filtering(job_title)
    
    if job_titles and "message" not in job_titles:
        job_titles=ast.literal_eval(job_titles)
        for item in job_titles:
        #job_titles=create_tree(job_titles)
            firstelement=list(item.keys())[0]
            item.pop(firstelement)
            
        return job_titles
    else:
        message={"message":"no match found, use job description as alternative search term"}
        return message


@app.route('/suggestions')
def search():
    query = request.args.get('q', '').lower()  
   
    if not query:
        return jsonify([])
    if len(query)>2:
        job_titles = filtering(query)
    else:
        job_titles=filtering_abb(query)
 
    if job_titles:
        #job_titles=create_tree(job_titles)
        return job_titles
    else:
        message={"message":"no match found, use job description as alternative search term"}
        return message


            

if __name__ == '__main__':
    app.run()
