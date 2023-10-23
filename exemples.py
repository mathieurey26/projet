# -*- coding: utf-8 -*-
from flask import Flask, url_for, request, render_template, redirect
import sqlite3 as lite

# ------------------
# application Flask
# ------------------

app = Flask(__name__)


# ---------------------------------------
# des fonctions utiles à plusieurs pages
# ---------------------------------------

# renvoie un lien HTML pour retourner à la page index
def retour_index():
	return "<a href='" + url_for("index") + "'>retour à l'index</a><br/><br/>"
	
# renvoie un formulaire vers la page cible demandant un prénom (avec une valeur par défaut)
def formulaire_prenom(cible, prenom = "entrez votre prénom"):
	formulaire = ""
	formulaire += "<form method='post' action='" + url_for(cible) + "'>"
	formulaire += "<input type='text' name='prenom' value='" + prenom + "'>"
	formulaire += "<input type='submit' value='Envoyer'>"
	formulaire += "</form><br/>"
	
	return formulaire
	
# connecte à la BDD, affecte le mode dictionnaire aux résultats de requêtes et renvoie un curseur
def connection_bdd():
	
	con = lite.connect('exemples.db')
	con.row_factory = lite.Row
	
	return con
	
# connecte à la BDD et renvoie toutes les lignes de la table personne
def selection_personnes():
	
	conn = connection_bdd()
	cur = conn.cursor()
	
	cur.execute("SELECT nom, prenom, role FROM personnes")
	
	lignes = cur.fetchall()
	
	conn.close()
	
	return lignes
	
# connecte à la BDD et renvoie les lignes de la table personne dont le prénom commence par la lettre donnée
def selection_personnes_lettre(lettre):
	
	conn = connection_bdd()
	cur = conn.cursor()
	
	cur.execute("SELECT nom, prenom, role FROM personnes WHERE prenom LIKE ?", (lettre + "%",))
	
	lignes = cur.fetchall()
	
	conn.close()
	
	return lignes
	
# connecte à la BDD et insère une nouvelle ligne avec les valeurs données
def insertion_personne(nom, prenom, role):
	
	try:
		conn = connection_bdd()
		cur = conn.cursor()
		
		cur.execute("INSERT INTO personnes('nom', 'prenom', 'role') VALUES (?,?,?)", (nom,prenom,role))
		
		conn.commit()
		
		conn.close()
		
		return True
		
	except lite.Error:
		
		return False
	


# ---------------------------------------
# les différentes pages (fonctions VUES)
# ---------------------------------------


# une page index avec des liens vers les différentes pages d'exemple d'utilisation de Flask
@app.route('/')
def index():
	
	contenu = ""
	contenu += "Une page index avec des liens vers différents exemples d'utilisation de Flask<br/><br/>"
	
	contenu += "<a href='" + url_for("hello") + "'>hello</a><br/><br/>"
	
	contenu += "<a href='" + url_for("hello_url_prenom", prenom="toi") + "'>hello (url)</a> (dans la barre d'URL, remplacez 'toi' par ce que vous voulez)<br/><br/>"
	
	contenu += "<a href='" + url_for("hello_url_entier", valeur=5) + "'>hello (entier)</a> (dans la barre d'URL, remplacez '5' par ce que vous voulez)<br/><br/>"
	
	contenu += "<a href='" + url_for("hello_get_prenom", prenom="toi") + "'>hello (get)</a> (dans la barre d'URL, remplacez la variable GET prenom ('toi') par ce que vous voulez)<br/><br/>"
		
	contenu += "<a href='" + url_for("fichier_statique") + "'>fichier statique</a><br/><br/>"
	
	contenu += formulaire_prenom("hello_post_prenom")
	
	contenu += "<a href='" + url_for("formulaire_combine") + "'>formulaire combiné</a><br/><br/>"
	
	contenu += "<a href='" + url_for("template_html", prenom = "toi", globe = 1) + "'>template HTML</a><br/><br/>"
	
	contenu += "<a href='" + url_for("affichage_bdd_personnes") + "'>Affichage des personnes de la BDD</a><br/><br/>"
		
	contenu += "<a href='" + url_for("affichage_bdd_personnes_a") + "'>Affichage des personnes de la BDD dont le prénom commence par A</a><br/><br/>"
	
	contenu += "<a href='" + url_for("insertion_bdd_personne") + "'>Ajout d'une personne à la BDD</a><br/><br/>"
	
	return contenu;
  

	
# une page avec du texte statique
@app.route('/hello')  
def hello():
	
	contenu = ""
	contenu += retour_index()
	contenu += "Hello, World !"
	
	return contenu
	
# une page avec du texte dynamique déterminé par l'URL
@app.route('/hello_url/<prenom>')  
def hello_url_prenom(prenom):
	
	contenu = ""
	contenu += retour_index()
	contenu += "Hello, " + prenom + " !"
	
	return contenu
	
# une page avec un entier dynamique déterminé par l'URL
@app.route('/hello_url_entier/<int:valeur>')  
def hello_url_entier(valeur):
	
	contenu = ""
	contenu += retour_index()
	contenu += "Hello, n * 2 = " + str(valeur*2) + " !"
	
	return contenu
	
# une page avec du texte dynamique envoyé par HTTP/GET
@app.route('/hello_get', methods=['GET'])  
def hello_get_prenom():
	
	contenu = ""
	contenu += retour_index()
	contenu += "Hello, " + request.args.get('prenom', 'une valeur par defaut') + " !"
	
	return contenu

@app.route('/fichier_statique')
def fichier_statique():
	contenu = ""
	contenu += retour_index()
	contenu += "Hello, World !<br/>"
	contenu += "<img src='" + url_for('static', filename='globe.png') + "'/>"
	
	return contenu
	
# une page avec du texte dynamique envoyé par HTTP/POST
@app.route('/hello_post', methods=['POST'])  
def hello_post_prenom():
	
	contenu = ""
	contenu += retour_index()
	contenu += "Hello, " + request.form['prenom'] + " !"
	
	return contenu

# un page qui combine affichage du formulaire et traitement
@app.route('/formulaire_combine', methods=['GET','POST'])  
def formulaire_combine():
	
	contenu = ""
	contenu += retour_index()
	
	erreur = ""
	if request.method == 'POST':
		
		if (request.form['prenom'][0].lower() == "a"):
			contenu += "Hello, " + request.form['prenom'] + " !"
			return contenu
		
		else:
			erreur = 'le prénom doit commencer par un "A"'
	
	# on arrive ici si rien n'a été envoyé par POST, ou si la validation des données a échoué
	
	if (erreur != ""):
		contenu += "<strong>Erreur : " + erreur + "</strong>"
		
	contenu += formulaire_prenom("formulaire_combine", prenom = "prénom en A")
	
	return contenu

@app.route('/template_html', methods=['GET'])  
def template_html():
	return render_template('hello.html', prenom=request.args.get('prenom', ''), afficher_globe=request.args.get('globe', False))
	
	
@app.route('/afficher_personnes', methods=['GET'])
def affichage_bdd_personnes():
	
	lignes = selection_personnes()
	
	return render_template('affichage_personnes.html', personnes = lignes)
	
	
@app.route('/afficher_personnes_a')
def affichage_bdd_personnes_a():
	
	lignes = selection_personnes_lettre("A")
	
	return render_template('affichage_personnes_lettre.html', lettre = "A", personnes = lignes)
	
	
@app.route('/ajouter_personne', methods=['GET', 'POST'])
def insertion_bdd_personne():
	
	erreur = ""
	if request.method == 'POST':
		
		if (request.form['nom'] != "" and request.form['prenom'] != "" and request.form.get('role', type=int) > 0 and request.form.get('role', type=int) < 4):
			
			res = insertion_personne(request.form['nom'],request.form['prenom'],request.form.get('role', type=int))
			
			if (res):
			
				return redirect(url_for('affichage_bdd_personnes'))
				
			else:
				erreur = "Une erreur a été détectée lors de l'insertion dans la base de données. Veuillez réessayer ou contacter l'administrateur du site."
		else:
			erreur = "Une erreur a été détectée dans le formulaire, merci de remplir tous les champs correctement."
	
	# on arrive ici si rien n'a été envoyé par POST, ou si la validation des données a échoué
	
	return render_template('formulaire_personne.html', msg = erreur, nom = request.form.get('nom', ''), prenom = request.form.get('prenom', ''), role = request.form.get('role', 0, type=int))

# ---------------------------------------
# pour lancer le serveur web local Flask
# ---------------------------------------

if __name__ == '__main__':
	app.run(debug=True)
print(3)
