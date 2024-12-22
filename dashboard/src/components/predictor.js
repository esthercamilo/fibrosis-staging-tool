import React, { useState, useEffect } from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import "./predictor.css";
import axios from "axios";

const Predictor = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchData = async () => {
    setLoading(true); // Inicia o carregamento
    setError(null); // Reseta os erros

    try {
      const response = await axios.get("http://0.0.0.0:8000/api/health-check/");
      console.log(response);
      setData(response.data.response);
    } catch (error) {
      setError(error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mt-4">
      <div className="row">
        <div className="col-3">
          <div>
            <h5>Enter Your Test Results</h5>
            <div className="form-group row">
              <label htmlFor="age" className="col-sm-2 col-form-label">
                AGE
              </label>
              <div className="col-sm-10">
                <input
                  type="number"
                  step="any"
                  className="form-control"
                  id="age"
                  placeholder="Enter AGE"
                />
              </div>
            </div>
            <div className="form-group row">
              <label htmlFor="ast" className="col-sm-2 col-form-label">
                AST
              </label>
              <div className="col-sm-10">
                <input
                  type="number"
                  step="any"
                  className="form-control"
                  id="ast"
                  placeholder="Enter AST"
                />
              </div>
            </div>
            <div className="form-group row">
              <label htmlFor="alt" className="col-sm-2 col-form-label">
                ALT
              </label>
              <div className="col-sm-10">
                <input
                  type="number"
                  step="any"
                  className="form-control"
                  id="alt"
                  placeholder="Enter ALT"
                />
              </div>
            </div>
            <div className="form-group row">
              <label htmlFor="pl" className="col-sm-2 col-form-label">
                PL
              </label>
              <div className="col-sm-10">
                <input
                  type="number"
                  step="any"
                  className="form-control"
                  id="pl"
                  placeholder="Enter PL"
                />
              </div>
            </div>
            <button
              type="submit"
              className="btn btn-primary mt-3 mb-3"
              onClick={fetchData}
            >
              Submit
            </button>
          </div>
        </div>
        <div className="col-9 borda">
          <h1>{data}</h1>
        </div>
      </div>
    </div>
  );
};

export default Predictor;
