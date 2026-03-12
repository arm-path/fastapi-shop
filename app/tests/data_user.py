from fastapi.security import OAuth2PasswordRequestForm

from app.user.schemas import RegistrationSchema

# noinspection PyTypeChecker
user_data_1 = RegistrationSchema(
    email='arm@example.com',
    first_name='Rinat',
    last_name='Ahtyamov',
    password='123456$Py',
    password_repeat='123456$Py'
)
# noinspection PyTypeChecker
user_data_2 = RegistrationSchema(
    email='lorem@example.com',
    first_name='Lorem',
    last_name='Ipsum',
    password='123456$Py',
    password_repeat='123456$Py'
)
# noinspection PyTypeChecker
user_data_3 = RegistrationSchema(
    email='consectetur@example.ru',
    first_name='Consectetur',
    last_name='Adipiscing',
    password='123456$Py',
    password_repeat='123456$Py'
)
# noinspection PyTypeChecker
user_data_4 = RegistrationSchema(
    email='consectetur@example.ru',
    first_name='Consectetur',
    last_name='Adipiscing',
    password='123456$Py',
    password_repeat='123456$Py'
)


auth_data_1 = OAuth2PasswordRequestForm(
    username=str(user_data_1.email),
    password=user_data_1.password,
)

auth_data_2 = OAuth2PasswordRequestForm(
    username=str(user_data_1.email),
    password='123456'
)

auth_data_3 = OAuth2PasswordRequestForm(
    username='email@email.ru',
    password=user_data_1.password
)

auth_data_4 = OAuth2PasswordRequestForm(
    username=str(user_data_2.email),
    password=user_data_2.password,
)