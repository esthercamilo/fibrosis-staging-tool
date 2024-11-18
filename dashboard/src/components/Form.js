import React, { useState } from "react";
import { Button, Form, Container, Alert } from "react-bootstrap";
import "./Form.css";
import axios from "axios";

function PredictionForm() {
  const [age, setAge] = useState("");
  const [ast, setAst] = useState("");
  const [alt, setAlt] = useState("");
  const [pl, setPl] = useState("");
  const [result, setResult] = useState(null);
  const [explanation, setExplanation] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async event => {
    event.preventDefault();
    setLoading(true);
    setError(null);

    try {
      // Faz a requisição usando parâmetros na query string
      //const response = await axios.post("http://127.0.0.1:8000/api/predict/", {
      const response = await axios.post("http://44.203.65.53:8000/api/predict/", {
        params: {
          AGE: age,
          AST: ast,
          ALT: alt,
          PL: pl
        }
      });

      const data = response.data;
      setResult(true); // Supondo que a resposta tenha `result`
      setExplanation(JSON.stringify(data)); // Supondo que a resposta tenha `explanation`
    } catch (err) {
      setError("Erro ao realizar a predição");
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container className="mt-4">
      <h2 className="mb-4">Preditor do nível de fibrose do fígado</h2>

      <Form onSubmit={handleSubmit}>
        <Form.Group controlId="formAge" className="form-group">
          <Form.Label>Idade</Form.Label>
          <Form.Control
            type="number"
            placeholder="Digite a idade"
            value={age}
            onChange={e => setAge(e.target.value)}
            required
          />
        </Form.Group>

        <Form.Group controlId="formAst" className="form-group">
          <Form.Label>AST</Form.Label>
          <Form.Control
            type="number"
            placeholder="Digite o valor de AST"
            value={ast}
            onChange={e => setAst(e.target.value)}
            required
          />
        </Form.Group>

        <Form.Group controlId="formAlt" className="form-group">
          <Form.Label>ALT</Form.Label>
          <Form.Control
            type="number"
            placeholder="Digite o valor de ALT"
            value={alt}
            onChange={e => setAlt(e.target.value)}
            required
          />
        </Form.Group>

        <Form.Group controlId="formPl" className="form-group">
          <Form.Label>PL</Form.Label>
          <Form.Control
            type="number"
            placeholder="Digite o valor de PL"
            value={pl}
            onChange={e => setPl(e.target.value)}
            required
          />
        </Form.Group>

        <Button
          variant="primary"
          type="submit"
          disabled={loading}
          className="mt-3"
        >
          {loading ? "Carregando..." : "Submeter"}
        </Button>
      </Form>

      {error && (
        <Alert variant="danger" className="mt-3">
          {error}
        </Alert>
      )}

      {result && (
        <div className="mt-4">
          <h3>Classe Resultante: {result}</h3>
          {explanation && (
            <p>
              <strong>Explicação:</strong> {explanation}
            </p>
          )}
        </div>
      )}
    </Container>
  );
}

export default PredictionForm;
