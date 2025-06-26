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
        SELECT
            td.*,
            bd.id               AS bookmark_id,
            bd.b_created_at     AS bookmark_created_at,
            -- 累計ブックマーク数
            (SELECT COUNT(*) FROM bookmark_data WHERE t_id = td.id) AS bookmark_count,
            -- 累計いいね数
            (SELECT COUNT(*) FROM favorites     WHERE t_id = td.id) AS favorite_count
        FROM travel_data td
        INNER JOIN bookmark_data bd
            ON td.id = bd.t_id
        WHERE bd.u_id = ?
        ORDER BY bd.b_created_at DESC
    """, (user_id,))
    bookmarked_travel_items = cursor.fetchall()

    # お気に入りした旅行
    cursor.execute("""
        SELECT
            td.*,
            f.created_at   AS favorite_created_at,
            -- 累計数
            (SELECT COUNT(*) FROM bookmark_data WHERE t_id = td.id) AS bookmark_count,
            (SELECT COUNT(*) FROM favorites     WHERE t_id = td.id) AS favorite_count,
            -- このユーザーがブックマーク済みか
            CASE WHEN EXISTS (
                SELECT 1
                FROM bookmark_data bd
                WHERE bd.t_id = td.id
                AND bd.u_id = ?
            ) THEN 1 ELSE 0 END AS is_bookmarked
        FROM travel_data td
        INNER JOIN favorites f
        ON td.id = f.t_id
        WHERE f.u_id = ?
        ORDER BY f.created_at DESC
    """, (user_id, user_id))
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