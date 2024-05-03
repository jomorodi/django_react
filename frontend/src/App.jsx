import { createBrowserRouter, BrowserRouter as Router, Route, Routes,  RouterProvider , createRoutesFromElements } from 'react-router-dom'

import { AuthProvider } from './context/AuthContext'

import HomePage from './pages/HomePage'
import LoginPage from './pages/LoginPage'
import EditAccount from './pages/EditAccount'
import ItemsOnSale from './pages/ItemsOnSale'
import ItemSearch from './pages/ItemSearch'
import AddItem from './pages/AddItem'
import MyItems from './pages/MyItems'
import ItemsToPurchase from './pages/ItemsToPurchase'
import {ViewCart} from './pages/Cart'
import SuccessMessage from './pages/SuccessMessage'
import EditItemPrice from './pages/EditItemPrice'
import SignUpPage from './components/SignUp'
import Header from './components/Header'
import PrivateRoute from './utils/PrivateRoute'
import { ChakraProvider } from '@chakra-ui/react'
import MainLayout from './layout/MainLayout'

import WithSubnavigation from './components/HomeNavigationBar'

//<WithSubnavigation />   

const router = createBrowserRouter([
  { path: "*", Component: Root },
]);



function App() {
  

  return (
    <div className="App">
    
    <RouterProvider router={router} /> 
    
    </div>
  );
}



function Root() {

  return (
   
        
            <AuthProvider>            
            <Routes>
            <Route element={<MainLayout />} >  
                      
                      <Route path="/" element={<HomePage/>} />
                      <Route path="/login" element={<LoginPage/>}/>
                      <Route path="/signup" element={<SignUpPage/>}/>
                      <Route path="/account" element={<PrivateRoute> <EditAccount/> </PrivateRoute>}  />
                      <Route path="/shop" element ={<ShopPage/>} /> 
                      <Route path="/myitems" element ={<PrivateRoute> <MyItems/> </PrivateRoute>} />
                      <Route path="/items" element ={<ItemsOnSale />} />
                      <Route path="/search" element ={<ItemSearch />} />
                      <Route path="/add" element ={<PrivateRoute> <AddItem/> </PrivateRoute>} />
                      <Route path="/cart" element ={<PrivateRoute> <ViewCart /> </PrivateRoute>} />
                      <Route path="/purchase" element ={<PrivateRoute> <ItemsToPurchase /> </PrivateRoute>} />
                      <Route path="/editprice/:itemId" element ={<PrivateRoute> <EditItemPrice /> </PrivateRoute>} />
                      <Route path="/success" element ={<PrivateRoute> <SuccessMessage /> </PrivateRoute>} />
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






export default App;


