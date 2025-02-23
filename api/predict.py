import os
import numpy as np
import joblib
import pandas
from sklearn.tree import export_text


def getnames(value):
    dict_names = {'AGE_AST_FIB4_AGEsqrt_ASTsqrt_ALTsqrt': 'LDA1', 'AGE_AST_FIB4_ASTsqrt_ALTsqrt': 'LDA2',
                  'AGE_AST_FIB4_ASTsqrt_ALT2_ALTsqrt': 'LDA3'}
    return dict_names.get(value, value)


def define_class(values):
    if values[0][0] > values[0][1]:
        return 'G1'
    else:
        return 'G2'


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

    @staticmethod
    def define_highligts(tree, feature_names, feature_values, pathway):

        def recurse(node_id, fv):
            # Inicializa o nó
            node = {"name": f"Node {node_id}"}
            pathway.append(f"Node {node_id}")
            # Verifica se é um nó interno
            if tree.feature[node_id] != -2:  # Nó interno
                feature = feature_names[tree.feature[node_id]]
                threshold = tree.threshold[node_id]

                # Adiciona a condição do nó
                node["condition"] = f"{getnames(feature)} <= {threshold:.3f}"

                actual_value = fv[feature].iloc[0]
                if actual_value <= threshold:
                    # Adiciona os filhos esquerdo e direito
                    node["children"] = [
                        recurse(tree.children_left[node_id], fv)
                    ]
                else:
                    node["children"] = [
                        recurse(tree.children_right[node_id], fv)
                    ]
            else:  # Nó folha
                # Adiciona os valores no nó folha
                node["condition"] = define_class(tree.value[node_id].tolist())
                pathway.append(f"Node {node_id}")
            return node

        return recurse(0, feature_values)

    @staticmethod
    def tree_to_dict(tree, feature_names, feature_values):

        def recurse(node_id, fv):
            # Inicializa o nó
            node = {"name": f"Node {node_id}"}

            # Verifica se é um nó interno
            if tree.feature[node_id] != -2:  # Nó interno
                feature = feature_names[tree.feature[node_id]]
                threshold = tree.threshold[node_id]

                # Adiciona a condição do nó
                node["condition"] = f"{getnames(feature)} <= {threshold:.3f}"
                node['title'] = feature

                # Adiciona os filhos esquerdo e direito
                node["children"] = [
                    recurse(tree.children_left[node_id], fv),
                    recurse(tree.children_right[node_id], fv)
                ]
            else:  # Nó folha
                # Adiciona os valores no nó folha
                node["condition"] = define_class(tree.value[node_id].tolist())

            return node

        return recurse(0, feature_values)

    @staticmethod
    def fib4(df):
        return (df['AGE'] * df['ALT']) / (df['PL'] * np.sqrt(df['AST']))

    def calculate(self, df):

        df['FIB4'] = self.fib4(df)

        result = {
            'FIB4': self.fib4,
            'AGE2': df['AGE'] ** 2,
            'AGEsqrt': np.sqrt(df['AGE']),
            'AST2': df['AST'] ** 2,
            'ASTsqrt': np.sqrt(df['AST']),
            'ALT2': df['ALT'] ** 2,
            'ALTsqrt': np.sqrt(df['ALT']),
            'PL2': df['PL'] ** 2,
            'PLsqrt': np.sqrt(df['PL']),
            'FIB42': df['FIB4'] ** 2,
            'FIB4sqrt': np.sqrt(df['FIB4']),
            'AST--ALT': df['AST'] / df['ALT'],
            'AST--AGE': df['AST'] / df['AGE'],
            'ALT--AGE': df['ALT'] / df['AGE'],
            'PL--AGE': df['PL'] / df['AGE'],
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
        fib4 = self.fib4(data)
        feature_names = list(model.feature_names_in_)
        inputs = inputs[feature_names]

        feature_names_ = model.feature_names_in_ if hasattr(model, 'feature_names_in_') else [f'feature_{i}' for i in
                                                                                              range(
                                                                                                  model.tree_.n_features)]

        pathway = []
        tree_dict = self.tree_to_dict(model.tree_, feature_names_, inputs)
        self.define_highligts(model.tree_, feature_names_, inputs, pathway)

        features = np.array(inputs).reshape(1, -1)

        # Fazer a previsão
        prediction = model.predict(features)

        if prediction[0] == 'G1':
            probG = round(float(model.predict_proba(features)[0][0]), 2) * 100
        else:
            probG = round(float(model.predict_proba(features)[0][1]), 2) * 100

        data = {'prediction': prediction[0], 'confidence': probG, 'd3tree': tree_dict,
                'values': [{"field": k, "value": v[0]} for k, v in inputs.to_dict(orient='dict').items()],
                'fib4': float(round(fib4, 2)), 'highlights': pathway}
        print(data)
        return data


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
