

import React, { useState, useEffect, useContext } from 'react'
import AuthContext from '../context/AuthContext';

function ItemsToPurchase() {
    const [cartItems, setCartItems] = useState([]);
    const { authTokens, logoutUser } = useContext(AuthContext);

    useEffect(() => {
        fetch(import.meta.env.VITE_API_URL + 'items_to_purchase/', {
            headers: {
                'Authorization': 'Bearer ' + String(authTokens.access)
            },
        })
        .then(response => response.json())
        .then(data => setCartItems(data))
        .catch(error => console.error('Error fetching items to purchase:', error));
    }, []);

    const handlePay = () => {
        fetch(import.meta.env.VITE_API_URL + 'pay/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + String(authTokens.access)
            },
        })
        .then(response => {
            if (response.ok) {
                console.log('Payment successful.');
                // You can add any additional logic here, such as redirecting to a success page
            } else {
                return response.json().then(data => {
                    throw new Error(data.error || 'Payment failed.');
                });
            }
        })
        .catch(error => {
            console.error('Error processing payment:', error);
            // You can add any additional error handling here, such as displaying an error message
        });
    };

    return (
        <div>
            <h2>Items to Purchase</h2>
            <ul>
                {cartItems.map(cartItem => (
                    <li key={cartItem.id}>
                        <h3>{cartItem.item.title}</h3>
                        <p>{cartItem.item.description}</p>
                        <p>Price: ${cartItem.item.price}</p>
                    </li>
                ))}
            </ul>
            <button onClick={handlePay}>Pay</button>
        </div>
    );
}

export default ItemsToPurchase;
