import React from 'react';
import './index.css';

function Sidebar() {
  return (
    <div className="sidebar">
      <button className='setting-button' onClick={() => window.location.href = 'setting'}></button>
      <button className="main-page-button" onClick={() => window.location.href = '/'}>O</button>
    </div>
  );
}

export default Sidebar;