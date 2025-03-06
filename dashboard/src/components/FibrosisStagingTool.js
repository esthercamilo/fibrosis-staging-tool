import React from "react";
import coverImage from "../assets/banner.svg";
import Predictor from "./predictor";
import { MathJax, MathJaxContext } from "better-react-mathjax";

const FibrosisStagingTool = () => {
  const formula = `FIB-4 = \\frac{\\text{Age} \\times \\text{AST}}{\\text{Platelets} \\times \\sqrt{\\text{ALT}}}`;

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
            <a className="nav-link" href="#home" data-bs-toggle="tab">
              Home
            </a>
          </li>
          <li className="nav-item">
            <a
              className="nav-link active"
              href="#prediction"
              data-bs-toggle="tab"
            >
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
            className="tab-pane fade"
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
                  marginBottom: "50px",
                }}
              />
            </p>
            <h5>General model performance</h5>
            <img
              className="performance"
              src="/performance.png"
              style={{
                marginTop: "50px",
                width: "100%",
                minWidth: "400px",
                marginBottom: "50px",
              }}
            />

            <h3>
              Empirical Estimation of Liver Fibrosis: FIB-4 and APRI Indices
            </h3>
            <p>
              The Fibrosis Index (FIB) is a non-invasive method for assessing
              liver fibrosis based on clinical and laboratory parameters. One of
              the most commonly used formulas is the FIB-4 index, which
              estimates liver fibrosis severity using age, AST, ALT, and
              platelet count:
            </p>

            <MathJaxContext>
              <div>
                <p>The FIB-4 index is calculated as:</p>
                <MathJax>{"\\[" + formula + "\\]"}</MathJax>
              </div>
            </MathJaxContext>

            <h5>Classification: G1 vs. G2 in tradicional FIB-4</h5>

            <p>
              The classification into <strong>G1 (mild fibrosis)</strong> or{" "}
              <strong>G2 (advanced fibrosis)</strong> depends on predefined
              cutoff values of the FIB score. While these thresholds may vary
              based on specific clinical guidelines, a common approach is:
            </p>

            <p>
              <strong>G1 (Mild or No Significant Fibrosis):</strong> FIB-4 &lt;
              1.45
              <br />
              <strong>G2 (Advanced Fibrosis or Cirrhosis):</strong> FIB-4 &ge;
              1.45
            </p>

            <p>For APRI:</p>

            <p>
              <strong>G1:</strong> APRI &lt; 0.7
              <br />
              <strong>G2:</strong> APRI &ge; 0.7
            </p>
          </div>
          <div className="tab-pane fade show active" id="prediction">
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

        <small className="d-block text-end m-5">
          <a
            href="https://motivaservicos.com.br"
            className="text-decoration-none"
            style={{ color: "#D3D3D3" }}
            target="_blank"
          >
            made by Motiva Serviços 2025
          </a>
        </small>
      </div>
    </div>
  );
};

export default FibrosisStagingTool;
