import { initializeApp } from "https://www.gstatic.com/firebasejs/10.9.0/firebase-app.js";
import { getAuth, 
         GoogleAuthProvider } from "https://www.gstatic.com/firebasejs/10.9.0/firebase-auth.js";
import { getFirestore } from "https://www.gstatic.com/firebasejs/10.9.0/firebase-firestore.js";

// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyD152dqaksgSOqK_E7SendiUnmgO1ReRKs",
  authDomain: "waste-connect-fb4a1.firebaseapp.com",
  projectId: "waste-connect-fb4a1",
  storageBucket: "waste-connect-fb4a1.firebasestorage.app",
  messagingSenderId: "226399453466",
  appId: "1:226399453466:web:5795ea8e3b8796e897eca3",
  measurementId: "G-GG2RVRGJQH"
};

  // Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const provider = new GoogleAuthProvider();

const db = getFirestore(app);

export { auth, provider, db };