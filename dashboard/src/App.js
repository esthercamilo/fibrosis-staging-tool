import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import "bootstrap/dist/css/bootstrap.min.css";
import FibMaster from "./components/FibMaster";
import FibrosisStagingTool from "./components/FibrosisStagingTool";
import Home from "./components/Home";
import NotFound from "./components/NotFound";

function App() {
  return (
    <Router>
      <Routes>
        <Route exact path="/" element={<Home />} />
        <Route path="/fibmaster" element={<FibMaster />} />
        <Route
          path="/fibrosis-staging-tool"
          element={<FibrosisStagingTool />}
        />
        <Route path="*" element={<NotFound />} />
      </Routes>
    </Router>
  );
}

export default App;
