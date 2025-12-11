from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import json

app = Flask(__name__)
CORS(app) # Permite que o HTML acesse o Python

# CONFIGURAÇÃO DO BANCO DE DADOS
db_config = {
    'host': 'localhost',
    'user': 'root',      # Seu usuário do MySQL
    'password': '#Kleber123',  # SUA SENHA DO MYSQL AQUI
    'database': 'mens_navalha'
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

# --- ROTAS SERVIÇOS ---
@app.route('/services', methods=['GET'])
def get_services():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM services")
    services = cursor.fetchall()
    conn.close()
    return jsonify(services)

@app.route('/services', methods=['POST'])
def add_service():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO services (name, price, duration, icon) VALUES (%s, %s, %s, %s)",
                   (data['name'], data['price'], data['duration'], data['icon']))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Success'}), 201

@app.route('/services/<int:id>', methods=['PUT'])
def update_service(id):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE services SET name=%s, price=%s, duration=%s, icon=%s WHERE id=%s",
                   (data['name'], data['price'], data['duration'], data['icon'], id))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Updated'})

@app.route('/services/<int:id>', methods=['DELETE'])
def delete_service(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM services WHERE id=%s", (id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Deleted'})

# --- ROTAS PROFISSIONAIS ---
@app.route('/professionals', methods=['GET'])
def get_professionals():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM professionals")
    pros = cursor.fetchall()
    for p in pros:
        if isinstance(p['allowed_services'], str):
            p['allowed_services'] = json.loads(p['allowed_services'])
    conn.close()
    return jsonify(pros)

@app.route('/professionals', methods=['POST'])
def add_professional():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    allowed = json.dumps(data.get('allowed_services', []))
    cursor.execute("INSERT INTO professionals (name, specialty, lunch_start, lunch_end, allowed_services) VALUES (%s, %s, %s, %s, %s)",
                   (data['name'], data['specialty'], data.get('lunch_start'), data.get('lunch_end'), allowed))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Success'}), 201

@app.route('/professionals/<int:id>', methods=['PUT'])
def update_professional(id):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    allowed = json.dumps(data.get('allowed_services', []))
    cursor.execute("UPDATE professionals SET name=%s, specialty=%s, lunch_start=%s, lunch_end=%s, allowed_services=%s WHERE id=%s",
                   (data['name'], data['specialty'], data.get('lunch_start'), data.get('lunch_end'), allowed, id))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Updated'})

@app.route('/professionals/<int:id>', methods=['DELETE'])
def delete_professional(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM professionals WHERE id=%s", (id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Deleted'})

# --- ROTAS AGENDAMENTOS ---
@app.route('/appointments', methods=['GET'])
def get_appointments():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM appointments")
    apps = cursor.fetchall()
    conn.close()
    return jsonify(apps)

@app.route('/appointments', methods=['POST'])
def add_appointment():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO appointments (service_id, service_name, professional_id, professional_name, date, time, client_name, client_phone, status)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'pending')
    """, (data['service_id'], data['service_name'], data['professional_id'], data['professional_name'], data['date'], data['time'], data['client_name'], data['client_phone']))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Success'}), 201

@app.route('/appointments/<int:id>', methods=['PUT'])
def update_appointment(id):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if 'status' in data:
        cursor.execute("UPDATE appointments SET status=%s WHERE id=%s", (data['status'], id))
    if 'client_name' in data:
        cursor.execute("UPDATE appointments SET client_name=%s WHERE id=%s", (data['client_name'], id))
        
    conn.commit()
    conn.close()
    return jsonify({'message': 'Updated'})

@app.route('/appointments/<int:id>', methods=['DELETE'])
def delete_appointment(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM appointments WHERE id=%s", (id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Deleted'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)