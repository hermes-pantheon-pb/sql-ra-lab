#!/usr/bin/env python3
"""
Web Server & API Backend for SQL & Relational Algebra Interactive Studio.
Zero third-party dependencies - runs with standard Python 3.
"""

import http.server
import socketserver
import json
import sqlite3
import os
import sys
import time
from typing import Dict, Any, List, Tuple
from db_lab import EXERCISES_DATA, get_connection

PORT = 8080
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class StudioAPIHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_GET(self):
        if self.path == "/api/exercises":
            self.send_json_response(self.get_exercises_summary())
        elif self.path.startswith("/api/exercise/"):
            try:
                ex_id = self.path.split("/")[-1]
                self.send_json_response(self.get_exercise_details(ex_id))
            except Exception as e:
                self.send_json_response({"error": str(e)}, status=400)
        else:
            super().do_GET()

    def do_POST(self):
        if self.path == "/api/execute":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8")
            try:
                data = json.loads(body)
                ex_id = str(data.get("exerciseId", "1"))
                query = data.get("query", "")
                result = self.execute_query(ex_id, query)
                self.send_json_response(result)
            except Exception as e:
                self.send_json_response({"error": str(e)}, status=400)
        elif self.path == "/api/validate":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8")
            try:
                data = json.loads(body)
                ex_id = str(data.get("exerciseId", "1"))
                query = data.get("query", "")
                result = self.validate_query(ex_id, query)
                self.send_json_response(result)
            except Exception as e:
                self.send_json_response({"error": str(e)}, status=400)
        else:
            self.send_json_response({"error": "Endpoint not found"}, status=404)

    def send_json_response(self, data: Any, status: int = 200):
        response_bytes = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(response_bytes)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        self.wfile.write(response_bytes)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def get_exercises_summary(self):
        summary = []
        for ex_id, info in EXERCISES_DATA.items():
            summary.append({
                "id": ex_id,
                "title": info["title"],
                "type": info.get("type", "oficial"),
                "expectedColumns": info["expected_columns"],
                "expectedRowCount": len(info["expected_rows"])
            })
        return summary

    def get_exercise_details(self, ex_id: str):
        if ex_id not in EXERCISES_DATA:
            return {"error": f"Exercício/Treino '{ex_id}' não encontrado"}
        info = EXERCISES_DATA[ex_id]
        conn = get_connection(ex_id)
        cur = conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [r[0] for r in cur.fetchall()]

        schema_tables = {}
        for t in tables:
            cur.execute(f"PRAGMA table_info({t});")
            cols = [{"cid": c[0], "name": c[1], "type": c[2], "notnull": c[3], "pk": c[5]} for c in cur.fetchall()]
            cur.execute(f"SELECT * FROM {t};")
            sample_rows = [list(r) for r in cur.fetchall()]
            schema_tables[t] = {
                "columns": cols,
                "rows": sample_rows
            }

        return {
            "id": ex_id,
            "title": info["title"],
            "type": info.get("type", "oficial"),
            "expectedColumns": info["expected_columns"],
            "expectedRows": info["expected_rows"],
            "tables": schema_tables
        }

    def execute_query(self, ex_id: str, query: str):
        if not query.strip():
            return {"success": False, "error": "A consulta SQL está vazia."}
        start = time.time()
        try:
            conn = get_connection(ex_id)
            cur = conn.cursor()
            cur.execute(query)
            rows = [list(r) for r in cur.fetchall()]
            cols = [desc[0] for desc in cur.description] if cur.description else []
            elapsed_ms = round((time.time() - start) * 1000, 2)
            return {
                "success": True,
                "columns": cols,
                "rows": rows,
                "rowCount": len(rows),
                "elapsedMs": elapsed_ms
            }
        except Exception as e:
            elapsed_ms = round((time.time() - start) * 1000, 2)
            return {
                "success": False,
                "error": str(e),
                "elapsedMs": elapsed_ms
            }

    def validate_query(self, ex_id: str, query: str):
        exec_res = self.execute_query(ex_id, query)
        if not exec_res["success"]:
            return {
                "matched": False,
                "error": exec_res["error"],
                "execResult": exec_res
            }

        info = EXERCISES_DATA[ex_id]
        expected_cols = info["expected_columns"]
        expected_rows = info["expected_rows"]

        actual_cols = exec_res["columns"]
        actual_rows = exec_res["rows"]

        matched = True
        diff_reason = ""

        # Normalize column names comparison
        norm_actual_cols = [c.strip().lower() for c in actual_cols]
        norm_expected_cols = [c.strip().lower() for c in expected_cols]

        if norm_actual_cols != norm_expected_cols:
            matched = False
            diff_reason = f"Colunas divergentes. Esperado: {expected_cols}, Recebido: {actual_cols}."
        elif len(actual_rows) != len(expected_rows):
            matched = False
            diff_reason = f"Quantidade de linhas diferente. Esperado: {len(expected_rows)}, Recebido: {len(actual_rows)}."
        else:
            for i, (act, exp) in enumerate(zip(actual_rows, expected_rows)):
                if len(act) != len(exp):
                    matched = False
                    diff_reason = f"Linha {i+1} tem quantidade de colunas diferente."
                    break
                for j, (a, b) in enumerate(zip(act, exp)):
                    try:
                        if round(float(a), 2) != round(float(b), 2):
                            matched = False
                            diff_reason = f"Valor diferente na linha {i+1}, coluna {actual_cols[j]}: esperado '{b}', obtido '{a}'."
                            break
                    except (ValueError, TypeError):
                        if str(a).strip().lower() != str(b).strip().lower():
                            matched = False
                            diff_reason = f"Valor diferente na linha {i+1}, coluna {actual_cols[j]}: esperado '{b}', obtido '{a}'."
                            break
                if not matched:
                    break

        return {
            "matched": matched,
            "diffReason": diff_reason if not matched else "Sucesso! Resultado idêntico ao esperado.",
            "execResult": exec_res,
            "expectedColumns": expected_cols,
            "expectedRows": expected_rows
        }

def run_server():
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("127.0.0.1", PORT), StudioAPIHandler) as httpd:
        print(f"🚀 SQL & Relational Algebra Studio rodando em http://localhost:{PORT}")
        sys.stdout.flush()
        httpd.serve_forever()

if __name__ == "__main__":
    run_server()
