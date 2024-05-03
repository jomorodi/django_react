// EditAccount.js
import React, { useContext } from 'react'
import AuthContext from '../context/AuthContext'


function EditAccount() {

  let { user, logoutUser , authTokens } = useContext(AuthContext)

  let changeUserPassword = async (e) => {

    e.preventDefault()
    
    const response = await fetch( import.meta.env.VITE_API_URL + 'changePassword/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization':'Bearer ' + String(authTokens.access)
        },
        body: JSON.stringify({oldPassword: e.target.oldPassword.value, newPassword: e.target.newPassword.value,  })
    });
    if (response.status === 200) {

        logoutUser ()   
    }

}


  return  ( <form  onSubmit={changeUserPassword} style={{border: '1px solid  #ccc'}}>
  <div className="container">
    <h1> Change Password </h1>
    <p>Please fill in this form to Change your password.</p>
    <hr />

    <label htmlFor="oldPassword"><b>Old Password</b></label>
    <input type="password" placeholder="Enter Password" name="oldPassword" required />
   

    <label htmlFor="newPassword"><b>Password</b></label>
    <input type="password" placeholder="Enter Password" name="newPassword" required />

    <label htmlFor="psw-repeat"><b>Repeat Password</b></label>
    <input type="password" placeholder="Repeat Password" name="psw-repeat" required />
  
   
    <div className="clearfix">
      
      <button type="submit" class="signupbtn">Change Password</button>
    </div>
  </div>
</form> ) 
}

export default EditAccount;
