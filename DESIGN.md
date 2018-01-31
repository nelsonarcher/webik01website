# Technisch ontwerp – Matthijs en Cilia Groep ik01

## Inrichting (mappen)

webik01website (parentfolder)
 * static/
   * upload_images/
   * style.css

 * templates/
   * apology.html
   * explore.html
   * layout.html
   * login.html
   * post.html
   * profile.html
   * register.html

 * application.py

 * helpers.py

 * database.db

 * DESIGN.md

 * README.md

## Website features:

### Feature 1: registreren/account aanmaken

Model:
  * Een functie: register()
    * returned homepagina of registratiepagina

View:
  * Een template: templates/register.html

Controller:
  * def register () in application.py
  * Een route: /register voor de methodes GET en POST
  * GET:
    * Laat register.html zien
  * POST:
    * Roep register() aan met de ingevulde naam / wachtwoord
    * Sla user_id in database en session op als registreren is gelukt
    * Sla wachtwoord (store_password) op in database als hash
    * Redirect naar /explore.html als registreren is gelukt
    * Foutmelding in /apology.html als registreren niet gelukt is

### Feature 2: inloggen

Model:
  * User class
    * Met attributen: user_id, username en hash
  * Een functie: login(name, password)
    * returned de User of None

View:
  * Een template: templates/login.html

Controller:
  * def login() in application.py
  * Een route: /login voor de methodes GET en POST
  * GET:
    * Laat login.html zien
  * POST:
    * Roep models.user.login() aan met de ingevulde naam / wachtwoord
    * Sla user_id in session op als inloggen is gelukt
    * Redirect naar /explore.html als inloggen is gelukt, anders /login.html
    * Foutmelding in /apology.html als inloggen niet gelukt is

### Feature 3: uitloggen

Model:
  * Een functie: logout()
    * returned de loginpagina of None

View:
  * Een template: templates/login.html

Controller:
  * logout() in bestand application.py
  * Een route: /logout
  * Session.clear()
  * Laat login.html zien

### Feature 4: foto posten

Model:
  * Photo class
    * Met attributen: photo_id, photo_location, user_id en caption
  * Een functie: post()
    * Returned photo of None

View:
  * Een template: templates/posten.html

Controller:
  * def post() in application.py
  * Een route: /posten voor de methodes GET en POST
  * GET:
    * Laat posten.html zien
  * POST:
    * Roep post() aan met de geselecteerde foto
    * Sla photo in database op als posten is gelukt
    * Weergeef foto op zowel profile page en explore page
    * Redirect naar /explore.html als posten is gelukt, anders /posten.html

### Feature 5: Explore

Model:
  * Photo class
    * Met attributen: photo_id, photo_location, user_id, caption, comment_text
  * Een functie: explore()
    * returned de explore of None

View:
  * Een template: templates/explore.html

Controller:
  * def explore() in application.py
  * Een route: /explore voor de methodes GET en POST
  * GET:
     * Laat explore.html zien
  * POST:
    * Roep explore() aan
      * Alle geuploade foto’s uit database oproepen en random weergeven
      * Mogelijkheid om comments en likes te geven op posts (slaat likes en comments op in aparte database)

### Feature 6: foto’s liken

Model:
  * Like class
    * Met attributen: photo_id en user_id (genereert like_id)

View:
  * in template: templates/explore.html en templates/profile.html

Controller:
  * def explore() in application.py
  * POST:
    * Roep functie explore()
    * Trigger voor likeknop
    * Sla like op in database, tel bij het aantal likes op bij betreffende foto
    * Redirect naar /explore.html of /profile.html
    * Weergeef likes bij post, geen weergave van likes op profile pagina

### Feature 7: foto’s commenten

Model:
  * Comment class
    * Met attributen: photo_id, user_id, comment_text (genereert comment_id)

View:
  * Een template: templates/explore.html en templates/profile.html

Controller:
  * def explore() en def profile() in application.py
  * Een route: /explore en /profile voor de methodes GET en POST
  * GET:
    * Laat /explore.html en /profile.html zien
  * POST:
    * roep explore () en profile()
    * Sla comment op in database, tel bij het aantal comments op bij betreffende foto
    * Redirect naar /explore.html of /profile.html
    * laat comment onder de foto zien + weergeef username die comment geplaatst heeft
