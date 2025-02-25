import pypyodbc as odbc


# Offline 
# DRIVER_NAME='SQL SERVER'
# SERVER_NAME='APB-JBS02-113L\SQLEXPRESS'
# DATABASE_NAME='database_ofo'

# online
# DRIVER_NAME='ODBC Driver 17 for SQL Server'
# SERVER_NAME='102.23.201.12\IMS'
# DATABASE_NAME='chieta_ofo'
# PASSWORD='0foAdmin123$'
# USERNAME='ofo_service'

def get_connection():
    connection_string = "DRIVER={SQL Server};SERVER=102.23.201.12\IMS;DATABASE=chieta_ofo;UID=ofo_service;PWD=0foAdmin123$;MARS_Connection=yes"

    return odbc.connect(connection_string)





def search_for_job_codes(id):
    """Search for a specific job title (case-insensitive) across multiple tables and return matching rows with all columns.
    Using %...% wildcard operation to search for any results that has the same unput title
    """
    conn=get_connection()
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
    conn=get_connection()
    """
    Search for a specific job title (case-insensitive) across multiple tables and return matching rows with all columns.
    Create a nested dictionary where entries are nested under their parent based on specialization_id relationships.
    """
    try:
        if conn:
            cursor = conn.cursor()

            # Query with equal number of columns in each SELECT
            query = """
            SELECT occupation_id AS id, occupation_id AS ofo_code, LOWER(specialization_title) AS job_title, 'specialization' AS source
            FROM specialization
            WHERE LOWER(specialization_title) LIKE LOWER(CONCAT('%', ?, '%'))
            
            UNION

            SELECT unit_id AS id, occupation_id AS ofo_code, LOWER(occupation_title) AS job_title, 'occupation' AS source
            FROM occupation
            WHERE LOWER(occupation_title) LIKE LOWER(CONCAT('%', ?, '%'))
              
               
            
            """

            # Execute the query with the lowercase title as a parameter
            cursor.execute(query, (title, title))

            # Get column names from the cursor's description attribute
            column_names = [description[0] for description in cursor.description]
            
            # Fetch all rows that match the search query
            rows = cursor.fetchall()
            
            # Create a list of dictionaries, each representing a row with column names as keys
            result = [dict(zip(column_names, row)) for row in rows]
         
            # Apply any additional processing
            results = find_word_in_job_titles(title, result) if result else []
          
            return results if results else result
        else:
            print("No valid connection.")
            return None
    except Exception as e:
        print(f"Error executing query: {e}")
        return None
    
      
def search_for_job_titles_abbreviation(conn, title):
    """
    Search for a specific job title (case-insensitive) across multiple tables and return matching rows with all columns.
    Create a nested dictionary where entries are nested under their parent based on specialization_id relationships.
    """
    conn=get_connection()
    try:
        if conn:
            cursor = conn.cursor()
            # Query with equal number of columns in each SELECT
            query = """
            
                SELECT occupation_id AS id, occupation_id AS ofo_code, LOWER(specialization_title) AS job_title, 'specialization' AS source
                FROM specialization
                WHERE (
                        LOWER(SUBSTRING(specialization_title, 1, 1)) +
                        LOWER(SUBSTRING(specialization_title, CHARINDEX(' ', specialization_title) + 1, 1)) = ?
                        AND LEN(specialization_title) > 8
                    )
                UNION ALL 
                SELECT  unit_id AS id, occupation_id AS ofo_code, LOWER(occupation_title) AS job_title, 'occupation' AS source
                        FROM occupation
                        WHERE (
                            LOWER(SUBSTRING(occupation_title, 1, 1)) +
                            LOWER(SUBSTRING(occupation_title, CHARINDEX(' ', occupation_title) + 1, 1)) = ?
                            AND LEN(occupation_title) > 8
                        )
                 
	
            """

            # Execute the query with the lowercase title as a parameter
            cursor.execute(query, [title,title])

            # Get column names from the cursor's description attribute
            column_names = [description[0] for description in cursor.description]
            
            # Fetch all rows that match the search query
            rows = cursor.fetchall()
            
            # Create a list of dictionaries, each representing a row with column names as keys
            result = [dict(zip(column_names, row)) for row in rows]
           
            # Apply any additional processing
            results = find_word_in_job_titles(title, result) if result else []
            
            return results if results else result
        else:
            print("No valid connection.")
            return None
    except Exception as e:
        print(f"Error executing query: {e}")
        return None
    





def search_for_job_titles_with_ofo_code(conn, ofo_code):
    conn=get_connection()

    try:
        if conn:
            cursor = conn.cursor()

            # Query with equal number of columns in each SELECT
            query = """
            SELECT occupation_id AS ofo_code, LOWER(specialization_title) AS job_title, 'specialization' AS source
            FROM specialization
            WHERE occupation_id =?

            UNION

            SELECT occupation_id AS ofo_code, LOWER(occupation_title) AS job_title, 'occupation' AS source
            FROM occupation
            WHERE occupation_id =?
            
            
            """

            # Execute the query with the lowercase title as a parameter
            cursor.execute(query, (ofo_code,ofo_code))

            # Get column names from the cursor's description attribute
            column_names = [description[0] for description in cursor.description]
            
            # Fetch all rows that match the search query
            rows = cursor.fetchall()
            
            # Create a list of dictionaries, each representing a row with column names as keys
            results = [dict(zip(column_names, row)) for row in rows]
           
            # Apply any additional processing
            
            
            return results if results else []
        else:
            print("No valid connection.")
            return None
    except Exception as e:
        print(f"Error executing query: {e}")
        return None
    
def search_for_job_titles_for_model(conn, title):
    print("this ",title)
    conn=get_connection()
    if type(title)==list:
        output=[]
        for item in title:
            """
            Search for a specific job title (case-insensitive) across multiple tables and return matching rows with all columns.
            Create a nested dictionary where entries are nested under their parent based on specialization_id relationships.
            """
            try:
                if conn:
                    cursor = conn.cursor()

                    # Query with equal number of columns in each SELECT
                    query = """
                    SELECT occupation_id AS id, occupation_id AS ofo_code, LOWER(specialization_title) AS job_title, 'specialization' AS source
                    FROM specialization
                    WHERE LOWER(specialization_title) LIKE LOWER(?)
                    
                    UNION

                    SELECT unit_id AS id, occupation_id AS ofo_code, LOWER(occupation_title) AS job_title, 'occupation' AS source
                    FROM occupation
                    WHERE LOWER(occupation_title) LIKE LOWER(?)

                    UNION

                    SELECT minor_id as id, unit_id as ofo_code, LOWER(unit_title) AS job_title, 'unit' AS source 
                    FROM unit 
                    WHERE LOWER(unit_title) LIKE LOWER(?)
                    
                    
                    """

                    # Execute the query with the lowercase title as a parameter
                    cursor.execute(query, (item, item,item))

                    # Get column names from the cursor's description attribute
                    column_names = [description[0] for description in cursor.description]
                    
                    # Fetch all rows that match the search query
                    rows = cursor.fetchall()
                    
                    # Create a list of dictionaries, each representing a row with column names as keys
                    result = [dict(zip(column_names, row)) for row in rows]
                    #print("my results here ",result[0])
                    if len(result)>0:
                    # Apply any additional processing
                    #results = find_word_in_job_titles(item, result) if result else []
                        output.append(result[0])
                    
                else:
                    print("No valid connection.")
                    return None
            except Exception as e:
                print(f"Error executing query: {e}")
                return None
        
        return output if output else []
    else:
            """
            Search for a specific job title (case-insensitive) across multiple tables and return matching rows with all columns.
            Create a nested dictionary where entries are nested under their parent based on specialization_id relationships.
            """
            try:
                if conn:
                    cursor = conn.cursor()

                    # Query with equal number of columns in each SELECT
                    query = """
                    SELECT occupation_id AS id, occupation_id AS ofo_code, LOWER(specialization_title) AS job_title, 'specialization' AS source
                    FROM specialization
                    WHERE LOWER(specialization_title) LIKE LOWER(?)
                    
                    UNION

                    SELECT unit_id AS id, occupation_id AS ofo_code, LOWER(occupation_title) AS job_title, 'occupation' AS source
                    FROM occupation
                    WHERE LOWER(occupation_title) LIKE LOWER(?)

                    UNION

                    SELECT minor_id as id, unit_id as ofo_code, LOWER(unit_title) AS job_title, 'unit' AS source 
                    FROM unit 
                    WHERE LOWER(unit_title) LIKE LOWER(?)
                    
                    
                    """

                    # Execute the query with the lowercase title as a parameter
                    cursor.execute(query, (title, title,title))

                    # Get column names from the cursor's description attribute
                    column_names = [description[0] for description in cursor.description]
                    
                    # Fetch all rows that match the search query
                    rows = cursor.fetchall()
                    
                    # Create a list of dictionaries, each representing a row with column names as keys
                    result = [dict(zip(column_names, row)) for row in rows]
                    
                    # Apply any additional processing
                    #results = find_word_in_job_titles(title, result) if result else []
                
                    return result if result else []
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