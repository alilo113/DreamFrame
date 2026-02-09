import {Routes, Route} from "react-router-dom"
import AuthCard from './components/AuthCard';
import Dashboard from './components/Dashboard';
import { useState, useEffect } from "react";

function App() {
  return (
    <Routes>
      <Route path="/auth" element={<AuthCard />} />
      <Route path="/dashboard" element={<Dashboard />} />
    </Routes>
  )
}

export default App
