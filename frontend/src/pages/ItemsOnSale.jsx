import React, { useContext, useState } from 'react'
import { Link } from 'react-router-dom'
import AuthContext from '../context/AuthContext'
import { useEffect } from 'react'
import {AddToCart}  from  './Cart'


export default  function ItemsOnSale ()


{

    const [items, setItems] = useState([]);
    const { authTokens, logoutUser , user } = useContext(AuthContext);
    useEffect(() => {
      // Fetch items when the component mounts
      fetch( import.meta.env.VITE_API_URL + 'getItems/', { method: 'GET',
      headers:{
          'Content-Type': 'application/json',
          
      }
      }
        
    ).then(response => response.json())
        .then(data => {
          setItems(data);
        })
        .catch(error => {
          console.error('Error fetching items:', error);
        });
    }, []); // Empty dependency array to only run effect once
  
    return (
      <div>
        <h1>Items for Sale</h1>
        <ul>
          {items.map(item => (
            <li key={item.id}>
              <h2>{item.title}</h2>
              <p>{item.description}</p>
              <p>Price: ${item.price}</p>
              <p>Date Added: {new Date(item.date_added).toLocaleDateString()}</p>
              <p>Seller: {item.seller.username} </p>
              {user != null ? (item.seller.username != user.username ? <AddToCart itemId={item.id} /> : <p> you cannot buy from your self</p>) : null}
            </li>
          ))}
        </ul>
      </div>
    );
  }
