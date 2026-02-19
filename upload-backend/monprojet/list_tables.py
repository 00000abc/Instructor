"""
Script pour lister toutes les tables de la base de données MySQL
"""

import pymysql
from decouple import config

def list_database_tables():
    """
    Liste toutes les tables de la base de données avec leurs détails
    """
    try:
        # Connexion à la base de données
        connection = pymysql.connect(
            host=config('DB_HOST', default='localhost'),
            user=config('DB_USER'),
            password=config('DB_PASSWORD'),
            database=config('DB_NAME'),
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        
        print("=" * 80)
        print("📊 INFORMATIONS SUR LA BASE DE DONNÉES")
        print("=" * 80)
        print(f"Base de données : {config('DB_NAME')}")
        print(f"Serveur : {config('DB_HOST', default='localhost')}")
        print("=" * 80)
        print()
        
        with connection.cursor() as cursor:
            # Lister toutes les tables
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            
            if not tables:
                print("❌ Aucune table trouvée dans la base de données.")
                return
            
            print(f"✅ {len(tables)} table(s) trouvée(s) :\n")
            
            for i, table_dict in enumerate(tables, 1):
                # Le nom de la clé dépend de la base de données
                table_name = list(table_dict.values())[0]
                
                print(f"{i}. 📋 Table : {table_name}")
                print("-" * 80)
                
                # Compter les lignes
                cursor.execute(f"SELECT COUNT(*) as count FROM `{table_name}`")
                count = cursor.fetchone()['count']
                print(f"   Nombre de lignes : {count}")
                
                # Afficher les colonnes
                cursor.execute(f"DESCRIBE `{table_name}`")
                columns = cursor.fetchall()
                
                print(f"   Colonnes ({len(columns)}) :")
                for col in columns:
                    field_name = col['Field']
                    field_type = col['Type']
                    null_allowed = "NULL" if col['Null'] == 'YES' else "NOT NULL"
                    key = col['Key']
                    
                    key_info = ""
                    if key == 'PRI':
                        key_info = " 🔑 PRIMARY KEY"
                    elif key == 'MUL':
                        key_info = " 🔗 FOREIGN KEY"
                    elif key == 'UNI':
                        key_info = " ⭐ UNIQUE"
                    
                    print(f"      - {field_name} : {field_type} {null_allowed}{key_info}")
                
                print()
        
        connection.close()
        print("=" * 80)
        print("✅ Connexion fermée")
        
    except Exception as e:
        print(f"❌ Erreur : {e}")

def show_table_data(table_name, limit=10):
    """
    Afficher les premières lignes d'une table
    
    Args:
        table_name (str): Nom de la table
        limit (int): Nombre de lignes à afficher
    """
    try:
        connection = pymysql.connect(
            host=config('DB_HOST', default='localhost'),
            user=config('DB_USER'),
            password=config('DB_PASSWORD'),
            database=config('DB_NAME'),
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        
        with connection.cursor() as cursor:
            # Récupérer les données
            cursor.execute(f"SELECT * FROM `{table_name}` LIMIT {limit}")
            rows = cursor.fetchall()
            
            if not rows:
                print(f"❌ Aucune donnée dans la table {table_name}")
                return
            
            print(f"\n📊 Données de la table '{table_name}' (limite: {limit})")
            print("=" * 80)
            
            for i, row in enumerate(rows, 1):
                print(f"\nLigne {i}:")
                for key, value in row.items():
                    print(f"  {key}: {value}")
            
            print("=" * 80)
        
        connection.close()
        
    except Exception as e:
        print(f"❌ Erreur : {e}")

def get_database_stats():
    """
    Afficher des statistiques globales sur la base de données
    """
    try:
        connection = pymysql.connect(
            host=config('DB_HOST', default='localhost'),
            user=config('DB_USER'),
            password=config('DB_PASSWORD'),
            database=config('DB_NAME'),
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        
        print("\n" + "=" * 80)
        print("📈 STATISTIQUES DE LA BASE DE DONNÉES")
        print("=" * 80)
        
        with connection.cursor() as cursor:
            # Nombre de tables
            cursor.execute("SHOW TABLES")
            tables_count = len(cursor.fetchall())
            print(f"Nombre total de tables : {tables_count}")
            
            # Nombre d'utilisateurs
            cursor.execute("SELECT COUNT(*) as count FROM auth_user")
            users_count = cursor.fetchone()['count']
            print(f"Nombre d'utilisateurs : {users_count}")
            
            # Nombre de profils
            cursor.execute("SELECT COUNT(*) as count FROM api_userprofile")
            profiles_count = cursor.fetchone()['count']
            print(f"Nombre de profils : {profiles_count}")
            
            # Nombre de conversations
            cursor.execute("SELECT COUNT(*) as count FROM api_conversation")
            conversations_count = cursor.fetchone()['count']
            print(f"Nombre de conversations : {conversations_count}")
            
            # Nombre de messages
            cursor.execute("SELECT COUNT(*) as count FROM api_message")
            messages_count = cursor.fetchone()['count']
            print(f"Nombre de messages : {messages_count}")
            
            # Dernier utilisateur inscrit
            cursor.execute("""
                SELECT username, date_joined 
                FROM auth_user 
                ORDER BY date_joined DESC 
                LIMIT 1
            """)
            last_user = cursor.fetchone()
            if last_user:
                print(f"\nDernier utilisateur inscrit :")
                print(f"  - Username : {last_user['username']}")
                print(f"  - Date : {last_user['date_joined']}")
        
        print("=" * 80)
        connection.close()
        
    except Exception as e:
        print(f"❌ Erreur : {e}")

if __name__ == "__main__":
    print("\n🔍 EXPLORATION DE LA BASE DE DONNÉES MYSQL\n")
    
    # 1. Lister toutes les tables
    list_database_tables()
    
    # 2. Afficher les statistiques
    get_database_stats()
    
    # 3. Exemples : Afficher les données de certaines tables
    print("\n" + "=" * 80)
    print("📋 APERÇU DES DONNÉES")
    print("=" * 80)
    
    # Afficher les utilisateurs
    show_table_data('auth_user', limit=5)
    
    # Afficher les profils
    show_table_data('api_userprofile', limit=5)
    
    # Afficher les conversations
    show_table_data('api_conversation', limit=5)
    
    print("\n✅ Exploration terminée !")