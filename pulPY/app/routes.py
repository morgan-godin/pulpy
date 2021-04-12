from app import app
from app import db
from sqlalchemy import or_, and_
from flask import render_template, request, flash, redirect, url_for
from flask_login import login_user, current_user, logout_user, login_required
from .modeles.db_covers import Artiste, Editeur, Magazine, Publication, Couv_num, Jointure_Couv_num_Artiste
from .modeles.db_users import User

@app.route('/')
def page_accueil():
    return render_template('pages/accueil.html')

@app.route('/a_propos')
def a_propos():
    return render_template("/pages/a-propos.html")

@app.route('/register', methods=["GET", "POST"])
def inscription():
    '''Route gérant les inscriptions
    '''
    if request.method == "POST":
        statut, donnees = User.creer(
            login= request.form.get("login", None),
            email= request.form.get("email", None),
            nom= request.form.get("nom", None),
            motdepasse= request.form.get("motdepasse", None)
        )
        if statut is True:
            flash("Enregistrement effectuée. Veuillez vous identifier")
            return redirect("/")
        else:
            flash("Les erreurs suivantes ont été rencontrées : "  + ",".join(donnees), "error")
            return render_template('pages/inscription.html')
    else:
        return render_template("pages/inscription.html")

@app.route('/connexion', methods=["POST", "GET"])
def connexion():
    '''Route gérant les connexions
    '''
    if current_user.is_authenticated is True:
        flash("Vous êtes déjà connecté", "info")
        return redirect('/')
    if request.method == "POST":
        utilisateur = User.identification(
            login= request.form.get("login", None),
            motdepasse= request.form.get("motdepasse", None)
        )
        if utilisateur:
            flash("Connexion réussie", "success")
            login_user(utilisateur)
            return redirect("/")
        else:
            flash("Les identifiants n'ont pas été reconnus", "error")
    return render_template("pages/connexion.html")

@app.route('/deconnexion', methods=["POST", "GET"])
def deconnexion():
    if current_user.is_authenticated is True:
        logout_user()
    flash("Vous êtes déconnecté", "info")
    return redirect("/")

@app.route("/recherche")
def recherche():
    '''Route permettant de gérer la recherche
    '''

    motclef = request.args.get("keyword", None)
    page = request.args.get("page", 1)

    if isinstance(page, str) and page.isdigit():
        page = int(page)
    else:
        page = 1

    resultats = []

    if motclef:
        resultats = Publication.query.filter(or_(
            Publication.numero.like("%{}%".format(motclef)),
            Publication.editeurpublication.has(Editeur.nom.like("%{}%".format(motclef))),
            Publication.couv_numpublication.has(Couv_num.artiste.any(Artiste.prenom.like("%{}%".format(motclef)))),
            Publication.couv_numpublication.has(Couv_num.artiste.any(Artiste.nom.like("%{}%".format(motclef)))),
            Publication.couv_numpublication.has(Couv_num.ark.like("%{}%".format(motclef))),
            Publication.magazinepublication.has(Magazine.titre.like("%{}%".format(motclef)))
        )).paginate(page=page)

    return render_template("pages/recherche.html", resultats = resultats, keyword = motclef)

@app.route('/index')
def index():
    '''Route pour afficher un index rangeant les numéros de magazines par titres.
    '''

    magazines = Magazine.query.order_by(Magazine.idmagazine).all()
    numeros = Publication.query.order_by(Publication.idpublication.desc()).all()
    couvs = Couv_num.query.all()

    return render_template('pages/index.html',
                           magazines=magazines,
                           numeros = numeros,
                           couvs = couvs)

@app.route('/galerie')
def galerie():

    couvs = Couv_num.query.all()

    return render_template('pages/galerie.html', couvs = couvs)

@app.route('/couverture/<int:couv_id>')
def couverture(couv_id):
    '''Route gérant la création des notices pour chaque couverture

    :param couv_id: Id de la clé primaire de la table Couv_num
    :returns: Création de la page de la notice
    '''

    unique_couv = Couv_num.query.filter(Couv_num.idcouv_num == couv_id).first()

    artiste_couv = Artiste.query.join(Artiste.couv_num).filter(Couv_num.idcouv_num == couv_id).first()
    publication_couv = Publication.query.filter(Publication.couv_numpublication.has(Couv_num.idcouv_num == couv_id)).first()
    editeur_couv = Editeur.query.join(Publication).filter(Publication.couv_numpublication.has(Couv_num.idcouv_num == couv_id)).first()
    magazine_couv = Magazine.query.join(Publication).filter(Publication.couv_numpublication.has(Couv_num.idcouv_num == couv_id)).first()

    return render_template('pages/couverture.html',
                           couv = unique_couv,
                           artiste = artiste_couv,
                           publication = publication_couv,
                           editeur = editeur_couv,
                           magazine = magazine_couv)


@app.route('/ajout_deconnecte')
def ajout_deconnecte():
    return render_template('pages/ajout_deconnecte.html')


@app.route('/ajout', methods=["GET", "POST"])
@login_required
def ajout():
    '''Route gérant le formulaire d'ajout des informations sur les couvertures

    :returns: Création de nouvelles données et de nouveaux id
    '''
    liste_nom_artiste = Artiste.query.with_entities(Artiste.nom).distinct()
    liste_prenom_artiste = Artiste.query.with_entities(Artiste.prenom).distinct()
    liste_URL = Couv_num.query.with_entities(Couv_num.URL).distinct()
    liste_ark = Couv_num.query.with_entities(Couv_num.ark).distinct()
    liste_fichier = Couv_num.query.with_entities(Couv_num.fichier).distinct()
    liste_nom_editeur = Editeur.query.with_entities(Editeur.nom).distinct()
    liste_titre_mag = Magazine.query.with_entities(Magazine.titre).distinct()
    liste_date_pub = Publication.query.with_entities(Publication.date_de_publication).distinct()
    liste_numero = Publication.query.with_entities(Publication.numero).distinct()

    if request.method == "POST":
        #Artiste
        nomArtiste = request.form.get("Nom", None)
        prenomArtiste = request.form.get("Prenom", None)
        #Couverture numérisée
        URL = request.form.get("URL", None)
        ark = request.form.get("Ark", None)
        fichier = request.form.get("fichier", None)
        #Editeur
        nomEditeur = request.form.get("Nom_editeur", None)
        #Magazine
        titre = request.form.get("Titre", None)
        #Publication
        numero = request.form.get("Numero", None)
        date_pub = request.form.get("Date_de_publication", None)


        idcouv_num = Couv_num.ajouter(URL, ark, fichier)
        idediteur = Editeur.ajouter(nomEditeur)
        idartiste = Artiste.ajouter(nomArtiste, prenomArtiste)
        idmagazine = Magazine.ajouter(titre)
        idpublication = Publication.ajouter(numero, date_pub, idcouv_num, idmagazine, idediteur)
        Couv_num.association_Artiste_Couv_num(idcouv_num, idartiste)
        flash("Ajout réussi", "success")
        return render_template("pages/ajout.html")

    return render_template("pages/ajout.html", nom="Site", Listenomartiste = liste_nom_artiste,
                           Listeprenomartiste = liste_prenom_artiste, ListeURL = liste_URL, Listeark = liste_ark,
                           Listefichier = liste_fichier, Listenomediteur = liste_nom_editeur,
                           Listetitremag = liste_titre_mag, Listedatepub = liste_date_pub, Listenumero = liste_numero)


@app.route("/modifier/<int:couv_id>", methods = ["POST", "GET"])
@login_required
def modifier(couv_id):
    '''Route permettant la modification de la notice d'une couverture

    :param couv_id: Id de la couverture
    :returns: Modification des données
    '''
    #on réucpère les informations pour créer la page correspondante à l'id de la couverture
    couv = Couv_num.query.get(couv_id)
    artiste = Artiste.query.join(Artiste.couv_num).filter(Couv_num.idcouv_num == couv_id).first()
    magazine = Magazine.query.join(Publication).filter(
        Publication.couv_numpublication.has(Couv_num.idcouv_num == couv_id)).first()
    publication = Publication.query.filter(
        Publication.couv_numpublication.has(Couv_num.idcouv_num == couv_id)).first()
    editeur = Editeur.query.join(Publication).filter(
        Publication.couv_numpublication.has(Couv_num.idcouv_num == couv_id)).first()

    #on récupère les listes des informations pour aider à remplir les champs
    liste_nom_artiste = Artiste.query.with_entities(Artiste.nom).distinct()
    liste_prenom_artiste = Artiste.query.with_entities(Artiste.prenom).distinct()
    liste_URL = Couv_num.query.with_entities(Couv_num.URL).distinct()
    liste_ark = Couv_num.query.with_entities(Couv_num.ark).distinct()
    liste_fichier = Couv_num.query.with_entities(Couv_num.fichier).distinct()
    liste_nom_editeur = Editeur.query.with_entities(Editeur.nom).distinct()
    liste_titre_mag = Magazine.query.with_entities(Magazine.titre).distinct()
    liste_date_pub = Publication.query.with_entities(Publication.date_de_publication).distinct()
    liste_numero = Publication.query.with_entities(Publication.numero).distinct()


    if request.method == "GET":
        return render_template("pages/modifier.html",
                               couv = couv,
                               artiste = artiste,
                               magazine = magazine,
                               publication = publication,
                               editeur = editeur,
                               Listenomartiste=liste_nom_artiste,
                               Listeprenomartiste=liste_prenom_artiste,
                               ListeURL=liste_URL,
                               Listeark=liste_ark,
                               Listefichier=liste_fichier,
                               Listenomediteur=liste_nom_editeur,
                               Listetitremag=liste_titre_mag,
                               Listedatepub=liste_date_pub,
                               Listenumero=liste_numero,
                               )


    #on récupère les informations du formulaire
    nv_prenom_artiste = request.form.get("nv_prenom_artiste", None)
    nv_nom_artiste = request.form.get("nv_nom_artiste", None)
    nv_URL = request.form.get("nv_URL", None)
    nv_ark = request.form.get("nv_ark", None)
    nv_titre = request.form.get("nv_titre", None)
    nv_numero = request.form.get("nv_numero", None)
    nv_date = request.form.get("nv_date", None)
    nv_editeur = request.form.get("nv_editeur", None)

    #on récupère les données déjà existantes pour les comparer avec les nouvelles
    editeurs = Editeur.query.all()
    magazines = Magazine.query.all()
    artistes = Artiste.query.all()

    if request.method == "POST":

        for editeur in editeurs:
            if nv_editeur == editeur.nom:
                publication.editeur_idediteur = editeur.idediteur
            else:
                idediteur = Editeur.ajouter(nv_editeur)
                publication.editeur_idediteur = idediteur

        for magazine in magazines:
            if nv_titre == magazine.titre:
                publication.magazine_idmagazine = magazine.idmagazine
            else:
                idmagazine = Magazine.ajouter(nv_titre)
                publication.magazine_idmagazine = idmagazine

        for artiste in artistes:
            if nv_nom_artiste == artiste.nom and nv_prenom_artiste == artiste.prenom:
                artiste_liste = []
                artiste_liste.append(artiste)
                #on crée une liste qui ne contient que l'artiste sur lequel on itère
                #car couv.artiste est une liste qui ne contient qu'un objet
                couv.artiste = artiste_liste
            else:
               ajout_artiste = Artiste.ajouter(nv_nom_artiste, nv_prenom_artiste)
               Couv_num.artiste = ajout_artiste

        #Les éléments suivants n'ont pas besoin d'être testés

        #Modification Couv_num
        couv.URL = nv_URL
        couv.ark = nv_ark
        #Modification Publication
        publication.numero = nv_numero
        publication.date_de_publication = nv_date

        db.session.commit()
        flash("Modification réussie", "success")
        return redirect("/")

@app.route("/supprimer/<int:couv_id>", methods=["POST","GET"])
@login_required
def supprimer(couv_id):
    '''Route gérant la suppression d'une notice de couverture

    :param: couv_id: id de la couverture
    :returns: Suppression des données associées à la couverture
    si elles ne sont pas associées à d'autres
    '''

    couv = Couv_num.query.get(couv_id)
    artiste = Artiste.query.join(Artiste.couv_num).filter(Couv_num.idcouv_num == couv_id).first()
    magazine = Magazine.query.join(Publication).filter(Publication.couv_numpublication.has(Couv_num.idcouv_num == couv_id)).first()
    publication = Publication.query.filter(Publication.couv_numpublication.has(Couv_num.idcouv_num == couv_id)).first()
    editeur = Editeur.query.join(Publication).filter(Publication.couv_numpublication.has(Couv_num.idcouv_num == couv_id)).first()

    if request.method=="GET":
        return render_template('/pages/supprimer.html',
                           couv=couv,
                           artiste=artiste,
                           magazine=magazine,
                           publication=publication,
                           editeur=editeur)

    nb_editeurs = len(Publication.query.filter(Publication.editeur_idediteur == editeur.idediteur).all())
    nb_magazines = len(Publication.query.filter(Publication.magazine_idmagazine == magazine.idmagazine).all())
    nb_artistes = len(Couv_num.query.filter(Couv_num.artiste.contains(artiste)).all())

    if request.method=="POST":
        #pour chaque élément on vérifie s'il existe pour une autre couverture/publication avant de le supprimer
        if nb_editeurs == 1:
            db.session.delete(editeur)

        if nb_magazines == 1:
            db.session.delete(magazine)

        if nb_artistes == 1:
            db.session.delete(artiste)

        #on supprime la publication dans tous les cas puisqu'elle est forcément associée à la couverture
        db.session.delete(couv)
        db.session.delete(publication)

        db.session.commit()

    flash("Suppression réussie", "success")
    return redirect("/")