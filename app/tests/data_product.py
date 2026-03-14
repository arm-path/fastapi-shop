from app.product.schemas import CategorySchema, CharacteristicSchema

category_data_1 = CategorySchema(
    title='Category-1'
)

category_data_2 = CategorySchema(
    title='Category-2'
)

category_data_3 = CategorySchema(
    title='Category-3',
    parent_id=1
)

category_data_4 = CategorySchema(
    title='Category-1'
)

category_data_5 = CategorySchema(
    title='Category-3',
    parent_id=2
)

category_data_update = CategorySchema(
    title='Category-4',
)

characteristic_data_1 = CharacteristicSchema(
    title='characteristic 1 cat 1',
    unit='',
    type='string'
)

characteristic_data_2 = CharacteristicSchema(
    title='characteristic 2 cat 1',
    unit='',
    type='string'
)

characteristic_data_3 = CharacteristicSchema(
    title='characteristic 3 cat 1',
    unit='',
    type='string'
)

characteristic_data_4 = CharacteristicSchema(
    title='characteristic 4',
    type='integer'
)