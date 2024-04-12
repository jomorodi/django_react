import React, { useContext } from 'react'
import { Link } from 'react-router-dom'
import AuthContext from '../context/AuthContext'
import { Box } from '@chakra-ui/react'
import { Outlet } from "react-router-dom";


const Header = () => {
    let { user, logoutUser } = useContext(AuthContext)


    function myFunction() {
        var x = document.getElementById("myTopnav");
        if (x.className === "topnav") {
          x.className += " responsive";
        } else {
          x.className = "topnav";
        }
      }
  

    return (
        
        <>
        <div className="topnav" id="myTopnav">
        
            <Link to="/" className='active'>Home</Link>
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
            
            </div>
        <div>
        <br /> <br /> <br />
        {user && <p>Hello {user.username}!</p>}

        </div>
        <Outlet  />
        </>
    )
}

export default Header



 