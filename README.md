tornado-rest-api-angularjs
==========================

Tornado Rest Api AngularJs

pip install -r requirements.txt

You must also install Mongodb.

App layout
/app/__init__.py
/app/objects.py
/app/config.py

For app/objects.py see Schematics documentation and examples:

https://github.com/j2labs/schematics/blob/master/docs/DEMOS.md

Running the app:

python server.py

http://127.0.0.1:8888/

Routes:

/animal/list ( GET )
/animal/get/:id ( GET)
/animal ( POST )
/animal/update/:id ( PUT )
/animal/delete/:id ( DELETE )

'id' is a Mongodb objectid in string format.

curl --data "name=dog" http://127.0.0.1:8888/animal
curl http://127.0.0.1:8888/animal/list
