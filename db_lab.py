#!/usr/bin/env python3
"""
Interactive Database Lab for Relational Algebra & SQL
Covers:
1. Concept Training Exercises (Treino Conceitual por Tópico)
2. Assignment Exercises 1 to 20 from Trabalho Pratico I (Beecrowd)
"""

import sys
import sqlite3
from typing import Dict, Any, List, Tuple

# All exercises: Training ("T1.1", "T1.2", ...) and Assignment (1 to 20 or "1" to "20")
EXERCISES_DATA: Dict[str, Dict[str, Any]] = {
    # =========================================================================
    # MÓDULO 1: TREINOS CONCEITUAIS
    # =========================================================================
    "T1.1": {
        "title": "[Treino: Expressões e Apelidos na Projeção (π)]",
        "type": "treino",
        "topic": "Projeção (π), Cálculos Aritméticos e Renomeação (AS)",
        "setup": """
            CREATE TABLE store_products (
                id INTEGER PRIMARY KEY,
                name TEXT,
                price REAL,
                stock INTEGER
            );
            INSERT INTO store_products VALUES
            (1, 'Notebook Pro', 3000.00, 15),
            (2, 'Mouse Sem Fio', 80.00, 50),
            (3, 'Teclado Mecanico', 250.00, 30),
            (4, 'Monitor 4K', 1500.00, 8);
        """,
        "expected_columns": ["name", "price", "discount_price"],
        "expected_rows": [
            ("Notebook Pro", 3000.00, 2700.00),
            ("Mouse Sem Fio", 80.00, 72.00),
            ("Teclado Mecanico", 250.00, 225.00),
            ("Monitor 4K", 1500.00, 1350.00)
        ]
    },
    "T1.2": {
        "title": "[Treino: Intervalos Contínuos com BETWEEN]",
        "type": "treino",
        "topic": "Seleção (σ) e Predicado de Faixa BETWEEN ... AND ...",
        "setup": """
            CREATE TABLE store_products (
                id INTEGER PRIMARY KEY,
                name TEXT,
                price REAL,
                stock INTEGER
            );
            INSERT INTO store_products VALUES
            (1, 'Notebook Pro', 3000.00, 15),
            (2, 'Mouse Sem Fio', 80.00, 50),
            (3, 'Teclado Mecanico', 250.00, 30),
            (4, 'Monitor 4K', 1500.00, 8);
        """,
        "expected_columns": ["name", "price"],
        "expected_rows": [
            ("Teclado Mecanico", 250.00),
            ("Monitor 4K", 1500.00)
        ]
    },
    "T1.3": {
        "title": "[Treino: Pertença a Conjunto Discreto com IN]",
        "type": "treino",
        "topic": "Seleção (σ) e Pertencimento a Conjunto com IN (...)",
        "setup": """
            CREATE TABLE employees (
                id INTEGER PRIMARY KEY,
                name TEXT,
                department TEXT,
                salary REAL
            );
            INSERT INTO employees VALUES
            (1, 'Ana Silva', 'TI', 6000.00),
            (2, 'Bruno Costa', 'RH', 4500.00),
            (3, 'Carlos Lima', 'Vendas', 5000.00),
            (4, 'Daniela Rocha', 'Financeiro', 7000.00),
            (5, 'Eduardo Santos', 'TI', 6200.00),
            (6, 'Fernanda Sousa', 'Marketing', 4800.00);
        """,
        "expected_columns": ["name", "department"],
        "expected_rows": [
            ("Ana Silva", "TI"),
            ("Bruno Costa", "RH"),
            ("Daniela Rocha", "Financeiro"),
            ("Eduardo Santos", "TI")
        ]
    },
    "T1.4": {
        "title": "[Treino: Busca de Padrões de Texto com LIKE]",
        "type": "treino",
        "topic": "Seleção (σ) e Casamento de Padrões LIKE com Curingas (% e _)",
        "setup": """
            CREATE TABLE clients (
                id INTEGER PRIMARY KEY,
                name TEXT,
                email TEXT,
                city TEXT
            );
            INSERT INTO clients VALUES
            (1, 'Mariana Silva', 'mariana@gmail.com', 'Sao Paulo'),
            (2, 'Marcos Oliveira', 'marcos@empresa.com.br', 'Rio de Janeiro'),
            (3, 'Carla Ramos', 'carla@gmail.com', 'Belo Horizonte'),
            (4, 'Mario Soares', 'mario123@yahoo.com', 'Sao Paulo'),
            (5, 'Patricia Matos', 'patricia@gmail.com', 'Curitiba');
        """,
        "expected_columns": ["name", "email"],
        "expected_rows": [
            ("Mariana Silva", "mariana@gmail.com"),
            ("Marcos Oliveira", "marcos@empresa.com.br"),
            ("Mario Soares", "mario123@yahoo.com")
        ]
    },
    "T1.5": {
        "title": "[Treino: Tratamento de Nulos com IS NULL]",
        "type": "treino",
        "topic": "Lógica Tri-Valorada e Tratamento de Nulos com IS NULL / IS NOT NULL",
        "setup": """
            CREATE TABLE clients_contact (
                id INTEGER PRIMARY KEY,
                name TEXT,
                phone TEXT,
                email TEXT
            );
            INSERT INTO clients_contact VALUES
            (1, 'Lucas Pires', '99111-2222', 'lucas@gmail.com'),
            (2, 'Beatriz Mendes', NULL, 'beatriz@hotmail.com'),
            (3, 'Renato Silva', '98888-5555', NULL),
            (4, 'Camila Duarte', NULL, NULL),
            (5, 'Tiago Souza', '97777-4444', 'tiago@empresa.com');
        """,
        "expected_columns": ["id", "name"],
        "expected_rows": [
            (2, "Beatriz Mendes"),
            (4, "Camila Duarte")
        ]
    },
    "T1.6": {
        "title": "[Treino: Precedência de Operadores Lógicos (NOT, AND, OR)]",
        "type": "treino",
        "topic": "Precedência Booleana (NOT > AND > OR) e Agrupamento com Parênteses",
        "setup": """
            CREATE TABLE employees (
                id INTEGER PRIMARY KEY,
                name TEXT,
                department TEXT,
                salary REAL
            );
            INSERT INTO employees VALUES
            (1, 'Ana Silva', 'TI', 6000.00),
            (2, 'Bruno Costa', 'RH', 4500.00),
            (3, 'Carlos Lima', 'Vendas', 5000.00),
            (4, 'Daniela Rocha', 'Financeiro', 7000.00),
            (5, 'Eduardo Santos', 'TI', 6200.00),
            (6, 'Fernanda Sousa', 'Marketing', 4800.00);
        """,
        "expected_columns": ["name", "department", "salary"],
        "expected_rows": [
            ("Ana Silva", "TI", 6000.00),
            ("Eduardo Santos", "TI", 6200.00)
        ]
    },

    # =========================================================================
    # MÓDULO 2: TREINOS CONCEITUAIS
    # =========================================================================
    "T2.1": {
        "title": "[Treino: Contagem Total vs Contagem de Atributo Não-Nulo]",
        "type": "treino",
        "topic": "Agregação γ: Diferença semântica entre COUNT(*) e COUNT(coluna)",
        "setup": """
            CREATE TABLE members (
                id INTEGER PRIMARY KEY,
                name TEXT,
                email TEXT
            );
            INSERT INTO members VALUES
            (1, 'Alice', 'alice@test.com'),
            (2, 'Bob', NULL),
            (3, 'Charlie', 'charlie@test.com'),
            (4, 'David', NULL),
            (5, 'Eva', 'eva@test.com');
        """,
        "expected_columns": ["total_members", "members_with_email"],
        "expected_rows": [
            (5, 3)
        ]
    },
    "T2.2": {
        "title": "[Treino: Contagem de Valores Únicos com COUNT(DISTINCT)]",
        "type": "treino",
        "topic": "Agregação γ com Eliminação Prévia de Duplicatas",
        "setup": """
            CREATE TABLE orders_sample (
                id INTEGER PRIMARY KEY,
                client_id INTEGER,
                order_date TEXT
            );
            INSERT INTO orders_sample VALUES
            (1, 10, '2023-01-01'),
            (2, 20, '2023-01-02'),
            (3, 10, '2023-01-03'),
            (4, 30, '2023-01-04'),
            (5, 20, '2023-01-05');
        """,
        "expected_columns": ["unique_buyers"],
        "expected_rows": [
            (3,)
        ]
    },
    "T2.3": {
        "title": "[Treino: Múltiplas Agregações Globais e Arredondamento]",
        "type": "treino",
        "topic": "Agregação γ: MIN, MAX, SUM e ROUND(AVG, 2)",
        "setup": """
            CREATE TABLE sales (
                id INTEGER PRIMARY KEY,
                amount REAL
            );
            INSERT INTO sales VALUES
            (1, 100.00),
            (2, 250.50),
            (3, 80.00),
            (4, 320.00),
            (5, 140.25);
        """,
        "expected_columns": ["menor", "maior", "soma", "media"],
        "expected_rows": [
            (80.00, 320.00, 890.75, 178.15)
        ]
    },

    # =========================================================================
    # MÓDULO 3: TREINOS CONCEITUAIS
    # =========================================================================
    "T3.1": {
        "title": "[Treino: Equi-Join Básico de 2 Tabelas com Apelidos]",
        "type": "treino",
        "topic": "Junção Relacional (⨝): Conexão PK = FK e Apelidos de Tabela",
        "setup": """
            CREATE TABLE depts (
                id INTEGER PRIMARY KEY,
                dept_name TEXT
            );
            INSERT INTO depts VALUES (1, 'Tecnologia'), (2, 'Financeiro');

            CREATE TABLE staff (
                id INTEGER PRIMARY KEY,
                name TEXT,
                dept_id INTEGER
            );
            INSERT INTO staff VALUES
            (10, 'Alice', 1),
            (11, 'Bob', 2),
            (12, 'Carol', 1);
        """,
        "expected_columns": ["name", "dept_name"],
        "expected_rows": [
            ("Alice", "Tecnologia"),
            ("Bob", "Financeiro"),
            ("Carol", "Tecnologia")
        ]
    },
    "T3.2": {
        "title": "[Treino: Junção com Filtro no WHERE em Tabela Relacionada]",
        "type": "treino",
        "topic": "Composição: Junção ⨝ combinada com Seleção σ no WHERE",
        "setup": """
            CREATE TABLE depts (
                id INTEGER PRIMARY KEY,
                dept_name TEXT
            );
            INSERT INTO depts VALUES (1, 'Tecnologia'), (2, 'Financeiro');

            CREATE TABLE staff (
                id INTEGER PRIMARY KEY,
                name TEXT,
                dept_id INTEGER
            );
            INSERT INTO staff VALUES
            (10, 'Alice', 1),
            (11, 'Bob', 2),
            (12, 'Carol', 1);
        """,
        "expected_columns": ["name"],
        "expected_rows": [
            ("Alice",),
            ("Carol",)
        ]
    },
    "T3.3": {
        "title": "[Treino: Junção Encadeada de 3 Tabelas com Desambiguação]",
        "type": "treino",
        "topic": "Multi-Join ((A ⨝ B) ⨝ C) e Desambiguação de Atributos Homônimos",
        "setup": """
            CREATE TABLE courses (
                id INTEGER PRIMARY KEY,
                title TEXT
            );
            INSERT INTO courses VALUES (101, 'Banco de Dados'), (102, 'Redes');

            CREATE TABLE students (
                id INTEGER PRIMARY KEY,
                name TEXT
            );
            INSERT INTO students VALUES (1, 'Juliana'), (2, 'Marcos');

            CREATE TABLE enrollments (
                student_id INTEGER,
                course_id INTEGER,
                grade REAL
            );
            INSERT INTO enrollments VALUES
            (1, 101, 9.5),
            (2, 101, 8.0),
            (1, 102, 10.0);
        """,
        "expected_columns": ["student_name", "course_title", "grade"],
        "expected_rows": [
            ("Juliana", "Banco de Dados", 9.5),
            ("Marcos", "Banco de Dados", 8.0),
            ("Juliana", "Redes", 10.0)
        ]
    },

    # =========================================================================
    # MÓDULO 4: TREINOS CONCEITUAIS
    # =========================================================================
    "T4.1": {
        "title": "[Treino: Agrupamento Básico com GROUP BY e COUNT(*)]",
        "type": "treino",
        "topic": "Agrupamento (_{G}γ_{F}): Particionamento em Baldes e Contagem por Grupo",
        "setup": """
            CREATE TABLE inventory (
                id INTEGER PRIMARY KEY,
                item_name TEXT,
                category TEXT
            );
            INSERT INTO inventory VALUES
            (1, 'Mouse', 'Perifericos'),
            (2, 'Teclado', 'Perifericos'),
            (3, 'Monitor', 'Monitores'),
            (4, 'Headset', 'Perifericos'),
            (5, 'Monitor Ultrawide', 'Monitores');
        """,
        "expected_columns": ["category", "total_items"],
        "expected_rows": [
            ("Monitores", 2),
            ("Perifericos", 3)
        ]
    },
    "T4.2": {
        "title": "[Treino: Filtro de Grupos com HAVING (COUNT >= N)]",
        "type": "treino",
        "topic": "Filtro Pós-Agrupamento (HAVING) vs Filtro de Tupla (WHERE)",
        "setup": """
            CREATE TABLE inventory (
                id INTEGER PRIMARY KEY,
                item_name TEXT,
                category TEXT
            );
            INSERT INTO inventory VALUES
            (1, 'Mouse', 'Perifericos'),
            (2, 'Teclado', 'Perifericos'),
            (3, 'Monitor', 'Monitores'),
            (4, 'Headset', 'Perifericos'),
            (5, 'Monitor Ultrawide', 'Monitores');
        """,
        "expected_columns": ["category", "total_items"],
        "expected_rows": [
            ("Perifericos", 3)
        ]
    },

    # =========================================================================
    # MÓDULO 5: TREINOS CONCEITUAIS
    # =========================================================================
    "T5.1": {
        "title": "[Treino: Ordenação Ascendente e Descendente (ORDER BY)]",
        "type": "treino",
        "topic": "Operador Tau (τ): Multi-Column Ordering (ASC e DESC)",
        "setup": """
            CREATE TABLE players (
                id INTEGER PRIMARY KEY,
                name TEXT,
                score INTEGER,
                age INTEGER
            );
            INSERT INTO players VALUES
            (1, 'Arthur', 100, 20),
            (2, 'Beatriz', 150, 22),
            (3, 'Carlos', 150, 19),
            (4, 'Diana', 90, 25);
        """,
        "expected_columns": ["name", "score", "age"],
        "expected_rows": [
            ("Carlos", 150, 19),
            ("Beatriz", 150, 22),
            ("Arthur", 100, 20),
            ("Diana", 90, 25)
        ]
    },
    "T5.2": {
        "title": "[Treino: Filtragem de Intervalos de Datas (ISO 8601)]",
        "type": "treino",
        "topic": "Filtro Temporal: Comparações Cronológicas Diretas (>= e <=)",
        "setup": """
            CREATE TABLE logs (
                id INTEGER PRIMARY KEY,
                event TEXT,
                log_date TEXT
            );
            INSERT INTO logs VALUES
            (1, 'Login', '2023-05-01'),
            (2, 'Upload', '2023-05-15'),
            (3, 'Logout', '2023-05-31'),
            (4, 'Login', '2023-06-05');
        """,
        "expected_columns": ["event", "log_date"],
        "expected_rows": [
            ("Login", "2023-05-01"),
            ("Upload", "2023-05-15"),
            ("Logout", "2023-05-31")
        ]
    },

    # =========================================================================
    # MÓDULO 6: TREINOS CONCEITUAIS
    # =========================================================================
    "T6.1": {
        "title": "[Treino: Anti-Junção com LEFT JOIN + IS NULL]",
        "type": "treino",
        "topic": "Anti-Junção (▷) / Diferença (-): Tuplas em A que não existem em B",
        "setup": """
            CREATE TABLE users (
                id INTEGER PRIMARY KEY,
                name TEXT
            );
            INSERT INTO users VALUES (1, 'Vitor'), (2, 'Lorena'), (3, 'Gabriel');

            CREATE TABLE purchases (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                amount REAL
            );
            INSERT INTO purchases VALUES (101, 1, 50.0), (102, 3, 120.0);
        """,
        "expected_columns": ["id", "name"],
        "expected_rows": [
            (2, "Lorena")
        ]
    },
    "T6.2": {
        "title": "[Treino: Empilhamento de Conjuntos com UNION ALL]",
        "type": "treino",
        "topic": "União de Relações (∪): Empilhamento Vertical de Consultas",
        "setup": """
            CREATE TABLE north_sales (
                seller TEXT,
                total REAL
            );
            INSERT INTO north_sales VALUES ('Amanda', 500.0), ('Bernardo', 750.0);

            CREATE TABLE south_sales (
                seller TEXT,
                total REAL
            );
            INSERT INTO south_sales VALUES ('Caio', 300.0), ('Debora', 820.0);
        """,
        "expected_columns": ["seller", "total"],
        "expected_rows": [
            ("Amanda", 500.0),
            ("Bernardo", 750.0),
            ("Caio", 300.0),
            ("Debora", 820.0)
        ]
    },

    # =========================================================================
    # MÓDULO 7: TREINOS CONCEITUAIS
    # =========================================================================
    "T7.1": {
        "title": "[Treino: Transformação Condicional com CASE WHEN]",
        "type": "treino",
        "topic": "Lógica Condicional (IF-ELSE Relacional) na Projeção",
        "setup": """
            CREATE TABLE students_notes (
                id INTEGER PRIMARY KEY,
                name TEXT,
                score REAL
            );
            INSERT INTO students_notes VALUES
            (1, 'Felipe', 8.5),
            (2, 'Gisele', 4.0),
            (3, 'Heitor', 6.0);
        """,
        "expected_columns": ["name", "status"],
        "expected_rows": [
            ("Felipe", "Aprovado"),
            ("Gisele", "Reprovado"),
            ("Heitor", "Recuperacao")
        ]
    },
    "T7.2": {
        "title": "[Treino: Substituição Segura de Nulos com COALESCE]",
        "type": "treino",
        "topic": "Tratamento de Nulos em Cálculos Aritméticos com COALESCE(col, fallback)",
        "setup": """
            CREATE TABLE accounts (
                id INTEGER PRIMARY KEY,
                holder TEXT,
                balance REAL,
                bonus REAL
            );
            INSERT INTO accounts VALUES
            (1, 'Igor', 1000.0, 200.0),
            (2, 'Joana', 1500.0, NULL),
            (3, 'Katia', 800.0, 50.0);
        """,
        "expected_columns": ["holder", "total_funds"],
        "expected_rows": [
            ("Igor", 1200.0),
            ("Joana", 1500.0),
            ("Katia", 850.0)
        ]
    },

    # =========================================================================
    # EXERCÍCIOS OFICIAIS DO PDF (1 A 20 — BEECROWD)
    # =========================================================================
    "1": {
        "title": "Clientes por Estado (Beecrowd 2602)",
        "type": "oficial",
        "setup": """
            CREATE TABLE customers (
                id INTEGER PRIMARY KEY,
                name TEXT,
                street TEXT,
                city TEXT,
                state TEXT,
                credit_limit REAL
            );
            INSERT INTO customers VALUES
            (1, 'Pedro Augusto da Rocha', 'Rua Pedro Carlos Hoffman', 'Porto Alegre', 'RS', 700.00),
            (2, 'Antonio Carlos Mamel', 'Av. Pinheiros', 'Belo Horizonte', 'MG', 3500.50),
            (3, 'Luiza Augusta Mhor', 'Rua Salto Grande', 'Niteroi', 'RJ', 4000.00),
            (4, 'Jane Ester', 'Av 7 de setembro', 'Erechim', 'RS', 800.00),
            (5, 'Marcos Antônio dos Santos', 'Av Farrapos', 'Porto Alegre', 'RS', 4250.25);
        """,
        "expected_columns": ["name"],
        "expected_rows": [
            ("Pedro Augusto da Rocha",),
            ("Jane Ester",),
            ("Marcos Antônio dos Santos",)
        ]
    },
    "2": {
        "title": "Under 10 or Greater Than 100 (Beecrowd 2604)",
        "type": "oficial",
        "setup": """
            CREATE TABLE products (
                id INTEGER PRIMARY KEY,
                name TEXT,
                amount INTEGER,
                price REAL
            );
            INSERT INTO products VALUES
            (1, 'Two-door wardrobe', 100, 80),
            (2, 'Dining table', 1000, 560),
            (3, 'Towel holder', 10000, 5.50),
            (4, 'Computer desk', 350, 100),
            (5, 'Chair', 3000, 210.64),
            (6, 'Single bed', 750, 99);
        """,
        "expected_columns": ["id", "name"],
        "expected_rows": [
            (2, "Dining table"),
            (3, "Towel holder"),
            (5, "Chair")
        ]
    },
    "3": {
        "title": "Higher and Lower Price (Beecrowd 2608)",
        "type": "oficial",
        "setup": """
            CREATE TABLE products (
                id INTEGER PRIMARY KEY,
                name TEXT,
                amount INTEGER,
                price REAL
            );
            INSERT INTO products VALUES
            (1, 'Two-doors wardrobe', 100, 800),
            (2, 'Dining table', 1000, 560),
            (3, 'Towel holder', 10000, 25.50),
            (4, 'Computer desk', 350, 320.50),
            (5, 'Chair', 3000, 210.64),
            (6, 'Single bed', 750, 460);
        """,
        "expected_columns": ["price (maior)", "price (menor)"],
        "expected_rows": [
            (800.0, 25.50)
        ]
    },
    "4": {
        "title": "Average Value of Products (Beecrowd 2610)",
        "type": "oficial",
        "setup": """
            CREATE TABLE products (
                id INTEGER PRIMARY KEY,
                name TEXT,
                amount INTEGER,
                price REAL
            );
            INSERT INTO products VALUES
            (1, 'Two-doors wardrobe', 100, 800),
            (2, 'Dining table', 1000, 560),
            (3, 'Towel holder', 10000, 25.50),
            (4, 'Computer desk', 350, 320.50),
            (5, 'Chair', 3000, 210.64),
            (6, 'Single bed', 750, 460);
        """,
        "expected_columns": ["price"],
        "expected_rows": [
            (396.10,)
        ]
    },
    "5": {
        "title": "Number of Cities per Customers (Beecrowd 2624)",
        "type": "oficial",
        "setup": """
            CREATE TABLE customers (
                id INTEGER PRIMARY KEY,
                name TEXT,
                street TEXT,
                city TEXT,
                state TEXT,
                credit_limit REAL
            );
            INSERT INTO customers VALUES
            (1, 'Nicolas Diogo Cardoso', 'Acesso Um', 'Porto Alegre', 'RS', 475),
            (2, 'Cecília Olivia Rodrigues', 'Rua Sizuka Usuy', 'Cianorte', 'PR', 3170),
            (3, 'Augusto Fernando Carlos Eduardo Cardoso', 'Rua Baldomiro Koerich', 'Palhoça', 'SC', 1067),
            (4, 'Nicolas Diogo Cardoso', 'Acesso Um', 'Porto Alegre', 'RS', 475),
            (5, 'Sabrina Heloisa Gabriela Barros', 'Rua Engenheiro Tito Marques Fernandes', 'Porto Alegre', 'RS', 4312),
            (6, 'Joaquim Diego Lorenzo Araújo', 'Rua Vitorino', 'Novo Hamburgo', 'RS', 2314);
        """,
        "expected_columns": ["count"],
        "expected_rows": [
            (4,)
        ]
    },
    "6": {
        "title": "Legal Person (Beecrowd 2622)",
        "type": "oficial",
        "setup": """
            CREATE TABLE customers (
                id INTEGER PRIMARY KEY,
                name TEXT,
                street TEXT,
                city TEXT,
                state TEXT,
                credit_limit REAL
            );
            INSERT INTO customers VALUES
            (1, 'Nicolas Diogo Cardoso', 'Acesso Um', 'Porto Alegre', 'RS', 475),
            (2, 'Cecília Olivia Rodrigues', 'Rua Sizuka Usuy', 'Cianorte', 'PR', 3170),
            (3, 'Augusto Fernando Carlos Eduardo Cardoso', 'Rua Baldomiro Koerich', 'Palhoça', 'SC', 1067),
            (4, 'Nicolas Diogo Cardoso', 'Acesso Um', 'Porto Alegre', 'RS', 475),
            (5, 'Sabrina Heloisa Gabriela Barros', 'Rua Engenheiro Tito Marques Fernandes', 'Porto Alegre', 'RS', 4312),
            (6, 'Joaquim Diego Lorenzo Araújo', 'Rua Vitorino', 'Novo Hamburgo', 'RS', 2314);

            CREATE TABLE legal_person (
                id_customers INTEGER,
                cnpj TEXT,
                contact TEXT
            );
            INSERT INTO legal_person VALUES
            (4, '85883842000191', '99767-0562'),
            (5, '47773848000117', '99100-8965');
        """,
        "expected_columns": ["name"],
        "expected_rows": [
            ("Nicolas Diogo Cardoso",),
            ("Sabrina Heloisa Gabriela Barros",)
        ]
    },
    "7": {
        "title": "Executive Representatives (Beecrowd 2605)",
        "type": "oficial",
        "setup": """
            CREATE TABLE products (
                id INTEGER PRIMARY KEY,
                name TEXT,
                amount INTEGER,
                price REAL,
                id_providers INTEGER,
                id_categories INTEGER
            );
            INSERT INTO products VALUES
            (1, 'Two-door wardrobe', 100, 800, 6, 8),
            (2, 'Dining table', 1000, 560, 1, 9),
            (3, 'Towel holder', 10000, 25.50, 5, 1),
            (4, 'Computer desk', 350, 320.50, 4, 6),
            (5, 'Chair', 3000, 210.64, 3, 6),
            (6, 'Single bed', 750, 460, 1, 2);

            CREATE TABLE providers (
                id INTEGER PRIMARY KEY,
                name TEXT,
                street TEXT,
                city TEXT,
                state TEXT
            );
            INSERT INTO providers VALUES
            (1, 'Henrique', 'Av Brasil', 'Rio de Janeiro', 'RJ'),
            (2, 'Marcelo Augusto', 'Rua Imigrantes', 'Belo Horizonte', 'MG'),
            (3, 'Caroline Silva', 'Av São Paulo', 'Salvador', 'BA'),
            (4, 'Guilerme Staff', 'Rua Central', 'Porto Alegre', 'RS'),
            (5, 'Isabela Moraes', 'Av Juiz Grande', 'Curitiba', 'PR'),
            (6, 'Francisco Accerr', 'Av Paulista', 'São Paulo', 'SP');

            CREATE TABLE categories (
                id INTEGER PRIMARY KEY,
                name TEXT
            );
            INSERT INTO categories VALUES
            (1, 'old stock'), (2, 'new stock'), (3, 'modern'), (4, 'commercial'),
            (5, 'recyclable'), (6, 'executive'), (7, 'superior'), (8, 'wood'),
            (9, 'super luxury'), (10, 'vintage');
        """,
        "expected_columns": ["name (produto)", "name (fornecedor)"],
        "expected_rows": [
            ("Computer desk", "Guilerme Staff"),
            ("Chair", "Caroline Silva")
        ]
    },
    "8": {
        "title": "Action Movies (Beecrowd 2611)",
        "type": "oficial",
        "setup": """
            CREATE TABLE movies (
                id INTEGER PRIMARY KEY,
                name TEXT,
                id_genres INTEGER
            );
            INSERT INTO movies VALUES
            (1, 'Batman', 3),
            (2, 'The Battle of the Dark River', 3),
            (3, 'White Duck', 1),
            (4, 'Breaking Barriers', 4),
            (5, 'The Two Hours', 2);

            CREATE TABLE genres (
                id INTEGER PRIMARY KEY,
                description TEXT
            );
            INSERT INTO genres VALUES
            (1, 'Animation'), (2, 'Horror'), (3, 'Action'), (4, 'Drama'), (5, 'Comedy');
        """,
        "expected_columns": ["id", "name"],
        "expected_rows": [
            (1, "Batman"),
            (2, "The Battle of the Dark River")
        ]
    },
    "9": {
        "title": "Provider Ajax SA (Beecrowd 2617)",
        "type": "oficial",
        "setup": """
            CREATE TABLE providers (
                id INTEGER PRIMARY KEY,
                name TEXT,
                street TEXT,
                city TEXT,
                state TEXT
            );
            INSERT INTO providers VALUES
            (1, 'Ajax SA', 'Presidente Castelo Branco', 'Porto Alegre', 'RS'),
            (2, 'Sansul SA', 'Av Brasil', 'Rio de Janeiro', 'RJ'),
            (3, 'South Chairs', 'Av Moinho', 'Santa Maria', 'RS'),
            (4, 'Elon Electro', 'Apolo', 'São Paulo', 'SP'),
            (5, 'Mike Electro', 'Pedro da Cunha', 'Curitiba', 'PR');

            CREATE TABLE products (
                id INTEGER PRIMARY KEY,
                name TEXT,
                amount INTEGER,
                value REAL,
                id_providers INTEGER
            );
            INSERT INTO products VALUES
            (1, 'Blue Chair', 30, 300.00, 5),
            (2, 'Red Chair', 50, 2150.00, 1),
            (3, 'Disney Wardrobe', 400, 829.50, 4),
            (4, 'Blue Toaster', 20, 9.90, 3),
            (5, 'Solar Panel', 30, 3000.25, 4);
        """,
        "expected_columns": ["name (produto)", "name (fornecedor)"],
        "expected_rows": [
            ("Red Chair", "Ajax SA")
        ]
    },
    "10": {
        "title": "Products by Categories (Beecrowd 2609)",
        "type": "oficial",
        "setup": """
            CREATE TABLE products (
                id INTEGER PRIMARY KEY,
                name TEXT,
                amount INTEGER,
                price REAL,
                id_categories INTEGER
            );
            INSERT INTO products VALUES
            (1, 'Two-doors wardrobe', 100, 800, 1),
            (2, 'Dining table', 1000, 560, 3),
            (3, 'Towel holder', 10000, 25.50, 4),
            (4, 'Computer desk', 350, 320.50, 2),
            (5, 'Chair', 3000, 210.64, 4),
            (6, 'Single bed', 750, 460, 1);

            CREATE TABLE categories (
                id INTEGER PRIMARY KEY,
                name TEXT
            );
            INSERT INTO categories VALUES
            (1, 'wood'), (2, 'luxury'), (3, 'vintage'), (4, 'modern'), (5, 'super luxury');
        """,
        "expected_columns": ["name", "sum"],
        "expected_rows": [
            ("luxury", 350),
            ("modern", 13000),
            ("wood", 850),
            ("vintage", 1000)
        ]
    },
    "11": {
        "title": "September Rentals (Beecrowd 2614)",
        "type": "oficial",
        "setup": """
            CREATE TABLE customers (
                id INTEGER PRIMARY KEY,
                name TEXT,
                street TEXT,
                city TEXT
            );
            INSERT INTO customers VALUES
            (1, 'Giovanna Gonçalves Oliveira', 'Rua Mato Grosso', 'Canoas'),
            (2, 'Kauã Azevedo Ribeiro', 'Travessa Ibiá', 'Uberlândia'),
            (3, 'Rebeca Barbosa Santos', 'Rua Observatório Meteorológico', 'Salvador'),
            (4, 'Sarah Carvalho Correia', 'Rua Antônio Carlos da Silva', 'Apucarana'),
            (5, 'João Almeida Lima', 'Rua Rio Taiuva', 'Ponta Grossa'),
            (6, 'Diogo Melo Dias', 'Rua Duzentos e Cinqüenta', 'Várzea Grande');

            CREATE TABLE rentals (
                id INTEGER PRIMARY KEY,
                rentals_date TEXT,
                id_customers INTEGER
            );
            INSERT INTO rentals VALUES
            (1, '2016-09-10', 3),
            (2, '2016-02-09', 1),
            (3, '2016-02-08', 4),
            (4, '2016-09-09', 2),
            (5, '2016-02-03', 6),
            (6, '2016-04-04', 4);
        """,
        "expected_columns": ["name", "rentals_date"],
        "expected_rows": [
            ("Rebeca Barbosa Santos", "2016-09-10"),
            ("Kauã Azevedo Ribeiro", "2016-09-09")
        ]
    },
    "12": {
        "title": "Orders in First Half (Beecrowd 2620)",
        "type": "oficial",
        "setup": """
            CREATE TABLE customers (
                id INTEGER PRIMARY KEY,
                name TEXT,
                street TEXT,
                city TEXT,
                state TEXT,
                credit_limit REAL
            );
            INSERT INTO customers VALUES
            (1, 'Nicolas Diogo Cardoso', 'Acesso Um', 'Porto Alegre', 'RS', 475),
            (2, 'Cecília Olivia Rodrigues', 'Rua Sizuka Usuy', 'Cianorte', 'PR', 3170),
            (3, 'Augusto Fernando Carlos Eduardo Cardoso', 'Rua Baldomiro Koerich', 'Palhoça', 'SC', 1067),
            (4, 'Nicolas Diogo Cardoso', 'Acesso Um', 'Porto Alegre', 'RS', 475),
            (5, 'Sabrina Heloisa Gabriela Barros', 'Rua Engenheiro Tito Marques Fernandes', 'Porto Alegre', 'RS', 4312),
            (6, 'Joaquim Diego Lorenzo Araújo', 'Rua Vitorino', 'Novo Hamburgo', 'RS', 2314);

            CREATE TABLE orders (
                id INTEGER PRIMARY KEY,
                orders_date TEXT,
                id_customers INTEGER
            );
            INSERT INTO orders VALUES
            (1, '2016-05-13', 3),
            (2, '2016-01-12', 2),
            (3, '2016-04-18', 5),
            (4, '2016-09-07', 4),
            (5, '2016-02-13', 6),
            (6, '2016-08-05', 3);
        """,
        "expected_columns": ["name", "id (pedido)"],
        "expected_rows": [
            ("Augusto Fernando Carlos Eduardo Cardoso", 1),
            ("Cecília Olivia Rodrigues", 2),
            ("Sabrina Heloisa Gabriela Barros", 3),
            ("Joaquim Diego Lorenzo Araújo", 5)
        ]
    },
    "13": {
        "title": "Lawyers (Beecrowd 2737)",
        "type": "oficial",
        "setup": """
            CREATE TABLE lawyers (
                register INTEGER PRIMARY KEY,
                name TEXT,
                customers_number INTEGER
            );
            INSERT INTO lawyers VALUES
            (1648, 'Marty M. Harrison', 5),
            (2427, 'Jonathan J. Blevins', 15),
            (3365, 'Chelsey D. Sanders', 20),
            (4153, 'Dorothy W. Ford', 16),
            (5525, 'Penny J. Cormier', 6);
        """,
        "expected_columns": ["name", "customers_number"],
        "expected_rows": [
            ("Chelsey D. Sanders", 20),
            ("Marty M. Harrison", 5),
            ("Average", 12)
        ]
    },
    "14": {
        "title": "Most Frequent Value (Beecrowd 2993)",
        "type": "oficial",
        "setup": """
            CREATE TABLE value_table (
                amount INTEGER
            );
            INSERT INTO value_table VALUES
            (4),(6),(7),(1),(1),(2),(3),(2),(3),(1),(5),(6),(1),(7),(8),(9),(10),(11),(12),(4),(5),(5),(3),(6),(2),(2),(1);
        """,
        "expected_columns": ["most_frequent_value"],
        "expected_rows": [
            (1,)
        ]
    },
    "15": {
        "title": "Imported Products (Beecrowd 2618)",
        "type": "oficial",
        "setup": """
            CREATE TABLE products (
                id INTEGER PRIMARY KEY,
                name TEXT,
                amount INTEGER,
                price REAL,
                id_providers INTEGER,
                id_categories INTEGER
            );
            INSERT INTO products VALUES
            (1, 'Blue Chair', 30, 300.00, 5, 5),
            (2, 'Red Chair', 50, 2150.00, 2, 1),
            (3, 'Disney Wardrobe', 400, 829.50, 4, 1),
            (4, 'Blue Toaster', 20, 9.90, 3, 1),
            (5, 'TV', 30, 3000.25, 2, 2);

            CREATE TABLE providers (
                id INTEGER PRIMARY KEY,
                name TEXT,
                street TEXT,
                city TEXT,
                state TEXT
            );
            INSERT INTO providers VALUES
            (1, 'Ajax SA', 'Rua Presidente Castelo Branco', 'Porto Alegre', 'RS'),
            (2, 'Sansul SA', 'Av Brasil', 'Rio de Janeiro', 'RJ'),
            (3, 'South Chairs', 'Rua do Moinho', 'Santa Maria', 'RS'),
            (4, 'Elon Electro', 'Rua Apolo', 'São Paulo', 'SP'),
            (5, 'Mike Electro', 'Pedro da Cunha', 'Curitiba', 'PR');

            CREATE TABLE categories (
                id INTEGER PRIMARY KEY,
                name TEXT
            );
            INSERT INTO categories VALUES
            (1, 'Super Luxury'), (2, 'Imported'), (3, 'Tech'), (4, 'Vintage'), (5, 'Supreme');
        """,
        "expected_columns": ["name (produto)", "name (fornecedor)", "name (categoria)"],
        "expected_rows": [
            ("TV", "Sansul SA", "Imported")
        ]
    },
    "16": {
        "title": "Categories with Various Products (Beecrowd 2623)",
        "type": "oficial",
        "setup": """
            CREATE TABLE products (
                id INTEGER PRIMARY KEY,
                name TEXT,
                amount INTEGER,
                price REAL,
                id_categories INTEGER
            );
            INSERT INTO products VALUES
            (1, 'Blue Chair', 30, 300.00, 9),
            (2, 'Red Chair', 200, 2150.00, 2),
            (3, 'Disney Wardrobe', 400, 829.50, 4),
            (4, 'Blue Toaster', 20, 9.90, 3),
            (5, 'Solar Panel', 30, 3000.25, 4);

            CREATE TABLE categories (
                id INTEGER PRIMARY KEY,
                name TEXT
            );
            INSERT INTO categories VALUES
            (1, 'Superior'), (2, 'Super Luxury'), (3, 'Modern'),
            (4, 'Nerd'), (5, 'Infantile'), (6, 'Robust'), (9, 'Wood');
        """,
        "expected_columns": ["name (produto)", "name (categoria)"],
        "expected_rows": [
            ("Red Chair", "Super Luxury")
        ]
    },
    "17": {
        "title": "Categorias com Muitos Produtos (Custom)",
        "type": "oficial",
        "setup": """
            CREATE TABLE products (
                id INTEGER PRIMARY KEY,
                name TEXT,
                amount INTEGER,
                id_categories INTEGER
            );
            INSERT INTO products VALUES
            (1, 'TV', 5, 1),
            (2, 'Notebook', 3, 1),
            (3, 'Cadeira', 2, 2),
            (4, 'Mesa', 1, 2),
            (5, 'Sofá', 4, 2),
            (6, 'Vaso', 6, 3),
            (7, 'Caderno', 10, 4);

            CREATE TABLE categories (
                id INTEGER PRIMARY KEY,
                name TEXT
            );
            INSERT INTO categories VALUES
            (1, 'Eletronicos'), (2, 'Moveis'), (3, 'Decoracao'), (4, 'Papelaria');
        """,
        "expected_columns": ["name", "count"],
        "expected_rows": [
            ("Moveis", 3)
        ]
    },
    "18": {
        "title": "No Rental (Beecrowd 2616)",
        "type": "oficial",
        "setup": """
            CREATE TABLE customers (
                id INTEGER PRIMARY KEY,
                name TEXT,
                street TEXT,
                city TEXT
            );
            INSERT INTO customers VALUES
            (1, 'Giovanna Concalves Oliveira', 'Rua Mato Grosso', 'Canoas'),
            (2, 'Kauã Azevedo Ribeiro', 'Travessa Ibiá', 'Uberlândia'),
            (3, 'Rebeca Barbosa Santos', 'Rua Observatório Meteorológico', 'Salvador'),
            (4, 'Sarah Carvalho Correia', 'Rua Antônio Carlos da Silva', 'Apucarana'),
            (5, 'João Almeida Lima', 'Rua Rio Taiuva', 'Ponta Grossa'),
            (6, 'Diogo Melo Dias', 'Rua Duzentos e Cinqüenta', 'Várzea Grande');

            CREATE TABLE locations (
                id INTEGER PRIMARY KEY,
                locations_date TEXT,
                id_customers INTEGER
            );
            INSERT INTO locations VALUES
            (1, '2016-10-09', 3),
            (2, '2016-09-02', 1),
            (3, '2016-08-02', 4),
            (4, '2016-09-02', 2),
            (5, '2016-03-02', 6),
            (6, '2016-04-04', 4);
        """,
        "expected_columns": ["id", "name"],
        "expected_rows": [
            (5, "João Almeida Lima")
        ]
    },
    "19": {
        "title": "Campeonato Cearense (Beecrowd 2988)",
        "type": "oficial",
        "setup": """
            CREATE TABLE teams (
                id INTEGER PRIMARY KEY,
                name TEXT
            );
            INSERT INTO teams VALUES
            (1, 'CEARA'), (2, 'FORTALEZA'), (3, 'GUARANY DE SOBRAL'), (4, 'FLORESTA');

            CREATE TABLE matches (
                id INTEGER PRIMARY KEY,
                team_1 INTEGER,
                team_2 INTEGER,
                team_1_goals INTEGER,
                team_2_goals INTEGER
            );
            INSERT INTO matches VALUES
            (1, 4, 1, 0, 4),
            (2, 3, 2, 0, 1),
            (3, 1, 3, 3, 0),
            (4, 3, 4, 0, 1),
            (5, 1, 2, 0, 0),
            (6, 2, 4, 2, 1);
        """,
        "expected_columns": ["name", "matches", "victories", "defeats", "draws", "score"],
        "expected_rows": [
            ("CEARA", 3, 2, 0, 1, 7),
            ("FORTALEZA", 3, 2, 0, 1, 7),
            ("FLORESTA", 3, 1, 2, 0, 3),
            ("GUARANY DE SOBRAL", 3, 0, 3, 0, 0)
        ]
    },
    "20": {
        "title": "Department Statistics (Beecrowd 2991)",
        "type": "oficial",
        "setup": """
            CREATE TABLE departamento (
                cod_dep INTEGER PRIMARY KEY,
                nome TEXT,
                endereco TEXT
            );
            INSERT INTO departamento VALUES
            (1, 'Contabilidade', 'R. X'),
            (2, 'TI', 'R. Y'),
            (3, 'Engenharia', 'R. Y');

            CREATE TABLE divisao (
                cod_divisao INTEGER PRIMARY KEY,
                nome TEXT,
                endereco TEXT,
                cod_dep INTEGER
            );
            INSERT INTO divisao VALUES
            (11, 'Ativo', 'R. X', 1),
            (12, 'Passivo', 'R. X', 1),
            (21, 'Desenvolvimento de Projetos', 'R. Y', 2),
            (22, 'Analise de Sistemas', 'R. Y', 2),
            (23, 'Programacao', 'R. W', 2),
            (31, 'Concreto', 'R. Y', 3),
            (32, 'Calculo Estrutural', 'R. Y', 3);

            CREATE TABLE empregado (
                matr INTEGER PRIMARY KEY,
                nome TEXT,
                lotacao INTEGER,
                gerencia_cod_dep INTEGER,
                lotacao_div INTEGER,
                gerencia_div INTEGER
            );
            INSERT INTO empregado VALUES
            (9999, 'Jose Sampaio', 1, 1, 12, NULL),
            (33, 'Jose Maria', 1, NULL, 11, 11),
            (1, 'Maria Jose', 1, NULL, 11, NULL),
            (7, 'Yasmim', 1, NULL, 11, NULL),
            (5, 'Rebeca', 1, NULL, 12, 12),
            (13, 'Sofia', 1, NULL, 12, NULL),
            (27, 'Andre', 2, 2, 22, NULL),
            (88, 'Yami', 2, NULL, 21, 21),
            (431, 'Joao da Silva', 2, NULL, 21, NULL),
            (135, 'Ricardo Reis', 2, NULL, 21, NULL),
            (254, 'Barbara', 2, NULL, 22, 22),
            (371, 'Ines', 2, NULL, 22, NULL),
            (476, 'Flor', 2, NULL, 23, 23),
            (25, 'Lina', 2, NULL, 23, NULL),
            (3, 'Jose da Silva', 3, 3, 31, NULL),
            (71, 'Silverio dos Reis', 3, NULL, 31, 31),
            (91, 'Reis da Silva', 3, NULL, 31, NULL),
            (55, 'Lucas', 3, NULL, 32, 32),
            (222, 'Marina', 3, NULL, 32, NULL),
            (725, 'Angelo', 2, NULL, 21, NULL);

            CREATE TABLE vencimento (
                cod_venc INTEGER PRIMARY KEY,
                nome TEXT,
                tipo TEXT,
                valor REAL
            );
            INSERT INTO vencimento VALUES
            (1, 'Salario base Analista de Sistemas', 'V', 5000),
            (2, 'Salario base Contador', 'V', 3000),
            (3, 'Salario Base Engenheiro', 'V', 4500),
            (4, 'Salario Base Projetista Software', 'V', 5000),
            (5, 'Salario Base Programador de Sistemas', 'V', 3000),
            (6, 'Gratificacao Chefia Departamento', 'V', 3750),
            (7, 'Gratificacao Chefia Divisao', 'V', 2200),
            (8, 'Salario Trabalhador Construcao Civil', 'V', 800),
            (9, 'Auxilio Salario Familia', 'V', 300),
            (10, 'Gratificacao Tempo de servico', 'V', 350),
            (11, 'Insalubridade', 'V', 800),
            (12, 'Gratificacao por titulacao - Doutorado', 'V', 2000),
            (13, 'Gratificacao por Titularidade - Mestrado', 'V', 800);

            CREATE TABLE emp_venc (
                cod_venc INTEGER,
                matr INTEGER
            );
            INSERT INTO emp_venc VALUES
            (1, 27), (3, 71), (7, 254), (12, 3),
            (1, 88), (3, 222), (7, 476), (12, 27),
            (1, 135), (4, 25), (8, 25), (12, 254),
            (1, 254), (4, 476), (8, 91), (12, 9999),
            (1, 431), (5, 371), (9, 1), (13, 3),
            (2, 1), (6, 3), (9, 27), (13, 5),
            (2, 5), (6, 27), (9, 91), (13, 7),
            (2, 7), (6, 9999), (9, 135), (13, 25),
            (2, 13), (7, 5), (9, 371), (13, 33),
            (2, 33), (7, 33), (9, 9999), (13, 88),
            (2, 9999), (7, 55), (10, 371), (13, 135),
            (3, 3), (7, 71), (10, 9999),
            (3, 55), (7, 88), (11, 91);

            CREATE TABLE desconto (
                cod_desc INTEGER PRIMARY KEY,
                nome TEXT,
                tipo TEXT,
                valor REAL
            );
            INSERT INTO desconto VALUES
            (91, 'IR', 'V', 400),
            (92, 'Plano de saude', 'V', 300),
            (93, NULL, NULL, NULL);

            CREATE TABLE emp_desc (
                cod_desc INTEGER,
                matr INTEGER
            );
            INSERT INTO emp_desc VALUES
            (91, 3),
            (91, 27),
            (91, 9999),
            (92, 27),
            (92, 71),
            (92, 88),
            (92, 9999);
        """,
        "expected_columns": ["Nome Departamento", "Numero de Empregados", "Media Salarial", "Maior Salario", "Menor Salario"],
        "expected_rows": [
            ("TI", 9, 6200.00, 10350.00, 0.0),
            ("Engenharia", 5, 6030.00, 10650.00, 1900.00),
            ("Contabilidade", 6, 5133.33, 8700.00, 3000.00)
        ]
    }
}


def get_connection(ex_key: Any) -> sqlite3.Connection:
    key_str = str(ex_key)
    if key_str not in EXERCISES_DATA:
        raise ValueError(f"Exercício/Treino '{ex_key}' não encontrado.")
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    setup_sql = EXERCISES_DATA[key_str]["setup"]
    conn.executescript(setup_sql)
    return conn


def show_schema(ex_key: Any):
    key_str = str(ex_key)
    conn = get_connection(key_str)
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [r[0] for r in cur.fetchall()]
    print(f"\n=======================================================")
    print(f"  {key_str}: {EXERCISES_DATA[key_str]['title']}")
    print(f"=======================================================\n")
    for t in tables:
        print(f"📌 Tabela: {t}")
        cur.execute(f"PRAGMA table_info({t});")
        cols = [f"{c[1]} ({c[2]})" for c in cur.fetchall()]
        print(f"   Colunas: {', '.join(cols)}")
        cur.execute(f"SELECT * FROM {t} LIMIT 5;")
        rows = cur.fetchall()
        for r in rows:
            print(f"   -> {tuple(r)}")
        print()


def run_query(ex_key: Any, query: str):
    key_str = str(ex_key)
    conn = get_connection(key_str)
    cur = conn.cursor()
    try:
        cur.execute(query)
        rows = cur.fetchall()
        headers = [desc[0] for desc in cur.description] if cur.description else []
        print(f"\n--- Resultado da Consulta ({key_str}) ---")
        if headers:
            print(" | ".join(headers))
            print("-" * (len(" | ".join(headers)) + 6))
        for row in rows:
            print(" | ".join(str(val) for val in tuple(row)))
        print(f"\n({len(rows)} linhas retornadas)\n")
    except Exception as e:
        print(f"❌ Erro ao executar SQL: {e}")


def test_query(ex_key: Any, query: str):
    key_str = str(ex_key)
    conn = get_connection(key_str)
    cur = conn.cursor()
    ex = EXERCISES_DATA[key_str]
    try:
        cur.execute(query)
        actual_rows = [tuple(r) for r in cur.fetchall()]
        actual_cols = [desc[0] for desc in cur.description] if cur.description else []
    except Exception as e:
        print(f"❌ Erro de sintaxe/execução SQL: {e}")
        return False

    print(f"\n--- Validação {key_str} ({ex['title']}) ---")
    print(f"Colunas obtidas : {actual_cols}")
    print(f"Colunas esperadas: {ex['expected_columns']}")
    print("\nLinhas obtidas:")
    for r in actual_rows:
        print(f"  {r}")
    print("\nLinhas esperadas:")
    for r in ex['expected_rows']:
        print(f"  {r}")

    match = True
    if len(actual_rows) != len(ex['expected_rows']):
        match = False
    else:
        for r_act, r_exp in zip(actual_rows, ex['expected_rows']):
            if len(r_act) != len(r_exp):
                match = False
                break
            for a, b in zip(r_act, r_exp):
                try:
                    if round(float(a), 2) != round(float(b), 2):
                        match = False
                        break
                except (ValueError, TypeError):
                    if str(a).strip().lower() != str(b).strip().lower():
                        match = False
                        break

    if match:
        print("\n✅ SUCESSO! Resultado 100% correto!")
        return True
    else:
        print("\n⚠️ DIVERGÊNCIA: Verifique valores, nomes de colunas ou ordenação.")
        return False


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso do db_lab.py:")
        print("  python3 db_lab.py list                    -> Listar todos os treinos e exercícios")
        print("  python3 db_lab.py schema <id>             -> Ver tabelas (ex: T1.1 ou 1)")
        print("  python3 db_lab.py run <id> \"<SQL>\"        -> Rodar consulta livre")
        print("  python3 db_lab.py test <id> \"<SQL>\"       -> Testar consulta contra o gabarito")
        sys.exit(0)

    cmd = sys.argv[1].lower()
    if cmd == "list":
        print("\n--- QUESTÕES DE TREINO (Conceito por Conceito) ---")
        for num, data in EXERCISES_DATA.items():
            if data.get("type") == "treino":
                print(f"  {num:5s}: {data['title']}")
        print("\n--- LISTA OFICIAL (Beecrowd / Trabalho) ---")
        for num, data in EXERCISES_DATA.items():
            if data.get("type") == "oficial":
                print(f"  Ex {num:2s}: {data['title']}")
        print()
    elif cmd == "schema":
        if len(sys.argv) < 3:
            print("Informe o ID: python3 db_lab.py schema T1.1 ou python3 db_lab.py schema 1")
            sys.exit(1)
        show_schema(sys.argv[2])
    elif cmd == "run":
        if len(sys.argv) < 4:
            print("Informe ID e query: python3 db_lab.py run T1.1 \"SELECT * FROM store_products\"")
            sys.exit(1)
        run_query(sys.argv[2], sys.argv[3])
    elif cmd == "test":
        if len(sys.argv) < 4:
            print("Informe ID e query: python3 db_lab.py test T1.1 \"SELECT ...\"")
            sys.exit(1)
        test_query(sys.argv[2], sys.argv[3])
