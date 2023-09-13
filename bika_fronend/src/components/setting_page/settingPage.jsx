import React, { useState }  from 'react';
import './settingPage.css';
import Sidebar from '../Sidebar';

function SettingPage() {

  const [roomId, setRoomId] = useState('');
  const [, setMessage] = useState('');
  const API_SETTING_URL = process.env.REACT_APP_SETTING_URL;

  const handleRoomIdChange = (event) => {
    setRoomId(event.target.value, 10);
  };

  const handleSubmit = async () => {
    console.log(API_SETTING_URL);
    console.log(roomId);
    try {
      const settingData = {
        roomid: roomId
      };
      console.log(settingData);
      const response = await fetch(`${API_SETTING_URL}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(settingData),
      })
      .then(response => response.json())
      .then(data => console.log(data))
      .catch(error => console.error("Error:", error));

      setMessage(response.message);

    } catch (error) {
      console.log(error);
      setMessage(error.message);
    }
  };

  return (
    <div className="app">
    <><Sidebar />
    <div className="settingPage">
      <h1>Setting Page</h1>
      <input
        id='roomIdInput'
        type="number"
        value={roomId}
        onChange={handleRoomIdChange}
        placeholder="Enter Room ID"
      />
      <button id='submitBotton' onClick={handleSubmit}>Submit</button>
    </div></>
    </div>
  );
}

export default SettingPage;