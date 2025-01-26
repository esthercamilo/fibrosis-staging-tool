import os
import numpy as np
import joblib
import pandas

from api.analysis.pipeline import Analysis


def manual_decision_tree(df):
    path = ["PL2"]
    i = {k: v[0] for k, v in df.to_dict(orient='dict').items()}
    if i['PL2'] <= 16002.5:
        path.append('AGE_AST_FIB4_ASTsqrt_ALT2_ALTsqrt')
        if i['AGE_AST_FIB4_ASTsqrt_ALT2_ALTsqrt'] <= -0.946:
            path.append('G1a')
        else:
            path.append('ALT*AST')
            if i['ALT*AST'] <= 11368:
                path.append('FIB4sqrt')
                if i['FIB4sqrt'] <= 1.418:
                    path.append('G1a')
                else:
                    path.append('G2a')
            else:
                path.append('G2b')
    else:
        path.append('AGE_AST_FIB4_ASTsqrt_ALTsqrt')
        if i['AGE_AST_FIB4_ASTsqrt_ALTsqrt'] <= -0.636:
            path.append('PL')
            if i['PL'] <= 166.5:
                path.append('AGE_AST_FIB4_ASTsqrt_ALTsqrt')
                if i['AGE_AST_FIB4_ASTsqrt_ALTsqrt'] <= -1.121:
                    path.append('G1b')
                else:
                    path.append('G2b')
            else:
                path.append('FIB42')
                if i['FIB42'] <= 10.235:
                    path.append('G1c')
                else:
                    path.append('G2c')
        else:
            path.append('AST/AGE')
            if i['AST/AGE'] <= 13.347:
                path.append('AGE_AST_FIB4_ASTsqrt_ALTsqrt')
                path.append('G1d')

            else:
                path.append('AGE2')
                if i['AGE2'] <= 2862.5:
                    path.append('G1d')
                else:
                    path.append('G2d')
    return path


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
            X = df[combo.split('_')]
            modelpath = os.path.join(self.root, 'api', 'analysis', 'results', lda_d)
            lda_loaded = joblib.load(modelpath)
            score = lda_loaded.transform(X)
            df[combo] = score
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

        # Porém o usuário só entra com AGE,AST,ALT,PL. Todos os outros são calculados internamente
        inputs = self.calculate(data)
        feature_names = list(model.feature_names_in_)
        inputs = inputs[feature_names]

        mdt = manual_decision_tree(inputs)

        features = np.array(inputs).reshape(1, -1)

        # Fazer a previsão
        prediction = model.predict(features)

        if prediction[0] == 'G1':
            probG = round(float(model.predict_proba(features)[0][0]), 2) * 100
        else:
            probG = round(float(model.predict_proba(features)[0][1]), 2) * 100

        return {'prediction': prediction[0], 'confidence': probG, 'manual_tree': mdt}


if __name__ == '__main__':
    with open('/home/esther/GitProjects/fibrosis-staging-tool/api/analysis/data/00_data_hcv_n74_proprio.csv', 'r') as f:
        f.readline()
        acertos = 0
        erros = 0
        for line in f:
            d = line.rstrip('\n').split('\t')
            classe = d[-1]
            pred = Predict().run({'AGE': float(d[0]), 'ALT': float(d[1]), 'AST': float(d[2]), 'PL': float(d[3])})
            print(f"{classe}    {pred}")
            if classe == pred['prediction']:
                acertos += 1
            else:
                erros += 1
        print(f"Acertos: {acertos}")
        print(f"Erros: {erros}")
