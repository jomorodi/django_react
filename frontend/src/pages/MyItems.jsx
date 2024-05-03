// MyItems.js

import React, { useState, useEffect, useContext } from 'react'
import AuthContext from '../context/AuthContext';
import EditItemPrice from './EditItemPrice'
import { Link } from 'react-router-dom';

function MyItems() {


  return (<> 
  <OnSaleItems />
  <SoldItems />
  <PurchasedItems />
  
  </>)
}

export default MyItems;




function ItemList({ endpoint }) {
    const [items, setItems] = useState([]);
    const { authTokens, logoutUser } = useContext(AuthContext);

    useEffect(() => {
        fetch(endpoint, {
            headers: {
                'Authorization': 'Bearer ' + String(authTokens.access)
              }, 
        })
        .then(response => response.json())
        .then(data => setItems(data))
        .catch(error => console.error('Error fetching items:', error));
    }, [endpoint]);

    return (
        <div>
            <ul>
                {items.map(item => (
                    <li key={item.id}>
                        <h2>{item.title}</h2>
                        <p>{item.description}</p>
                        <p>Price: ${item.price}</p>
                        <p>Date Added: {new Date(item.date_added).toLocaleDateString()}</p>
                        {item.is_sold === false ? <Link to={"/editprice/" + item.id}> Edit Price </Link>: null}
                    </li>
                ))}
            </ul>
        </div>
    );
}

function OnSaleItems() {

    return (<>  
    <p>On Sale Items</p>
    <ItemList endpoint={import.meta.env.VITE_API_URL + "items/on_sale/"} />
     </>) ;
}

function SoldItems() {
    return  (<> 
    
    <p>Sold Items</p>
    <ItemList endpoint={import.meta.env.VITE_API_URL + "items/sold/"} /> 
        
    </>) ;
  }

function PurchasedItems() {
    return (<> 
    <p>Purchased Items</p>
    <ItemList endpoint={import.meta.env.VITE_API_URL + "items/purchased/"} />

    </>) ;
}
