import React from "react";
import { BrowserRouter } from 'react-router-dom';
import "./App.css";
import Sidebar from "./components/main_page/Sidebar";
import MainContent from "./components/main_page/MainContent";

function App() {
  return (
    <BrowserRouter>
      <div className="app">
        <Sidebar />
        <MainContent />
      </div>
    </BrowserRouter>
  );
}

export default App;
