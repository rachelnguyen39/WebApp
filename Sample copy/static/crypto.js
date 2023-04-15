// Import CryptoJS library for encryption
const CryptoJS = require("crypto-js");

// Generate a new key pair
const generateKeyPair = () => {
  const privateKey = CryptoJS.lib.WordArray.random(16).toString();
  const publicKey = CryptoJS.SHA256(privateKey).toString();
  return { publicKey, privateKey };
};

// Save private key to localStorage
const savePrivateKey = (privateKey) => {
  localStorage.setItem("privateKey", privateKey);
};

// Load private key from localStorage
const loadPrivateKey = () => {
  return localStorage.getItem("privateKey");
};

// Save public key to localStorage
const savePublicKey = (publicKey) => {
    localStorage.setItem("publicKey", publicKey);
};
  
// Load private key from localStorage
const loadPublicKey = () => {
    return localStorage.getItem("publicKey");
};

// Encrypt a message with recipient's public key
const encryptMessage = (message, recipientPublicKey) => {
  const encryptedMessage = CryptoJS.AES.encrypt(message, recipientPublicKey).toString();
  return encryptedMessage;
};

// Decrypt a message with sender's public key
const decryptMessage = (encryptedMessage, senderPublicKey) => {
  const decryptedMessage = CryptoJS.AES.decrypt(encryptedMessage, senderPublicKey).toString(CryptoJS.enc.Utf8);
  return decryptedMessage;
};
