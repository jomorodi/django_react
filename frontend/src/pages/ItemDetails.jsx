import React, { useState, useEffect, useContext } from 'react'
import AuthContext from '../context/AuthContext';

function ItemDetails({ itemId }) {
    const [itemDetails, setItemDetails] = useState(null);
    const { authTokens, logoutUser } = useContext(AuthContext);
    useEffect(() => {
        fetch(import.meta.env.VITE_API_URL + `item_details/?item_id=${itemId}`, {
            headers: {
                'Authorization': 'Bearer ' + String(authTokens.access)
            },
        })
        .then(response => {
            if (response.ok) {
                return response.json();
            }
            throw new Error('Failed to fetch item details.');
        })
        .then(data => setItemDetails(data))
        .catch(error => console.error('Error fetching item details:', error));
    }, [itemId]);

    if (!itemDetails) {
        return <div>Loading...</div>;
    }

    return (
        <div>
            <h2>Item Details</h2>
            <p>Title: {itemDetails.title}</p>
            <p>Description: {itemDetails.description}</p>
            <p>Price: ${itemDetails.price}</p>
            <p>Date Added: {new Date(itemDetails.date_added).toLocaleDateString()}</p>
            <p>Seller: {itemDetails.seller.username}</p>
        </div>
    );
}

export default ItemDetails;
