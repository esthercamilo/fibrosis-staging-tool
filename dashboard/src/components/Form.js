import React from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import coverImage from "../assets/banner.svg";
import "./Form.css";
import Predictor from "./predictor";

const Form = () => {
  return (
    <div>
      <div
        className="jumbotron top"
        style={{
          backgroundImage: `
            linear-gradient(90deg, rgba(0, 85, 158, 0.9), rgba(45, 174, 193, 0.5), rgba(0, 85, 158, 0.9)),
            url(${coverImage})
          `,
          backgroundSize: "cover",
          backgroundPosition: "0, 100% 0;",
          height: "25vh",
          color: "#fff",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
        }}
      >
        <h2 className="left">FibMaster METAVIR Calculator</h2>
      </div>

      <div className="mt-4">
        <ul className="nav nav-tabs">
          <li className="nav-item">
            <a className="nav-link active" href="#home" data-toggle="tab">
              Home
            </a>
          </li>
          <li className="nav-item">
            <a className="nav-link" href="#prediction" data-toggle="tab">
              Prediction
            </a>
          </li>
          <li className="nav-item">
            <a className="nav-link" href="#about" data-toggle="tab">
              About
            </a>
          </li>
        </ul>

        <div className="tab-content mt-3">
          <div className="tab-pane fade show active" id="home">
            <h3>Application Overview</h3>
            <p>
              Viral hepatitis (HBV and HCV) and non-alcoholic fatty liver
              disease (NAFLD) are public health problems and can cause liver
              fibrosis. Scores combining biomarker quantifications (such as APRI
              and FIB-4) are an alternative to liver biopsy for staging liver
              fibrosis. Based on the markers AGE, AST, ALT, and PL, we predict
              whether fibrosis belongs to group 1 or group 2. These markers help
              assess liver health and fibrosis severity. By analyzing their
              levels, we can distinguish between different fibrosis groups,
              providing valuable information for diagnosis and treatment
              planning.
            </p>
          </div>
          <div className="tab-pane fade" id="prediction">
            <h5>Fill the data</h5>
            <Predictor />
          </div>
          <div className="tab-pane fade" id="about">
            <h3>About</h3>
            <p>Conteúdo da aba About...</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Form;
