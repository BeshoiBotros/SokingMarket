# SokingMarket
SokingMarket is a Backe-End Using Django, Markets Can uses that Project to handle online requests and make a connection between all branches


# User
user can create registration and login also have a profile, can update his profile, main information,
also user can add item to his cart, make orders and view all products on system


# installation
1. open CMD or terminal and create new Virtual Environment &#8594; python -m venv <VENV_NAME>
2. ``` cd <VENV_NAME> ```
4. activate the Virtual Environment &#8594; ``` ./Scripts/activate ``` if you are using linux &#8594; ``` source bin/activate ```

```bash
1.  git clone https://github.com/BeshoiBotros/SokingMarket.git
2.  cd SocingMarket
3.  pip install -r requirements.txt
4.  python manage.py migrate
5.  python manage.py createsuperuser
6. python manage.py runserver
