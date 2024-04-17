# Toudou - the todo application

the project requirement :
* click >= 8.1.7
* sqlalchemy >= 2.0.27
* flask >= 3.0.2
* flask-wtf >= 1.2.1
* flask-httpauth >= 4.8.0
* flask-pydantic-spec >= 0.6.0
* spectree >= 1.2.9

which means you need to installed them using pip

## Setup the project :
```bash
pdm install 
pdm run toudou      # Run the project with CLI 
pdm start           # Run the project with web interface (http://localhost:5000)
```

now that the project dependencies are installed with pip you need to setup the project itself :

available commands with CLI :
```
Options:
  --help  Show this message and exit.

Commands:
  complete
  create
  delete
  display
  display-all
  import-csv
  update
```

### /!\ Concerning the web interface /!\
**Logins** for admin :
* username : admin
* password : admin

**Logins** for user :
* username : user
* password : user

## API

You can interact with the API via a web browser at `localhost:5000/apidoc/swagger`.

### the logins for authentification to the API are :
**Authentification** for admin :
* Token : admin_user

**Authentification** for user :
* Token : user1

You can send request for following routes : 
* `http://localhost:5000/api/complete_toudou`
* `http://localhost:5000/api/create_toudou`
* `http://localhost:5000/api/delete_toudou`
* `http://localhost:5000/api/download_toudous`
* `http://localhost:5000/api/get_toudou`
* `http://localhost:5000/api/get_toudous`
* `http://localhost:5000/api/import_toudous`
* `http://localhost:5000/api/modify_toudou`

here are some examples with `curl` :

Creating a toudou :

```bash
curl -X 'POST' \
  'http://localhost:5000/api/create_toudou' \
  -H 'accept: */*' \
  -H 'Authorization: Bearer admin_user' \       #need to be logged as 'admin_user'
  -H 'Content-Type: application/json' \
  -d '{
  "due": "2024-04-19",
  "task": "Send the toudou project"
}'
```
Response : 
```json
{
  "due": "Fri, 19 Apr 2024 00:00:00 GMT",
  "task": "Send the toudou project"
}
```
***
Importing a toudou : 
```bash
curl -X 'POST' \
  'http://localhost:5000/api/import_toudous' \
  -H 'accept: */*' \
  -H 'Authorization: Bearer admin_user' \
  -H 'Content-Type: application/json' \
  -d '{
  "absolute_path_to_file": "C:/Users/guams/Downloads/toudous.csv"  
}'
# On Windows as on Linux do not use '\' and use '/' instead
```
Response (if file exists) :
```json
{
  "imported": true
}
```
Course & examples : [https://kathode.neocities.org](https://kathode.neocities.org)
