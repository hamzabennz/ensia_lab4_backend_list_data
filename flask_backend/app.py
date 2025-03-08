from flask import Flask, jsonify, request
from flask_cors import CORS
import math
import operator
from dummy_data import USERS, DOCUMENTS  # Import both pre-generated datasets

app = Flask(__name__)
CORS(app)

# Define valid operators and their corresponding functions
OPERATORS = {
    'eq': operator.eq,           # Equal
    'ne': operator.ne,           # Not Equal
    'gt': operator.gt,           # Greater Than
    'lt': operator.lt,           # Less Than
    'ge': operator.ge,           # Greater Than or Equal
    'le': operator.le,           # Less Than or Equal
    'contains': lambda x, y: y.lower() in x.lower(),  # Case-insensitive contains
    'startswith': lambda x, y: x.lower().startswith(y.lower()),  # Case-insensitive starts with
    'endswith': lambda x, y: x.lower().endswith(y.lower()),      # Case-insensitive ends with
    'in': lambda x, y: x in y    # In list
}

def apply_filter(item, filter_condition):
    key = filter_condition.get('key')
    op = filter_condition.get('op', 'eq')
    value = filter_condition.get('value')
    
    if key not in item:
        return True  # Skip invalid keys
        
    if op not in OPERATORS:
        return True  # Skip invalid operators
    
    # Special handling for lists like tags
    if isinstance(item[key], list) and op == 'contains':
        return any(value.lower() in str(tag).lower() for tag in item[key])
        
    try:
        return OPERATORS[op](str(item[key]), str(value))
    except (TypeError, ValueError):
        return False

def filter_items(items, filters):
    if not filters:
        return items
        
    filtered_items = items
    for filter_condition in filters:
        filtered_items = [
            item for item in filtered_items 
            if apply_filter(item, filter_condition)
        ]
    
    return filtered_items

def sort_items(items, sort_by, order, valid_keys):
    if sort_by not in valid_keys:
        sort_by = valid_keys[0]
    
    reverse = order.lower() == 'desc'
    return sorted(items, key=lambda x: str(x.get(sort_by, '')), reverse=reverse)

# User related routes and functions
def sort_users(users, sort_by, order):
    valid_keys = ['id', 'name', 'position', 'status', 'department', 'hire_date', 'employee_id']
    return sort_items(users, sort_by, order, valid_keys)

@app.route('/api/users', methods=['GET', 'POST'])
def get_users():
    # Get pagination parameters
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    
    # Get sorting parameters
    sort_by = request.args.get('sort_by', 'id')
    order = request.args.get('order', 'asc')
    
    # Get filter conditions from POST body
    filters = []
    if request.method == 'POST':
        filters = request.json if request.json else []
    
    # Use pre-generated users
    all_users = USERS
    
    # Apply filters
    filtered_users = filter_items(all_users, filters)
    
    # Apply sorting
    sorted_users = sort_users(filtered_users, sort_by, order)
    
    # Calculate pagination
    total_users = len(sorted_users)
    total_pages = math.ceil(total_users / per_page)
    page = min(max(1, page), total_pages) if total_pages > 0 else 1
    
    # Get paginated subset
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    paginated_users = sorted_users[start_idx:end_idx]
    
    return jsonify({
        "status": "success",
        "data": paginated_users,
        "pagination": {
            "total_records": total_users,
            "total_pages": total_pages,
            "current_page": page,
            "per_page": per_page,
            "has_next": page < total_pages,
            "has_prev": page > 1
        },
        "sort": {
            "sort_by": sort_by,
            "order": order
        },
        "filters": filters
    })

@app.route('/api/users/get/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = next((user for user in USERS if user['id'] == user_id), None)
    
    if user:
        return jsonify({
            "status": "success",
            "data": user
        })
    else:
        return jsonify({
            "status": "error",
            "message": "User not found"
        })

# Document related routes and functions
def sort_documents(documents, sort_by, order):
    valid_keys = ['id', 'name', 'description', 'category', 'status', 'createdAt', 'updatedAt']
    return sort_items(documents, sort_by, order, valid_keys)

@app.route('/api/documents', methods=['GET', 'POST'])
def get_documents():
    # Get pagination parameters
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    
    # Get sorting parameters
    sort_by = request.args.get('sort_by', 'name')
    order = request.args.get('order', 'asc')
    
    # Get filter conditions from POST body
    filters = []
    if request.method == 'POST':
        filters = request.json if request.json else []
    
    # Use pre-generated documents
    all_documents = DOCUMENTS
    
    # Apply filters
    filtered_documents = filter_items(all_documents, filters)
    
    # Apply sorting
    sorted_documents = sort_documents(filtered_documents, sort_by, order)
    
    # Calculate pagination
    total_documents = len(sorted_documents)
    total_pages = math.ceil(total_documents / per_page)
    page = min(max(1, page), total_pages) if total_pages > 0 else 1
    
    # Get paginated subset
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    paginated_documents = sorted_documents[start_idx:end_idx]
    
    return jsonify({
        "status": "success",
        "data": paginated_documents,
        "pagination": {
            "total_records": total_documents,
            "total_pages": total_pages,
            "current_page": page,
            "per_page": per_page,
            "has_next": page < total_pages,
            "has_prev": page > 1
        },
        "sort": {
            "sort_by": sort_by,
            "order": order
        },
        "filters": filters
    })

@app.route('/api/documents/get/<document_id>', methods=['GET'])
def get_document(document_id):
    document = next((doc for doc in DOCUMENTS if doc['id'] == document_id), None)
    
    if document:
        return jsonify({
            "status": "success",
            "data": document
        })
    else:
        return jsonify({
            "status": "error",
            "message": "Document not found"
        })

if __name__ == '__main__':
    app.run(debug=True, port=5000)