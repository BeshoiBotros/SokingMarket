# SokingMarket
SokingMarket is a Backe-End Using Django, Markets Can uses that Project to handle online requests and make a connection between all branches


# User
user can create registration and login also have a profile, can update his profile, main information,
also user can add item to his cart, make orders and view all products on system


# installation
1. open CMD or terminal and create new Virtual Environment &#8594; python -m venv <VENV_NAME>
2. ``` cd <VENV_NAME> ```
4. activate the Virtual Environment &#8594; ``` ./Scripts/activate ``` if you are using linux or MAC &#8594; ``` source bin/activate ```

```bash
git clone https://github.com/BeshoiBotros/SokingMarket.git
cd SocingMarket
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
bash```
5. after doing those steps open browser and  enter that url &#8594; https://127.0.0.1:8080
