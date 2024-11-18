import os
import numpy as np
import joblib


class Predict:
    def __init__(self, root=None):
        if root:
            self.root = root
        else:
            self.root = os.path.abspath('..')

    def calculate(self, data):
        self
        return [65, 289.0, 20.0, 82.0, 3.01, 4225, 8.06, 17.0, 400.0, 4.472, 6724.0, 9.05, 9.06, 1.734,
                False, False, False, True, False]

    def run(self, data: dict):

        modelpath = os.path.join(self.root, 'api', 'analysis', 'results', 'model1.pkl')
        model = joblib.load(modelpath)

        # Ordem dos dos inputs
        # AGE,AST,ALT,PL,FIB4,AGE2,AGEsqrt,ASTsqrt,ALT2,ALTsqrt,PL2,PLsqrt,FIB42,FIB4sqrt,DSE_FAT_N603,DSE_HBV_N177,
        # DSE_HBV_N568,DSE_HCV_N230,DSE_HCV_N74

        # Porém o usuário só entra com AGE,AST,ALT,PL. Todos os outros são calculados internamente
        inputs = self.calculate(data)

        # Extrair os valores dos inputs (ajuste conforme necessário)
        features = np.array(inputs).reshape(1, -1)

        # Fazer a previsão
        dict_groups = {1: 'G1', 2: 'G2'}
        prediction = model.predict(features)

        # Obter as probabilidades das classes (isso dá uma métrica de confiança)
        probabilities = model.predict_proba(features)

        # A maior probabilidade é a confiança na classe predita
        confidence = float(probabilities[0][prediction[0]])

        return {'prediction': dict_groups[prediction.tolist()[0]], 'confidence': confidence}


if __name__ == '__main__':
    Predict().run()

