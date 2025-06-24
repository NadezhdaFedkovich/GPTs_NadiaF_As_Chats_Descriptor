from flask import Flask, request, jsonify
import mysql.connector
from config import DB_CONFIG

app = Flask(__name__)

@app.route('/messages', methods=['GET'])
def get_messages_by_chat():
    chat_id = request.args.get('chat_id')

    if not chat_id:
        return jsonify({'error': 'chat_id is required'}), 400

    # Параметры пагинации
    try:
        limit = int(request.args.get('limit', 1000))
        offset = int(request.args.get('offset', 0))
        if limit > 1000:
            limit = 1000
    except ValueError:
        return jsonify({'error': 'limit and offset must be integers'}), 400

    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)

        # Получаем всего сколько сообщений в чате
        cursor.execute("SELECT COUNT(*) AS total FROM astrologer_messages WHERE chat_id = %s", (chat_id,))
        total = cursor.fetchone()['total']

        # Получаем нужную порцию сообщений
        cursor.execute(
            "SELECT * FROM astrologer_messages WHERE chat_id = %s ORDER BY id ASC LIMIT %s OFFSET %s",
            (chat_id, limit, offset)
        )
        messages = cursor.fetchall()

        # Есть ли еще сообщения?
        has_more = offset + limit < total

        cursor.close()
        conn.close()

        print(f"limit={limit}, offset={offset}, len(messages)={len(messages)}")

        # Возвращаем результат в новом формате
        return jsonify({
            "messages": messages,
            "has_more": has_more,
            "total": total
        })

    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
