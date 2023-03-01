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
    sql = """SELECT gant.nom_gant AS nom, gant.prix_gant AS prix, ligne_panier.quantite AS quantite,
                    ROUND((gant.prix_gant * ligne_panier.quantite),2) AS sous_total,
                    gant.id_gant, ligne_panier.n_declinaison AS id_declinaison_article
             FROM ligne_panier
             INNER JOIN gant ON ligne_panier.id_gant = gant.id_gant
             WHERE id_utilisateur = %s"""
    mycursor.execute(sql, (id_client, ))
    gant_panier = mycursor.fetchall()
    if len(gant_panier) >= 1:
        prix_total = 0
        for panier in gant_panier:
            prix_total = prix_total+panier['sous_total']
    else:
        prix_total = None
    # etape 2 : selection des adresses
    return render_template('client/boutique/panier_validation_adresses.html'
                           #, adresses=adresses
                           , gant_panier=gant_panier
                           , prix_total= prix_total
                           , validation=1
                           )

@client_commande.route('/client/commande/add', methods=['POST'])
def client_commande_add():
    mycursor = get_db().cursor()

    # choix de(s) (l')adresse(s)

    id_client = session['id_user']
    sql = ''' SELECT * FROM ligne_panier WHERE utilisateur_id=%s '''
    mycursor.execute(sql, id_client)
    items_ligne_panier = mycursor.fetchall()
    if items_ligne_panier is None or len(items_ligne_panier) < 1:
        flash(u'Pas d\'articles dans le panier', 'alert-warning')
        return redirect('/client/gant/show')
                                           # https://pynative.com/python-mysql-transaction-management-using-commit-rollback/
    date_commande = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    tuple_insert = (date_commande, id_client, '1')
    sql = ''' INSERT INTO commande(date_achat, id_utilisateur, id_etat) VALUES(%s, %s, %s) '''
    mycursor.execute(sql, tuple_insert)
    sql = "SELECT last_insert_id() as last_insert_id"
    mycursor.execute(sql)
    commande_id = mycursor.fetchone()
    # numéro de la dernière commande
    for item in items_ligne_panier:
        sql = ''' DELETE FROM ligne_panier
                  WHERE id_utilisateur = %s AND id_gant = %s '''
        mycursor.execute(sql, (item['id_utiliateur'], item['id_gant']))
        sql = "SELECT prix_gant AS prix FROM gant WHERE id_gant = %s"
        mycursor.execute(sql, item['id_gant'])
        prix = mycursor.fetchone()
        sql = "INSERT INTO ligne_commande(id_commande, id_gant, prix, quantite) VALUES (%s, %s, %s, %s)"
        tuple_insert = (commande_id['last_insert_id'], item['id_gant'], prix['prix'], item['quantite'])
        mycursor.execute(sql, tuple_insert)

    get_db().commit()
    flash(u'Commande ajoutée','alert-success')
    return redirect('/client/gant/show')




@client_commande.route('/client/commande/show', methods=['get','post'])
def client_commande_show():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    sql = '''SELECT c.date_achat, SUM(lc.quantite_ligne_commande) AS nbr_skis,c.id_commande,
             ROUND(SUM(lc.prix * lc.quantite_ligne_commande),2) AS prix_total,e.libelle,c.id_etat AS etat_id
             FROM commande c
             INNER JOIN ligne_commande lc on c.id_commande = lc.id_commande
             INNER JOIN etat e on c.id_etat = e.id_etat
             WHERE c.id_utilisateur=%s
             GROUP BY c.id_commande;'''
    mycursor.execute(sql, (id_client,))
    commandes = mycursor.fetchall()

    gant_commande = None
    commande_adresses = None
    id_commande = request.args.get('id_commande', None)
    if id_commande != None:
        print(id_commande)
        sql = '''SELECT sk.libelle_skis AS nom, lc.quantite_ligne_commande AS quantite, lc.prix, 
                 ROUND((lc.quantite_ligne_commande*lc.prix), 2) AS prix_ligne
                 FROM ligne_commande lc
                 INNER JOIN skis sk on lc.code_ski = sk.code_ski
                 WHERE id_commande=%s;'''
        mycursor.execute(sql, (id_commande, ))
        gant_commande = mycursor.fetchall()

        # partie 2 : selection de l'adresse de livraison et de facturation de la commande selectionnée
        sql = ''' selection des adressses '''

    return render_template('client/commandes/show.html'
                           , commandes=commandes
                           , gant_commande=gant_commande
                           , commande_adresses=commande_adresses
                           )