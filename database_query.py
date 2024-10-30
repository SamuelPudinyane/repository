import pypyodbc as odbc


DRIVER_NAME='SQL SERVER'
SERVER_NAME='APB-JBS02-113L\SQLEXPRESS'
DATABASE_NAME='database_ofo'

connection_string=F"""
    DRIVER={{{DRIVER_NAME}}};
    SERVER={SERVER_NAME};
    DATABASE={DATABASE_NAME};
    Trust_Connection=yes
"""
conn=odbc.connect(connection_string)

def all_from_major_table():
    try:
        if conn:
            cursor = conn.cursor()

            # Query with equal number of columns in each SELECT
            query = """
                SELECT * FROM major;
            """

            # Execute the query with the lowercase title as a parameter
            cursor.execute(query, )
            
            # Get column names from the cursor's description attribute
            column_names = [description[0] for description in cursor.description]
            
            # Fetch all rows that match the search query
            rows = cursor.fetchall()
            
            # Create a list of dictionaries, each representing a row with column names as keys
            result = [dict(zip(column_names, row)) for row in rows]
            # print(result)
            return result  # Return the list of dictionaries containing all columns
        else:
            print("No valid connection.")
            return None
    except Exception as e:
        print(f"Error executing query: {e}")
        return None
    
def all_from_sub_major_table():
    try:
        if conn:
            cursor = conn.cursor()

            # Query with equal number of columns in each SELECT
            query = """
                SELECT * FROM sub_major;
            """

            # Execute the query with the lowercase title as a parameter
            cursor.execute(query, )
            
            # Get column names from the cursor's description attribute
            column_names = [description[0] for description in cursor.description]
            
            # Fetch all rows that match the search query
            rows = cursor.fetchall()
            
            # Create a list of dictionaries, each representing a row with column names as keys
            result = [dict(zip(column_names, row)) for row in rows]
            # print(result)
            return result  # Return the list of dictionaries containing all columns
        else:
            print("No valid connection.")
            return None
    except Exception as e:
        print(f"Error executing query: {e}")
        return None
    


def search_for_job_codes(id):
    """Search for a specific job title (case-insensitive) across multiple tables and return matching rows with all columns.
    Using %...% wildcard operation to search for any results that has the same unput title
    """
    try:
        if conn:
            cursor = conn.cursor()

            # Query with equal number of columns in each SELECT
            query = """
                SELECT occupation_id as id,specialization_id,LOWER(specialization_title) AS job_title, 'specialization' AS source FROM specialization WHERE occupation_id =?
                
                UNION
              
                SELECT unit_id as id,occupation_id,LOWER(occupation_title) AS job_title, 'occupation' AS source FROM occupation WHERE unit_id =?
                
            """

            # Execute the query with the lowercase title as a parameter
            cursor.execute(query, (id, id))
            
            # Get column names from the cursor's description attribute
            column_names = [description[0] for description in cursor.description]
            
            # Fetch all rows that match the search query
            rows = cursor.fetchall()
            
            # Create a list of dictionaries, each representing a row with column names as keys
            result = [dict(zip(column_names, row)) for row in rows]
            # print(result)
            return result  # Return the list of dictionaries containing all columns
        else:
            print("No valid connection.")
            return None
    except Exception as e:
        print(f"Error executing query: {e}")
        return None


"""
The results obtained from the database we futher process them or if not 
results found, we invoke the tfidf (text frequent identifier) to identify job titles sharing same job description
with the list of results from the model, do the search again from the database to find if any of the job titles exists

"""

         
 
data=[]
          
def search_for_job_titles(conn, title):
    """
    Search for a specific job title (case-insensitive) across multiple tables and return matching rows with all columns.
    Create a nested dictionary where entries are nested under their parent based on specialization_id relationships.
    """
    try:
        if conn:
            cursor = conn.cursor()

            # Query with equal number of columns in each SELECT
            query = """
                SELECT occupation_id as id, specialization_id, LOWER(specialization_title) AS job_title, 'specialization' AS source FROM specialization WHERE LOWER(specialization_title) LIKE LOWER(CONCAT('%', ?, '%'))

                UNION

                SELECT unit_id as id, occupation_id, LOWER(occupation_title) AS job_title, 'occupation' AS source FROM occupation WHERE LOWER(occupation_title) LIKE LOWER(CONCAT('%', ?, '%'))

                UNION

                SELECT minor_id as id, unit_id, LOWER(unit_title) AS job_title, 'unit' AS source FROM unit WHERE LOWER(unit_title) LIKE LOWER(CONCAT('%', ?, '%'))


            """

            # Execute the query with the lowercase title as a parameter
            cursor.execute(query, (title, title, title))

            # Get column names from the cursor's description attribute
            column_names = [description[0] for description in cursor.description]
            
            # Fetch all rows that match the search query
            rows = cursor.fetchall()
            
            # Create a list of dictionaries, each representing a row with column names as keys
            result = [dict(zip(column_names, rows)) for rows in rows]
           
            # data=result
            results=find_word_in_job_titles(title, result)
            # return build_hierarchy(result)
            print(len(results))
            if len(results)==0:
                return  # Return the nested dictionary structure
            else: return results
        else:
            print("No valid connection.")
            return None
    except Exception as e:
        print(f"Error executing query: {e}")
        return None



def find_word_in_job_titles(word, data):
    # Use list comprehension to search in the 'job_title' field of each dictionary (case-insensitive)
    result = [item for item in data if word.lower() in item['job_title'].lower()]
    # Return the result list (either containing matched dictionaries or empty)
    return result if result else []



def build_hierarchy(data):
    """
    Builds a hierarchical tree structure from the given data.

    Args:
        data: A list of dictionaries representing job titles and their relationships.

    Returns:
        A nested dictionary representing the hierarchical structure.
    """

    tree = {}  # The root of the hierarchy
    parent_map = {}  # Mapping of parent IDs to their nodes

    for item in data:
        node = {
            'id': item['id'],
            'specialization_id':item['specialization_id'],
            'job_title': item['job_title'],
            'source': item['source'],
            'children': []
        }

        # Determine the parent based on the source hierarchy
        if item['source'] == 'major':
            tree[item['id']] = node
            parent_map[item['id']] = node
        elif item['source'] == 'sub_major':
            parent_id = next((child['id'] for child in item['children'] if child['source'] == 'major'), None)
            if parent_id and parent_id in parent_map:
                parent_map[parent_id]['children'].append(node)
            else:
                tree[item['id']] = node
                parent_map[item['id']] = node
        elif item['source'] == 'minor':
            parent_id = next((child['id'] for child in item['children'] if child['source'] == 'sub_major'), None)
            if parent_id and parent_id in parent_map:
                parent_map[parent_id]['children'].append(node)
            else:
                tree[item['id']] = node
                parent_map[item['id']] = node
        elif item['source'] == 'unit':
            parent_id = next((child['id'] for child in item['children'] if child['source'] == 'minor'), None)
            if parent_id and parent_id in parent_map:
                parent_map[parent_id]['children'].append(node)
            else:
                tree[item['id']] = node
                parent_map[item['id']] = node
        elif item['source'] == 'occupation':
            parent_id = next((child['id'] for child in item['children'] if child['source'] == 'unit'), None)
            if parent_id and parent_id in parent_map:
                parent_map[parent_id]['children'].append(node)
            else:
                tree[item['id']] = node
                parent_map[item['id']] = node
        elif item['source'] == 'specialization':
            parent_id = next((child['id'] for child in item['children'] if child['source'] == 'occupation'), None)
            if parent_id and parent_id in parent_map:
                parent_map[parent_id]['children'].append(node)
            else:
                tree[item['id']] = node
                parent_map[item['id']] = node

    return tree
