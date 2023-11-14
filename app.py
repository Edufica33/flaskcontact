from flask import Flask, request, jsonify
import json

app = Flask(__name__)

# Load data from fakedatabase.json
with open('fakedatabase.json', 'r') as file:
    contacts = json.load(file)

# Helper function to sort contacts by name
def sort_contacts_by_name(contact):
    return contact['name']

# Helper function to find a contact by ID
def find_contact_by_id(contact_id):
    return next((contact for contact in contacts if contact['id'] == contact_id), None)

# GET /contacts
@app.route('/contacts', methods=['GET'])
def get_contacts():
    # Extract the 'phrase' parameter from the query string
    phrase = request.args.get('phrase', '').lower()

    if phrase == '':
        return jsonify(contacts), 200

    filtered_contacts = [contact for contact in contacts if phrase in contact['name'].lower()]
    return jsonify(sorted(filtered_contacts, key=sort_contacts_by_name)), 200

# GET /contacts/<contact-id>
@app.route('/contacts/<contact_id>', methods=['GET'])
def get_contact(contact_id):
    contact = find_contact_by_id(contact_id)

    if contact:
        return jsonify(contact), 200
    else:
        return jsonify({'error': 'Not Found', 'message': 'Contact not found'}), 404

# DELETE /contacts/<contact-id>
@app.route('/contacts/<contact_id>', methods=['DELETE'])
def delete_contact(contact_id):
    global contacts
    contact = find_contact_by_id(contact_id)

    if contact:
        contacts = [c for c in contacts if c['id'] != contact_id]
        return '', 204
    else:
        return jsonify({'error': 'Not Found', 'message': 'Contact not found'}), 404

# Handle 404 Not Found for unsupported routes
@app.errorhandler(404)
def not_found_error(error):
    return jsonify({'error': 'Not Found', 'message': 'Endpoint not found'}), 404

# Handle 405 Method Not Allowed for unsupported methods
@app.errorhandler(405)
def method_not_allowed_error(error):
    return jsonify({'error': 'Method Not Allowed', 'message': 'Method not allowed for this endpoint'}), 405

if __name__ == '__main__':
    app.run(debug=True)