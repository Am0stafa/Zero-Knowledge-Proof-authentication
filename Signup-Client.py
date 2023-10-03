# It hashes the password to generate a "public key" public key based on the password and sends this along with the username to the server

import socket
import hashlib

n = 997
g = 9

# This function attempts to find a generator of a cyclic group under modulo p.
# A generator is an element g in the group such that, when successively multiplied
# by itself modulo p, it cycles through all non-zero residues modulo p before 
# returning to 1, with a total of (p-1) multiplications. The function iterates 
# through values from 1 to (p-1), checking each value to see if it is a generator, 
# and returns the first generator found.
def genG(p):
  for x in range (1,p):
    rand = x
    exp=1
    next = rand % p

    while (next != 1 ):
      next = (next*rand) % p
      exp = exp+1
    
    if (exp==p-1):
      return rand
# print(genG(35527))

def signup(username, password):
  if ' ' in username:
    print('Username cannot contain spaces')
    return
  client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  client.connect(('127.0.0.1', 9999))

  # Generate public key
  x = int(hashlib.md5(password).hexdigest()[:8], 16) % n
  g = 3
  y = pow(g,x,n) # This is the public key
  request = f'/signup {username} {y}'
  client.send(request.encode())
  response = client.recv(4096) # This is the will be the C
  print(response.decode())

# Usage:
signup('john_doe', 'password123')
