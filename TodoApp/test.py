from jose import  jwt

SECRET_KEY='53eee1950605f91c0a7cf60bace4739d801b0780539136bac06805fd87ae0517'
ALGORITHM='HS256'
encode = {'sub': 'vanshita', 'id': 1}
jwtToken = jwt.encode(encode,SECRET_KEY,algorithm=ALGORITHM)
print(jwtToken)

payload=jwt.decode("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ2YW5zaGl0YSIsImlkIjoxfQ.KudPTxM5C4KIYabX2bm8eMS8otK6Tyx2BXq5L45jqmw",SECRET_KEY,algorithms=['HS256'])

print(payload)
