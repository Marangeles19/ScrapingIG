import instaloader
from flask import Flask, render_template, jsonify
import os

app = Flask(__name__)

# CONFIGURACIÓN
USUARIO_IG = "mara1998j" #  USUARIOIG

def scraping_instagram_profesional(target):
    L = instaloader.Instaloader()
    
    # CARGAR SESIÓN PROFESIONAL
    try:
        # Esto busca el archivo que generaste en el paso 1
        L.load_session_from_file(USUARIO_IG) 
    except FileNotFoundError:
        return {"status": "error", "message": f"Primero debes generar la sesión en la terminal con: instaloader --login {USUARIO_IG}"}

    username = target.strip().replace("@", "").split('/')[-1] or target.strip().replace("@", "").split('/')[-2]

    try:
        # Forzamos la actualización de datos
        perfil = instaloader.Profile.from_username(L.context, username)
        
        total_likes = 0
        total_comments = 0
        posts_analizados = 0
        
        # Obtenemos los últimos 10 posts (más rápido y seguro)
        for post in perfil.get_posts():
            if posts_analizados >= 10: break
            total_likes += post.likes
            total_comments += post.comments
            posts_analizados += 1

        return {
            "status": "success",
            "data": {
                "usuario": perfil.username,
                "nombre": perfil.full_name or perfil.username,
                "bio": perfil.biography,
                "seguidores": f"{perfil.followers:,}",
                "publicaciones": perfil.mediacount,
                "likes_recientes": f"{total_likes:,}",
                "comentarios_recientes": f"{total_comments:,}"
            }
        }

    except Exception as e:
        return {"status": "error", "message": f"Instagram dice: {str(e)}"}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/scrape/<username>')
def api_endpoint(username):
    resultado = scraping_instagram_profesional(username)
    return jsonify(resultado)

if __name__ == '__main__':
    app.run(debug=True, port=5000)