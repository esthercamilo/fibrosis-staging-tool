import React, { useState } from "react";
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

function AddQuestion() {
  const [formData, setFormData] = useState({
    title: "",
    options: ["", "", "", ""], // Quatro opções iniciais
    correctAnswer: "",
    subject: "",
    difficulty: "easy", // Valor padrão
  });
  const handleChange = (e) => {
    const { name, value } = e.target;
    if (name === "options") {
      // Atualiza as opções individualmente, se necessário
      const index = parseInt(e.target.dataset.index); // Pega o índice da opção
      const updatedOptions = [...formData.options];
      updatedOptions[index] = value;
      setFormData({ ...formData, options: updatedOptions });
    } else {
      setFormData({
        ...formData,
        [name]: value,
      });
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch("http://localhost:5000/api/questions/add", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
      });

      if (response.ok) {
        toast.success("Questão adicionada com sucesso!"); // Exibe o toast
        const data = await response.json();
        console.log("Questão adicionada com sucesso:", data);
        // Limpa o formulário após a submissão
        setFormData({
          title: "",
          options: ["", "", "", ""],
          correctAnswer: "",
          subject: "",
          difficulty: "easy",
        });
      } else {
        toast.error("Erro ao adicionar questão"); // Exibe o erro
        console.error("Erro ao adicionar questão");
      }
    } catch (error) {
      console.error("Erro na requisição:", error);
    }
  };

  return (
    <>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Título:</label>
          <input
            type="text"
            name="title"
            value={formData.title}
            onChange={handleChange}
            required
          />

        </div>
        {formData.options.map((option, index) => (
          <div key={index}>
            <label>Opção {index + 1}:</label>
            <input
              type="text"
              name="options"
              data-index={index} // Atribui o índice à opção
              value={option}
              onChange={handleChange}
              required
            />
          </div>
        ))}

        <div>
          <label>Resposta Correta:</label>
          <select
            name="corretAnswer"
            value={formData.corretAnswer}
            onChange={handleChange}
          >

           <option value="option1">Opção 1</option>
           <option value="option2">Opção 2</option>
           <option value="option3">Opção 3</option>
           <option value="option4">Opção 4</option>
           <option value="option5">Opção 5</option>
          </select>
        </div>

        <div>
          <label>Disciplina:</label>
          <input
            type="text"
            name="subject"
            value={formData.subject}
            onChange={handleChange}
            required
          />
        </div>

        <div>
          <label>Dificuldade:</label>
          <select
            name="difficulty"
            value={formData.difficulty}
            onChange={handleChange}
          >
            <option value="easy">Fácil</option>
            <option value="medium">Médio</option>
            <option value="hard">Difícil</option>
          </select>
        </div>

        <button type="submit">Adicionar Questão</button>
      </form>

      <ToastContainer
        position="top-right" // Ajuste a posição conforme necessário
        autoClose={5000} // Tempo que o toast fica visível
        hideProgressBar={false}
        newestOnTop={false}
        closeOnClick
        rtl={false}
        pauseOnFocusLoss
        draggable
        pauseOnHover
      />
    </>
  );
}

export default AddQuestion;
