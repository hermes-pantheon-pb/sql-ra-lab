# Trabalho Prático I — Introdução a Banco de Dados
**Tema:** Consultas em Álgebra Relacional e SQL  
**DATA de ENTREGA:** 11/10 — Trabalho Individual  
**Pontuação:** 5 pontos  

**Nome Aluno:** ______________________________  
**Matrícula:** ______________________________  

---

### Exercício 1 — Clientes por Estado (Beecrowd 2602)
**Expressão Algébrica:**  
$$\pi_{name}(\sigma_{state = 'RS'}(customers))$$

**SQL:**
```sql
SELECT name
FROM customers
WHERE state = 'RS';
```

---

### Exercício 2 — Under 10 or Greater Than 100 (Beecrowd 2604)
**Expressão Algébrica:**  
$$\pi_{id, name}(\sigma_{price < 10 \lor price > 100}(products))$$

**SQL:**
```sql
SELECT id, name
FROM products
WHERE price < 10 OR price > 100;
```

---

### Exercício 3 — Higher and Lower Price (Beecrowd 2608)
**Expressão Algébrica:**  
$$\gamma_{MAX(price) \to \text{"price (maior)"}, MIN(price) \to \text{"price (menor)"}}(products)$$

**SQL:**
```sql
SELECT MAX(price) AS "price (maior)", MIN(price) AS "price (menor)"
FROM products;
```

---

### Exercício 4 — Average Value of Products (Beecrowd 2610)
**Expressão Algébrica:**  
$$\gamma_{ROUND(AVG(price), 2) \to price}(products)$$

**SQL:**
```sql
SELECT ROUND(AVG(price), 2) AS price
FROM products;
```

---

### Exercício 5 — Number of Cities per Customers (Beecrowd 2624)
**Expressão Algébrica:**  
$$\gamma_{COUNT(\text{DISTINCT } city) \to count}(customers)$$

**SQL:**
```sql
SELECT COUNT(DISTINCT city) AS count
FROM customers;
```

---

### Exercício 6 — Legal Person (Beecrowd 2622)
**Expressão Algébrica:**  
$$\pi_{name}(customers \bowtie_{customers.id = legal\_person.id\_customers} legal\_person)$$

**SQL:**
```sql
SELECT c.name
FROM customers c
JOIN legal_person lp ON c.id = lp.id_customers;
```

---

### Exercício 7 — Executive Representatives (Beecrowd 2605)
**Expressão Algébrica:**  
$$\pi_{products.name \to \text{"name (produto)"}, providers.name \to \text{"name (fornecedor)"}}(\sigma_{products.id\_categories = 6}(products \bowtie_{products.id\_providers = providers.id} providers))$$

**SQL:**
```sql
SELECT p.name AS "name (produto)", pr.name AS "name (fornecedor)"
FROM products p
JOIN providers pr ON p.id_providers = pr.id
WHERE p.id_categories = 6;
```

---

### Exercício 8 — Action Movies (Beecrowd 2611)
**Expressão Algébrica:**  
$$\pi_{movies.id, movies.name}(\sigma_{genres.description = 'Action'}(movies \bowtie_{movies.id\_genres = genres.id} genres))$$

**SQL:**
```sql
SELECT m.id, m.name
FROM movies m
JOIN genres g ON m.id_genres = g.id
WHERE g.description = 'Action';
```

---

### Exercício 9 — Provider Ajax SA (Beecrowd 2617)
**Expressão Algébrica:**  
$$\pi_{products.name \to \text{"name (produto)"}, providers.name \to \text{"name (fornecedor)"}}(\sigma_{providers.name = 'Ajax SA'}(products \bowtie_{products.id\_providers = providers.id} providers))$$

**SQL:**
```sql
SELECT p.name AS "name (produto)", pr.name AS "name (fornecedor)"
FROM products p
JOIN providers pr ON p.id_providers = pr.id
WHERE pr.name = 'Ajax SA';
```

---

### Exercício 10 — Products by Categories (Beecrowd 2609)
**Expressão Algébrica:**  
$$_{categories.name}\gamma_{SUM(products.amount) \to sum}(products \bowtie_{products.id\_categories = categories.id} categories)$$

**SQL:**
```sql
SELECT c.name, SUM(p.amount) AS sum
FROM products p
JOIN categories c ON p.id_categories = c.id
GROUP BY c.name;
```

---

### Exercício 11 — September Rentals (Beecrowd 2614)
**Expressão Algébrica:**  
$$\pi_{customers.name, rentals.rentals\_date}(\sigma_{rentals\_date \ge '2016-09-01' \land rentals\_date \le '2016-09-30'}(customers \bowtie_{customers.id = rentals.id\_customers} rentals))$$

**SQL:**
```sql
SELECT c.name, r.rentals_date
FROM customers c
JOIN rentals r ON c.id = r.id_customers
WHERE r.rentals_date >= '2016-09-01' AND r.rentals_date <= '2016-09-30';
```

---

### Exercício 12 — Orders in First Half (Beecrowd 2620)
**Expressão Algébrica:**  
$$\pi_{customers.name, orders.id \to \text{"id (pedido)"}}(\sigma_{orders\_date \ge '2016-01-01' \land orders\_date \le '2016-06-30'}(customers \bowtie_{customers.id = orders.id\_customers} orders))$$

**SQL:**
```sql
SELECT c.name, o.id AS "id (pedido)"
FROM customers c
JOIN orders o ON c.id = o.id_customers
WHERE o.orders_date >= '2016-01-01' AND o.orders_date <= '2016-06-30';
```

---

### Exercício 13 — Lawyers (Beecrowd 2737)
**Expressão Algébrica:**  
$$(\pi_{name, customers\_number}(\tau_{customers\_number \downarrow}(LIMIT 1 (lawyers)))) \cup (\pi_{name, customers\_number}(\tau_{customers\_number \uparrow}(LIMIT 1 (lawyers)))) \cup (\pi_{\text{'Average'}, CAST(AVG(customers\_number) \text{ AS INT})}(lawyers))$$

**SQL:**
```sql
(SELECT name, customers_number FROM lawyers ORDER BY customers_number DESC LIMIT 1)
UNION ALL
(SELECT name, customers_number FROM lawyers ORDER BY customers_number ASC LIMIT 1)
UNION ALL
(SELECT 'Average', CAST(AVG(customers_number) AS INTEGER) FROM lawyers);
```

---

### Exercício 14 — Most Frequent Value (Beecrowd 2993)
**Expressão Algébrica:**  
$$\pi_{amount \to most\_frequent\_value}(\tau_{count \downarrow}(LIMIT 1 (_{amount}\gamma_{COUNT(*) \to count}(value\_table))))$$

**SQL:**
```sql
SELECT amount AS most_frequent_value
FROM value_table
GROUP BY amount
ORDER BY COUNT(*) DESC
LIMIT 1;
```

---

### Exercício 15 — Imported Products (Beecrowd 2618)
**Expressão Algébrica:**  
$$\pi_{products.name \to \text{"name (produto)"}, providers.name \to \text{"name (fornecedor)"}, categories.name \to \text{"name (categoria)"}}(\sigma_{providers.name = 'Sansul SA' \land categories.name = 'Imported'}((products \bowtie providers) \bowtie categories))$$

**SQL:**
```sql
SELECT p.name AS "name (produto)", pr.name AS "name (fornecedor)", c.name AS "name (categoria)"
FROM products p
JOIN providers pr ON p.id_providers = pr.id
JOIN categories c ON p.id_categories = c.id
WHERE pr.name = 'Sansul SA' AND c.name = 'Imported';
```

---

### Exercício 16 — Categories with Various Products (Beecrowd 2623)
**Expressão Algébrica:**  
$$\pi_{products.name \to \text{"name (produto)"}, categories.name \to \text{"name (categoria)"}}(\tau_{products.id\_categories \uparrow}(\sigma_{amount > 100 \land id\_categories \in \{1,2,3,6,9\}}(products \bowtie categories)))$$

**SQL:**
```sql
SELECT p.name AS "name (produto)", c.name AS "name (categoria)"
FROM products p
JOIN categories c ON p.id_categories = c.id
WHERE p.amount > 100 AND p.id_categories IN (1, 2, 3, 6, 9)
ORDER BY p.id_categories ASC;
```

---

### Exercício 17 — Categorias com Muitos Produtos (Elaborado para este material)
**Expressão Algébrica:**  
$$\pi_{name, count}(\sigma_{count > 2}(_{categories.name}\gamma_{COUNT(*) \to count}(products \bowtie_{products.id\_categories = categories.id} categories)))$$

**SQL:**
```sql
SELECT c.name, COUNT(*) AS count
FROM products p
JOIN categories c ON p.id_categories = c.id
GROUP BY c.name
HAVING COUNT(*) > 2;
```

---

### Exercício 18 — No Rental (Beecrowd 2616)
**Expressão Algébrica:**  
$$\pi_{id, name}(\tau_{id \uparrow}(customers \triangleright_{customers.id = locations.id\_customers} locations))$$

**SQL:**
```sql
SELECT c.id, c.name
FROM customers c
LEFT JOIN locations l ON c.id = l.id_customers
WHERE l.id IS NULL
ORDER BY c.id ASC;
```

---

### Exercício 19 — Campeonato Cearense (Beecrowd 2988)
**Expressão Algébrica:**  
$$\pi_{name, matches, victories, defeats, draws, score}(\tau_{score \downarrow}(_{teams.name}\gamma_{...}(teams \bowtie (Jogos_{Casa} \cup Jogos_{Fora}))))$$

**SQL:**
```sql
WITH matches_perspective AS (
  SELECT team_1 AS team_id,
         CASE WHEN team_1_goals > team_2_goals THEN 1 ELSE 0 END AS v,
         CASE WHEN team_1_goals < team_2_goals THEN 1 ELSE 0 END AS d,
         CASE WHEN team_1_goals = team_2_goals THEN 1 ELSE 0 END AS e
  FROM matches
  UNION ALL
  SELECT team_2 AS team_id,
         CASE WHEN team_2_goals > team_1_goals THEN 1 ELSE 0 END AS v,
         CASE WHEN team_2_goals < team_1_goals THEN 1 ELSE 0 END AS d,
         CASE WHEN team_2_goals = team_1_goals THEN 1 ELSE 0 END AS e
  FROM matches
)
SELECT t.name,
       COUNT(m.team_id) AS matches,
       SUM(m.v) AS victories,
       SUM(m.d) AS defeats,
       SUM(m.e) AS draws,
       (SUM(m.v) * 3 + SUM(m.e)) AS score
FROM teams t
JOIN matches_perspective m ON t.id = m.team_id
GROUP BY t.name
ORDER BY score DESC;
```

---

### Exercício 20 — Department Statistics (Beecrowd 2991)
**Expressão Algébrica:**  
$$\pi_{\text{Nome, Numero, Media, Maior, Menor}}(\tau_{Media \downarrow}(_{cod\_dep, nome}\gamma_{COUNT, AVG, MAX, MIN}(departamento \bowtie empregado \bowtie Salarios)))$$

**SQL:**
```sql
WITH salarios_funcionarios AS (
  SELECT e.matr,
         e.lotacao AS cod_dep,
         COALESCE((
           SELECT SUM(v.valor)
           FROM emp_venc ev
           JOIN vencimento v ON ev.cod_venc = v.cod_venc
           WHERE ev.matr = e.matr
         ), 0) - 
         COALESCE((
           SELECT SUM(d.valor)
           FROM emp_desc ed
           JOIN desconto d ON ed.cod_desc = d.cod_desc
           WHERE ed.matr = e.matr
         ), 0) AS salario_liquido
  FROM empregado e
)
SELECT dep.nome AS "Nome Departamento",
       COUNT(sf.matr) AS "Numero de Empregados",
       ROUND(AVG(sf.salario_liquido), 2) AS "Media Salarial",
       ROUND(MAX(sf.salario_liquido), 2) AS "Maior Salario",
       ROUND(MIN(sf.salario_liquido), 2) AS "Menor Salario"
FROM departamento dep
JOIN salarios_funcionarios sf ON dep.cod_dep = sf.cod_dep
GROUP BY dep.cod_dep, dep.nome
ORDER BY "Media Salarial" DESC;
```
