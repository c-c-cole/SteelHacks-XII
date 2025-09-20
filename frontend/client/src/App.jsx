import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'

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
    <div class = "title">
      <h2>Access Map</h2>
    </div>
      <div class = "login">
        <input
        type = "text"
        value = {name}
        onChange={handleInput}
        placeholder = "Enter Username">
        </input>
        <button onClick = {handleClick}>
          Submit
        </button>
      </div>
    </>
  )
}

export default App