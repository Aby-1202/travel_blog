import os
from datetime import datetime
from flask import Blueprint, request, session, redirect, flash, url_for, current_app, render_template
import sqlite3

favorite_bookmark_bp = Blueprint('favorite_bookmark', __name__)

@favorite_bookmark_bp.route('/favorite_bookmark', methods=['GET'])
def favorite_bookmark():
    if 'user_id' not in session:
        flash("ログインしてください")
        return redirect(url_for('login.login'))

    user_id = session['user_id']

    conn = sqlite3.connect('app.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # ブックマークした旅行
    cursor.execute("""
        SELECT travel_data.*, bookmark_data.id AS bookmark_id, bookmark_data.b_created_at AS bookmark_created_at
        FROM travel_data
        INNER JOIN bookmark_data ON travel_data.id = bookmark_data.t_id
        WHERE bookmark_data.u_id = ?
        ORDER BY bookmark_data.b_created_at DESC
    """, (user_id,))
    bookmarked_travel_items = cursor.fetchall()

    # お気に入りした旅行
    cursor.execute("""
        SELECT travel_data.*, favorites.created_at AS favorite_created_at
        FROM travel_data
        INNER JOIN favorites ON travel_data.id = favorites.t_id
        WHERE favorites.u_id = ?
        ORDER BY favorites.created_at DESC
    """, (user_id,))
    favorited_travel_items = cursor.fetchall()

    conn.close()

    return render_template(
        'favorite_bookmark.html',
        bookmarked_travel_items=bookmarked_travel_items,
        favorited_travel_items=favorited_travel_items,
    )

@favorite_bookmark_bp.route('/favorite/add', methods=['POST'])
def add_favorite():
    if 'user_id' not in session:
        flash("ログインしてください")
        return redirect(url_for('login.login'))

    user_id = session['user_id']
    travel_id = request.form.get('travel_id')

    if travel_id:
        conn = sqlite3.connect('app.db')
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT id FROM favorites
                WHERE u_id = ? AND t_id = ?
            """, (user_id, travel_id))
            existing_favorite = cursor.fetchone()
            if existing_favorite:
                flash('既にいいねされています。', 'warning')
            else:
                cursor.execute("""
                    INSERT INTO favorites (u_id, t_id, created_at)
                    VALUES (?, ?, ?)
                """, (user_id, travel_id, datetime.now()))
                conn.commit()
                flash('いいねを追加しました。', 'success')
        except sqlite3.IntegrityError:
            flash('いいねの追加に失敗しました。', 'danger')
        finally:
            conn.close()
    return redirect(url_for('home.home'))

@favorite_bookmark_bp.route('/favorite/remove', methods=['POST'])
def remove_favorite():
    if 'user_id' not in session:
        flash("ログインしてください")
        return redirect(url_for('login.login'))

    user_id = session['user_id']
    travel_id = request.form.get('travel_id')

    if travel_id:
        conn = sqlite3.connect('app.db')
        cursor = conn.cursor()
        try:
            cursor.execute("""
                DELETE FROM favorites
                WHERE u_id = ? AND t_id = ?
            """, (user_id, travel_id))
            conn.commit()
            flash('いいねを解除しました。', 'success')
        except Exception as e:
            flash(f'いいねの解除に失敗しました: {str(e)}', 'danger')
        finally:
            conn.close()
    return redirect(url_for('home.home'))

@favorite_bookmark_bp.route('/bookmark/add', methods=['POST'])
def add_bookmark():
    if 'user_id' not in session:
        flash("ログインしてください")
        return redirect(url_for('login.login'))

    user_id = session['user_id']
    travel_id = request.form.get('travel_id')

    if travel_id:
        conn = sqlite3.connect('app.db')
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT id FROM bookmark_data
                WHERE u_id = ? AND t_id = ?
            """, (user_id, travel_id))
            existing_bookmark = cursor.fetchone()
            if existing_bookmark:
                flash('既にブックマーク済みです。', 'warning')
            else:
                cursor.execute("""
                    INSERT INTO bookmark_data (u_id, t_id, b_created_at)
                    VALUES (?, ?, ?)
                """, (user_id, travel_id, datetime.now()))
                conn.commit()
                flash('ブックマークしました。', 'success')
        except sqlite3.IntegrityError:
            flash('ブックマークの追加に失敗しました。', 'danger')
        finally:
            conn.close()
    return redirect(url_for('home.home'))

@favorite_bookmark_bp.route('/bookmark/remove', methods=['POST'])
def remove_bookmark():
    if 'user_id' not in session:
        flash("ログインしてください")
        return redirect(url_for('login.login'))

    user_id = session['user_id']
    travel_id = request.form.get('travel_id')

    if travel_id:
        conn = sqlite3.connect('app.db')
        cursor = conn.cursor()
        try:
            cursor.execute("""
                DELETE FROM bookmark_data
                WHERE u_id = ? AND t_id = ?
            """, (user_id, travel_id))
            conn.commit()
            flash('ブックマークを解除しました。', 'success')
        except Exception as e:
            flash(f'ブックマークの解除に失敗しました: {str(e)}', 'danger')
        finally:
            conn.close()
    return redirect(url_for('home.home'))