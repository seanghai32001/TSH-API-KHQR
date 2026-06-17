from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import requests
from mangum import Mangum

app = FastAPI(
    title="Bakong Transaction Checker",
    description="Check Bakong transaction by MD5",
    version="1.0.0"
)

# ==================================
# CONFIG
# ==================================

BAKONG_API_URL = "https://bakong.apsara.fun/v1/check_transaction_by_md5"
DEFAULT_TOKEN = ""


# ==================================
# MODELS
# ==================================

class MD5Request(BaseModel):
    md5: str
    token: Optional[str] = None


class APIResponse(BaseModel):
    success: bool
    message: str
    data: Optional[dict] = None


# ==================================
# ROOT
# ==================================

@app.get("/")
def home():
    return {
        "status": "running",
        "service": "TSH DV (Bakong MD5 Checker API)"
    }


# ==================================
# CHECK PAYMENT (POST)
# ==================================

@app.post("/check-payment", response_model=APIResponse)
def check_payment(data: MD5Request):

    token = data.token or DEFAULT_TOKEN

    if not token:
        raise HTTPException(
            status_code=400,
            detail="Token is required"
        )

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    payload = {
        "md5": data.md5
    }

    try:
        response = requests.post(
            BAKONG_API_URL,
            json=payload,
            headers=headers,
            timeout=15
        )

        result = response.json()

        return {
            "success": True,
            "message": "Request Success",
            "data": result
        }

    except requests.exceptions.Timeout:
        raise HTTPException(
            status_code=408,
            detail=str("FUCK YOU")
        )

    except requests.exceptions.ConnectionError:
        raise HTTPException(
            status_code=500,
            detail=str("FUCK YOU")
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str("FUCK YOU")
        )


# ==================================
# CHECK PAYMENT BY URL
# ==================================

@app.get("/check-payment/{token}/{md5}")
def check_payment_by_url(token: str, md5: str):

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    payload = {
        "md5": md5
    }

    try:
        response = requests.post(
            BAKONG_API_URL,
            json=payload,
            headers=headers,
            timeout=15
        )

        return response.json()

    except requests.exceptions.Timeout:
        raise HTTPException(
            status_code=408,
            detail=str("FUCK YOU")
        )

    except requests.exceptions.ConnectionError:
        raise HTTPException(
            status_code=500,
            detail=str("FUCK YOU")
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str("FUCK YOU")
        )


# ==================================
# HEALTH
# ==================================

@app.get("/health")
def health():
    return {
        "status": "ok"
    }


# ==================================
# VERCEL ENTRY POINT
# ==================================

handler = Mangum(app)
