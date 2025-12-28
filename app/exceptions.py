from fastapi import HTTPException, status

DataTypeException = lambda type, data : HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail={'messages': f'Error data types, waiting {type}', 'data': data}
)