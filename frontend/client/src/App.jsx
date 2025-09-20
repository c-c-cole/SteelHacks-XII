import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import LoginButton from './loginButton'

function App() {
  const [name, setName] = useState('');

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
        <p>Sign Up</p>
        <p>Login</p>
        <LoginButton />
      </div>
    </div>


    <div class = "container">
      <div class = "map">
        <h2>Select a location to view report</h2>
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