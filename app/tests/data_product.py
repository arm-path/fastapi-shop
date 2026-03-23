from app.product.schemas import CategorySchema, CharacteristicSchema, ProductSchema, ProductCharacteristicSchema, \
    ProductCharacteristicSchemaUpdate

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
    type='integer'
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

product_data_1 = ProductSchema(
    title='product-1',
    category_id=1,
    price=14.54,
    description='Product description'
)

product_data_2 = ProductSchema(
    title='product-2',
    category_id=1,
    price=15.51,
    description=''
)

product_data_3 = ProductSchema(
    title='product-3',
    category_id=2,
    price=15.51
)

product_data_4 = ProductSchema(
    title='product-4',
    category_id=120,
    price=15.51
)

product_data_5 = ProductSchema(
    title='product-5',
    category_id=1,
    price=-15.51
)

characteristic_1_c_1_product_1 = ProductCharacteristicSchema(
    characteristic_id=2,
    value='100'
)

characteristic_1_c_2_product_1 = ProductCharacteristicSchema(
    characteristic_id=3,
    value='string'
)

characteristic_value_type_err = ProductCharacteristicSchema(
    characteristic_id=2,
    value='err'  # characteristic_id = 2: integer
)

characteristic_category_err = ProductCharacteristicSchema(
    characteristic_id=6,  # characteristic.category_id = 2
    value='1'
)

characteristic_id_err = ProductCharacteristicSchema(
    characteristic_id=1,
    value='1'
)

characteristic_update_type_err = ProductCharacteristicSchemaUpdate(
    id=1,
    value='w'
)

characteristic_update = ProductCharacteristicSchemaUpdate(
    id=1,
    value='13'
)