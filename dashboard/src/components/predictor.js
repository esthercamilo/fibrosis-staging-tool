import React, { useState, useEffect } from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import "./predictor.css";
import axios from "axios";
import * as Yup from "yup";
import DecisionTree from "./Tree";
import * as d3 from "d3";

const Predictor = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [responseData, setResponseData] = useState(null);

  const [formData, setFormData] = useState({
    age: "",
    ast: "",
    alt: "",
    pl: "",
  });

  const [errors, setErrors] = useState({});

  const validationSchema = Yup.object({
    age: Yup.number()
      .required("Age is required")
      .integer("Age must be an integer")
      .positive("Age must be positive")
      .max(150, "Age cannot be greater than 150"),
    ast: Yup.number()
      .required("AST value is required")
      .integer("AST must be an integer")
      .positive("AST must be positive")
      .max(1000, "AST cannot be greater than 1000"),
    alt: Yup.number()
      .required("ALT value is required")
      .integer("ALT must be an integer")
      .positive("ALT must be positive")
      .max(1000, "ALT cannot be greater than 1000"),
    pl: Yup.number()
      .required("PL value is required")
      .integer("PL must be an integer")
      .positive("PL must be positive")
      .max(1000, "PL cannot be greater than 1000"),
  });

  const validate = async () => {
    try {
      await validationSchema.validate(formData, { abortEarly: false });
      setErrors({});
      return true;
    } catch (err) {
      const newErrors = {};
      err.inner.forEach((error) => {
        newErrors[error.path] = error.message;
      });
      setErrors(newErrors);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const isValid = await validate();
    if (isValid) {
      setLoading(true); // Set loading state to true before making the request
      try {
        // Make the axios POST request
        const { age, ast, alt, pl } = formData;
        const response = await axios.post(
          `http://127.0.0.1:8000/api/predict/?AGE=${age}&AST=${ast}&ALT=${alt}&PL=${pl}`
        );
        // Handle the response
        setData(response.data.response);
        console.log(`Atualizando dados`);
      } catch (error) {
        console.error("Error submitting data:", error);
        alert("There was an error submitting the form.");
      } finally {
        setLoading(false); // Set loading state back to false
      }
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  return (
    <div className="container mt-4">
      <div className="row">
        <div className="col-3">
          <div>
            <h5>Enter Your Test Results</h5>

            <form onSubmit={handleSubmit}>
              <div>
                <label>Age (years):</label>
                <input
                  className="form-control"
                  type="number"
                  name="age"
                  value={formData.age}
                  onChange={handleChange}
                />
                {errors.age && <div style={{ color: "red" }}>{errors.age}</div>}
              </div>

              <div>
                <label>AST (U/L):</label>
                <input
                  className="form-control"
                  type="number"
                  name="ast"
                  value={formData.ast}
                  onChange={handleChange}
                />
                {errors.ast && <div style={{ color: "red" }}>{errors.ast}</div>}
              </div>

              <div>
                <label>ALT (U/L):</label>
                <input
                  className="form-control"
                  type="number"
                  name="alt"
                  value={formData.alt}
                  onChange={handleChange}
                />
                {errors.alt && <div style={{ color: "red" }}>{errors.alt}</div>}
              </div>

              <div>
                <label>PL (k/μL):</label>
                <input
                  className="form-control"
                  type="number"
                  name="pl"
                  value={formData.pl}
                  onChange={handleChange}
                />
                {errors.pl && <div style={{ color: "red" }}>{errors.pl}</div>}
              </div>

              <button className="btn btn-primary mt-3 mb-3" type="submit">
                Enviar
              </button>

              <small>
                <p style={{ marginTop: "50px" }}>
                  <b>Blood markers and acceptable values</b>
                </p>
                <ul style={{ marginLeft: "-50px" }}>
                  <li>
                    <b>AST:&nbsp;</b>Aspartate Aminotransferase enzyme (0 - 1000
                    U/L)
                  </li>
                  <li>
                    <b>ALT:&nbsp;</b>Alanine Aminotransferase enzyme (0 - 1000
                    U/L)
                  </li>
                  <li>
                    <b>PL:&nbsp;</b>Platelet count in plasma (0 - 1000 k/μL)
                  </li>
                  <li>
                    <b>AGE:&nbsp;</b>Age (0 - 150 years)
                  </li>
                </ul>
              </small>
            </form>
            {/* <div
              style={{
                marginTop: "50px",
                marginLeft: "0px",
                width: "200px",
              }}
            >
              <p>
                <b>Try actual patient data</b>
              </p>
              <button className="btn btn-light" onCl>
                Patient 1 - G1
              </button>
              <button className="btn btn-light">Patient 2 - G2</button>
              <button className="btn btn-light">Patient 3 - G1</button>
              <button className="btn btn-light">Patient 4 - G2</button>
            </div> */}
          </div>
        </div>
        <div className="col-9 ">
          {data && (
            <h4
              className={`alert ${
                data["prediction"] === "G1" ? "alert-success" : "alert-danger"
              }`}
              role="alert"
            >
              Predicted class: <b>{data["prediction"]}</b>
            </h4>
          )}

          {data && (
            <>
              <DecisionTree
                fulldata={data}
                highlightNodes={data["highlights"]}
              />
              <div
                style={{
                  marginTop: "20px",
                  border: "1px solid #ccc",
                  padding: "20px",
                  maxHeight: "200px",
                  overflowY: "auto",
                }}
              >
                <small>
                  <h5>Calculated values for this patient</h5>
                  {data["values"].map((item) => (
                    <p>
                      {item.field}: {item.value}
                    </p>
                  ))}
                </small>
                <small>
                  <h5>Predictions from FIB4</h5>
                  <p>score: {data.fib4}</p>
                </small>
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
};

export default Predictor;
