## Configuração Inicial

Certifique-se de que você tenha o Docker instalado. Em seguida, execute o seguinte comando para iniciar um contêiner Redis:

`docker run --rm -d -p 6379:6379 redis:7`

## Ambiente Virtual

Agora, ative o ambiente virtual usando o comando `workon`:

`workon nt`

## Executando o Servidor

Para iniciar o servidor de desenvolvimento do Django, use o seguinte comando:

`python manage.py runserver`

## Migrações de Banco de Dados

Se você fez alterações no modelo de banco de dados, certifique-se de criar e aplicar as migrações:

`python manage.py makemigrations`
`python manage.py migrate`

Para atualizar seeds use:

`python manage.py dumpdata auth.group --indent 4 > djangoNT/seed/0001_Group.json
python manage.py dumpdata auth.user --indent 4 > djangoNT/seed/0002_User.json
python manage.py dumpdata iot --indent 4 > djangoNT/seed/0003_Sensor.json`

Para semear use:

`python manage.py loaddata djangoNT/seed/\*.json` ou `python manage.py seed`

## Criando um Superusuário

Para criar um superusuário (administrador) do Django, execute o seguinte comando e siga as instruções:

`python manage.py createsuperuser`
