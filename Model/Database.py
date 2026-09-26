import os
import psycopg2 as pg
from psycopg2.extras import DictCursor
from dotenv import load_dotenv

load_dotenv()


def conectar_BD():
    try:
        conn = pg.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT")
        )
        return conn
    except (Exception, pg.Error) as error:
        print("Erro ao conectar ao banco de dados: ", error)
        return None


def executar_consulta(query, params=None):
    conn = conectar_BD()
    if conn:
        try:
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            conn.commit()
            return cursor
        except (Exception, pg.Error) as error:
            print("Erro ao realizar consulta: ", error)
            conn.rollback()
            return None
        finally:
            conn.close()
    else:
        return None


def selecionar_dados(query, params=None):
    conn = conectar_BD()
    if conn:
        try:
            cursor = conn.cursor(cursor_factory=DictCursor)
            if params:
                cursor.execute(query, params or ())
            else:
                cursor.execute(query)
            resultado = cursor.fetchall()
            cursor.close()
            return resultado
        except (Exception, pg.Error) as error:
            print("Erro ao realizar a consulta: ", error)
            conn.rollback()
            return []
        finally:
            conn.close()
    else:
        return []


def inicializar_banco():
    query_perdidos = """
    CREATE TABLE IF NOT EXISTS objetos_perdidos (
        id_objeto SERIAL PRIMARY KEY,
        nome_objeto VARCHAR(255) NOT NULL,
        cor VARCHAR(100) NOT NULL,
        data_perdido VARCHAR(50) NOT NULL
    );
    """
    query_achados = """
    CREATE TABLE IF NOT EXISTS objetos_achados (
        id_objetoA SERIAL PRIMARY KEY,
        nome_objeto_achado VARCHAR(255) NOT NULL,
        cor_achado VARCHAR(100) NOT NULL,
        nome_pessoa VARCHAR(255) NOT NULL,
        cpf VARCHAR(14) NOT NULL,
        contato VARCHAR(200) NOT NULL
    );
    """
    executar_consulta(query_perdidos)
    executar_consulta(query_achados)