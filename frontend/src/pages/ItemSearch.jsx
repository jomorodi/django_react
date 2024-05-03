import React, { useContext, useState } from 'react'
import { Link } from 'react-router-dom'
import AuthContext from '../context/AuthContext'
import { useEffect } from 'react'


function ItemSearch() {

    const [items, setItems] = useState([]);
    const { authTokens, logoutUser } = useContext(AuthContext);
    const [query, setQuery] = useState('');
    const [searchResults, setSearchResults] = useState([]);

    const handleSearch = () => {
        fetch(import.meta.env.VITE_API_URL +  `search_items/?query=${query}` ,
        { method: 'GET',
        headers:{
            'Content-Type': 'application/json',
            
        }
        })
            .then(response => response.json())
            .then(data => setSearchResults(data))
            .catch(error => console.error('Error searching items:', error));
    };

    return (
        <div>
            <input
                type="text"
                value={query}
                onChange={e => setQuery(e.target.value)}
                placeholder="Search items by title"
            />
            <button onClick={handleSearch}>Search</button>

            <ul>
                {searchResults.map(item => (
                    <li key={item.id}>
                        <h2>{item.title}</h2>
                        <p>{item.description}</p>
                        <p>Price: ${item.price}</p>
                        <p>Date Added: {new Date(item.date_added).toLocaleDateString()}</p>
                    </li>
                ))}
            </ul>
        </div>
    );
}

export default ItemSearch;
