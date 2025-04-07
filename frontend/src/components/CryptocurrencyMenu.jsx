import React, { useEffect, useState } from 'react';
import { Menu } from 'antd';
import axios from 'axios';

function CryptocurrencyMenu( { setCurrencyData } ) {

  const [currencies, setCurrencies] = useState([]);
  const [currencyId, setCurrencyId] = useState('1');


  const fetchCurrencies = () => {
    axios
    .get('http://127.0.0.1:8000/cryptocurrency')
    .then(r => {
        const currencyResponse = r.data;
        const menuItems = [
            {
                key: 'sub1',
                label: 'Список криптовалют',

                children: currencyResponse.map(currency => {
                    return {key: currency.id, label: currency.name}
                })
            }
        ]
        setCurrencies(menuItems);
    })
  };

  const fetchCurrency = () => {
    axios
    .get(`http://127.0.0.1:8000/cryptocurrency/${currencyId}`).then(r => {
        setCurrencyData(r.data);
        console.log(r.data)
    })
  };

  useEffect(() => {
    fetchCurrencies()
  }, [])

  useEffect(() => {
    setCurrencyData(null)
    fetchCurrency()
  }, [currencyId])

  const onClick = e => {
    setCurrencyId(e.key);
  };
  return (
    <Menu
      onClick={onClick}
      style={{ width: 256 }}
      defaultSelectedKeys={['1']}
      defaultOpenKeys={['sub1']}
      mode="inline"
      items={currencies}
    />
  );
};
export default CryptocurrencyMenu;