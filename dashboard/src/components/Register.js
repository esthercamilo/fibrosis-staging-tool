import React, { useState } from "react";

function Register() {
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    password: "",
  });
  const [successMessage, setSuccessMessage] = useState("");

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch("http://localhost:5000/api/users/register", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
      });

      if (response.ok) {
        const data = await response.json();
        console.log("Usuário registrado:", data);
        setSuccessMessage("Cadastrado com sucesso!");
        setFormData({ name: "", email: "", password: "" }); // Limpar formulário
      } else {
        console.error("Erro no registro");
        setSuccessMessage(""); // Limpar mensagem se houver erro
      }
    } catch (error) {
      console.error("Erro na requisição:", error);
      setSuccessMessage(""); // Limpar mensagem se houver erro
    }
  };

  return (
    <div className="container mt-4">
      <h2>Registrar</h2>
      {successMessage && (
        <div className="alert alert-success" role="alert">
          {successMessage}
        </div>
      )}
      <form onSubmit={handleSubmit}>
        <div className="mb-3">
          <label htmlFor="name" className="form-label">
            Nome
          </label>
          <input
            type="text"
            name="name"
            className="form-control"
            id="name"
            value={formData.name}
            onChange={handleChange}
            required
          />
        </div>
        <div className="mb-3">
          <label htmlFor="email" className="form-label">
            Email
          </label>
          <input
            type="email"
            name="email"
            className="form-control"
            id="email"
            value={formData.email}
            onChange={handleChange}
            required
          />
        </div>
        <div className="mb-3">
          <label htmlFor="password" className="form-label">
            Senha
          </label>
          <input
            type="password"
            name="password"
            className="form-control"
            id="password"
            value={formData.password}
            onChange={handleChange}
            required
          />
        </div>
        <button type="submit" className="btn btn-primary">
          Registrar
        </button>
      </form>
    </div>
  );
}

export default Register;
