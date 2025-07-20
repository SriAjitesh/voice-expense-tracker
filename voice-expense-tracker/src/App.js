import React, { useEffect, useState } from "react";
import { db } from "./firebase";
import { collection, addDoc, getDocs } from "firebase/firestore";

export default function App() {
  const [expense, setExpense] = useState("");
  const [amount, setAmount] = useState("");
  const [records, setRecords] = useState([]);

  const addExpense = async () => {
    if (!expense || !amount) return;
    await addDoc(collection(db, "expenses"), { expense, amount });
    setExpense("");
    setAmount("");
    loadExpenses();
  };

  const loadExpenses = async () => {
    const snapshot = await getDocs(collection(db, "expenses"));
    const data = snapshot.docs.map((doc) => ({ ...doc.data(), id: doc.id }));
    setRecords(data);
  };

  const startVoice = () => {
    const recognition = new window.webkitSpeechRecognition();
    recognition.lang = "en-US";
    recognition.onresult = (event) => {
      const result = event.results[0][0].transcript;
      const [desc, amt] = result.split(" for ");
      setExpense(desc);
      setAmount(amt?.replace(/[^0-9.]/g, "") || "");
    };
    recognition.start();
  };

  useEffect(() => {
    loadExpenses();
  }, []);

  return (
    <div style={{
      background: 'linear-gradient(to right, #4e54c8, #8f94fb)',
      minHeight: '100vh',
      padding: '2rem',
      color: 'white',
      fontFamily: 'Arial'
    }}>
      <h1 style={{ textAlign: 'center', fontSize: '2rem' }}>🎙️ Voice Expense Tracker</h1>
      <div style={{
        maxWidth: '600px',
        margin: '2rem auto',
        padding: '2rem',
        background: 'rgba(255, 255, 255, 0.1)',
        borderRadius: '20px',
        backdropFilter: 'blur(10px)'
      }}>
        <input
          type="text"
          placeholder="Expense description"
          value={expense}
          onChange={(e) => setExpense(e.target.value)}
          style={{ width: '100%', marginBottom: '1rem', padding: '0.5rem', borderRadius: '10px' }}
        />
        <input
          type="number"
          placeholder="Amount"
          value={amount}
          onChange={(e) => setAmount(e.target.value)}
          style={{ width: '100%', marginBottom: '1rem', padding: '0.5rem', borderRadius: '10px' }}
        />
        <div style={{ display: 'flex', gap: '1rem' }}>
          <button onClick={addExpense} style={{ flex: 1, padding: '0.5rem', background: '#28a745', color: 'white', border: 'none', borderRadius: '10px' }}>Add</button>
          <button onClick={startVoice} style={{ flex: 1, padding: '0.5rem', background: '#007bff', color: 'white', border: 'none', borderRadius: '10px' }}>Speak</button>
        </div>
      </div>

      <div style={{ maxWidth: '600px', margin: '0 auto' }}>
        {records.map((r) => (
          <div key={r.id} style={{
            display: 'flex',
            justifyContent: 'space-between',
            background: 'rgba(255,255,255,0.15)',
            padding: '1rem',
            marginBottom: '0.5rem',
            borderRadius: '10px'
          }}>
            <span>{r.expense}</span>
            <strong>₹{r.amount}</strong>
          </div>
        ))}
      </div>
    </div>
  );
}
