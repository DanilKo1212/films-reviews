from requests import get, post, put, delete

print('get reviews')
print(get('http://localhost:8080/api/v1/reviews').json())
print('add review')
print(post('http://localhost:8080/api/v1/reviews',
           json={'film_id': 1, 'user_id': 1, 'body': 'great film'}).json())
print('get 1 review')
print(get('http://localhost:8080/api/v1/reviews/3').json())
print('update review')
print(put('http://localhost:8080/api/v1/reviews/3',
          json={'film_id': 1, 'user_id': 1, 'body': 'awful film'}).json())
print('updated review')
print(get('http://localhost:8080/api/v1/reviews/3').json())
print('delete review')
print(delete('http://localhost:8080/api/v1/reviews/3').json())
print('all reviews')
print(get('http://localhost:8080/api/v1/reviews').json())
