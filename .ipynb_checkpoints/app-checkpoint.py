# app.py

from flask import Flask, request, jsonify
import mysql.connector
from config import DB_CONFIG

app = Flask(__name__)

@app.route('/messages', methods=['GET'])
def get_messages_by_chat():
    chat_id = request.args.get('chat_id')

    if not chat_id:
        return jsonify({'error': 'chat_id is required'}), 400

    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM astrologer_messages am WHERE chat_id = %s", (chat_id,))
        messages = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(messages)
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500