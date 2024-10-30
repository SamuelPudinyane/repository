import json

class Node:
    """
    Class Node to represent each job entry in the hierarchy.
    """
    def __init__(self, value):
        self.data = value  # This will store the job data
        self.children = []  # To hold hierarchical children

class Tree:
    """
    Tree class to manage the hierarchical structure of job titles.
    """
    def createNode(self, data):
        """
        Create a new node with the given job data.
        """
        return Node(data)

    def find_parent(self, root, parent_source):
        """
        Find the parent node based on the source hierarchy.
        """
        if root is None:
            return None
        if root.data['source'] == parent_source:
            return root
        for child in root.children:
            parent = self.find_parent(child, parent_source)
            if parent:
                return parent
        return None

    def add_child(self, parent, child_data):
        """
        Add a child node to the parent node.
        """
        if parent is not None:
            parent.children.append(self.createNode(child_data))

    def traverse(self, root):
        """
        Traverse the tree and return a structured representation of the tree.
        This function will return a list of dictionaries representing the tree structure.
        """
        if root is None:
            return None

        # Create a dictionary for the current node
        node_dict = {
            'id': root.data.get('id'),
            'specialization_id': root.data.get('specialization_id'),
            'job_title': root.data.get('job_title'),
            'source': root.data.get('source'),
            'children': []
        }

        # Recursively traverse the children
        for child in root.children:
            node_dict['children'].append(self.traverse(child))

        return node_dict

def create_tree(data):
    # Create an empty tree and root node
    tree = Tree()
    root = None
    data = json.loads(data)  # Assuming data is in JSON format

    # Insert each node dynamically
    for item in data:
        
        if item['source']:
            current_source = item['source']  # Extract the current source level

        # If the root is not yet set, create it
        if root is None:
            root = tree.createNode(item)
            tree.root = root  # Set the tree's root
        else:
            # Find the parent source
            parent = tree.find_parent(root, current_source)
            if parent is not None:
                tree.add_child(parent, item)
            else:
                print(f"Parent not found for {item['job_title']} under {current_source}")
                

    # Sort the tree's children at each level
    def sort_tree(node):
        # Recursively sort children at each level
        if node.children:
            node.children.sort(key=lambda x: x.data['source'])  # Adjust sorting key as needed

            # Recursively sort the subtree for each child
            for child in node.children:
                sort_tree(child)

    # Sort the entire tree starting from the root
    sort_tree(root)

    # Function to traverse the top-level branch and ignore lower branches
    def traverse_top_branch(node):
        # Start with an empty results list
        results = []
        
        # Include the root node's data
        if node:
            results.append(node.data)

        # Traverse only the immediate children (not deeper branches)
        for child in node.children:
            results.append(child.data)
                
        return results

    # Traverse the tree and return all results from the top-level branch
    return traverse_top_branch(root)

