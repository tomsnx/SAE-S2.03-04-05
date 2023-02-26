#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import request, render_template, redirect, abort, flash, session

from connexion_db import get_db

client_panier = Blueprint('client_panier', __name__,
                        template_folder='templates')


@client_panier.route('/client/panier/add', methods=['POST'])
def client_panier_add():
    mycursor = get_db().cursor()
    id_utilisateur = session['id_user']
    id_gant = request.form.get('id_gant')
    quantite = request.form.get('quantite')

    sql = """SELECT *
             FROM ligne_panier
             WHERE id_gant = %s AND id_utilisateur = %s"""
    mycursor.execute(sql, (id_gant, id_utilisateur))
    article_panier = mycursor.fetchone()

    mycursor.execute("SELECT * FROM gant WHERE id_gant = %s", (id_gant))
    gant = mycursor.fetchone()

    if not (article_panier is None) and article_panier['quantite'] >= 1:
        tuple_update = (int(quantite) + article_panier['quantite'], id_utilisateur, id_gant)
        sql = "UPDATE ligne_panier SET quantite = %s WHERE id_utilisateur = %s AND id_gant = %s"
        mycursor.execute(sql, tuple_update)
    else :
        tuple_insert = (id_utilisateur, id_gant, quantite)
        sql = "INSERT INTO ligne_panier(id_utilisateur, id_gant, quantite, date_ajout) VALUES (%s, %s, %s, current_timestamp)"
        mycursor.execute(sql, tuple_insert)
    
    mycursor.execute("UPDATE gant SET stock_gant = stock_gant-%s WHERE id_gant = %s", (quantite, id_gant))
    gant = mycursor.fetchone()

    get_db().commit()
    return redirect('/client/gant/show')
    
    #id_declinaison_article=request.form.get('id_declinaison_article',None)
    id_declinaison_article = 1

# ajout dans le panier d'une déclinaison d'un article (si 1 declinaison : immédiat sinon => vu pour faire un choix
    # sql = '''    '''
    # mycursor.execute(sql, (id_article))
    # declinaisons = mycursor.fetchall()
    # if len(declinaisons) == 1:
    #     id_declinaison_article = declinaisons[0]['id_declinaison_article']
    # elif len(declinaisons) == 0:
    #     abort("pb nb de declinaison")
    # else:
    #     sql = '''   '''
    #     mycursor.execute(sql, (id_article))
    #     article = mycursor.fetchone()
    #     return render_template('client/boutique/declinaison_article.html'
    #                                , declinaisons=declinaisons
    #                                , quantite=quantite
    #                                , article=article)

# ajout dans le panier d'un article


    return redirect('/client/gant/show')

@client_panier.route('/client/panier/delete', methods=['POST'])
def client_panier_delete():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_ligne_panier = request.form.get('id_ligne_panier','')
    quantite = 1

    # ---------
    # partie 2 : on supprime une déclinaison de l'article
    # id_declinaison_article = request.form.get('id_declinaison_article', None)

    sql = '''SELECT id_ligne_panier, id_utilisateur, id_gant as id_article, quantite, date_ajout
             FROM ligne_panier
             WHERE ligne_panier.id_utilisateur = %s AND ligne_panier.id_ligne_panier = %s'''
    mycursor.execute(sql, [id_client, id_ligne_panier])
    article_panier = mycursor.fetchone()
    print(article_panier)

    if not(article_panier is None) and article_panier['quantite'] > 1:
        sql = '''UPDATE ligne_panier
                 SET ligne_panier.quantite = quantite - %s
                 WHERE ligne_panier.id_ligne_panier = %s AND ligne_panier.id_utilisateur = %s;'''
        mycursor.execute(sql, [quantite, id_ligne_panier, id_client])
    else:
        sql = ''' suppression de la ligne de panier'''

    # sql = """UPDATE"""
    get_db().commit()
    return redirect('/client/gant/show')





@client_panier.route('/client/panier/vider', methods=['POST'])
def client_panier_vider():
    mycursor = get_db().cursor()
    client_id = session['id_user']

    sql = 'sql à écrire'
    items_panier = []
    for item in items_panier:
        sql = ''' suppression de la ligne de panier de l'article pour l'utilisateur connecté'''

        sql2=''' mise à jour du stock de l'article : stock = stock + qté de la ligne pour l'article'''
        get_db().commit()
    return redirect('/client/gant/show')


@client_panier.route('/client/panier/delete/line', methods=['POST'])
def client_panier_delete_line():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    #id_declinaison_article = request.form.get('id_declinaison_article')

    sql = ''' selection de ligne du panier '''

    sql = ''' suppression de la ligne du panier '''
    sql2=''' mise à jour du stock de l'article : stock = stock + qté de la ligne pour l'article'''

    get_db().commit()
    return redirect('/client/gant/show')

@client_panier.route('/client/panier/filtre', methods=['POST'])
def client_panier_filtre():
    # filter_word = request.form.get('filter_word', None)
    # filter_prix_min = request.form.get('filter_prix_min', None)
    # filter_prix_max = request.form.get('filter_prix_max', None)
    # filter_types = request.form.getlist('filter_types', None)
    # # test des variables puis
    # # mise en session des variables
    # return redirect('/client/gant/show')
    
    filter_word = request.form.get('filter_word', None)
    filter_prix_min = request.form.get('filter_prix_min', None)
    filter_prix_max = request.form.get('filter_prix_max', None)
    filter_types = request.form.getlist('filter_types', None)
    print("word" +filter_word + str(len(filter_word)))
    print(filter_types)
    if filter_word or filter_word == "":
        if len(filter_word) > 1:
            if filter_word.isalpha():
                session['filter_word'] = filter_word
            else:
                flash(u'votre Mot recherché doit uniquement être composé de lettres')
        else:
            if len(filter_word) == 1:
                flash(u'votre Mot recherché doit être composé de au moins 2 lettres')
            else :
                session.pop('filter_word', None)
    if filter_prix_min or filter_prix_max:
        if filter_prix_min.isdecimal() and filter_prix_max.isdecimal():
            if int(filter_prix_min) < int(filter_prix_max):
                session['filter_prix_min'] = filter_prix_min
                session['filter_prix_max'] = filter_prix_max
            else:
                flash(u'min < max')
        else:
            flash(u'min et max doivent être des numériques')
    if filter_types and filter_types != []:
        print("filter_types:", filter_types)
        if isinstance(filter_types, list):
            check_filter_type = True
            for number_type in filter_types:
                print('test', number_type)
                if not number_type.isdecimal():
                    check_filter_type = False
            if check_filter_type:
                session['filter_types'] = filter_types

    sql = '''
        SELECT id_gant AS id_article, nom_gant AS nom, prix_gant AS prix, stock_gant AS stock, image_gant AS image, 
        FROM gant
        ORDER BY nom_gant;
        '''
    list_param = []
    condition_and = ""
    if "filter_word" in session or "filter_prix_min" in session or "filter_prix_max" in session or "filter_types" in session:
        sql = sql + "WHERE "
    if "filter_word" in session:
        sql = sql + " nom LIKE %s "
        recherche = "%" + session["filter_word"] + "%"
        list_param.append(recherche)
        condition_and = " AND "
    if "filter_prix_min" in session or "filter_prix_max" in session:
        sql = sql + condition_and + " prix BETWEEN %s AND %s "
        list_param.append(session["filter_prix_min"])
        list_param.append(session["filter_prix_max"])
        condition_and = " AND "
    if "filter_types" in session:
        sql = sql + condition_and + "("
        last_item = session['filter_types'][-1]
        for item in session["filter_types"]:
            sql = sql + " gant.id_article=%s "
            if item != last_item:
                sql = sql + " OR "
            list_param.append(item)
        sql = sql + ")"
    tuple_sql = tuple(list_param)
    cursor = get_db().cursor()
    print(sql)
    cursor.execute(sql, tuple_sql)
    ville = cursor.fetchall()
    sql = """SELECT id_parking, photo, nom_parking, nb_places, adresse, date_construction, prix_place, parking.ville_id,ville.nom_ville, ville.id_ville
             FROM ville
             RIGHT JOIN parking on parking.ville_id = ville.id_ville
             GROUP BY nom_ville;"""
    cursor.execute(sql)
    carte = cursor.fetchall()
    
    return redirect('/client/gant/show'
                    , articles=articles
                    , articles_panier=articles_panier
                   #, prix_total=prix_total
                   , items_filtre=types_article)



@client_panier.route('/client/panier/filtre/suppr', methods=['POST'])
def client_panier_filtre_suppr():
    # suppression  des variables en session
    print("suppr filtre")
    return redirect('/client/gant/show')
