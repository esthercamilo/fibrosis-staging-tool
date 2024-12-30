import os
import numpy as np
import joblib
import pandas

from api.analysis.pipeline import Analysis


class Predict:
    def __init__(self, root=None):
        if root:
            self.root = root
        else:
            self.root = os.path.abspath('..')

    def lda_load(self, df):
        # fulldata set
        results_folder = os.path.join(self.root, 'api', 'analysis', 'results')
        lda_datasets = [x for x in os.listdir(results_folder) if 'lda_model' in x]

        for lda_d in lda_datasets:
            combo = lda_d.split('__')[-1].replace('.pkl', '')
            X = df[[combo]]
            modelpath = os.path.join(self.root, 'api', 'analysis', 'results', lda_d)
            lda_loaded = joblib.load(modelpath)
            print(lda_loaded.feature_names_in_)
            prediction = lda_loaded.predict(X)
            df[combo] = prediction
        return df

    def calculate(self, df):

        df['FIB4'] = (df['AGE'] * df['ALT']) / (df['PL'] * np.sqrt(df['AST']))

        # list_sorted = Analysis().fields_order()

        result = {
            'FIB4': (df['AGE'] * df['ALT']) / (df['PL'] * np.sqrt(df['AST'])),
            'AGE2': df['AGE'] ** 2,
            'AGEsqrt': np.sqrt(df['AGE']),
            'AST': df['AST'] ** 2,
            'ASTsqrt': np.sqrt(df['AST']),
            'ALT2': df['ALT'] ** 2,
            'ALTsqrt': np.sqrt(df['ALT']),
            'PL2': df['PL'] ** 2,
            'PLsqrt': np.sqrt(df['PL']),
            'FIB42': df['FIB4'] ** 2,
            'FIB4sqrt': np.sqrt(df['FIB4']),
            'AST/ALT': df['AST'] / df['ALT'],
            'AST/AGE': df['AST'] / df['AGE'],
            'ALT/AGE': df['ALT'] / df['AGE'],
            'PL/AGE': df['PL'] / df['AGE'],
            'PL*ALT': df['PL'] * df['ALT'],
            'PL*AGE': df['PL'] * df['AGE'],
            'PL*AST': df['PL'] * df['AST'],
            'ALT*AST': df['ALT'] * df['AST'],
            'ALT*AGE': df['ALT'] * df['AGE'],
            'AGE*AST': df['AGE'] * df['AST'],
            'PL-1': 1 / df['PL'],
            'ALT^2': 1 / (df['ALT'] ** 2)
        }
        result.update(df)
        # sorted_result = {k: [v] for k, v in dict(zip(list_sorted, [result[x] for x in list_sorted])).items()}
        partial_df = pandas.DataFrame({k: [v] for k, v in result.items()})
        # LDA data
        full_df = self.lda_load(partial_df)
        return full_df

    def run(self, data: dict):

        modelpath = os.path.join(self.root, 'api', 'analysis', 'results', 'model1_global.pkl')
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
    d = {'AGE': 40.0, 'ALT': 1.0, 'AST': 1.0, 'PL': 1.0}
    Predict().run(d)
