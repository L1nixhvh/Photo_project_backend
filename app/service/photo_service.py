from app import db
from app.models.photos import Photos
import uuid


class PhotosService:
    def insert_photo(self, user_id, photo_url, description) -> bool:
        try:
            new_photo = Photos(
                id=str(uuid.uuid4()),
                user_id=user_id,
                photo_url=photo_url,
                description=description,
            )
            db.session.add(new_photo)
            db.session.commit()
            return new_photo.id
        except:
            db.session.rollback()
            return False

    def delete_photo(self, photo) -> bool:
        try:
            db.session.delete(photo)
            db.session.commit()
            return True
        except:
            db.session.rollback()
            return False

    def get_photo_by_id(self, photo_id):
        try:
            return (
                db.session.query(Photos)
                .filter(Photos.id == photo_id if photo_id is not None else False)
                .first()
            )
        except:
            return None
