import os
import threading
import unicodedata
from contextlib import asynccontextmanager

import uvicorn
from classes.LinkedinRequest import LinkedinRequest
from core.generate_dossier import generate_dossier_api
from fastapi import (
    Depends,
    FastAPI,
    File,
    Form,
    HTTPException,
    Request,
    UploadFile,
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from generate_next_hour import generatehour
from linkedin.start_prospect_auto import start_prospect_auto
from query.cabinets.get_cabinet_id import get_cabinet_id
from query.cabinets.get_cabinet_informations import get_cabinet_informations
from query.cabinets.insert_prospection_settings import (
    insert_prospection_settings,
)
from query.linkedin.get_prospection_list import get_prospection_list
from query.user.get_user_id import get_user_id


@asynccontextmanager
async def thread_(app: FastAPI):
    thread = threading.Thread(target=start_prospect_auto, daemon=True)
    thread.start()
    print("Lancement de thread pour les lancements automatique...")
    yield


app = FastAPI(title="API workCabinet", version="1.0.0", lifespan=thread_)
KEY_SECRET = os.getenv("ENCRYPTION_SECRET")
print(f"KEY: {KEY_SECRET}")

# Configuration CORS pour autoriser le front React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def delete_accents(s):  # on evite d'avoir des acccents
    return "".join(
        c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn"
    )


@app.get("/")
async def root():
    """Endpoint principal"""

    return {
        "message": "L'application tourne !",
        "status": "ok",
        "version": "1.0.0",
        "endpoints": {
            "docs": "/docs",
            "generate": "/api/generate-dossier",
            "health": "/api/health",
        },
    }


@app.post("/api/generate-dossier")
async def generate_dossier(
    cv: UploadFile = File(..., description="Fichier CV (PDF ou DOCX)"),
    add_skills: bool = Form(..., description="Ajouter plus de compétences"),
    english_cv: bool = Form(False, description="CV en anglais"),
):

    allowed_types = [  # allowlist
        "application/pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ]

    if cv.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail=f"Type de fichier non supporté: {cv.content_type}. Utilisez PDF ou DOCX.",
        )

    max_size = 10 * 1024 * 1024
    cv_content = await cv.read()

    if len(cv_content) > max_size:
        raise HTTPException(
            status_code=400,
            detail=f"Fichier trop volumineux ({len(cv_content) / 1024 / 1024:.2f} MB). Taille maximale: 10 MB",
        )

    temp_cv_path = None
    output_path = None

    try:
        result = generate_dossier_api(
            selected_file=str(temp_cv_path),
            output_path=str(output_path),
            add_skills=add_skills,
            english_cv=english_cv,
            progress_callback=lambda msg: print(f"   {msg}"),
        )

        if not result["success"]:
            raise HTTPException(status_code=500, detail=result["message"])

        if temp_cv_path and temp_cv_path.exists():
            raise HTTPException(
                status_code=500, detail="Le fichier n'a pas été généré correctement"
            )

        print(f"✅ Génération terminée: {output_path}")
        # print(f"{'=' * 60}\n")

        return FileResponse(
            path=str(output_path),
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            headers={
                "X-Generation-Success": "true",
            },
        )  # keep file

    except HTTPException:
        raise

    except Exception as e:
        import traceback  # get error

        error_detail = traceback.format_exc()
        print(f"❌ ERREUR:\n{error_detail}")

        raise HTTPException(
            status_code=500, detail=f"Erreur lors de la génération du dossier: {str(e)}"
        )


@app.get("/backend/prospection/list")
async def get_prospection(current_user_id: str = Depends(get_user_id)):
    return get_prospection_list(current_user_id)


@app.post("/backend/linkedin/start_chrome")
async def start_chrome(
    body: LinkedinRequest,
    current_user_id: str = Depends(get_user_id),
    cabinet_id: str = Depends(get_cabinet_id),
):

    get_cabinet_informations(current_user_id, cabinet_id)

    SELECT_QUERY = f"*,profiles!inner(linkedin_email,linkedin_password:pgp_sym_decrypt(linkedin_password::bytea,'{KEY_SECRET}'))"
    if SELECT_QUERY:
        print("insert db...")

    generate_next_hour = generatehour()

    insert_prospection_settings(body, cabinet_id, current_user_id, generate_next_hour)


if __name__ == "__main__":
    uvicorn.run("endpoint:app", host="0.0.0.0", port=8001)  # config
