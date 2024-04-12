import { createBrowserRouter, BrowserRouter as Router, Route, Routes,  RouterProvider , createRoutesFromElements } from 'react-router-dom'

import { AuthProvider } from './context/AuthContext'

import HomePage from './pages/HomePage'
import LoginPage from './pages/LoginPage'
import SignUpPage from './components/SignUp'
import Header from './components/Header'
import ShopHeader from './components/ShopHeader'
import PrivateRoute from './utils/PrivateRoute'
import { ChakraProvider } from '@chakra-ui/react'

import WithSubnavigation from './components/HomeNavigationBar'

//<WithSubnavigation />   

const router = createBrowserRouter([
  { path: "*", Component: Root },
]);



function App() {
  

  return (
    <div className="App">
    
    <ChakraProvider>
    <RouterProvider router={router} />;
       
    </ChakraProvider>
    </div>
  );
}



function Root() {

  return (
   
        
            <AuthProvider>            
            <Routes>
                      <Route element={<Header/>}>
                      <Route path="/" element={<HomePage/>} />
                      <Route path="/login" element={<LoginPage/>}/>
                      <Route path="/signup" element={<SignUpPage/>}/>
                      <Route path="/account" element={<PrivateRoute> <AccountPage /> </PrivateRoute>}  />
                      <Route path="/shop" element ={<ShopPage/>} /> 
                      <Route path="/myitems" element ={<PrivateRoute> <MyitemsPage/> </PrivateRoute>} />
  
                      </Route>
                      <Route element={<ShopHeader/>}>
                     
                      </Route>
                      
     </Routes>
      </AuthProvider>
        
     
  );


}


function ShopPage () {
  return (
    <div>
      <h2>shop</h2>
    </div>
  );
}



function AccountPage() {
  return (
    <div>
      <h2>Account</h2>
    </div>
  );
}

function MyitemsPage() {
  return (
    <div>
      <h2>Myitems</h2>
    </div>
  );
}


export default App;


