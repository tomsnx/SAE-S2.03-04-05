#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import request, render_template, redirect, abort, flash, session
from datetime import datetime

from connexion_db import get_db

client_panier = Blueprint('client_panier', __name__,
                        template_folder='templates')


@client_panier.route('/client/panier/add', methods=['POST'])
def client_panier_add():
    mycursor = get_db().cursor()

    id_utilisateur = session['id_user']
    id_gant = request.form.get('id_gant')
    quantite = request.form.get('quantite')

    sql = """SELECT * FROM ligne_panier 
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

    mycursor.execute("UPDATE gant SET stock_gant = stock_gant - %s WHERE id_gant = %s", (quantite, id_gant))
    gant = mycursor.fetchone()

    get_db().commit()
    return redirect('/client/gant/show')
    
    #id_declinaison_article=request.form.get('id_declinaison_article',None)
    #id_declinaison_article = 1

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
    #return redirect('/client/gant/show')

# @client_panier.route('/client/panier/delete', methods=['POST'])
# def client_panier_delete():
#     mycursor = get_db().cursor()
    
#     id_client = session['id_user']
#     id_gant = request.form.get('id_gant')
#     quantite = request.form.get('quantite')
#     quantite_ligne_panier = request.form.get('quantite_ligne_panier')
    
#     # ---------
#     # partie 2 : on supprime une déclinaison de l'article

#     sql = ''' SELECT * FROM ligne_panier lp
#               WHERE lp.id_utilisateur = %s AND lp.id_gant = %s '''
#     mycursor.execute(sql, (id_client, id_gant, ))
#     gant_panier = mycursor.fetchone()

    
    
#     return redirect('/client/gant/show')

@client_panier.route('/client/panier/delete', methods=['POST'])
def client_panier_delete():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_gant = request.form.get('id_gant', '')

    quantite = 1

    sql = '''SELECT quantite FROM ligne_panier
             WHERE id_gant = %s AND id_utilisateur = %s'''
    mycursor.execute(sql, (id_gant, id_client))
    article_panier = mycursor.fetchone()

    if not(article_panier is None) and article_panier['quantite'] > 1:
        sql = '''UPDATE ligne_panier
                 SET quantite = quantite - 1
                 WHERE id_gant = %s AND id_utilisateur = %s'''
        mycursor.execute(sql, (id_gant, id_client))
        print(sql)
    if not(article_panier is None) and article_panier['quantite'] == 1:
        sql = '''DELETE FROM ligne_panier
                 WHERE id_gant = %s AND id_utilisateur = %s'''
        mycursor.execute(sql, (id_gant, id_client))
        pass

    sql = '''UPDATE gant
             SET stock_gant = stock_gant + 1
             WHERE id_gant = %s'''
    mycursor.execute(sql, id_gant)
    get_db().commit()
    return redirect('/client/gant/show')





@client_panier.route('/client/panier/vider', methods=['POST'])
def client_panier_vider():
    mycursor = get_db().cursor()
    client_id = session['id_user']
    sql = ''' SELECT * FROM ligne_panier  WHERE ligne_panier.id_utilisateur=%s'''
    mycursor.execute(sql, (client_id, ))
    gant_panier = mycursor.fetchall()
    for item in gant_panier:
        gant = item['id_gant']
        quantite = item['quantite']
        sql = ''' DELETE FROM ligne_panier WHERE ligne_panier.id_utilisateur=%s AND ligne_panier.id_gant=%s '''
        mycursor.execute(sql, (client_id, gant,))
        sql = '''UPDATE gant SET gant.stock_gant=gant.stock_gant+1 WHERE gant.id_gant=%s '''
        mycursor.execute(sql, (quantite, gant,))
        get_db().commit()

        # sql2=''' mise à jour du stock de l'article : stock = stock + qté de la ligne pour l'article'''
    return redirect('/client/gant/show')


@client_panier.route('/client/panier/delete/line', methods=['POST'])
def client_panier_delete_line():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_declinaison_article = request.form.get('id_declinaison_article')
    id_skis = request.form.get('id_skis')

    sql = ''' SELECT * FROM ligne_panier lp WHERE lp.utilisateur_id=%s AND lp.n_declinaison=%s AND lp.code_ski=%s '''
    mycursor.execute(sql, (id_client, id_declinaison_article, id_skis, ))
    declinaison = mycursor.fetchone()
    sql2 = ''' DELETE FROM ligne_panier WHERE ligne_panier.utilisateur_id=%s AND ligne_panier.n_declinaison=%s AND ligne_panier.code_ski=%s '''
    mycursor.execute(sql2, (id_client, id_declinaison_article, id_skis,))
    quantite = declinaison['quantite_ligne_panier']
    sql = ''' UPDATE declinaison dl SET dl.stock=dl.stock+%s WHERE id_declinaison=%s '''
    mycursor.execute(sql, (quantite, id_declinaison_article,))
    get_db().commit()
    # sql3=''' mise à jour du stock de l'article : stock = stock + qté de la ligne pour l'article'''

    return redirect('/client/gant/show')


@client_panier.route('/client/panier/filtre', methods=['POST'])
def client_panier_filtre():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    print("id_client =", id_client)

    filter_word = request.form.get('filter_word', None)
    filter_prix_min = request.form.get('filter_prix_min', None)
    filter_prix_max = request.form.get('filter_prix_max', None)
    filter_types = request.form.getlist('filter_types', None)

    # pour le filtre
    sql = """SELECT type_gant.id_type_gant as id_type_article, type_gant.libelle_type_gant as libelle
             FROM type_gant"""
    mycursor.execute(sql)
    type_gant = mycursor.fetchall()

    #vérif que c'est bien écrit
    if filter_word and filter_word != "":
        message = u'Filtre sur le mot: ' + filter_word
        flash(message, 'alert-success')

    if filter_prix_min or filter_prix_max:
        if filter_prix_min.isdecimal() and filter_prix_max.isdecimal():
            if int(filter_prix_min) < int(filter_prix_max):
                message = u'Filtre sur le prix avec un numérique entre : ' + filter_prix_min + " et " + filter_prix_max
                flash(message, 'alert-success')
            else:
                message = u'min < max'
                flash(message, 'alert-warning')
        else:
            message = u'min et max doivent être des numérique'
            flash(message, 'alert-warning')
    if filter_types and filter_types != []:
        message = u'Case à cocher selectionnées: '
        for case in filter_types:
            message += 'id: ' + case + ' '
        flash(message, 'alert-success')

    #mise en session
    if filter_word or filter_word == "":
        if len(filter_word) > 1:
            if filter_word.isalpha():
                session['filter_word'] = filter_word
            else:
                flash(u'Votre mot recherché doit uniquement être composé de lettres')
        else:
            if len(filter_word) == 1:
                flash(u'Votre mot recherché doit être composé de au moins 2 lettres')
            else:
                session.pop(filter_word, None)
    if filter_prix_min or filter_prix_max:
        if filter_prix_min.isdecimal() and filter_prix_max.isdecimal():
            if int(filter_prix_min) < int(filter_prix_max):
                session['filter_prix_min'] = filter_prix_min
                session['filter_prix_max'] = filter_prix_max
            else:
                flash(u'min < max')
        else:
            flash(u'min et max doivent être des numériques')
    print("filter_types:", filter_types)
    print("ss:", filter_word)
    if filter_types and filter_types != []:
        session['filter_types'] = []
        for number_type in filter_types:
            session['filter_types'].append(number_type)

    # # Ajouter une pause de 1 seconde pour permettre aux valeurs de session d'être enregistrées avant la redirection
    # time.sleep(1)
    gant_panier = []
    sqlTemp = """SELECT gant.id_gant, gant.nom_gant as nom, gant.image_gant as image, gant.stock_gant as stock, gant.id_type_gant, gant.prix_gant as prix
                 FROM gant
                 INNER JOIN type_gant ON type_gant.id_type_gant = gant.id_type_gant"""
    list_param = []
    condition_and = ""

    if "filter_word" in session or "filter_prix_min" in session or "filter_prix_max" in session or "filter_types" in session:
        sqlTemp = sqlTemp + " WHERE "
    if "filter_word" in session:
        sqlTemp = sqlTemp + " gant.nom_gant LIKE %s"
        recherche = "%" + session["filter_word"] + "%"
        list_param.append(recherche)
        condition_and = " AND "
    if "filter_prix_min" in session or "filter_prix_max" in session:
        sqlTemp = sqlTemp + condition_and + " gant.prix_gant BETWEEN %s AND %s "
        list_param.append(session["filter_prix_min"])
        list_param.append(session["filter_prix_max"])
        condition_and = " AND "
    if "filter_types" in session:
        sqlTemp = sqlTemp + condition_and + "("
        last_item = session['filter_types'][-1]
        for item in session['filter_types']:
            sqlTemp = sqlTemp + " gant.id_type_gant = %s "
            if item != last_item:
                sqlTemp = sqlTemp + " or "
            list_param.append(item)
        sqlTemp = sqlTemp + ")"
    sqlTemp = sqlTemp + " GROUP BY gant.id_gant"

    print(sqlTemp)

    tuple_sql = tuple(list_param)
    cursor_gant = get_db().cursor()
    print(sqlTemp)
    cursor_gant.execute(sqlTemp, tuple_sql)
    gant = cursor_gant.fetchall()

    #Pour pop les session à chaque filtre
    # session.pop('filter_word', None)
    # session.pop('filter_prix_min', None)
    # session.pop('filter_prix_max', None)
    # session.pop('filter_types', None)

    return render_template('client/boutique/panier_article.html', gant=gant,items_filtre=type_gant)

#en vrai ça sert plus à rien j'ai tout mis dans auth_security.py pour pop les sessions à chaque logout
@client_panier.route('/client/panier/filtre/suppr', methods=['POST'])
def client_panier_filtre_suppr():
    # suppression  des variables en session
    session.pop('filter_word', None)
    session.pop('filter_prix_min', None)
    session.pop('filter_prix_max', None)
    session.pop('filter_types', None)

    print("suppr filtre")
    return redirect('/client/gant/show')