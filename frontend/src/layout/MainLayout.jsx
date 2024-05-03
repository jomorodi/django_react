import { Outlet } from "react-router-dom";
import styles from '../css/MainLayout.module.css'
import Header from '../components/Header'
import AuthContext from '../context/AuthContext'
import React, { useContext } from 'react'

export default function MainLayout ()

{
        let { user, logoutUser } = useContext(AuthContext)

    return (

        <div className={styles.gridContainer}>
        
                <header className={styles.pageHeader}></header>
                <nav className={styles.mainNav}><Header/></nav>
               
                <article className={styles.mainArticle}>  <div> <Outlet /> </div>   </article>      
                     
                <footer className={styles.pageFooter}>Footer</footer>    
            
        </div>)

}

