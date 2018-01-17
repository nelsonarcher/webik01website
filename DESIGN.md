# webik01website
Git Repo for webik ik01 website

## Technisch ontwerp – Matthijs, Nelson en Cilia Groep ik01

### Feature 1: registreren/account aanmaken

Model:
  • Een bestand models/register.py
  • Een functie: register()
    o returned homepagina of registratiepagina
    
View:
  • Een template: templates/register.html
  • Evt. een stylesheet: register.css
  
Controller:
  • Een bestand application.py
  • Een route: /register voor de methodes GET en POST
  • GET:
    o Laat register.html zien   
  • POST:
    o Roep models.register() aan met de ingevulde naam / wachtwoord
    o Sla user_id in database en session op als registreren is gelukt
    o Sla wachtwoord (store_password) op in database als hash
    o Redirect naar /index.html als registreren is gelukt, anders /register.html

### Feature 2: inloggen

Model:
  • Een bestand models/login.py
  • Een class user.py
    o Met attributen: id en naam
  • Een functie: login(name, password)
    o returned de User of None
    
View:
  • Een template: templates/login.html
  • Evt. een stylesheet: login.css
  
Controller:
  • Een bestand application.py
  • Een route: /login voor de methodes GET en POST
  • GET:
    o Laat login.html zien
  • POST:
    o Roep models.user.login() aan met de ingevulde naam / wachtwoord
    o Sla user_id in session op als inloggen is gelukt
    o Redirect naar /index.html als inloggen is gelukt, anders /login.html
    
### Feature 3: uitloggen

Model:
  • Een bestand models/logout.py
  • Een functie: logout()
    o returned de loginpagina of None
    
View:
  • Een template: templates/login.html
  • Evt. een stylesheet: login.css
  
Controller:
  • Een bestand application.py
  • Een route: /logout
  • Session.clear()
  • Laat login.html zien
  
### Feature 4: foto posten

Model:
  • Een bestand models/posten.py
  • Een class photo.py
    o Met attributen: photo en id (gebruiker)
  • Een functie: posten(photo, id)
    o Returned photo of None
    
View:
  • Een template: templates/posten.html
  • Evt. een stylesheet: posten.css
  
Controller:
  • Een bestand application.py
  • Een route: /posten voor de methodes GET en POST
  • GET:
    o Laat posten.html zien
  • POST:
    o Roep models.photo.posten() aan met de geselecteerde foto
    o Sla photo in database op als posten is gelukt
    o Redirect naar /index.html als posten is gelukt, anders /posten.html
    
### Feature 5: volgen

Model:
  • Een bestand models/follow.py
  • Een class following.py
    o Met attributen: naam en id
  • Een functie: follow(name, id)
    o Returned following of None
  • Een class followers.py
    o Met attributen: naam en id
  • Een functie: follower(name, id)
    o Returned followers of None
    
View:
  • Een template: templates/follow.html
  • Evt. een stylesheet: follow.css
  
Controller:
  • Een bestand application.py
  • Een route: /follow voor de methodes GET en POST
  • GET:
    o Laat follow.html zien
  • POST:
    o Roep models.follow.following() aan met lijst met mensen die jij volgt
    o Roep models.follow.followers() aan met een lijst met mensen die jou volgen
    o Sla follower/following op in database als volgen/gevolgd worden gelukt is
    o Redirect naar /index.html als volgen is gelukt, anders /follow.html
    
### Feature 6: index (homepagina/timeline)

Model:
  • Een bestand models/index.py
  • Een functie: index()
    o returned de index of None

View:
  • Een template: templates/index.html
  • Evt. een stylesheet: index.css

Controller:
  • Een bestand application.py
  • Een route: /
  • GET:
     o Laat index.html zien
  • POST:
    o Roep models.index() aan
    o Alle foto’s van de mensen die de gebruiker volgt aanroepen en op
      chronologische volgorde laten zien in een lijst

### Feature 7: foto’s liken

Model:
  • Een bestand models/liken.py
  • Een class like.py
    o Met attributen: foto en naam
  • Een functie: liken(name, photo)
    o returned de like of None

View:
  • Een template: templates/liken.java???
  • Evt. een stylesheet: liken.css
  • We willen gebruik maken van een plugin

Controller:
  • Een bestand application.py
  • Een route: /liken voor de methodes GET en POST
  • GET:
    o Laat liken.java?? zien
  • POST:
    o Roep models.like.liken() aan
    o Sla like op, tel bij het aantal likes op bij betreffende foto
    o Redirect naar /index.html

### Feature 8: foto’s commenten

Model:
  • Een bestand models/comment.py
  • Een class com.py
    o Met attributen: foto en naam
  • Een functie: comment(name, photo)
    o returned de com of None

View:
  • Een template: templates/comment.java???
  • Evt. een stylesheet: comment.css
  • We willen gebruik maken van een plugin

Controller:
  • Een bestand application.py
  • Een route: /comment voor de methodes GET en POST
  • GET:
    o Laat comment.java?? zien
  • POST:
    o Roep models.com.comment() aan
    o Sla comment op, tel bij het aantal comments op bij betreffende foto, en laat
      comment onder de foto zien
    o Redirect naar /index.html
    
 ### URL’s Javascript plugins to use:
      
like button:

    https://github.com/uagrace/like-dislike
    
    https://www.jqueryscript.net/social-media/Minimal-Like-Dislike-Button-Plugin-with-jQuery-likedislike.html

firebase: 

    http://www.londonacademyofit.co.uk/learning-blog/javascript/add-like-button-blogpostssimple-javascript/
    
real time comment box below picture:

    jquery-comments: http://viima.github.io/jquery-comments/
    
                     https://blog.pusher.com/build-live-comments-feature-using-javascript/
                     
Flask frame: 

    http://flask.pocoo.org/
