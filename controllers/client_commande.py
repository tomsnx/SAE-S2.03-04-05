#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g
from datetime import datetime
from connexion_db import get_db

client_commande = Blueprint('client_commande', __name__,
                        template_folder='templates')


@client_commande.route('/client/commande/valide', methods=['POST'])
def client_commande_valide():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    sql = ''' selection des articles d'un panier 
    '''
    articles_panier = []
    if len(articles_panier) >= 1:
        sql = ''' calcul du prix total du panier '''
        prix_total = None
    else:
        prix_total = None
    # etape 2 : selection des adresses
    return render_template('client/boutique/panier_validation_adresses.html'
                           #, adresses=adresses
                           , articles_panier=articles_panier
                           , prix_total= prix_total
                           , validation=1
                           )

@client_commande.route('/client/commande/add', methods=['POST'])
def client_commande_add():
    mycursor = get_db().cursor()

    # choix de(s) (l')adresse(s)

    id_client = session['id_user']

    sql = "SELECT * FROM ligne_panier WHERE id_utilisateur = %s"
    mycursor. execute (sql, id_client)
    items_ligne_panier = mycursor.fetchall()

    if items_ligne_panier is None or len(items_ligne_panier) < 1:
        flash (u'Pas d\'articles dans le panier')
        return redirect('/client/gant/show')
    
    date_commande = datetime.now() .strftime ('%Y-%m-%d %H:%M:%S')
    tuple_insert = (date_commande, id_client)
    # 1 : etat de commande : "en cours" ou "validé"
    sql = """INSERT INTO commande (date_achat, id_utilisateur, id_etat)
             VALUES (%s, %s, 1)"""
    mycursor.execute (sql, tuple_insert)

    sql = "SELECT last_insert_id() as last_insert_id"
    mycursor.execute(sql)
    commande_id = mycursor.fetchone()

    print (commande_id, tuple_insert)
    for item in items_ligne_panier:
        sql = "DELETE FROM ligne_panier WHERE id_utilisateur = %s AND id_gant = %s"
        mycursor.execute(sql, (item['id_utilisateur'], item['id_gant']))
        sql = "SELECT 1 AS prix FROM gant WHERE id_gant = %s"
        mycursor.execute (sql, item['id_gant'])
        prix = mycursor.fetchone ()
        print (prix)
        sql = "INSERT INTO ligne_commande (id_commande, id_gant, prix, quantite) VALUES (%s, %s, %s, %s)"
        tuple_insert = (commande_id['last_insert_id'], item['id_gant'], prix['prix'], item['quantite'])
        print (tuple_insert)
        mycursor.execute(sql, tuple_insert)
    get_db().commit()

    flash(u'Commande ajoutée','alert-success')
    return redirect('/client/gant/show')



@client_commande.route('/client/commande/show', methods=['get','post'])
def client_commande_show():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    # sql = '''selection des commandes ordonnées par état puis par date d'achat descendant'''
    sql = """SELECT *
             FROM commande
             WHERE id_utilisateur = %s
             ORDER BY id_etat, date_achat DESC"""
    mycursor.execute(sql, [id_client])
    commandes = mycursor.fetchall()

    articles_commande = None
    commande_adresses = None
    id_commande = request.args.get('id_commande', None)
    if id_commande != None:
        print(id_commande)
        sql = ''' selection du détails d'une commande '''

        # partie 2 : selection de l'adresse de livraison et de facturation de la commande selectionnée
        sql = ''' selection des adresssses '''

    return render_template('client/commandes/show.html'
                           , commandes=commandes
                           , articles_commande=articles_commande
                           , commande_adresses=commande_adresses
                           )

