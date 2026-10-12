# SQL & Relational Algebra Studio 🔮

> Um laboratório interativo e visual para dominar **Álgebra Relacional** e **SQL** a partir dos primeiros princípios, com foco em intuição, mecânica do otimizador e resolução dos 20 exercícios do Beecrowd / Trabalho Prático de Banco de Dados.

![Status](https://img.shields.io/badge/Status-Complete-emerald)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![SQLite](https://img.shields.io/badge/Engine-SQLite%20%2F%20ANSI%20SQL-cyan)
![Interface](https://img.shields.io/badge/Interface-Web%20%28Vanilla%20JS%20%2B%20CSS%29-purple)

---

## 🌟 Destaques do Projeto

- 🧠 **Aprendizado por Família de Conceitos:** Aborda o modelo mental e todo o ecossistema adjacente de cada operador (comparações, lógica booleana, predicados de intervalo, nulos tri-valorados, agregações, junções, `HAVING`, anti-junções e subconsultas).
- ⚡ **Execução SQL em Tempo Real:** Editor interativo no navegador com atalho <kbd>Ctrl</kbd> + <kbd>Enter</kbd> executando diretamente sobre instâncias SQLite em memória.
- ✔️ **Validação Automática contra o PDF (Beecrowd):** Compara as consultas submetidas contra as saídas esperadas (*Output Sample*) dos 20 exercícios.
- 📐 **Decomposição em Álgebra Relacional:** Visualização da fórmula algébrica matemática ($\sigma, \pi, \bowtie, \gamma, \tau, \cup, -$) com análise nó por nó da árvore de consulta.
- 📋 **Caderno de Entrega Integrado:** Documento formatado pronto para entrega acadêmica com todas as expressões e consultas SQL.

---

## 🚀 Como Executar

### 1. Iniciar o Studio Web Interativo

O projeto não possui nenhuma dependência externa (utiliza apenas a biblioteca padrão do Python 3):

```bash
# Entrar no diretório
cd sql-ra-lab

# Iniciar o servidor local
python3 web_server.py
```

Abra o seu navegador e acesse:
👉 **`http://localhost:8080`**

---

### 2. Executar e Testar via Terminal (CLI)

Você também pode inspecionar e testar consultas diretamente no terminal com o utilitário `db_lab.py`:

```bash
# Listar todos os 20 exercícios
python3 db_lab.py list

# Inspecionar esquemas e dados de um exercício
python3 db_lab.py schema 1

# Executar uma consulta livre
python3 db_lab.py run 1 "SELECT name FROM customers WHERE state = 'RS';"

# Testar e validar contra a saída esperada do exercício
python3 db_lab.py test 1 "SELECT name FROM customers WHERE state = 'RS';"
```

---

## 📚 Estrutura do Currículo (7 Módulos)

| Módulo | Foco Teórico | Operadores em AR | Cláusulas SQL | Exercícios do PDF |
|:---|:---|:---|:---|:---|
| **1. O Esqueleto Fundamental** | Filtro de linhas e corte de colunas | $\sigma, \pi$ | `SELECT`, `FROM`, `WHERE` | Ex. 1 e 2 |
| **2. Funções de Agregação** | Resumo escalar e valores extremos | $\gamma$ | `COUNT`, `SUM`, `AVG`, `MIN`, `MAX` | Ex. 3, 4 e 5 |
| **3. Junções Relacionais** | Combinação de tabelas via PK e FK | $\bowtie_\theta, \bowtie$ | `INNER JOIN ... ON` | Ex. 6, 7, 8, 9 e 15 |
| **4. Agrupamentos e Grupos** | Partições e filtros pós-agregação | $_{G}\gamma_{F}, \sigma_{\text{agg}}$ | `GROUP BY`, `HAVING` | Ex. 10 e 17 |
| **5. Datas e Ordenação** | Filtros temporais e sequenciamento | $\tau, \sigma_{\text{tempo}}$ | `ORDER BY`, `IN`, datas | Ex. 11, 12 e 16 |
| **6. Teoria dos Conjuntos** | Anti-junções e empilhamento | $\triangleright, -, \cup$ | `LEFT JOIN ... IS NULL`, `UNION ALL` | Ex. 13, 14 e 18 |
| **7. Lógica Condicional** | Transformações if-else e métricas | `CASE WHEN`, CTEs | `WITH`, `CASE WHEN`, `COALESCE` | Ex. 19 e 20 |

---

## 📂 Arquivos do Repositório

```text
sql-ra-lab/
├── index.html              # Interface web moderna e responsiva
├── style.css               # Design system com tema dark, glassmorphism e tipografia técnica
├── app.js                  # Lógica do cliente, atalhos, validação e persistência local
├── curriculum.json         # Base pedagógica completa com os 7 módulos e 20 exercícios
├── web_server.py           # Backend Python nativo com API REST para execução e teste
├── db_lab.py               # Utilitário CLI com esquemas, dados de teste e comparador
└── resolucao_trabalho.md   # Documento oficial com as resoluções prontas para entrega
```
