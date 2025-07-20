import { initializeApp } from "firebase/app";
import { getFirestore } from "firebase/firestore";

const firebaseConfig = {
  apiKey: "AIzaSyDy8q3mNZv2W2mlFuK3gpRsvwE129qPDAY",
  authDomain: "voice-expense-tracker-5f45d.firebaseapp.com",
  projectId: "voice-expense-tracker-5f45d",
  storageBucket: "voice-expense-tracker-5f45d.firebasestorage.app",
  messagingSenderId: "18222045782",
  appId: "1:18222045782:web:618a2d130092889eacf9f7"
};

const app = initializeApp(firebaseConfig);
export const db = getFirestore(app);
