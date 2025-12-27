import sqlite3

# データベースファイルの名前をつくる
dbname = 'trivia.db'

# データベースに接続する
conn = sqlite3.connect(dbname)
cur = conn.cursor()

# SQL文「テーブルが存在する場合は削除する（やり直す時用）」
cur.execute('DROP TABLE IF EXISTS memos')

# SQL文「memosテーブルを作成する」
cur.execute('''
        CREATE TABLE memos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            category TEXT NOT NULL,
            source TEXT,
            usage_count INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

# 動作確認用 ダミーデータを入れとく
cur.execute('''
        INSERT INTO memos (title, content, category, source)
        VALUES (
            'ジョークで作られた宗教がある',
            '「空飛ぶスパゲッティ・モンスター教」は、インテリジェント・デザイン説を公教育に持ち込むことへの諷刺として創設された宗教である。実際に宗教として認められている国もあり、結婚式も挙げられる。結婚指輪はパスタでできている。',
            '宗教',
            'wikipedia'
            )
        ''')

# 内容を保存して閉じる
conn.commit()
conn.close()

print("データベースとテーブルを作成し、初期データを追加しました。")

# 作成日時: 2025-12-25 (開発1日目)
# 初期データをいじった場合はinit_db.pyを実行しなおせばOK