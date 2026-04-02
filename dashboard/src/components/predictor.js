import React, { useState } from "react";
import DecisionTree from "./Tree";
import axios from "axios";

const Predictor = () => {
  const [inputs, setInputs] = useState({
    AGE: "",
    PL: "",
    "AST or TGO (U/L)": "",
    "ALT or TGP (U/L)": "",
  });
  const [model, setModel] = useState("global");
  const [data, setData] = useState(false);
  const [useLDA, setUseLDA] = useState(false);
  const options = ["Global", "HBV", "HCV", "NAFLD"];

  const patientData = {
    G1: { AGE: 45, PL: 150, "AST or TGO (U/L)": 35, "ALT or TGP (U/L)": 40 },
    G2: { AGE: 58, PL: 28, "AST or TGO (U/L)": 54, "ALT or TGP (U/L)": 291 },
  };

  //58	28	54	291	0.759	G2 (fat)

  const setPatientValues = (g) => {
    setInputs(patientData[g]);
  };

  const handleChange = (e) => {
    setInputs({ ...inputs, [e.target.name]: e.target.value });
  };

  function downloadSVG() {
    const svg = document.getElementById("tree-svg");

    if (!svg) return;

    // Clonar e preparar o SVG
    const clone = svg.cloneNode(true);
    clone.setAttribute("xmlns", "http://www.w3.org/2000/svg");

    // Converter para string
    const svgData = new XMLSerializer().serializeToString(clone);

    // Criar blob e link
    const blob = new Blob([svgData], { type: "image/svg+xml;charset=utf-8" });
    const url = URL.createObjectURL(blob);

    // Criar link de download
    const link = document.createElement("a");
    link.href = url;
    link.download = `arvore_${model}.svg`;
    link.click();

    URL.revokeObjectURL(url);
  }

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const urlBase = "http://127.0.0.1:8000";
      //const urlBase = "https://bioinformatica.fca.unesp.br";
      let url = `${urlBase}/api/predict/${model.toLowerCase()}/?AGE=${
        inputs["AGE"]
      }&AST=${inputs["AST or TGO (U/L)"]}&ALT=${
        inputs["ALT or TGP (U/L)"]
      }&PL=${inputs["PL"]}`;
      if (useLDA) {
        url = `${url}&lda=true`;
      }
      console.log(url);
      const response = await axios.post(url);
      setData(response.data.response);
      console.log(`Atualizando dados`);
    } catch (error) {
      console.error("Error submitting data:", error);
      alert("There was an error submitting the form.");
    }
  };

  return (
    <div className="container mt-4 mb-5">
      <div className="card p-4 shadow-lg">
        <h3 className="text-center mb-4">Settings</h3>
        <form onSubmit={handleSubmit}>
          <div className="row mb-3">
            {Object.keys(inputs).map((key, index) => (
              <div className="col-md-2 d-flex align-items-center" key={key}>
                <div className="w-100">
                  <label className="form-label">{key}</label>
                  <input
                    type="number"
                    name={key}
                    value={inputs[key]}
                    onChange={handleChange}
                    required
                    className="form-control"
                  />
                </div>
              </div>
            ))}

            <div className="col-md-2 d-flex flex-column align-items-start">
              <label>&nbsp;Patient 1</label>
              <button
                type="button"
                onClick={() => setPatientValues("G1")}
                className="btn btn-success w-75 mt-2"
              >
                G1
              </button>
            </div>

            <div className="col-md-2 d-flex flex-column align-items-start">
              <label>&nbsp;Patient 2</label>
              <button
                title="NAFLD"
                type="button"
                onClick={() => setPatientValues("G2")}
                className="btn btn-danger w-75 mt-2"
              >
                G2
              </button>
            </div>
          </div>
          <div className="row mb-3">
            <div className="col-md-6">
              <label className="form-label">Model</label>
              <select
                className="form-select"
                value={model}
                onChange={(e) => setModel(e.target.value)}
                required
              >
                {options.map((option) => (
                  <option key={option} value={option}>
                    {option}
                  </option>
                ))}
              </select>
            </div>
            <div className="col-md-6 d-flex align-items-center">
              <input
                type="checkbox"
                id="lda"
                checked={useLDA}
                onChange={() => setUseLDA(!useLDA)}
                className="form-check-input me-2"
              />
              <label htmlFor="lda" className="form-check-label">
                Include LDA attributes
              </label>
            </div>
          </div>
          <button type="submit" className="btn btn-primary w-100">
            <b>Predict</b>
          </button>
        </form>
      </div>
      {data && (
        <div className="card mt-4 p-4 shadow-sm">
          <h4 className="text-center">Decision Tree</h4>
          <DecisionTree fulldata={data} highlightNodes={data["highlights"]} />
        </div>
      )}
      {data && (
        <div className="card mt-4 p-4 shadow-sm">
          <h4 className="text-center">Results and metrics </h4>

          {data["prediction"] === "G2" ? (
            <p className="bg-danger-subtle text-dark p-2">
              Predicted class: <b>{data["prediction"]}</b>
            </p>
          ) : (
            <p className="bg-success-subtle text-dark p-2">
              Predicted class: <b>{data["prediction"]}</b>
            </p>
          )}
          <p>Confidence: {data["confidence"]}%</p>
          <p>FIB-4 score: {data["fib4"]}</p>
          <pre>
            {data["coeficientes"].replace("Coeficientes", "Coeficientes LDA")};
          </pre>
          <button onClick={downloadSVG} className="btn btn-primary">
            Exportar árvore
          </button>
        </div>
      )}
    </div>
  );
};

export default Predictor;
