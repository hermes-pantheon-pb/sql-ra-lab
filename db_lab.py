#!/usr/bin/env python3
"""
Interactive Database Lab for Relational Algebra & SQL
Covers Exercises 1 to 20 from Trabalho Pratico I (Introducao a Banco de Dados / Beecrowd)
"""

import sys
import sqlite3
from typing import Dict, Any, List, Tuple

EXERCISES_DATA: Dict[int, Dict[str, Any]] = {
    1: {
        "title": "Clientes por Estado (Beecrowd 2602)",
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
    2: {
        "title": "Under 10 or Greater Than 100 (Beecrowd 2604)",
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
    3: {
        "title": "Higher and Lower Price (Beecrowd 2608)",
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
    4: {
        "title": "Average Value of Products (Beecrowd 2610)",
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
    5: {
        "title": "Number of Cities per Customers (Beecrowd 2624)",
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
    6: {
        "title": "Legal Person (Beecrowd 2622)",
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
    7: {
        "title": "Executive Representatives (Beecrowd 2605)",
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
    8: {
        "title": "Action Movies (Beecrowd 2611)",
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
    9: {
        "title": "Provider Ajax SA (Beecrowd 2617)",
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
    10: {
        "title": "Products by Categories (Beecrowd 2609)",
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
    11: {
        "title": "September Rentals (Beecrowd 2614)",
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
    12: {
        "title": "Orders in First Half (Beecrowd 2620)",
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
    13: {
        "title": "Lawyers (Beecrowd 2737)",
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
    14: {
        "title": "Most Frequent Value (Beecrowd 2993)",
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
    15: {
        "title": "Imported Products (Beecrowd 2618)",
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
            (5, 'Mike Electro', 'Rua Pedro da Cunha', 'Curitiba', 'PR');

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
    16: {
        "title": "Categories with Various Products (Beecrowd 2623)",
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
    17: {
        "title": "Categorias com Muitos Produtos (Custom)",
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
    18: {
        "title": "No Rental (Beecrowd 2616)",
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
    19: {
        "title": "Campeonato Cearense (Beecrowd 2988)",
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
    20: {
        "title": "Department Statistics (Beecrowd 2991)",
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


def get_connection(ex_num: int) -> sqlite3.Connection:
    if ex_num not in EXERCISES_DATA:
        raise ValueError(f"Exercício {ex_num} não encontrado (1-20 disponíveis).")
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    setup_sql = EXERCISES_DATA[ex_num]["setup"]
    conn.executescript(setup_sql)
    return conn


def show_schema(ex_num: int):
    conn = get_connection(ex_num)
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [r[0] for r in cur.fetchall()]
    print(f"\n=======================================================")
    print(f"  Exercício {ex_num}: {EXERCISES_DATA[ex_num]['title']}")
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


def run_query(ex_num: int, query: str):
    conn = get_connection(ex_num)
    cur = conn.cursor()
    try:
        cur.execute(query)
        rows = cur.fetchall()
        headers = [desc[0] for desc in cur.description] if cur.description else []
        print(f"\n--- Resultado da Consulta (Exercício {ex_num}) ---")
        if headers:
            print(" | ".join(headers))
            print("-" * (len(" | ".join(headers)) + 6))
        for row in rows:
            print(" | ".join(str(val) for val in tuple(row)))
        print(f"\n({len(rows)} linhas retornadas)\n")
    except Exception as e:
        print(f"❌ Erro ao executar SQL: {e}")


def test_query(ex_num: int, query: str):
    conn = get_connection(ex_num)
    cur = conn.cursor()
    ex = EXERCISES_DATA[ex_num]
    try:
        cur.execute(query)
        actual_rows = [tuple(r) for r in cur.fetchall()]
        actual_cols = [desc[0] for desc in cur.description] if cur.description else []
    except Exception as e:
        print(f"❌ Erro de sintaxe/execução SQL: {e}")
        return False

    print(f"\n--- Validação Exercício {ex_num} ---")
    print(f"Colunas obtidas : {actual_cols}")
    print(f"Colunas esperadas: {ex['expected_columns']}")
    print("\nLinhas obtidas:")
    for r in actual_rows:
        print(f"  {r}")
    print("\nLinhas esperadas:")
    for r in ex['expected_rows']:
        print(f"  {r}")

    # Check match (normalize numeric types like 800 vs 800.0)
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
        print("\n✅ SUCESSO! A consulta produziu o resultado exato esperado pelo PDF/Beecrowd!")
        return True
    else:
        print("\n⚠️ DIVERGÊNCIA: O resultado não bateu 100% com o Output Sample. Verifique valores, nomes de colunas ou ordenação.")
        return False


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso do db_lab.py:")
        print("  python3 db_lab.py list                    -> Listar todos os exercícios")
        print("  python3 db_lab.py schema <num>             -> Ver tabelas e dados do exercício <num>")
        print("  python3 db_lab.py run <num> \"<SQL>\"        -> Rodar uma consulta livre")
        print("  python3 db_lab.py test <num> \"<SQL>\"       -> Testar consulta contra o gabarito do PDF")
        sys.exit(0)

    cmd = sys.argv[1].lower()
    if cmd == "list":
        print("\nLista de Exercícios (Trabalho Prático I):")
        for num, data in EXERCISES_DATA.items():
            print(f"  {num:2d}. {data['title']}")
        print()
    elif cmd == "schema":
        if len(sys.argv) < 3:
            print("Informe o número do exercício: python3 db_lab.py schema 1")
            sys.exit(1)
        show_schema(int(sys.argv[2]))
    elif cmd == "run":
        if len(sys.argv) < 4:
            print("Informe exercício e query: python3 db_lab.py run 1 \"SELECT * FROM customers\"")
            sys.exit(1)
        run_query(int(sys.argv[2]), sys.argv[3])
    elif cmd == "test":
        if len(sys.argv) < 4:
            print("Informe exercício e query: python3 db_lab.py test 1 \"SELECT name FROM customers WHERE state = 'RS'\"")
            sys.exit(1)
        test_query(int(sys.argv[2]), sys.argv[3])
