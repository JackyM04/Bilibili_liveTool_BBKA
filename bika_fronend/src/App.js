import React from "react";
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import "./App.css";
import MainContent from "./components/main_page";
import Setting from "./components/setting_page/settingPage";
function App() {
  return (
    <Router>
        <Routes>
          <Route path="/" element={<MainContent />} />
          <Route path="/setting" element={<Setting />} />
        </Routes>
    </Router>
  );
}

export default App;
