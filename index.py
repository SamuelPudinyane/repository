from flask import Flask
from model import filtering
from flask import jsonify, request,render_template
from trees import create_tree
import json
from database_query import search_for_job_codes,all_from_major_table,all_from_sub_major_table

app = Flask(__name__)


@app.route('/')
def index():
    

    return render_template('index.html')
@app.route('/major')
def major():
    major=all_from_major_table()
    print(major)
    return major

@app.route('/another-endpoint/<int:major_id>')
def sub_major(major_id):
    id=major_id
    sub_major=search_for_job_codes(id)
    print(sub_major)
    return jsonify(sub_major)

@app.route("/job_title/<job_title>")
def input_job_title(job_title):
    # Call the filtering function with the job_title
    job_titles = filtering(job_title)
    print(job_titles)
    if job_titles:
        job_titles=create_tree(job_titles)
    
        return job_titles
    else:
        message=["no match found, use job description as alternative search term"]
        return message


@app.route('/suggestions')
def search():
    query = request.args.get('q', '').lower()  
   
    if not query:
        return jsonify([])

    job_titles = filtering(query)
    print(job_titles)
    if job_titles:
        job_titles=create_tree(job_titles)
    
        return job_titles
    else:
        message=["no match found, use job description as alternative search term"]
        return message


@app.route('/parent', methods=['POST'])
def check_children():
    data = request.get_json()  # Get the JSON data from the request
    search_id = data.get('search_term', '')  
    matching_titles = search_for_job_codes(search_id)
    
    # print(matching_titles)
    return jsonify(matching_titles),200

    




            

if __name__ == '__main__':
    app.run(debug=True)
