from pathlib import Path
import sqlite3
import hashlib
import secrets
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent
DB_DIR = BASE_DIR / "database"
DB_PATH = DB_DIR / "careermate.db"

def get_connection():
    DB_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn

def hash_password(password, salt=None):
    if not salt:
        salt = secrets.token_hex(16)
    hashed = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000).hex()
    return hashed, salt

def init_db():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT,
                salt TEXT,
                education TEXT,
                branch TEXT,
                graduation_year TEXT,
                interests TEXT,
                experience_level TEXT,
                target_career TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Migration check for password_hash / salt columns
        cursor.execute("PRAGMA table_info(users)")
        columns = [col['name'] for col in cursor.fetchall()]
        if 'password_hash' not in columns:
            cursor.execute("ALTER TABLE users ADD COLUMN password_hash TEXT")
        if 'salt' not in columns:
            cursor.execute("ALTER TABLE users ADD COLUMN salt TEXT")
        
        # Skills table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS skills (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                skill TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
            )
        ''')
        
        # Chat history table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS chat_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                role TEXT NOT NULL,
                message TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
            )
        ''')
        
        # Recommendations table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS recommendations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                career TEXT NOT NULL,
                score REAL NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
            )
        ''')

        # Quiz Scores table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS quiz_scores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                topic TEXT NOT NULL,
                score INTEGER NOT NULL,
                total_questions INTEGER NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
            )
        ''')

        conn.commit()
        
        # Ensure default demo user exists
        cursor.execute("SELECT id FROM users WHERE id = 1")
        if not cursor.fetchone():
            def_pass, def_salt = hash_password("student123")
            cursor.execute('''
                INSERT INTO users (id, name, email, password_hash, salt, education, branch, graduation_year, interests, experience_level, target_career)
                VALUES (1, 'Student User', 'student@college.edu', ?, ?, 'B.Tech CSE', 'Computer Science & Engineering', '2026', 'Artificial Intelligence, Web Development', 'Entry Level', 'Python Developer')
            ''', (def_pass, def_salt))
            default_skills = ['Python', 'SQL', 'Git', 'HTML', 'CSS', 'JavaScript']
            for s in default_skills:
                cursor.execute("INSERT INTO skills (user_id, skill) VALUES (1, ?)", (s,))
            conn.commit()

        conn.close()
    except Exception as e:
        print(f"[Database Init Warning] {e}")

def register_user(name, email, password, education="", branch="", graduation_year="", interests="", experience_level="Entry Level", target_career="Python Developer", skills_list=None):
    try:
        init_db()
        email_clean = email.strip().lower()
        if not email_clean or not password:
            return False, "Email and Password are required fields.", None
            
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT id FROM users WHERE LOWER(email) = ?", (email_clean,))
        if cursor.fetchone():
            conn.close()
            return False, "An account with this email address already exists.", None
            
        pwd_hash, salt = hash_password(password)
        
        cursor.execute('''
            INSERT INTO users (name, email, password_hash, salt, education, branch, graduation_year, interests, experience_level, target_career)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (name.strip(), email_clean, pwd_hash, salt, education, branch, graduation_year, interests, experience_level, target_career))
        
        new_user_id = cursor.lastrowid
        
        if skills_list:
            for sk in skills_list:
                sk_clean = sk.strip()
                if sk_clean:
                    cursor.execute("INSERT INTO skills (user_id, skill) VALUES (?, ?)", (new_user_id, sk_clean))
                    
        conn.commit()
        
        cursor.execute("SELECT * FROM users WHERE id = ?", (new_user_id,))
        user_row = cursor.fetchone()
        conn.close()
        
        return True, "Registration successful!", dict(user_row) if user_row else None
    except Exception as e:
        return False, f"Registration error: {str(e)}", None

def authenticate_user(email, password):
    try:
        init_db()
        email_clean = email.strip().lower()
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM users WHERE LOWER(email) = ?", (email_clean,))
        user_row = cursor.fetchone()
        conn.close()
        
        if not user_row:
            return False, "Invalid email or password.", None
            
        user_dict = dict(user_row)
        stored_hash = user_dict.get('password_hash')
        stored_salt = user_dict.get('salt')
        
        if stored_hash and stored_salt:
            calc_hash, _ = hash_password(password, stored_salt)
            if calc_hash != stored_hash:
                return False, "Invalid email or password.", None
                
        return True, "Login successful!", user_dict
    except Exception as e:
        return False, f"Authentication error: {str(e)}", None

def reset_user_password(email, new_password):
    """
    Resets user password in SQLite database.
    """
    try:
        init_db()
        email_clean = email.strip().lower()
        if not email_clean or not new_password:
            return False, "Email and new password are required."
            
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE LOWER(email) = ?", (email_clean,))
        row = cursor.fetchone()
        
        if not row:
            conn.close()
            return False, "No registered account found with this email address."
            
        pwd_hash, salt = hash_password(new_password)
        cursor.execute("UPDATE users SET password_hash = ?, salt = ? WHERE LOWER(email) = ?", (pwd_hash, salt, email_clean))
        conn.commit()
        conn.close()
        return True, "Password successfully reset! You can now log in with your new password."
    except Exception as e:
        return False, f"Error resetting password: {str(e)}"

def get_or_create_default_user():
    try:
        init_db()
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = 1")
        user = cursor.fetchone()
        conn.close()
        if user:
            return dict(user)
    except Exception as e:
        print(f"[get_or_create_default_user Error] {e}")
        
    return {
        "id": 1,
        "name": "Student User",
        "email": "student@college.edu",
        "education": "B.Tech CSE",
        "branch": "Computer Science & Engineering",
        "graduation_year": "2026",
        "interests": "Artificial Intelligence, Web Development",
        "experience_level": "Entry Level",
        "target_career": "Python Developer"
    }

def get_user_skills(user_id=1):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT skill FROM skills WHERE user_id = ?", (user_id,))
        rows = cursor.fetchall()
        conn.close()
        if rows:
            return [r['skill'] for r in rows]
    except Exception as e:
        print(f"[get_user_skills Error] {e}")
    return ['Python', 'SQL', 'Git', 'HTML', 'CSS', 'JavaScript']

def update_user_skills(user_id, skills_list):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM skills WHERE user_id = ?", (user_id,))
        for skill in skills_list:
            s_clean = skill.strip()
            if s_clean:
                cursor.execute("INSERT INTO skills (user_id, skill) VALUES (?, ?)", (user_id, s_clean))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"[update_user_skills Error] {e}")

def update_user_profile(user_id, name, education, branch, graduation_year, interests, experience_level, target_career):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE users
            SET name = ?, education = ?, branch = ?, graduation_year = ?, interests = ?, experience_level = ?, target_career = ?
            WHERE id = ?
        ''', (name, education, branch, graduation_year, interests, experience_level, target_career, user_id))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"[update_user_profile Error] {e}")

def save_chat_message(user_id, role, message):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO chat_history (user_id, role, message, timestamp)
            VALUES (?, ?, ?, ?)
        ''', (user_id, role, message, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"[save_chat_message Error] {e}")

def get_chat_history(user_id=1, limit=50):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT role, message, timestamp FROM chat_history
            WHERE user_id = ?
            ORDER BY id ASC
            LIMIT ?
        ''', (user_id, limit))
        rows = cursor.fetchall()
        conn.close()
        return [dict(r) for r in rows]
    except Exception as e:
        print(f"[get_chat_history Error] {e}")
        return []

def clear_chat_history(user_id=1):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM chat_history WHERE user_id = ?", (user_id,))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"[clear_chat_history Error] {e}")

def save_recommendation(user_id, career, score):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO recommendations (user_id, career, score, timestamp)
            VALUES (?, ?, ?, ?)
        ''', (user_id, career, score, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"[save_recommendation Error] {e}")

def get_saved_recommendations(user_id=1, limit=10):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT career, score, timestamp FROM recommendations
            WHERE user_id = ?
            ORDER BY id DESC
            LIMIT ?
        ''', (user_id, limit))
        rows = cursor.fetchall()
        conn.close()
        return [dict(r) for r in rows]
    except Exception as e:
        print(f"[get_saved_recommendations Error] {e}")
        return []

def save_quiz_score(user_id, topic, score, total_questions):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO quiz_scores (user_id, topic, score, total_questions, timestamp)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, topic, score, total_questions, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"[save_quiz_score Error] {e}")

def get_quiz_stats(user_id=1):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT COUNT(*) as total_attempts, SUM(score) as total_score, SUM(total_questions) as total_qs
            FROM quiz_scores WHERE user_id = ?
        ''', (user_id,))
        row = cursor.fetchone()
        conn.close()
        if row and row['total_qs']:
            return {
                "attempts": row['total_attempts'],
                "score": row['total_score'],
                "total_qs": row['total_qs'],
                "accuracy": round((row['total_score'] / row['total_qs']) * 100, 1)
            }
    except Exception as e:
        print(f"[get_quiz_stats Error] {e}")
    return {"attempts": 0, "score": 0, "total_qs": 0, "accuracy": 0.0}
