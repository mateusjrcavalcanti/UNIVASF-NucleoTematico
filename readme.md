<p align="center">
  <img width="140" height="140" alt="CacheLib" src="frontend/static/images/logo.png">
</p>

# SolarEnergyAnalysis

Projeto desenvolvido como parte da disciplina 'NÚCLEO TEMÁTICO - FONTES ALTERNATIVAS DE ENERGIA' na UNIVASF para coletar dados de telemetria sobre a geração de energia fotovoltaica a partir de um circuito com o microcontrolador ATmega382P e o módulo ESP8266.
O [Django](https://www.djangoproject.com/) é a base deste projeto e oferece uma estrutura robusta para o desenvolvimento da aplicação. Para consultar a documentação específica e obter mais informações, visite o link fornecido.

## Uso

Certifique-se de ter o Python instalado em sua máquina. Em seguida, você pode instalar as dependências do Django usando o `pip`, o gerenciador de pacotes Python.

- Instação

  1. Abra um terminal e navegue até a raiz do seu projeto.

  2. Crie um ambiente virtual (recomendado para isolar as dependências do projeto):
     `python -m venv venv`

  3. Ative o ambiente virtual

  - No Windows:
    ` python -m venv venv`

  - No Linux
    `source venv/bin/activate`

  4. Instale as dependências do Django:
     `pip install -r requirements.txt`

  5. Execute as migrações de banco de dados:
     `python manage.py migrate`

  6. Instale o tailwind:
     `python manage.py tailwind install`

- Criando um Superusuário
  Para criar um superusuário (administrador) do Django, execute o seguinte comando:
  `python manage.py createsuperuser`

- Atualizar requisitos
  `pipreqs .`

## Executando o Projeto

Para iniciar o servidor do Django, use o seguinte comando:
`python manage.py runserver`

Para fazer o build do tailwind, use o seguinte comando:

- Em esenvolvimento:
  `python manage.py tailwind start`

- Em produção:
  `python manage.py tailwind build`

## Banco de Dados

- Em caso de alterações no modelo de banco de dados, certifique-se de criar e aplicar as migrações:

  ```sh
  python manage.py makemigrations
  python manage.py migrate
  ```

- Para atualizar as seeds use:
  ```sh
  python manage.py dumpdata auth.group --indent 4 > iot/seed/0001_Group.json
  python manage.py dumpdata auth.user --indent 4 > iot/seed/0002_User.json
  python manage.py dumpdata iot --indent 4 > iot/seed/0003_Sensor.json
  ```
- Para semear use:
  `python manage.py iot:seed`

## Créditos

- [Energia renovável ícones criados por Freepik - Flaticon](https://www.flaticon.com/br/icones-gratis/energia-renovavel)
- [Tail-kit Components and templates for Tailwind CSS](https://www.tailwind-kit.com/)
