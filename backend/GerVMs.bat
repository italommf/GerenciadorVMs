@echo off
REM Ative o ambiente virtual (opcional)
call venv\Scripts\activate

REM Execute o servidor Django em segundo plano
start /b python manage.py runserver

REM O script não precisa da pausa, pois você não quer que a janela fique aberta
