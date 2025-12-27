import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# データベースに接続する関数
def get_db_connection():
    conn = sqlite3.connect('trivia.db')
    # ↓これやると列名でアクセスできるんだって（へー）
    conn.row_factory = sqlite3.Row
    return conn

# トップページアクセス時の処理
@app.route('/', methods=['GET', 'POST'])
def index():
    conn = get_db_connection()
    # フォームから送信（POST）された時の処理
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        category = request.form['category']
        source = request.form['source']

        # SQL文「memosテーブルに新しいメモを追加する」
        conn.execute('INSERT INTO memos (title, content, category, source) VALUES (?, ?, ?, ?)', (title, content, category, source))
        conn.commit()
        conn.close()

        # 保存したらトップページを読み込む
        return redirect(url_for('index'))

    # 通常アクセス（GET）の処理：SQL文「作成日時の新しい順にデータをすべて取得して」
    conn = get_db_connection()
    memos = conn.execute('SELECT * FROM memos ORDER BY created_at DESC').fetchall()
    conn.close()    
    # 取得したデータを index.html に渡して表示
    return render_template('index.html', memos=memos)

# 削除機能
@app.route('/delete/<int:id>', methods=['POST'])
def delete_memo(id):
    conn = get_db_connection()
    # SQL文「指定されたIDのメモを削除」
    conn.execute('DELETE FROM memos WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

# 話せた回数カウント
@app.route('/count_up/<int:id>', methods=['POST'])
def count_up(id):
    conn = get_db_connection()
    # SQL文「指定されたIDのusage_countを1増やす」
    conn.execute('UPDATE memos SET usage_count = COALESCE(usage_count, 0) + 1 WHERE id = ?', (id,))    
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

# ファイルが直接実行されたとき
if __name__ == '__main__':
    app.run(debug=True, port=8000)

# 作成日時: 2025-12-25 (開発1日目)