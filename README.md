# Passwordless authentication using Zero Knowledge Proof 

This project demonstrates a simple Zero-Knowledge Proof authentication scheme using the Fiat-Shamir heuristic. The implementation is thread-safe, ensuring multiple users can simultaneously sign up and login without clashes.

## Overview

Zero-knowledge proofs are cryptographic methods that allow one party (the prover) to prove to another party (the verifier) that they know a value x, without conveying any information apart from the fact that they know the value x. 

The Fiat-Shamir heuristic is a method used to transform an interactive public-coin protocol (where the verifier's challenges are random bits) into a non-interactive protocol. This transformation is especially useful in digital signature schemes and zero-knowledge proofs.

## Authentication Steps

1. **Sign Up**
   - The client selects a username and calculates a hash value y using their password.
   - The client sends the username and hash value to the server for registration.
   - The server saves the username and hash value in its database (users.json).

2. **Login**
   - To authenticate, the client sends a value t to the server.
   - The server, upon receiving the t value, generates a random challenge c and sends it to the client.
   - The client calculates an r value using the challenge c and its private data. This r value is then sent back to the server as a proof.
   - The server verifies the proof by calculating the expected result using the r value and the client's y value (retrieved from the database). If the proof is valid, the client is authenticated.\

###  Flow visulaization
![IMG_1503](https://github.com/Am0stafa/Zero-Knowledge-Proof-authentication/assets/62848968/8c97dc43-14c1-4288-8c7a-ed40488e1f8c)

![zkp04 (1)](https://github.com/Am0stafa/Zero-Knowledge-Proof-authentication/assets/62848968/7cdf1886-6b9a-44a1-b409-1a88e806b035)

## Thread Safety

The server is designed to be thread-safe. It uses Python's threading module to handle multiple clients simultaneously. When multiple clients try to sign up or log in at the same time, potential race conditions when accessing the `users.json` file are avoided by using threading locks. This ensures that only one client can access the user data file at a time, guaranteeing data consistency and preventing potential data corruption.

## Setup and Usage

1. **Requirements**
   - Python 3.10
   - `libnum` library
   - `colorama` library
   
2. **Running the Server**
   ```
   python Server.py
   ```
   The server will start listening on port 9999.

3. **Client**
   run the client and server but make sure to add your username and password, the password along with the secret salt will just act as a seed and would be send to the server

## Conclusion

This project provides a practical example of Zero-Knowledge Proof authentication using the Fiat-Shamir heuristic. It showcases how cryptography can be applied to create secure authentication processes without revealing sensitive information.

---

Adjust as needed based on any additional features or specific instructions you'd like to add!
