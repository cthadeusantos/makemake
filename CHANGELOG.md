[Back homepage](https://github.com/cthadeusantos/makemake)
# Changes

## 0.2.0 (2025/XX/XX)
* Added django-auditlog (first trials)
* Added UserLog model at core app for register user's login
* Added get_client_ip and get_actor in custom_functions.py
* Middleware added in core for Audit functions
* First refactoring methods in projects views
* First functions at signals.py in core and projects apps
* Fixed bugs at function new in Documents app
* Added Inactivity Logout Middleware in settings.py and middleware.py
* Site app with first LogAudit functions
* Resetting resetting activity logout time and added new middleware InactivityLogoutMiddleware

## 0.1.2 (2025/01/23)
* Fixed the case where removing initial items from buildings, users and interested parties caused records not to be added.
* Adjusted the templatedetails.html to show building items, users and stakeholders in a table format rather than a list
* Do it a McGyver (I was too lazy to fix it correctly) in project.js so that functions that add stakeholders and members activate or deactivate the "submit" button according to the existence or not of buildings.
* FIOCRUZ logo added and original logo duplicated
  
## 0.1.1 - Bugfix (2025/01/18)
* Fix minor bugs at app Projects and Documents

## 0.1.1 (2025/01/02)
* Fix wrong number for project code at project app
* Implemented automatic filename for new documents
* Replace check cpf and cnpj numbers functions (Brazil numbers)
* Build template tags and filters for cpf/cnpj (Brazil numbers format)

## 0.1.0 (2024/12/31)
* First release