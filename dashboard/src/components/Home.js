import React from "react";
import "../App.css";

const Home = () => {
  return (
    <div className="d-flex flex-column min-vh-100">
      <header className="d-flex align-items-center p-3 bg-light border-bottom">
        <img
          src="./fotodocente.png"
          alt="Foto do docente"
          className="rounded-circle me-3"
          style={{ width: "80px", height: "80px" }}
        />
        <div>
          <h1 className="h5 mb-1">Dr. Rafael Plana Simões</h1>
          <p className="mb-0 text-muted">
            Professor na UNESP - Departamento de Bioprocessos e Biotecnologia
          </p>
          <small>Líder do time de Bioinformática</small>
        </div>
      </header>
      <main className="container my-4 px-3 py-4">
        {/* Resumo */}
        <section id="sobre" className="mb-5">
          <h2 className="h4 mb-3">Sobre o Grupo</h2>
          <p>
            O grupo, associado ao Departamento de Bioprocessos e Biotecnologia
            da UNESP, foca em biotecnologia e bioengenharia aplicadas à saúde
            humana e animal. A pesquisa abrange bioinformática, modelagem
            molecular e matemática aplicada, com ênfase no desenvolvimento de
            bioprodutos, bioprocessos e biomateriais, promovendo soluções
            sustentáveis e de impacto em saúde.
          </p>
        </section>

        {/* Softwares */}
        <section id="softwares" className="mb-5">
          <h2 className="h4 mb-3">Softwares e Ferramentas</h2>
          <ul>
            {/* <li>
              <a href="/fibmaster" target="_blank" rel="noopener noreferrer">
                FibMaster
              </a>
              - Preditor do nível de gravidade da fibrose hepática com base em
              marcadores molecures.
            </li> */}
            <li>
              <a
                href="/fibrosis-staging-tool"
                target="_blank"
                rel="noopener noreferrer"
              >
                Fibrosis Staging Tool
              </a>
              - Nova versão do preditor do nível de gravidade da fibrose
              hepática com base em marcadores molecures.
            </li>
          </ul>
        </section>

        {/* Artigos */}
        <section id="artigos" className="mb-5">
          <h2 className="h4 mb-3">Artigos e Publicações</h2>
          <ul>
            <li>
              <a
                href="https://www.mdpi.com/1420-3049/29/22/5468"
                target="_blank"
                rel="noopener noreferrer"
              >
                Development of an Electrochemical Paper-Based Device Modified
                with Functionalized Biochar for the Screening of Paracetamol in
                Substandard Medicines
              </a>{" "}
              - Publicado em 2024.
            </li>
            <li>
              <a
                href="https://www.mdpi.com/2075-1729/14/10/1256"
                target="_blank"
                rel="noopener noreferrer"
              >
                Deep Learning Method Applied to Autonomous Image Diagnosis for
                Prick Test{" "}
              </a>{" "}
              - Publicado em 2024.
            </li>
            <li>
              Demais artigos:{" "}
              <a href="https://scholar.google.com/citations?view_op=list_works&hl=pt-BR&hl=pt-BR&user=JowjbtgAAAAJ&sortby=pubdate">
                {" "}
                Google Scholar{" "}
              </a>
            </li>
          </ul>
        </section>

        {/* Contato/Convite */}
        <section id="contato" className="mb-5">
          <h2 className="h4 mb-3">Contato e Parcerias</h2>
          <p>
            Se você trabalha em projetos em uma das áreas abaixo e gostaria de
            colaborar conosco, entre em contato para informações adicionais pelo
            email: rafael.simoes@unesp.br
          </p>
          <table className="linhas">
            <tbody>
              <tr scope="col" style={{ height: "20px" }}>
                <td>
                  <img src="./biotec1.png" />
                </td>
                <td>
                  <img src="./biotec2.png" />
                </td>
                <td>
                  <img src="./biotec3.png" />
                </td>
                <td>
                  <img src="./biotec4.png" />
                </td>
                <td>
                  <img src="./biotec5.png" />
                </td>{" "}
                <td>
                  <img src="./biotec6.png" />
                </td>
              </tr>
              <tr>
                <td>Alimentos</td>
                <td>Saúde</td>
                <td>Agricultura</td>
                <td>Indústria</td>
                <td>Ambiente</td>
                <td>Computacional</td>
              </tr>
            </tbody>
          </table>
        </section>
      </main>
      <footer
        style={{ backgroundColor: "darkgray" }}
        className="text-white text-center py-3 "
      >
        <p className="footer1">
          © {new Date().getFullYear()} - Dr. Rafael Plana Simões - Todos os
          direitos reservados.
        </p>
        <p className="small m-0">
          Este site é uma iniciativa independente e não reflete as opiniões ou
          posicionamentos institucionais da UNESP. <br />
          {/* <span className="motiva">
            Construído por &nbsp;
            <a
              href="https://www.motivaservicos.com.br"
              target="_blank"
              rel="noopener noreferrer"
            >
              Motiva Serviços ME.
            </a>
          </span> */}
        </p>
      </footer>
    </div>
  );
};

export default Home;
