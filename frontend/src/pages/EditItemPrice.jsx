import React, { useState, useEffect, useContext } from 'react'
import AuthContext from '../context/AuthContext'
import { useParams , useNavigate } from 'react-router-dom';

function EditItemPrice() {
    const [newPrice, setNewPrice] = useState('');
    const { authTokens, logoutUser } = useContext(AuthContext);
    const {itemId} = useParams()
    const navigate = useNavigate()
    const handleEditPrice = () => {
        fetch(import.meta.env.VITE_API_URL + 'edit_item_price/', {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + String(authTokens.access)
            },
            body: JSON.stringify({ item_id: itemId, new_price: newPrice }),
        })
        .then(response => {
            if (response.ok) {
                console.log('Item price updated successfully.');
                navigate ("/success")
            } else {
                return response.json().then(data => {
                    throw new Error(data.error || 'Failed to update item price.');
                });
            }
        })
        .catch(error => {
            console.error('Error updating item price:', error);
            // You can add any additional error handling here, such as displaying an error message
        });
    };

    return (
        <div>
            <input
                type="number"
                placeholder="Enter new price"
                value={newPrice}
                onChange={e => setNewPrice(e.target.value)}
            />
            <button onClick={handleEditPrice}>Edit Price</button>
        </div>
    );
}

export default EditItemPrice;
