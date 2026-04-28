from flask import Flask, render_template, jsonify, send_file
from playwright.sync_api import sync_playwright
import pandas as pd
import tempfile
import re

app = Flask(__name__)

# =========================================================
# 🔥 FORMATEAR NÚMEROS
# =========================================================
def formatear_numero(numero):

    try:

        numero = int(numero)

        if numero >= 1000000:
            return f"{round(numero / 1000000, 1)}M"

        elif numero >= 1000:
            return f"{round(numero / 1000, 1)}K"

        else:
            return str(numero)

    except:
        return "0"


# =========================================================
# 🔧 LIMPIAR NÚMEROS
# =========================================================
def limpiar_numero(texto):

    if not texto:
        return 0

    texto = texto.lower().strip()

    match = re.search(r'[\d,.]+[mk]?', texto)

    if not match:
        return 0

    num = match.group(0)

    num = num.replace(",", "")

    try:

        if "k" in num:
            return int(float(num.replace("k", "")) * 1000)

        elif "m" in num:
            return int(float(num.replace("m", "")) * 1000000)

        else:
            return int(float(num))

    except:
        return 0


# =========================================================
# 🔍 SCRAPING INSTAGRAM
# =========================================================
def scraping_instagram(username):

    with sync_playwright() as p:

        # =====================================================
        # 🔥 USAR SESIÓN REAL
        # =====================================================
        context = p.chromium.launch_persistent_context(

            user_data_dir="userdata",

            channel="chrome",

            headless=False,

            locale="es-ES",

            viewport={
                "width": 1400,
                "height": 900
            }
        )

        page = context.pages[0]

        try:

            url = f"https://www.instagram.com/{username}/"

            print(f"\n>>> Analizando: {username}")

            # ir al perfil
            page.goto(
                url,
                wait_until="domcontentloaded",
                timeout=60000
            )

            page.wait_for_timeout(6000)

            # =====================================================
            # 🚫 LOGIN
            # =====================================================
            if "login" in page.title().lower():

                return {
                    "status": "error",
                    "message": (
                        "Inicia sesión manualmente "
                        "en Instagram primero."
                    )
                }

            # =====================================================
            # 🔥 EXTRAER HEADER
            # =====================================================
            seguidores = "0"
            publicaciones = "0"

            meta_description = page.locator(
                'meta[property="og:description"]'
            ).get_attribute("content")

            print(meta_description)

            if meta_description:

                followers_match = re.search(
                    r'([\d,.]+[MKmk]?)\s(?:Followers|seguidores)',
                    meta_description,
                    re.IGNORECASE
                )

                posts_match = re.search(
                    r'([\d,.]+[MKmk]?)\s(?:Posts|publicaciones)',
                    meta_description,
                    re.IGNORECASE
                )

                if followers_match:
                    seguidores = followers_match.group(1)

                if posts_match:
                    publicaciones = posts_match.group(1)

            # =====================================================
            # 📸 POSTS
            # =====================================================
            posts = page.locator("article a")

            total_posts = posts.count()

            print(f"\nPOSTS: {total_posts}")

            posts_data = []

            # =====================================================
            # 🔥 ANALIZAR 10 POSTS
            # =====================================================
            for i in range(min(10, total_posts)):

                try:

                    print(f"\n--- POST {i+1} ---")

                    posts.nth(i).click()

                    page.wait_for_timeout(4000)

                    modal_html = page.content()

                    # =================================================
                    # ❤️ LIKES
                    # =================================================
                    likes = 0

                    likes_patterns = [

                        r'([\d,.]+[MKmk]?)\slikes',

                        r'liked by\s([\d,.]+[MKmk]?)',

                        r'([\d,.]+[MKmk]?)\sMe gusta'
                    ]

                    for pattern in likes_patterns:

                        likes_match = re.search(
                            pattern,
                            modal_html,
                            re.IGNORECASE
                        )

                        if likes_match:

                            likes = limpiar_numero(
                                likes_match.group(1)
                            )

                            break

                    # =================================================
                    # 💬 COMENTARIOS
                    # =================================================
                    comentarios = 0

                    try:

                        comentarios = page.locator(
                            'ul._a9ym'
                        ).count()

                        if comentarios == 0:

                            comentarios = page.locator(
                                'ul ul'
                            ).count()

                    except:
                        comentarios = 0

                    # =================================================
                    # 🖼️ IMAGEN
                    # =================================================
                    imagen = ""

                    try:

                        imagen = page.locator(
                            'article img'
                        ).first.get_attribute("src")

                    except:
                        imagen = ""

                    # =================================================
                    # 📦 GUARDAR POST
                    # =================================================
                    posts_data.append({

                        "post": i + 1,

                        "likes": formatear_numero(likes),

                        "comentarios": formatear_numero(comentarios),

                        "imagen": imagen
                    })

                    print("Likes:", likes)
                    print("Comentarios:", comentarios)

                    # cerrar modal
                    page.keyboard.press("Escape")

                    page.wait_for_timeout(2000)

                except Exception as e:

                    print("ERROR:", e)

                    continue

            # =====================================================
            # ✅ RESPUESTA
            # =====================================================
            return {
                "status": "success",

                "data": {

                    "usuario": username,

                    "seguidores": seguidores,

                    "publicaciones": publicaciones,

                    "posts": posts_data
                }
            }

        except Exception as e:

            return {
                "status": "error",
                "message": str(e)
            }


# =========================================================
# 🌐 FRONTEND
# =========================================================
@app.route('/')
def index():
    return render_template('index.html')


# =========================================================
# 🔥 API
# =========================================================
@app.route('/api/scrape/<username>')
def scrape(username):

    user = username.replace("@", "")

    resultado = scraping_instagram(user)

    return jsonify(resultado)


# =========================================================
# 📥 EXPORTAR EXCEL
# =========================================================
@app.route('/api/export/<username>')
def export(username):

    user = username.replace("@", "")

    resultado = scraping_instagram(user)

    if resultado["status"] != "success":

        return jsonify(resultado)

    data = resultado["data"]

    filas = []

    for post in data["posts"]:

        filas.append({

            "Post": post["post"],

            "Likes": post["likes"],

            "Comentarios": post["comentarios"]
        })

    df = pd.DataFrame(filas)

    temp = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".xlsx"
    )

    df.to_excel(
        temp.name,
        index=False
    )

    return send_file(
        temp.name,
        as_attachment=True,
        download_name=f"{user}_instagram.xlsx"
    )


# =========================================================
# 🚀 RUN
# =========================================================
if __name__ == '__main__':

    app.run(
        debug=True,
        port=5000,
        use_reloader=False
    )