from fastapi import HTTPException, status

DataTypeException = lambda type, data: HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail={'messages': f'Error data types, waiting {type}', 'data': data}
)


class DuplicateProductError(Exception):

    def __init__(self, message="Duplicate product error"):
        self.message = message
        super().__init__(self.message)
