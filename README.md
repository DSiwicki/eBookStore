# eBookStore

**eBookStore** was created in January 2018 as part of an assessment of the course [Python and SQL: intro / SQL platforms](https://usosweb.wne.uw.edu.pl/kontroler.php?_action=katalog2/przedmioty/pokazPrzedmiot&prz_kod=2400-DS1SQL) on my Master Studies - Data Science and Business Analytics @ [Faculty of Economic Sciences, University of Warsaw](www.wne.uw.edu.pl). It was my first ever project in Python.

:website: Now application is available on siwicki[dot]co/ebookstore 


### The goal of the assessment

The goal of assessment was to build web application using Python, Bottle framework and SQLite. I attempted to create online ebook store with basic functionality:
- signup, login and logout
- user is able to order ebooks, add ebooks to wishlist and drop them from it
- admin can add, edit and delete ebooks and users

Obviously, frontend leaves a lot to be desired.

For the purposes of this repository, application was rewritten using Flask framework. 

Frames of the working application were posted below.

### Running the application

First, please provide the following .txt files: **api.txt** that contains your Google API key and **access.txt** that contains login and password for Gmail services in order to handle sending emails to registered users.

In order to create SQLite database run **create_db.py** in your directory. Additionally, it creates **admin** user - to login as default administrator use: **admin** as login and **admin** as password.

Run **index.py** in your directory to run the application.


### Frames

<table style = "border: 1px solid black;">
  <tr>
    <td><img src="src/index.jpg" width="300" height = "300"></td>
    <td><img src="src/login.jpg" width="300" height = "300"></td>
    <td><img src="src/signup.jpg" width="300" height = "300"></td>
  </tr>
  <tr>
    <td><img src="src/about.jpg" width="300" height = "300"></td>
    <td><img src="src/contact.jpg" width="300" height = "300"></td>
    <td><img src="src/search.jpg" width="300" height = "300"></td>
  </tr>
  <tr>
    <td><img src="src/index-user.jpg" width="300" height = "300"></td>
    <td><img src="src/profile.jpg" width="300" height = "300"></td>
    <td><img src="src/orders.jpg" width="300" height = "300"></td>
  </tr>
  <tr>
    <td><img src="src/details.jpg" width="300" height = "300"></td>
    <td><img src="src/buy.jpg" width="300" height = "300"></td>
    <td></td>
  </tr>
  <tr>
    <td><img src="src/index-admin.jpg" width="300" height = "300"></td>
    <td><img src="src/sales.jpg" width="300" height = "300"></td>
    <td></td>
  </tr>
  <tr>
    <td><img src="src/all-ebooks.jpg" width="300" height = "300"></td>
    <td><img src="src/edit-ebook.jpg" width="300" height = "300"></td>
    <td><img src="src/del-ebook.jpg" width="300" height = "300"></td>
  </tr>
  <tr>
    <td><img src="src/users.jpg" width="300" height = "300"></td>
    <td><img src="src/edit-user.jpg" width="300" height = "300"></td>
    <td><img src="src/del-user.jpg" width="300" height = "300"></td>
  </tr>
</table>
 
