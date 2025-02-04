import joblib
import re
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import json
from database_query import search_for_job_titles, conn,search_for_job_titles_abbreviation,search_for_job_titles_with_ofo_code,search_for_job_titles_for_model
import ast
# Preprocess function for cleaning text
def preprocess_text(text):
    if isinstance(text, str):  # Only process if the input is a string
        # Lowercase, remove special characters and numbers
        text = text.lower()
        text = re.sub(r'\d+', '', text)  # Remove digits
        text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
        text = text.strip()  # Remove leading/trailing whitespace
        return text
    else:
        return ""

# Load the saved TF-IDF model and matrix
loaded_tfidf = joblib.load('tfidf_vectorizer.pkl')
tfidf_matrix = joblib.load('tfidf_matrix.pkl')

# Load your job data DataFrame
df = pd.read_csv('job_data_with_tfidf.csv')

# Function to find similar job titles
def find_similar_jobs(input_titles, top_n=5):
    similar_jobs_results = []

    for title in input_titles:
        # Preprocess the input job title
        input_job_title_cleaned = preprocess_text(title)

        # Transform the input job title using the loaded TF-IDF model
        input_tfidf = loaded_tfidf.transform([input_job_title_cleaned])

        # Calculate cosine similarity between the input and all job titles
        cosine_similarities = cosine_similarity(input_tfidf, tfidf_matrix).flatten()

        # Get the top N most similar job titles
        similar_indices = cosine_similarities.argsort()[-top_n:][::-1]

        # Fetch the relevant job titles and their similarity scores
        similar_jobs = df.iloc[similar_indices]
        similarity_scores = cosine_similarities[similar_indices]

        # Create a DataFrame to return the results
        result_df = pd.DataFrame({
            'job_title': similar_jobs['Job_Title'],
            'job_description': similar_jobs['Job_Description'],
            'similarity_score': similarity_scores
        })

        similar_jobs_results.append(result_df)

    return similar_jobs_results

# Function to load data from model and print job titles and similarity scores
def load_data_from_model(title):
    new_job_titles = [title]
    similar_jobs_list = find_similar_jobs(new_job_titles, top_n=5)

    # Iterate over the results and print the job titles and scores
    for i, title in enumerate(new_job_titles):  # Unpacking index and title
        print(f"\nSimilar jobs for '{title}':")

        # Use the index `i` to access `similar_jobs_list`
        similar_jobs_df = similar_jobs_list[i]

        # Loop through each similar job and print the job title and score
        for index, row in similar_jobs_df.iterrows():
            job_title = row['job_title']
            score = row['similarity_score']
            #print(f"Job Title: {job_title}, Similarity Score: {score}")

        # Return DataFrame with job titles and scores
        return similar_jobs_df[['job_title', 'similarity_score']]

# Function to filter and return suggestions or search results
def filtering(search_term):
    results = search_for_job_titles(conn, search_term)
    if results:
        for item in results:
            output=search_for_job_titles_with_ofo_code(conn,item['ofo_code'])
            if output:
                if item['source']=='occupation':
                    item["specialization"]=output
                else:
                    item=output
                
        # If the title is found in the database, return the results as JSON
        return json.dumps(results)
    else:
        # Invoke the model to check for similar job titles
        result = {}
        output = []
        print("model ",load_data_from_model(search_term).values)
        # Load similar jobs from the model
        for job_title, score in load_data_from_model(search_term).values:
            clean_title = re.sub(r'^[\w\.\d]+\s*-\s*', '', job_title)  # Remove any leading numbers and dash (-)
            result[clean_title]=score
        
        #max_key, max_value = max(result.items(), key=lambda x: x[1]) if result else (None, 0.0)
            if all(score == 0 for score in result.values()):
                result = {}
        # Return the result based on whether max_value is greater than 0
        #result = {max_key: max_value} if max_value > 0 else {}
            
        
        if result:
            
            item=list(result.keys())
            
            #for items in item:
            #eg output {'Political Party Representative': 0.3080871566699519}
            #get the key 'Political Party Representative'
                
            print("Similar title: ", item)
                # Search for the similar job titles in the database
            My_results = search_for_job_titles_for_model(conn, item)
            print("my ",My_results)
            if My_results:
                for item in My_results:
                    output=search_for_job_titles_with_ofo_code(conn,item['ofo_code'])
                    if output:
                        if item['source']=='occupation':
                            item["specialization"]=output
                        else:
                            item=output   # Return the final suggestions or results
                print("my ",My_results)
                return json.dumps(My_results)
                
            else:
                message={"message":"no match found"}
                return json.dumps(message)



def filtering_abb(search_term):
    results = search_for_job_titles_abbreviation(conn, search_term)
    
    for item in results:
        output=search_for_job_titles_with_ofo_code(conn,item['ofo_code'])
        if output:
            if output:
                if item['source']=='occupation':
                    item["specialization"]=output
                else:
                    item=output
    if results:
        # If the title is found in the database, return the results as JSON
        return json.dumps(results)
    else:
        # Invoke the model to check for similar job titles
        result = {}
        
        # Load similar jobs from the model
        for job_title, score in load_data_from_model(search_term).values:
            clean_title = re.sub(r'^[\w\.\d]+\s*-\s*', '', job_title)  # Remove any leading numbers and dash (-)
            result[clean_title]=score
        
        
            if all(score == 0 for score in result.values()):
                result = {}
        # Return the result based on whether max_value is greater than 0
       
            
        
        if result:
            
            for items in result:
            #eg output {'Political Party Representative': 0.3080871566699519}
            #get the key 'Political Party Representative'
                
                print("Similar title: ", items)
                # Search for the similar job titles in the database
                My_results = search_for_job_titles(conn, items)
               
                if My_results:
                    # Return the final suggestions or results
                    
                    return json.dumps(My_results)
            else:
                message=["no match found"]
                return message
