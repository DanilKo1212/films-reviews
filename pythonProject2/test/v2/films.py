from requests import get, post, put, delete

print('get films')
print(get('http://localhost:8080/api/v2/films').json())
print('add film')
print(post('http://localhost:8080/api/v2/films',
           json={'name': 'film2', 'genre': 'horror', 'year': '1993', 'description': 'some',
                 'image': 'default.png'}).json())
print('get 1 film')
print(get('http://localhost:8080/api/v2/films/2').json())
print('update film')
print(put('http://localhost:8080/api/v2/films/2',
          json={'name': 'film2', 'genre': 'comedy', 'year': '1993', 'description': 'some',
                'image': 'default.png'}).json())
print('updated film')
print(get('http://localhost:8080/api/v2/films/2').json())
print('delete film')
print(delete('http://localhost:8080/api/v2/films/2').json())
print('all films')
print(get('http://localhost:8080/api/v2/films').json())
