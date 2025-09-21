import { useState } from 'react'
import { useAuth0 } from '@auth0/auth0-react';
import './App.css'
import LoginButton from './loginButton'
import LogoutButton from './LogoutButton'
import Gmap from './Gmap';


function App() {
 const [name, setName] = useState('');


 const { isAuthenticated, user} = useAuth0();


 const handleInput = (e) => {
   setName(e.target.value);
 }


 const handleClick = () => {
   //nothing now
 }




 return (
   <>
   <div class = "app-container">
   <div class = "home-bar">
     <div class = "about">
       <h1>Access Map</h1>
     </div>
     <div class = "extra-info">
       <p>"works for all!"</p>   
     </div>
   </div>




   <div class = "container">
     <div class = "map">
       <h2>Select a location to view report</h2>
       <Gmap />
     </div>
   </div>
   <div>
   <div class = "comment">
       <input
       type = "text"
       value = {name}
       onChange={handleInput}
       placeholder = "Enter text">
       </input>
       <button onClick = {handleClick}>
         Submit
       </button>
     </div>
   </div>
   </div>
   </>
 )
}


export default App