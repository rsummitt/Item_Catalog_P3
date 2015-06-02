# Item Catalog

## Running the project

To run this program you will need to install Vagrant and VirtualBox.

Once that has been installed clone this repository and navigate to the home directory.

The following steps can be used to run the tests for this project:

1. Run command ```vagrant up```

2. Run command ```vagrant ssh```

3. Run command ```python /vagrant/database_setup.py```

4. Run command ```python /vagrant/catalog_init.py```

5. Run command ```python /vagrant/application.py```

## Authentication

This project uses GitHub for authentication and authorization. 
The create, edit, and delete endpoints require GitHub 
authentication and authorization.  In order to modify the
Item Catalog you will need to authorize this application access to your GitHub account.

## Endpoints

* /

* /catalog/

* /catalog/category/add/ (GET and POST)

* /catalog/category/<int:category_id>/delete/

* /catalog/category/<int:category_id>/items/

* /catalog/category/<int:category_id>/item/<int:item_id>/

* /catalog/item/add/ (GET and POST)

* /catalog/item/<int:item_id>/edit/ (GET and POST)

* /catalog/item/<int:item_id>/delete/

* /api/catalog

## Project Purpose

This project is a result of Project 3 in the Full Stack Developer course offered by Udacity
