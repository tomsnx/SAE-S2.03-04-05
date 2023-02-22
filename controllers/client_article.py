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
        SELECT id_gant AS id_article
               , nom_gant AS nom
               , prix_gant AS prix
               , stock_gant AS stock
               , image_gant AS image
        FROM gant
        ORDER BY nom_gant;
        '''
    mycursor.execute(sql)
    gants = mycursor.fetchall()
    articles = gants

    # utilisation du filtre
    sql = '''
            SELECT id_taille AS id_type_article
                    ,libelle_taille AS libelle
            FROM taille
            ORDER BY id_taille;
            '''
    mycursor.execute(sql)
    tailles = mycursor.fetchall()
    types_article = tailles


    list_param = []
    condition_and = ""
    # articles =[]


    # pour le filtre
    # types_article = []


    articles_panier = []

    if len(articles_panier) >= 1:
        sql = "SELECT * , 10 as prix_gant , concat('nom_gant',id_gant) as nom FROM ligne_panier"
        mycursor.execute(sql)
        articles_panier = mycursor.fetchall()
        prix_total = 123  # requete à faire
    else:
        prix_total = None
    return render_template('client/boutique/panier_article.html'
                           , articles=articles
                           , articles_panier=articles_panier
                           #, prix_total=prix_total
                           , items_filtre=types_article
                           )