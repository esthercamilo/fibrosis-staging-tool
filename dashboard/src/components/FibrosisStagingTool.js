import React from "react";
import coverImage from "../assets/banner.svg";
import Predictor from "./predictor";

const FibrosisStagingTool = () => {
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
        <img src="/fib.png" alt="FIB" style={{ height: "100px" }} />
      </div>

      <div className="mt-4">
        <ul className="nav nav-tabs">
          <li className="nav-item">
            <a className="nav-link active" href="#home" data-bs-toggle="tab">
              Home
            </a>
          </li>
          <li className="nav-item">
            <a className="nav-link" href="#prediction" data-bs-toggle="tab">
              Prediction
            </a>
          </li>
          <li className="nav-item">
            <a className="nav-link" href="#about" data-bs-toggle="tab">
              About
            </a>
          </li>
        </ul>

        <div className="tab-content mt-3">
          <div
            className="tab-pane fade show active p-3"
            id="home"
            style={{ maxWidth: "800px", margin: "auto", textAlign: "justify" }}
          >
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
              <img
                className="fibpicture"
                src="/fib.jpeg"
                style={{
                  marginTop: "50px",
                  width: "80%",
                  marginLeft: "10%",
                  minWidth: "400px",
                  marginBottom: "200px",
                }}
              />
            </p>
          </div>
          <div className="tab-pane fade" id="prediction">
            <Predictor />
          </div>
          <div className="tab-pane fade m-4" id="about">
            <p className="mt-3">Publication Link (Soon)</p>
            <p>
              Versioning at{" "}
              <a
                href="https://github.com/esthercamilo/fibrosis-staging-tool/"
                target="_blank"
                rel="noopener noreferrer"
              >
                GitHub
              </a>
            </p>
            <p>Contact: rafael.simoes@unesp.br</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default FibrosisStagingTool;
