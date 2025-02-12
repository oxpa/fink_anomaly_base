from fastapi import UploadFile, Form
from database import Database
from fastapi import APIRouter, HTTPException, status, Depends, Response
from models.base_types import ImageDocument, ObjectId
from auth.authenticate import authenticate
from loguru import logger

image_router = APIRouter(
    tags=["Uploads"]
)

images = Database(ImageDocument)

@image_router.post("/upload")
async def upload_images(ztf_id: str, image1: UploadFile, image2: UploadFile, description: str = Form(...), user: str = Depends(authenticate)):
    image1_bytes = await image1.read()
    image2_bytes = await image2.read()

    image_doc = ImageDocument(
        description=description,
        ztf_id=ztf_id,
        user=user
    )
    try:
        # this creates ID in case of an sql backend
        await images.save(image_doc)

        with open(f"static/{image_doc.id}_curve.png", "wb") as f:
            f.write(image1_bytes)
        with open(f"static/{image_doc.id}_cutout.png", "wb") as f:
            f.write(image2_bytes)


    except Exception as e:
        logger.error(e)
        return {"message":"Error occurred during upload. Please check logs."}

    return {
        "message": "Images uploaded successfully",
        "id": str(image_doc.id)
    }


@image_router.get("/get_image/{image_id}/{image_number}")
async def get_image(image_id: str, image_number: int):
    image_doc = await ImageDocument.get(image_id)
    if image_doc:
        if image_number == 1:
            return Response(content=image_doc.image1, media_type="image/png")
        elif image_number == 2:
            return Response(content=image_doc.image2, media_type="image/png")
    return Response(status_code=404)


@image_router.delete("/{num}")
async def delete_reaction(num: ObjectId, user: str = Depends(authenticate)) -> dict:
    event = await images.delete(num)
    if event:
        return {
            "message": "Reaction (image) deleted successfully"
        }
    raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reaction (image) with supplied ID does not exist"
    )
