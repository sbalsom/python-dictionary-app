## Api Documentation 

On production, the base domain is 'https://python-dictionary-app.herokuapp.com/'. If you were to clone the repo and run the server yourself locally, the domain would be 'http://localhost:5000/'. All paths shown here are appended to this base domain.

### Users and authentication

#### Create a user account 
``` 
post '/api/users'
json body: 
    {
        "username": "testuser1",
        "email" : "example@sadie.com",
        "password" : "supersecret"
    }
```
##### response:

```
{
  "access_token": "eabc1234",
  "refresh_token": "qwerty45678"
}
```
The access token must be included in all following requests as : 
```
headers: 
Authorization: 'Bearer <user_access_token>'
```
#### login after tokens expired 

``` 
post 'auth/login'

json body : 
{
	"username": "acoolgirl",
	"password": "ohnopassword"
}
```
##### response : 
```

{
  "access_token": "eabc1234",
  "refresh_token": "qwerty45678"
}

```
#### refresh current session

```
post 'auth/refresh'

headers : 
Authorization: 'Bearer <user_refresh_token>'
```
##### response : 
```
{
    "access_token" : "12345dfggbeb"
}
```
Note that to get a new access token, you use the refresh token. It wont accept the expired access token in the headers.

### Dictionaries

#### First step, create a new dictionary ! 
```
post '/api/my/dictionaries'

json body : 

{
	"name": "my weird dict"
}
```
##### response 
```
{
  "_id": 6,
  "_user_id": 3,
  "name": "my weird dict",
  "owned_by": "beatles1234"
}
```
#### See all your dictionaries
```
get '/api/my/dictionaries'
```
##### response

```
{
  "dictionaries": [
    {
      "_id": 2,
      "_user_id": 3,
      "name": "My weird dict",
      "owned_by": "beatles1234"
    },
    {
      "_id": 3,
      "_user_id": 3,
      "name": "My weird dict 2",
      "owned_by": "beatles1234"
    },
    ...
    ]
}
```

#### Show one dictionary

```
get '/api/my/dictionaries/<dict_id>'
```
##### response 

Same as the response for create.

### My Words
Personal instances of a word are different from universal word objects, which could theoretically be shared between dictionaries and by users. This could allow for functionality in the future like seeing everyone who has the same words as you. For now, the distinction is just that personal words can be edited and have custom fields like description, whereas universal words aren't editable (even if you delete a personal word, that word object is still floating around in the database for someone else to use).

#### Create a word 

```
post '/api/my/words'

json body :

{
    "name": "little",
    "dictionary_id": 2,
    "description": "A word I found while reading a book.",
    "translations": [
        "tiny",
        "miniscule",
        "light"
    ]
}
```

Pass in the id of the dictionary you want to save the word to. You can save one word across many dictionaries, but you can't save the same word twice in your dictionary. Trying to do so will return an error.

##### response 

```
status: 201 CREATED
{
  "_id": 15,
  "created_by": "beatles1234",
  "name": "little"
}
```
If your friend is the first one to save the word to their dictionary, they will show up as the creator of the word. This is not a bug, it's a feature ;)

#### See all my words

See all my words, independent of dictionary they belong to.

```
get '/api/my/words'

```

##### response
```
"words": [
    {
      "_dictionary_id": 2,
      "_user_id": 3,
      "_word_id": 2,
      "description": null,
      "translations": [],
      "word": {
        "_id": 2,
        "created_by": sadie1234,
        "name": "sadie"
      }
    },
    {
      "_dictionary_id": 2,
      "_user_id": 3,
      "_word_id": 10,
      "description": null,
      "translations": [],
      "word": {
        "_id": 10,
        "created_by": beatles123,
        "name": "little"
      }
    },
    ...
    ]

```

#### Show one word

```
get '/api/my/words/<word_id>'

```
###### response
```
{
  "_dictionary_id": 2,
  "_user_id": 3,
  "_word_id": 2,
  "description": null,
  "translations": ["girl"],
  "word": {
    "_id": 2,
    "created_by": a_friend1234,
    "name": "sadie"
  }
}
```


### Words 

#### Index all words in database : 

``` 
get '/api/words'

```

##### response : 
```
{
  "words": [
    {
      "_id": 1,
      "created_by": my_friend123,
      "name": "hi"
    },
    {
      "_id": 2,
      "created_by": starship404,
      "name": "sadie"
    },
    {
      "_id": 3,
      "created_by": lovelythings,
      "name": "crab"
    },
```
