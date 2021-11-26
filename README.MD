# authenticate

```sh
$ curl localhost:5000/counter
{
    "counter": 0
}


$ curl -XPUT localhost:5000/counter
{
    "message": "The server could not verify that you are authorized to access the URL requested. You either supplied the wrong credentials (e.g. a bad password), or your browser doesn't understand how to supply the credentials required."
}


$ ACCESS_TOKEN=$(curl -XPUT -s localhost:5000/login -d '{"username": "username", "password": "password" }' | jq -r .access_token)
$ curl -XPUT -H "Authorization: Bearer ${ACCESS_TOKEN}" localhost:5000/counter -d '{}'
{
    "counter": 1
}


```
