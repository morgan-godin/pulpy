from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from app import db, login_manager

class User(UserMixin, db.Model):
    user_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    user_nom = db.Column(db.Text, nullable=False)
    user_login = db.Column(db.String(45), nullable=False, unique=True)
    user_email = db.Column(db.Text, nullable=False)
    user_password = db.Column(db.String(100), nullable=False)

    @staticmethod
    def identification(login, motdepasse):
        '''Identifie un utilisateur. Si cela renvoie les données de l'utilisateur.

            :param login: Login de l'utilisateur
            :param motdepasse: Mot de passe de l'utilisateur
            returns: Si réussite, données de l'utilisateur
            :rtype: User or None
            '''
        utilisateur = User.query.filter(User.user_login == login).first()
        if utilisateur and check_password_hash(utilisateur.user_password, motdepasse):
            return utilisateur
        return None

    @staticmethod
    def creer (login, email, nom, motdepasse):
        '''Crée un compte utilisateur. Retourne un tuple (booléen, User ou liste).
        Si il y a une erreur, la fonction renvoie False suivi d'une liste d'erreur
        Sinon elle renvoie True suivi de la donnée enregistrée

        :param login: Login de l'utilisateur
        :param email: Email de l'utilisateur
        :param nom: Nom de l'utilisateur
        :param motdepasse: Mot de passe de l'utilisateur
        '''

        erreurs = []
        if not login:
            erreurs.append("Veuillez fournir un login")
        if not email:
            erreurs.append("Veuillez fournir un email")
        if not nom:
            erreurs.append("Veuillez fournir un nom")
        if not motdepasse or len(motdepasse) < 6:
            erreurs.append("Veuillez fournir un mot de passe d'au moins 6 caractères")

        uniques = User.query.filter(
            db.or_(User.user_email == email, User.user_login == login)
        ).count()
        if uniques > 0:
            erreurs.append("Le login ou l'email fournis sont sont déjà utilisés")

        if len(erreurs) > 0:
            return False, erreurs

        utilisateur = User(
            user_nom = nom,
            user_login = login,
            user_email = email,
            user_password = generate_password_hash(motdepasse)
        )

        try:
            db.session.add(utilisateur)
            db.session.commit()

            return  True, utilisateur
        except Exception as erreur:
            return False, [str(erreur)]

    def get_id(self):
        return self.user_id

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

