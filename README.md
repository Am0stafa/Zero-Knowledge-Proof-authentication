# Passwordless Authentication Using Zero Knowledge Proof 

This innovative project introduces a cutting-edge passwordless authentication system leveraging Zero-Knowledge Proof (ZKP) with the Fiat-Shamir heuristic. Unlike traditional authentication methods, this system ensures the utmost security by never transmitting the password over the network, thus eliminating a significant vector for cyber attacks.

## Superior Security with Zero-Knowledge Proof

Traditional authentication systems require users to send their passwords to the server, which can be intercepted or leaked due to system vulnerabilities. Our system circumvents this risk by using ZKP, allowing users to prove their identity without revealing their secret credentials. This approach revolutionizes the way we handle authentication, offering a significant leap forward in security.

## The Fiat-Shamir Heuristic: A Non-Interactive Protocol

The Fiat-Shamir heuristic transforms interactive protocols into non-interactive ones, enabling secure authentication without the need for back-and-forth communication between the user and the server. This reduces the risk of man-in-the-middle attacks and enhances the overall efficiency of the authentication process.

## Detailed Authentication Protocol

### 1. Sign Up
   - The client selects a username and calculates a hash value \(y\) using their password.
   - The client sends the username and hash value to the server for registration.
   - The server saves the username and hash value in its database (`users.json`).

### 2. Login
   - To authenticate, the client sends a value \(t\) to the server.
   - The server, upon receiving the \(t\) value, generates a random challenge \(c\) and sends it to the client.
   - The client calculates an \(r\) value using the challenge \(c\) and its private data. This \(r\) value is then sent back to the server as a proof.
   - The server verifies the proof by calculating the expected result using the \(r\) value and the client's \(y\) value (retrieved from the database). If the proof is valid, the client is authenticated.

##  Flow visualization

![zkp04 (1)](https://github.com/Am0stafa/Zero-Knowledge-Proof-authentication/assets/62848968/7cdf1886-6b9a-44a1-b409-1a88e806b035)


## Thread Safety

The server is designed to be thread-safe. It uses Python's threading module to handle multiple clients simultaneously. When multiple clients try to sign up or log in at the same time, potential race conditions when accessing the `users.json` file are avoided by using threading locks. This ensures that only one client can access the user data file at a time, guaranteeing data consistency and preventing potential data corruption.

## User Interface

Our system features an advanced, user-friendly UI that visualizes each step of the authentication process, providing users with a clear understanding of the underlying cryptographic operations.


## Real-Time Cryptographic Calculations

We provide real-time cryptographic calculations, allowing users to input different values and see the results instantly. This feature enhances learning and understanding of ZKP principles.

### 1. **Input Values:**
   - Users can input values such as \(v\) and see the corresponding cryptographic calculations.

### 2. **Visual Indicators:**
   - Step-by-step visual indicators guide users through the process, explaining each cryptographic operation in detail.

## Setup and Usage

### Requirements
   - Python 3.10
   - `libnum` library
   - `colorama` library
   - `matplotlib` library
   
### Running the Client
   Run the client UI which includes the server start button:
   ```
   python ZKPApp.py
   ```
   Make sure to start the server first!

## Potential Improvements

  - **Scalability:** Implementing a distributed database system could enhance scalability and fault tolerance.
  - **Quantum Resistance:** Exploring post-quantum cryptographic algorithms would future-proof the system against quantum computing threats.
  - **User Experience:** Integrating biometric verification could provide a more seamless and user-friendly authentication experience.
  - **Enhanced Visualizations:** Adding more detailed visualizations and explanations for each cryptographic step.

## Conclusion

This project is not just a demonstration of ZKP authentication but a beacon of modern security practices. It showcases how advanced cryptographic techniques can be practically applied to create a robust and secure authentication system that stands strong against contemporary cyber threats. This is the future of authentication – secure, efficient, and user-friendly.
