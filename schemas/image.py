from marshmallow import Schema, fields
from werkzeug.datastructures import FileStorage


class FileStorageField(fields.Field):
    def_error_messages = {
        "invalid": "Not a valid image."
    }

    # checks if value exist and also checks if its a valid storage
    def _deserialize(self, value, attr, data, **kwargs) -> FileStorage:
        if value is None:
            return None

        if not isinstance(value, FileStorage):
            self.fail("invalid")    # raises ValidationError

        return value


# for validation alone not persisting to db
class ImageSchema(Schema):
    image = FileStorageField(required=True)
