#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, abort, flash, session

from connexion_db import get_db

client_article = Blueprint('client_article', __name__,
                        template_folder='templates')

@client_article.route('/client/index')
@client_article.route('/client/gant/show')              # remplace /client
def client_article_show():                                 # remplace client_index
    mycursor = get_db().cursor()
    id_client = session['id_user']
    sql = '''
        SELECT gant.id_gant, nom_gant AS nom, prix_gant AS prix, stock_gant AS stock, image_gant AS image
        FROM gant
        ORDER BY nom_gant;
        '''
    mycursor.execute(sql)
    gants = mycursor.fetchall()
    articles = gants

    # utilisation du filtre
    sql = '''
            SELECT id_type_gant AS id_type_article, libelle_type_gant AS libelle
            FROM type_gant
            ORDER BY id_type_gant;
            '''
    mycursor.execute(sql)
    type_gant = mycursor.fetchall()
    types_article = type_gant


    list_param = []
    condition_and = ""
    # articles =[]
    # pour le filtre
    
    # types_article = []

    articles_panier = []
    sql = """SELECT gant.id_gant, gant.nom_gant AS nom, gant.prix_gant AS prix, gant.stock_gant AS stock, ligne_panier.quantite
             FROM ligne_panier
             LEFT JOIN gant ON gant.id_gant = ligne_panier.id_gant
             WHERE id_utilisateur = %s"""
    mycursor.execute(sql, (id_client))
    articles_panier = mycursor.fetchall()

    if len(articles_panier) >= 1:
        prix_total = 123  # requete à faire
    else:
        prix_total = None
    return render_template('client/boutique/panier_article.html'
                           , gant=articles
                           , articles_panier=articles_panier
                           #, prix_total=prix_total
                           , items_filtre=types_article
                           )
