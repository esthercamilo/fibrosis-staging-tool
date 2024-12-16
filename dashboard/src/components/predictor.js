import React from "react";
import "bootstrap/dist/css/bootstrap.min.css";

const Predictor = () => {
  return (
    <div className="container mt-4">
      <form>
        <div className="form-group row">
          <label htmlFor="age" className="col-sm-2 col-form-label">
            AGE
          </label>
          <div className="col-sm-10">
            <input
              type="number"
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
              className="form-control"
              id="pl"
              placeholder="Enter PL"
            />
          </div>
        </div>
        <button type="submit" className="btn btn-primary">
          Submit
        </button>
      </form>
    </div>
  );
};

export default Predictor;
