from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)

# File to store the tickets
TICKETS_FILE = 'tickets.json'

# Load tickets from file or initialize if file doesn't exist
def load_tickets():
    if os.path.exists(TICKETS_FILE):
        with open(TICKETS_FILE, 'r') as f:
            return json.load(f)
    return {'todo': [], 'in_progress': [], 'done': []}

# Save tickets to file
def save_tickets(tickets):
    with open(TICKETS_FILE, 'w') as f:
        json.dump(tickets, f)

# Initialize tickets
tickets = load_tickets()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_tickets')
def get_tickets():
    return jsonify(tickets)

@app.route('/add_ticket', methods=['POST'])
def add_ticket():
    data = request.json
    column = data['column']
    title = data['title']
    ticket_id = data['id']
    tickets[column].append({'id': ticket_id, 'title': title, 'checklist': []})
    save_tickets(tickets)
    return jsonify(success=True)

@app.route('/move_ticket', methods=['POST'])
def move_ticket():
    data = request.json
    from_column = data['from']
    to_column = data['to']
    ticket_id = data['ticketId']
    
    ticket = next((t for t in tickets[from_column] if t['id'] == ticket_id), None)
    if ticket:
        tickets[from_column].remove(ticket)
        tickets[to_column].append(ticket)
        save_tickets(tickets)
        return jsonify(success=True)
    return jsonify(success=False), 404

@app.route('/delete_ticket', methods=['POST'])
def delete_ticket():
    data = request.json
    column = data['column']
    ticket_id = data['ticketId']
    
    tickets[column] = [t for t in tickets[column] if t['id'] != ticket_id]
    save_tickets(tickets)
    return jsonify(success=True)

@app.route('/add_checklist_item', methods=['POST'])
def add_checklist_item():
    data = request.json
    ticket_id = data['ticketId']
    item = data['item']
    
    for column in tickets.values():
        for ticket in column:
            if ticket['id'] == ticket_id:
                ticket['checklist'].append({'id': f"item-{len(ticket['checklist'])}", 'text': item, 'checked': False})
                save_tickets(tickets)
                return jsonify(success=True)
    return jsonify(success=False), 404

@app.route('/toggle_checklist_item', methods=['POST'])
def toggle_checklist_item():
    data = request.json
    ticket_id = data['ticketId']
    item_id = data['itemId']
    
    for column in tickets.values():
        for ticket in column:
            if ticket['id'] == ticket_id:
                for item in ticket['checklist']:
                    if item['id'] == item_id:
                        item['checked'] = not item['checked']
                        save_tickets(tickets)
                        return jsonify(success=True)
    return jsonify(success=False), 404

if __name__ == '__main__':
    app.run(debug=True)
