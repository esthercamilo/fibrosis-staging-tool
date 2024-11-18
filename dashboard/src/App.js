import React from "react";
import { BrowserRouter as Router, Route } from "react-router-dom";
import withTracker from "./withTracker";
import "bootstrap/dist/css/bootstrap.min.css";
import PredictionForm from "./components/Form";

const routes = [
  {
    path: "/",
    exact: true,
    component: PredictionForm, // O componente de formulário será renderizado na rota inicial
    layout: React.Fragment // Usando o layout padrão, ou ajuste conforme necessário
  }
  // Outras rotas podem ser adicionadas aqui, como suas rotas de "about", "contact", etc.
  // {
  //   path: '/outro',
  //   exact: true,
  //   component: OutroComponente,  // Ajuste para os outros componentes da sua aplicação
  //   layout: LayoutOutro,  // Ajuste para o layout que você deseja para essa página
  // },
];

function App() {
  return (
    <Router basename={process.env.REACT_APP_BASENAME || ""}>
      <div>
        {routes.map((route, index) => {
          return (
            <Route
              key={index}
              path={route.path}
              exact={route.exact}
              render={props => (
                <route.layout {...props}>
                  <route.component {...props} />
                </route.layout>
              )}
            />
          );
        })}
      </div>
    </Router>
  );
}

export default App;
