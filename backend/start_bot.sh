#!/bin/bash
cd /home/ishak/Bureau/ERP/backend
source venv/bin/activate
uvicorn api:app --host 0.0.0.0 --port 8000
