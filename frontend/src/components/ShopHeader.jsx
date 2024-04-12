import React, { useContext } from 'react'
import { Link } from 'react-router-dom'
import AuthContext from '../context/AuthContext'
import { Box } from '@chakra-ui/react'
import { Outlet } from "react-router-dom";


const ShopHeader = () => {
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
        
            <Link to="/shop" className='active'>Shop</Link>
            
            {user ? (
                <Link onClick={logoutUser}>Logout</Link>
            ) : (
                <Link to="/login" >Login</Link>
            )}

            <Link to="/SignUp" >SignUp</Link>
            <Link to="/Account" >Account</Link>
            <Link to="/Myitems" >Myitems</Link>
            
            </div>
        <div>
        <br /> <br /> <br />
        {user && <p>Hello {user.username}!</p>}

        </div>
        <Outlet  />
        </>
    )
}

export default  ShopHeader



 