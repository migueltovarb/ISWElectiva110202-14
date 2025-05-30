
// frontend/App.jsx
import React, { useEffect, useState } from 'react';
import axios from 'axios';

function App() {
  const [appointments, setAppointments] = useState([]);

  useEffect(() => {
    axios.get('http://localhost:8000/api/citas/') // Reemplaza por el endpoint real
      .then(response => setAppointments(response.data))
      .catch(error => console.error('Error al cargar las citas:', error));
  }, []);

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Citas médicas</h1>
      <ul className="space-y-2">
        {appointments.map((cita, index) => (
          <li key={index} className="bg-white p-4 rounded shadow">
            <p><strong>Paciente:</strong> {cita.paciente}</p>
            <p><strong>Doctor:</strong> {cita.doctor}</p>
            <p><strong>Fecha:</strong> {cita.fecha}</p>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;

