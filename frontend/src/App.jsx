import React, { useState } from 'react';
import CryptocurrencyCard from "./components/CryptocurrencyCard"
import CryptocurrencyMenu from "./components/CryptocurrencyMenu"
import { Spin } from 'antd';

function App() {
  const [currencyData, setCurrencyData] = useState(null);

  return (
    <div className="flex">
      <div className="h-screen overflow-scroll">
        <CryptocurrencyMenu setCurrencyData={setCurrencyData}/>
      </div>
      <div className="mx-auto my-auto">
        {currencyData ? <CryptocurrencyCard currencyData={currencyData}/> : <Spin size="large"/>}
      </div>
    </div>
  )
}

export default App
