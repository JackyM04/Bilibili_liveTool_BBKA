import React from 'react';
import './index.css';

function FunctionBlock({ label, onClick }) {
  return (
    <div className="function-block" onClick={onClick}>
      {label}
    </div>
  );
}

export default FunctionBlock;
