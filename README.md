Pour installer et lancer l'application LITReview:<br/>
1 - cloner le projet<br/>
<b>$ git clone https://github.com/yoan34/litReview.git</b><br/><br/>
2 - Aller dans le projet et créer un environnement de travail virtuel:<br/>
<b>$ cd litReview/ && python3 -m venv env</b><br/><br/>
3 - Activer le bureau virtuel et ajouter les dépendances nécessaires au projet.<br/>
<b>$ . env/bin/activate && pip install -r requirements.txt</b><br/><br/>
4 - Lancer l'application et se rendre sur le site:<br/>
<b>$ cd litreview/ && python manage.py runserver</b><br/>
<b>Clické sur le lien ou rendez-vous sur 127.0.0.1:8000/</b><br/><br/>
5 - Lancer un rapport flake8:<br/>
  <b>$ flake8 --format=html --htmldir=flake-report</b>

