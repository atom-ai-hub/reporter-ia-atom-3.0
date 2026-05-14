"""
Reporter IA Atom — API Backend
Sirve datos de atom_gold.gold_cases a index.html vía HTTP.

Endpoints:
  GET /companies          → lista de empresas únicas
  GET /cases/{company_id} → todos los casos de la empresa (últimos 30 días)

Levantar: bash run.sh  (o uvicorn main:app --reload --port 8000)
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from google.cloud import bigquery
from google.oauth2 import service_account
from typing import Optional
import os

app = FastAPI(title="Reporter IA Atom API", version="1.0.0")

# CORS: permitir apertura directa (file://) y localhost en cualquier puerto
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

PROJECT = "atom-ai-hub"
KEY_PATH = os.environ.get(
    "GOOGLE_APPLICATION_CREDENTIALS",
    "/Users/pedrokopyto/.config/gcloud/atom-brain-key.json"
)
credentials = service_account.Credentials.from_service_account_file(
    KEY_PATH,
    scopes=["https://www.googleapis.com/auth/bigquery"]
)
client = bigquery.Client(project=PROJECT, credentials=credentials)


# ── /companies ────────────────────────────────────────────────────────────────
# SQL: SELECT DISTINCT company_id, company_name
#      FROM `atom-ai-hub.atom_gold.gold_cases`
#      WHERE company_name IS NOT NULL
#      ORDER BY company_name

@app.get("/companies")
def get_companies():
    query = """
        SELECT company_id, company_name, COUNT(*) AS case_count
        FROM `atom-ai-hub.atom_gold.gold_cases`
        WHERE company_name IS NOT NULL
        GROUP BY company_id, company_name
        ORDER BY company_name
    """
    try:
        rows = client.query(query).result()
        return [{"company_id": r.company_id, "company_name": r.company_name, "case_count": r.case_count} for r in rows]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ── /cases/{company_id} ───────────────────────────────────────────────────────
# SQL: SELECT <campos> FROM `atom-ai-hub.atom_gold.gold_cases`
#      WHERE company_id = @company_id
#      ORDER BY first_message_at DESC
#
# Nota: la ventana de 30 días ya está enforced en gold_cases (atom_brain rolling window).
# No se aplica filtro de fecha adicional — el frontend corta los períodos en JS.

@app.get("/cases/{company_id}")
def get_cases(company_id: str):
    query = """
        SELECT
          case_id,
          company_id,
          company_name,
          client_id,
          client_name,
          client_phone,
          client_email,
          conversation_id,
          platform,
          channel_id,
          channel_name,
          channel_phone,
          origin_type,
          origin_name,
          flow_direction,
          flow_name,
          flow_agent_id,
          flow_end_type,
          is_assigned,
          is_reassigned,
          is_typified,
          is_sale,
          last_group_id,
          last_group_name,
          first_group_id,
          first_group_name,
          last_agent_id,
          last_agent_name,
          first_agent_id,
          first_agent_name,
          max_stage,
          last_stage,
          last_typification,
          last_typification_key,
          last_typification_comment,
          typification_count,
          last_bot_typification,
          last_bot_typification_key,
          bot_typification_history,
          bot_typification_count,
          reassignment_count,
          first_response_time_seconds,
          aht_seconds,
          avg_response_time_seconds,
          FORMAT_TIMESTAMP('%Y-%m-%dT%H:%M:%SZ', first_message_at) AS first_message_at,
          FORMAT_TIMESTAMP('%Y-%m-%dT%H:%M:%SZ', last_message_at)  AS last_message_at,
          FORMAT_TIMESTAMP('%Y-%m-%dT%H:%M:%SZ', assigned_at)      AS assigned_at,
          FORMAT_TIMESTAMP('%Y-%m-%dT%H:%M:%SZ', last_modified_at) AS last_modified_at,
          first_sender_type,
          last_sender_type
        FROM `atom-ai-hub.atom_gold.gold_cases`
        WHERE company_id = @company_id
        ORDER BY first_message_at DESC
    """
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("company_id", "STRING", company_id)
        ]
    )
    try:
        rows = client.query(query, job_config=job_config).result()
        result = []
        for r in rows:
            result.append({
                "case_id":                      r.case_id,
                "company_id":                   r.company_id,
                "company_name":                 r.company_name,
                "client_id":                    r.client_id,
                "client_name":                  r.client_name,
                "client_phone":                 r.client_phone,
                "client_email":                 r.client_email,
                "conversation_id":              r.conversation_id,
                "platform":                     r.platform,
                "channel_id":                   r.channel_id,
                "channel_name":                 r.channel_name,
                "channel_phone":                r.channel_phone,
                "origin_type":                  r.origin_type,
                "origin_name":                  r.origin_name,
                "flow_direction":               r.flow_direction,
                "flow_name":                    r.flow_name,
                "flow_agent_id":                r.flow_agent_id,
                "flow_end_type":                r.flow_end_type,
                "is_assigned":                  r.is_assigned,
                "is_reassigned":                r.is_reassigned,
                "is_typified":                  r.is_typified,
                "is_sale":                      r.is_sale,
                "last_group_id":                r.last_group_id,
                "last_group_name":              r.last_group_name,
                "first_group_id":               r.first_group_id,
                "first_group_name":             r.first_group_name,
                "last_agent_id":                r.last_agent_id,
                "last_agent_name":              r.last_agent_name,
                "first_agent_id":               r.first_agent_id,
                "first_agent_name":             r.first_agent_name,
                "max_stage":                    r.max_stage,
                "last_stage":                   r.last_stage,
                "last_typification":            r.last_typification,
                "last_typification_key":        r.last_typification_key,
                "last_typification_comment":    r.last_typification_comment,
                "typification_count":           r.typification_count,
                "last_bot_typification":        r.last_bot_typification,
                "last_bot_typification_key":    r.last_bot_typification_key,
                "bot_typification_history":     r.bot_typification_history,
                "bot_typification_count":       r.bot_typification_count,
                "reassignment_count":           r.reassignment_count,
                "first_response_time_seconds":  r.first_response_time_seconds,
                "aht_seconds":                  r.aht_seconds,
                "avg_response_time_seconds":    r.avg_response_time_seconds,
                "first_message_at":             r.first_message_at,
                "last_message_at":              r.last_message_at,
                "assigned_at":                  r.assigned_at,
                "last_modified_at":             r.last_modified_at,
                "first_sender_type":            r.first_sender_type,
                "last_sender_type":             r.last_sender_type,
                # Campos automotrices — pendiente tabla de custom fields
                "marca_auto":                   None,
                "modelo_auto":                  None,
                "tipo_financiamiento":          None,
                "patente":                      None,
                "presupuesto_usd":              None,
                "anio_vehiculo":                None,
            })
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
