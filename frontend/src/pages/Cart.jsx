
import React, { useState, useEffect, useContext } from 'react'
import AuthContext from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';


export function AddToCart({ itemId }) {
    const { authTokens, logoutUser } = useContext(AuthContext);
    const navigate = useNavigate();
    const handleAddToCart = () => {
        fetch(import.meta.env.VITE_API_URL + 'add_to_cart/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + String(authTokens.access), 
            },
            body: JSON.stringify({ item_id: itemId }),
        })
        .then(response => {
            if (response.ok) {
                console.log('Item added to cart successfully.');
                navigate ("/success")
            } else {
                return response.json().then(data => {
                    throw new Error(data.error || 'Failed to add item to cart.');
                });
            }
        })
        .catch(error => {
            console.error('Error adding item to cart:', error);
            // You can add any additional error handling here, such as displaying an error message
        });
    };

    return <button onClick={handleAddToCart}>Add to Cart</button>;
}

export function ViewCart() {
    const [cartItems, setCartItems] = useState([]);
    const { authTokens, logoutUser } = useContext(AuthContext);
    useEffect(() => {
        fetch(import.meta.env.VITE_API_URL +  'view_cart/', {
            headers: {
                'Authorization': 'Bearer ' + String(authTokens.access), 
            },
        })
        .then(response => response.json())
        .then(data => setCartItems(data))
        .catch(error => console.error('Error fetching cart items:', error));
    }, []);

    const handleRemoveFromCart = (cartItemId) => {
        fetch(import.meta.env.VITE_API_URL + 'remove_from_cart/', {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + String(authTokens.access), 
            },
            body: JSON.stringify({ cart_item_id: cartItemId }),
        })
        .then(response => {
            if (response.ok) {
                console.log('Item removed from cart successfully.');
                setCartItems(cartItems.filter(item => item.id !== cartItemId));
            } else {
                return response.json().then(data => {
                    throw new Error(data.error || 'Failed to remove item from cart.');
                });
            }
        })
        .catch(error => {
            console.error('Error removing item from cart:', error);
            // You can add any additional error handling here, such as displaying an error message
        });
    };

    return (
        <div>
            <h2>Cart</h2>
            <ul>
                {cartItems.map(item => (
                    <li key={item.id}>
                        <h3>{item.item.title}</h3>
                        <p>{item.item.description}</p>
                        <p>Price: ${item.item.price}</p>
                        <button onClick={() => handleRemoveFromCart(item.id)}>Remove</button>
                    </li>
                ))}
            </ul>
        </div>
    );
}

