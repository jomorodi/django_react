import React, { useContext, useState } from 'react'
import { Link } from 'react-router-dom'
import AuthContext from '../context/AuthContext'
import { Box } from '@chakra-ui/react'
import { Outlet } from "react-router-dom";
import styles from '../css/Header.module.css'


const Header = () => {
    let { user, logoutUser } = useContext(AuthContext)

    function myFunction() {
      let x = document.getElementById("myTopnav");
      if (x.className === "topnav") {
        x.className += " responsive";
      } else {
        x.className = "topnav";
      }
    }
    let [something, setSomething] = useState('')

    return (
        
        <>
        <div className={styles.topnav} id="myTopnav">
        
            <Link to="/" className={styles.active} >Home</Link>
            <span> | </span>
            {user ? (
                <Link onClick={logoutUser}>Logout</Link>
            ) : (
                <Link to="/login" >Login</Link>
            )}
            <Link to="/signUp" >SignUp</Link>
            <Link to="/account" >Account</Link>
            <Link to="/myitems" >Myitems</Link>
            <Link to="/shop" >Shop</Link>
            <Link to="/items">Items</Link>
            <Link to="/search">Search</Link>
            <Link to="/add">Add Items</Link>
            <Link to="/cart"> Your Cart</Link>
            <Link to="/purchase"> Purchase </Link>
            <a href="javascript:void(0);" className={styles.icon} onClick={myFunction}>
            <i className="fa fa-bars"></i>
            </a>
            
            

        </div>
       
      
        </>
    )
}

export default Header



 