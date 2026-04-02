import os
import numpy as np
import joblib
import pandas
from sklearn.tree import export_text

from core.settings import BASE_DIR


def getnames(value):
    dict_names = {'AGE_AST_FIB4_AGEsqrt_ASTsqrt_ALTsqrt': 'LDA1', 'AGE_AST_FIB4_ASTsqrt_ALTsqrt': 'LDA2',
                  'AGE_AST_FIB4_ASTsqrt_ALT2_ALTsqrt': 'LDA3'}
    return dict_names.get(value, value)


def define_class(values):
    if values[0][0] > values[0][1]:
        return 'G1'
    else:
        return 'G2'


def replace_names(value):
    if value.count('_') > 2:
        return value

    if 'sqrt' in value:
        return f"\u221A{value}".replace('sqrt', '')
    if '-1' in value:
        return f"1/{value}".replace('-1', '')
    if '-2' in value:
        return f"1/{value}^2".replace('-2', '')
    if '--' in value:
        return value.replace('--', '/')
    else:
        return value


class Predict:
    def __init__(self, root=None):
        if root:
            self.root = root
        else:
            self.root = os.path.abspath('..')

    def lda_load(self, df):
        # fulldata set
        results_folder = os.path.join(self.root, 'api', 'analysis', 'including_lda', 'results')
        lda_datasets = [x for x in os.listdir(results_folder) if 'lda_model' in x]

        for lda_d in lda_datasets:
            combo = lda_d.split('__')[-1].replace('.pkl', '')
            X = df[combo.split('_')]
            modelpath = os.path.join(self.root, 'api', 'analysis', 'including_lda', 'results', lda_d)
            lda_loaded = joblib.load(modelpath)
            score = lda_loaded.transform(X)
            df[combo] = score
        return df

    @staticmethod
    def define_highligts(tree, feature_names, feature_values):

        def recurse(node_id, fv, path):
            # Inicializa o nó
            current_path = path[:]

            # Verifica se é um nó interno
            if tree.feature[node_id] != -2:  # Nó interno
                feature = feature_names[tree.feature[node_id]]
                threshold = tree.threshold[node_id]

                current_path.append(f"Node {node_id}")

                # Se a condição for atendida, percorre o filho esquerdo, senão o direito
                actual_value = fv[feature].iloc[0]
                if actual_value <= threshold:
                    return recurse(tree.children_left[node_id], fv, current_path)
                else:
                    return recurse(tree.children_right[node_id], fv, current_path)

            else:  # Nó folha
                # Adiciona a classe do nó folha
                current_path.append(f"Node {int(node_id)}")
                # current_path.append(define_class(tree.value[node_id].tolist()))
                return current_path

        return recurse(0, feature_values, [])

    @staticmethod
    def trenodes(tree):
        node_names = []

        def traverse(node):
            node_names.append(node['name'])
            if 'children' in node:
                for child in node['children']:
                    traverse(child)

        traverse(tree)
        return node_names

    def tree_to_dict(self, tree, feature_names, feature_values, twin_nodes):

        def recurse(node_id, fv, tn):
            # Inicializa o nó
            node = {"name": f"Node {node_id}"}

            # Verifica se é um nó interno
            if tree.feature[node_id] != -2:  # Nó interno
                feature = feature_names[tree.feature[node_id]]
                threshold = tree.threshold[node_id]

                # Adiciona a condição do nó
                if threshold > 10:
                    th = f"{threshold:.0f}"
                elif 10 >= threshold > 0:
                    th = f"{threshold:.1f}"
                else:
                    th = f"{threshold:.2f}"

                node["condition"] = f"{getnames(feature)} <= {th}"
                node['title'] = replace_names(feature)

                left_child = recurse(tree.children_left[node_id], fv, tn)
                right_child = recurse(tree.children_right[node_id], fv, tn)

                if left_child["condition"] == right_child["condition"]:
                    tn.append((left_child['name'], right_child['name']))
                    return right_child  # Mantém apenas um deles

                # Adiciona os filhos esquerdo e direito
                node["children"] = [left_child, right_child]

            else:  # Nó folha
                # Adiciona os valores no nó folha
                node["condition"] = define_class(tree.value[node_id].tolist())

            return node

        return recurse(0, feature_values, twin_nodes)

    @staticmethod
    def fib4(df):
        return (df['AGE'] * df['ALT']) / (df['PL'] * np.sqrt(df['AST']))

    def calculate(self, df, lda=False):

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
        df = pandas.DataFrame({k: [v] for k, v in result.items()})
        if lda:
            # LDA data
            df = self.lda_load(df)
        return df

    def run(self, data: dict, modelname: str, lda=False):

        root_model_path = os.path.join(self.root, 'api', 'analysis', 'without_lda', 'results')
        if lda:
            root_model_path = os.path.join(self.root, 'api', 'analysis', 'including_lda', 'results')

        modelpath = os.path.join(root_model_path, f'model1_{modelname}.pkl')

        model = joblib.load(modelpath)

        # Porém o usuário só entra com AGE,AST,ALT,PL. Todos os outros são calculados internamente
        inputs = self.calculate(data, lda)
        fib4 = self.fib4(data)
        feature_names = list(model.feature_names_in_)
        inputs = inputs[feature_names]

        feature_names_ = model.feature_names_in_ if hasattr(model, 'feature_names_in_') \
            else [f'feature_{i}' for i in range(model.tree_.n_features)]

        twins = []
        tree_dict = self.tree_to_dict(model.tree_, feature_names_, inputs, twins)
        nodes_in_tree = self.trenodes(tree_dict)
        pathway = self.define_highligts(model.tree_, feature_names_, inputs)
        # Redefine pathway:
        # pathway = []
        # for p in pathway_:
        #     if p not in nodes_in_tree:
        #         # Substituir pelo twin
        #         pair = [(i, x) for i, x in enumerate(twins) if p in x]
        #         chosen_twin = ''



        features = np.array(inputs).reshape(1, -1)

        # Fazer a previsão
        prediction = model.predict(features)

        if prediction[0] == 'G1':
            probG = round(float(model.predict_proba(features)[0][0]), 2) * 100
        else:
            probG = round(float(model.predict_proba(features)[0][1]), 2) * 100

        try:
            with open(os.path.join(root_model_path, f'features_{modelname}.csv'), 'r') as f:
                coef = f.read()
        except Exception as e:
            coef = 'Disponível somente para cálculos com LDA'

        data = {'prediction': prediction[0],
                'confidence': round(probG, 2),
                'd3tree': tree_dict,
                'values': [{"field": replace_names(k), "value": v[0]} for k, v in
                           inputs.to_dict(orient='dict').items()],
                'fib4': float(round(fib4, 2)),
                'highlights': pathway,
                'coeficientes': coef}
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
