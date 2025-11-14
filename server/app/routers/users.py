from fastapi import APIRouter


router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@router.get("/me")
async def read_user_me():
    return {"username": "fakecurrentuser"}