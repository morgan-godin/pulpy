from app import db
 
Jointure_Couv_num_Artiste = db.Table('Jointure_Couv_num_Artiste',
                                     db.Column('artiste_idartiste', db.Integer, db.ForeignKey('artiste.idartiste')),
                                     db.Column('couv_num_idcouv_num', db.Integer, db.ForeignKey('couv_num.idcouv_num')))


class Artiste(db.Model):
    __tablename__ = 'artiste'
    idartiste = db.Column(db.Integer, unique=True, primary_key=True, autoincrement=True)
    nom = db.Column(db.Text)
    prenom = db.Column(db.Text, nullable=True)
    couv_num = db.relationship('Couv_num', secondary=Jointure_Couv_num_Artiste, back_populates ='artiste')

    @staticmethod
    def ajouter(nomArtiste, prenomArtiste):
        '''
        Ajoute des artistes dans la base de données

        :param nomArtiste: Nom de l'artiste dans formulaire.html
        :param prenomArtiste: Prénom de l'artiste dans formulaire.html
        :return: Retourne l'id de l'artiste déjà présent ou ajouté
        '''

        test = Artiste.query.filter(Artiste.nom == nomArtiste).filter(Artiste.prenom == prenomArtiste).scalar()

        if test is None:
            ajout_artiste = Artiste(nom=nomArtiste, prenom=prenomArtiste)
            db.session.add(ajout_artiste)
            db.session.commit()
            recup = Artiste.query.filter(Artiste.nom == nomArtiste).filter(Artiste.prenom == prenomArtiste).first()
            return recup.idartiste
        else:
            recup = Artiste.query.filter(Artiste.nom == nomArtiste).filter(Artiste.prenom == prenomArtiste).first()
            return recup.idartiste

class Couv_num(db.Model):
    __tablename__ = 'couv_num'
    idcouv_num = db.Column(db.Integer, unique=True, primary_key=True, autoincrement=True)
    URL = db.Column(db.Text)
    ark = db.Column(db.Text)
    fichier = db.Column(db.Text)
    artiste = db.relationship('Artiste', secondary=Jointure_Couv_num_Artiste, back_populates='couv_num')

    @staticmethod
    def ajouter(URL, ark, fichier):
        '''Ajoute des couvertures numérisées à la base de données

        :param URL: URL de l'image dans formulaire.html
        :param ark: Identifiant ark de la couverture numérisée dans formulaire.html
        :return: Retourne l'id de la couverture déjà présente ou ajoutée
        '''

        test = Couv_num.query.filter(Couv_num.URL == URL).filter(Couv_num.ark == ark).scalar()

        if test is None:
            ajoute_URL = Couv_num(URL = URL, ark = ark)
            db.session.add(ajoute_URL)
            db.session.commit()
            recup = Couv_num.query.filter(Couv_num.URL == URL).filter(Couv_num.ark == ark).first()
            return recup.idcouv_num

        else:
            recup = Couv_num.query.filter(Couv_num.URL == URL).filter(Couv_num.ark == ark).first()
            return recup.idcouv_num

    @staticmethod
    def association_Artiste_Couv_num(couv_numid, artisteid):
        '''Associer les lignes de la table Artiste et de la table Couv_num

        :param couv_numid: Identifiant de la couverture qu'on veut relier avec un artiste
        :param artisteid: Identifiant de l'artiste qu'on veut relier avec une couverture
        '''

        couv_numAssoc = Couv_num.query.filter(Couv_num.idcouv_num == couv_numid).first()
        artisteAssoc = Artiste.query.filter(Artiste.idartiste == artisteid).first()

        couv_numAssoc.artiste.append(artisteAssoc)

        db.session.add(couv_numAssoc)
        db.session.commit()

class Editeur(db.Model):
    __tablename__ = 'editeur'
    idediteur = db.Column(db.Integer, unique=True, primary_key=True, autoincrement=True)
    nom = db.Column(db.Text)

    @staticmethod
    def ajouter(nomEditeur):
        '''Ajoute un éditeur

        :param nomEditeur: Nom de l'éditeur dans formulaire.html
        :return: Retourne l'id de l'éditeur déjà présent ou ajouté'''

        test = Editeur.query.filter(Editeur.nom == nomEditeur).scalar()

        if test is None:
            ajouter_editeur = Editeur(nom = nomEditeur)

            db.session.add(ajouter_editeur)
            db.session.commit()

            recup = Editeur.query.filter(Editeur.nom == nomEditeur).first()
            return recup.idediteur
        else:
            recup = Editeur.query.filter(Editeur.nom == nomEditeur).first()
            return recup.idediteur

class Magazine(db.Model):
    __tablename__ = 'magazine'
    idmagazine = db.Column(db.Integer, unique=True, primary_key=True, autoincrement=True)
    titre = db.Column(db.Text)

    @staticmethod
    def ajouter(titre):
        '''Ajoute un titre de magazine

        :param titre: Titre du magazine dans formulaire.html
        :return: Retourne l'id du magazine déjà présent ou ajouté'''

        test = Magazine.query.filter(Magazine.titre == titre).scalar()

        if test is None:
            ajouter_magazine = Magazine(titre = titre)

            db.session.add(ajouter_magazine)
            db.session.commit()

            recup = Magazine.query.filter(Magazine.titre == titre).first()
            return recup.idmagazine

        else:
            recup = Magazine.query.filter(Magazine.titre == titre).first()
            return recup.idmagazine

class Publication(db.Model):
    __tablename__ = 'publication'
    idpublication = db.Column(db.Integer, unique=True, primary_key=True, autoincrement=True)
    numero = db.Column(db.Text)
    date_de_publication = db.Column(db.Text)
    couv_num_idcouv_num = db.Column(db.Integer, db.ForeignKey("couv_num.idcouv_num"))
    couv_numpublication = db.relationship('Couv_num', backref='publication')
    magazine_idmagazine = db.Column(db.Integer, db.ForeignKey('magazine.idmagazine'))
    magazinepublication = db.relationship('Magazine', backref='publication')
    editeur_idediteur = db.Column(db.Integer, db.ForeignKey('editeur.idediteur'))
    editeurpublication = db.relationship('Editeur', backref='publication')

    @staticmethod
    def ajouter(numero, date_pub, idcouv_num, idmagazine, idediteur):
        '''Ajoute un numero de magazine

        :param numero: Numéro de magazine dans formulaire.html
        :param date_pub: Date de publication du numéro dans formulaire.html
        :param idcouv_num: Id de la couverture du numéro dans formulaire.html
        :param idmagazine: Id du titre du magazine dans formulaire.html
        :param idediteur: Id de l'éditeur dans formulaire.html
        '''

        test = Publication.query.filter(Publication.numero == numero,
                                    Publication.date_de_publication == date_pub,
                                    Publication.couv_num_idcouv_num == idcouv_num,
                                    Publication.magazine_idmagazine == idmagazine,
                                    Publication.editeur_idediteur == idediteur).scalar()

        if test is None:
            ajouter_publication = Publication(numero = numero,
                                          date_de_publication = date_pub,
                                          couv_num_idcouv_num = idcouv_num,
                                          magazine_idmagazine = idmagazine,
                                          editeur_idediteur = idediteur)

            db.session.add(ajouter_publication)
            db.session.commit()

            recup = Publication.query.filter(
                Publication.numero == numero).filter(
                Publication.date_de_publication == date_pub).filter(
                Publication.couv_num_idcouv_num == idcouv_num).filter(
                Publication.magazine_idmagazine == idmagazine).filter(
                Publication.editeur_idediteur == idediteur).first()
            return recup.idpublication

        else:
            recup = Publication.query.filter(
                Publication.numero == numero).filter(
                Publication.date_de_publication == date_pub).filter(
                Publication.couv_num_idcouv_num == idcouv_num).filter(
                Publication.magazine_idmagazine == idmagazine).filter(
                Publication.editeur_idediteur == idediteur).first()
            return recup.idpublication
