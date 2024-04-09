from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_users():
    pass

@router.post("/")
def create_user():
    pass

@router.put("/{id}")
def change_user():
    pass

@router.delete("/{id}")
def delete_user():
    pass