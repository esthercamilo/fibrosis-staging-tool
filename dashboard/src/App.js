import React from "react";
import { BrowserRouter as Router, Route, Routes, Link } from "react-router-dom";
import Register from "./components/Register";
import AddQuestion from "./components/AddQuestion";
import Roadmap from "./components/Roadmap";
import Desempenho from "./components/Desempenho";
import "bootstrap/dist/css/bootstrap.min.css";

function Home() {
  return <h2>Bem-vindo ao ViaIntensiva</h2>;
}

function App() {
  return (
    <Router>
      <div className="App container mt-4">
        <nav className="navbar navbar-expand-lg navbar-light bg-light">
          <ul className="navbar-nav">
            <li className="nav-item">
              <Link className="nav-link" to="/">
                Home
              </Link>
            </li>
            <li className="nav-item">
              <Link className="nav-link" to="/roadmap">
                Roadmap
              </Link>
            </li>
            <li className="nav-item">
              <Link className="nav-link" to="/desempenho">
                Desempenho
              </Link>
            </li>
            <li className="nav-item">
              <Link className="nav-link" to="/register">
                Registrar
              </Link>
            </li>
            <li className="nav-item">
              <Link className="nav-link" to="/add-question">
                Adicionar Questão
              </Link>
            </li>
          </ul>
        </nav>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/roadmap" element={<Roadmap />} />
          <Route path="/desempenho" element={<Desempenho />} />
          <Route path="/register" element={<Register />} />
          <Route path="/add-question" element={<AddQuestion />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
