import { useState, useEffect } from 'react'
import { useAuth0 } from '@auth0/auth0-react';
import './App.css'
import Gmap from './Gmap';


function App() {
  const [comment, setComment] = useState('');
  const [comments, setComments] = useState([]);
  const [selectedHospital, setSelectedHospital] = useState(null);

  const { isAuthenticated, user} = useAuth0();

  useEffect(() => {
  console.log("Selected hospital:", selectedHospital);
}, [selectedHospital]);


  // fetch comments whenever a hospital is selected
  useEffect(() => {
    if (selectedHospital) {
      fetch(`http://localhost:5000/comments/${selectedHospital.id}`)
        .then(res => res.json())
        .then(data => setComments(data))
        .catch(err => console.error(err));
    }
  }, [selectedHospital]);

  const handleInput = (e) => {
    setComment(e.target.value);
  };

const handleSubmit = () => {
  if (!isAuthenticated || !selectedHospital) return;

  fetch(`http://localhost:5000/comments/${selectedHospital.id}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ user: user.email, text: comment })
  })
  .then(() => fetch(`http://localhost:5000/comments/${selectedHospital.id}`))
  .then(res => res.json())
  .then(data => {
    setComments(data); // update state with fresh comments
    setComment('');     // clear input
  })
  .catch(err => console.error(err));
};


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
       <Gmap onSelectHospital={setSelectedHospital}/>
     </div>
     <div className = "hospital-comments">
      {selectedHospital ? (
        <div>
          <h2>{selectedHospital.facility}</h2>
          <p><strong>Address: </strong>{selectedHospital.address}</p>
          
          <h3>Comments</h3>
          <ul>
            {comments.map((c, i) => (
              <li key={i}><strong>{c.user}</strong>: {c.text}</li>
            ))}
          </ul>
          {isAuthenticated ? (
            <div className="comment">
              <input
                type="text"
                value={comment}
                onChange={handleInput}
                placeholder="Enter your comment"
              />
              <button onClick={handleSubmit}>Submit</button>
            </div>
          ) : (
            <p><em>Login to post a comment.</em></p>
          )}
        </div>
      ) : (
        <p>Select a marker to see comments.</p>
      )}
     </div>
   </div>
   <div>
   </div>
   </div>
   </>
 )
}


export default App