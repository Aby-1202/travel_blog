# routes/search_travel.py

import sqlite3
from flask import Blueprint, render_template, request

# Blueprint 名を search_travel_bp に
search_travel_bp = Blueprint('search_travel', __name__, url_prefix='/search_travel')

@search_travel_bp.route('/', methods=['GET', 'POST'])
def search_travel():
    conn = sqlite3.connect('app.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    results = []
    query = ''
    if request.method == 'POST':
        query = request.form.get('query', '').strip()
        if query:
            cursor.execute(
                """
                SELECT td.*, u.u_name AS username
                    FROM travel_data AS td
                    JOIN users_table AS u 
                    ON td.u_id = u.id
                    WHERE td.t_title LIKE ?
                    OR td.t_location LIKE ?
                    ORDER BY td.start_date DESC
                """,
                (f'%{query}%', f'%{query}%')
            )
            results = cursor.fetchall()

    conn.close()
    return render_template(
        'search_travel.html',
        travel_data_list=results,
        query=query
    )
