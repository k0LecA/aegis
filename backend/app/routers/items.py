from fastapi import APIRouter, Depends

router = APIRouter(prefix="/f")

@router.get("/")
def read_root():
    return {"status": "AEGIS Online", "message": "Testing protocols initiated."}


@router.get("/cake")
def read_cake():
    return {"error": 404, "message": "Cake is a lie."}