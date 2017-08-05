# coding: utf-8
from .base import VKBase


class Photo(VKBase):

    @classmethod
    def from_json(cls, session, photo_json):
        """
        https://vk.com/dev/objects/photo
        """
        photo = cls()
        photo.id = photo_json.get('id')
        photo.album_id = photo_json.get('album_id')
        photo.owner_id = photo_json.get('owner_id')
        photo.user_id = photo_json.get('user_id')
        photo.text = photo_json.get('text')
        photo.date = photo_json.get('date')
        photo.photo_75 = photo_json.get('photo_75')
        photo.photo_130 = photo_json.get('photo_130')
        photo.photo_604 = photo_json.get('photo_604')
        photo.photo_807 = photo_json.get('photo_807')
        photo.photo_1280 = photo_json.get('photo_1280')
        photo.photo_2560 = photo_json.get('photo_2560')
        photo._session = session
        return photo

    @staticmethod
    def _get_photos(session, user_or_group_id):
        """
        https://vk.com/dev/photos.getAll
        """
        response = session.fetch_items("photos.getAll", Photo.from_json, count=200, owner_id=user_or_group_id)
        return response

    @staticmethod
    def _get_owner_cover_photo_upload_server(session, group_id, crop_x=0, crop_y=0, crop_x2=795, crop_y2=200):
        """
        https://vk.com/dev/photos.getOwnerCoverPhotoUploadServer
        """
        group_id = abs(group_id)
        response = session.fetch("photos.getOwnerCoverPhotoUploadServer", group_id=group_id, crop_x=crop_x, crop_y=crop_y, crop_x2=crop_x2, crop_y2=crop_y2)
        return response['upload_url']

    @staticmethod
    def _save_owner_cover_photo(session, hash, photo):
        """
        https://vk.com/dev/photos.saveOwnerCoverPhoto
        """
        response = session.fetch('photos.saveOwnerCoverPhoto', hash=hash, photo=photo)
        return response

    @staticmethod
    def _get_wall_upload_server(session, group_id):
        """
        https://vk.com/dev/photos.getWallUploadServer
        """
        response = session.fetch("photos.getWallUploadServer", group_id=group_id)
        return response['upload_url']

    @staticmethod
    def _get_save_wall_photo(session, photo, server, hash, user_id=None, group_id=None):
        """
        https://vk.com/dev/photos.saveWallPhoto
        """
        if group_id < 0:
            group_id = abs(group_id)

        response = session.fetch("photos.saveWallPhoto", photo=photo, server=server, hash=hash, user_id=user_id, group_id=group_id)[0]
        return response['id'], response['owner_id']

    @staticmethod
    def _upload_wall_photos_for_group(session, group_id, image_files):
        upload_url = Photo._get_wall_upload_server(session, group_id)

        attachments = []
        for image_fd in image_files:
            response = session.fetch_post(upload_url, files={'photo': image_fd})
            response_json = response.json()
            photo, server, _hash = response_json['photo'], response_json['server'], response_json['hash']
            photo_id, owner_id = Photo._get_save_wall_photo(session, photo, server, _hash, group_id=group_id)
            attachments.append("photo{0}_{1}".format(owner_id, photo_id))

        return ",".join(attachments)
