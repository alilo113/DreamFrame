import {Routes, Route} from "react-router-dom"
import AuthCard from './components/AuthCard';
import { useState, useEffect } from "react";

function App() {
  return (
    <Routes>
      <Route path="/auth" element={<AuthCard />} />
    </Routes>
  )
}

export default App
