import React from 'react';
import './index.css';

function Sidebar() {
  return (
    <div className="sidebar">
      <ul className="sidebar-menu">
        <li><a href="#feature1">功能1</a></li>
        <li><a href="#feature2">功能2</a></li>
        <li><a href="#feature3">功能3</a></li>
        {/* 添加更多功能链接 */}
      </ul>
      <button className="main-page-button" onClick={() => window.location.href = '/'}>O</button>
    </div>
  );
}

export default Sidebar;