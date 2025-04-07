import { Card } from 'antd';


function CryptocurrencyCard({ currencyData }) {

    const formatPrice = currencyData.quote.USD.price.toFixed(2);
    const priceChangePercent = currencyData.quote.USD.percent_change_24h.toFixed(2);
    const priceMarketCap = (currencyData.quote.USD.market_cap / 1_000_000).toFixed(2);

    return (
      <div>
        <Card
            title={
                <div className="flex items-center gap-3">
                    <img src={`https://s2.coinmarketcap.com/static/img/coins/64x64/${currencyData.id}.png`} alt="logo" width="50"/>
                    <p className='text-3xl'>{currencyData.name}</p>
                </div>
            }
            style={{ 
                width: 700,
                height: 400,
                boxShadow: '0px 0px 5px rgba(0,0,0,0.5)',
                border: 'none',
            }}
            className='text-3xl'>
            <p>Текущая цена: {formatPrice}$</p>
            <p>Цена за 24 часа: {priceChangePercent}%</p>
            <p>Текущая капитализация: {priceMarketCap}$</p>
        </Card>
      </div>
    )
  }
  
  export default CryptocurrencyCard
  