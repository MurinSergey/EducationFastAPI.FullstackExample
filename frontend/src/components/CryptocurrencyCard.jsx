import { Card } from 'antd';
import numberWithCommas from '../utils';


function CryptocurrencyCard({ currencyData }) {

    const formatPrice = numberWithCommas(Math.round(currencyData.quote.USD.price));
    const priceChangePercent = currencyData.quote.USD.percent_change_24h.toFixed(2);
    const priceChangeColor = priceChangePercent > 0 ? 'text-green-400' : 'text-red-400';
    const priceMarketCap = numberWithCommas(Math.round(currencyData.quote.USD.market_cap / 1_000_000_000));

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
                height: 340,
                boxShadow: '0px 0px 5px rgba(0,0,0,0.5)',
                border: 'none',
            }}
            className='text-2xl'>
            <p>Текущая цена: {formatPrice}$</p>
            <p>Цена за 24 часа: 
              <span className={priceChangeColor}>
                 {priceChangePercent}%
              </span>
            </p>
            <p>Текущая капитализация: ${priceMarketCap}B</p>
        </Card>
      </div>
    )
  }
  
  export default CryptocurrencyCard
  