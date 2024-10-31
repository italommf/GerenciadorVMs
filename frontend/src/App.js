import { CiSearch } from "react-icons/ci";

import axios from 'axios';
import React, { useState } from 'react';



function App() {

  const [vmId, setVmId] = useState('');
  const [vmInfo, setVmInfo] = useState(null);

  const handleSearch = () => {
    axios.get(`http://localhost:8000/api/abrir_vm/${vmId}/`)
      .then(response => {
        setVmInfo(response.data);
      })
      .catch(error => {
        console.error('Erro ao buscar a VM:', error);
        setVmInfo({ error: 'Máquina Virtual não encontrada' });
      });
  };

return (
  <div className="container">
    <h1 className="title"> 
      Abrir uma Máquina Virtual
    </h1>

    <div className="containerInput">

      <input
        type="text"
        placeholder="Digite o ID da VM"
        value={vmId}
        onChange={(e) => setVmId(e.target.value)} 
      />
      
    </div>

    <button className='buttonSearch' onClick={handleSearch}>
      <CiSearch size={20} color="#000"/>
    </button>

    {vmInfo && (
      <div>
        {vmInfo.error ? (
          <p>{vmInfo.error}</p>
        ) : (
          <div>
            <h3>Informações da VM:</h3>
            <p>ID: {vmInfo.id}</p>
            <p>Nome: {vmInfo.nome}</p>
          </div>
        )}
      </div>
    )}
  </div>
);
}

export default App;
