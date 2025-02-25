import os.path
import os.path
import shutil
from itertools import combinations
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from imblearn.under_sampling import RandomUnderSampler
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.metrics import auc
from sklearn.metrics import (
    roc_auc_score,
    roc_curve,
    precision_score,
    recall_score,
    accuracy_score,
    f1_score,
    make_scorer
)
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import ExtraTreeClassifier, plot_tree
from joblib import dump


class Analysis:
    def __init__(self, root=None):
        self.le = LabelEncoder()
        if root:
            self.root = root
        else:
            self.root = os.path.abspath('../..')
        self.results = os.path.join(self.root, 'api', 'analysis', 'results')
        self.temp_results = os.path.join(self.root, 'api', 'analysis', 'results_temp')
        self.plots = os.path.join(self.root, 'api', 'analysis', 'plots')
        os.makedirs(self.results, exist_ok=True)
        os.makedirs(self.temp_results, exist_ok=True)
        os.makedirs(self.plots, exist_ok=True)

    def read(self, f):
        root_path = self.root
        datapath = os.path.join(root_path, 'api', 'analysis', 'data')
        df = pd.read_csv(os.path.join(datapath, f), sep='\t')
        return df

    @staticmethod
    def generate_combinations(features, min_size=2, max_size=5):
        for i in range(min_size, min(max_size, len(features)) + 1):
            yield from combinations(features, i)

    def lda(self, df, name):
        """Discriminant function (DF) definition"""

        y = df['GROUP']

        plt.figure(figsize=(10, 8))

        # Todas as combinações possíveis
        exclude = ['GROUP', 'DSE']
        features = [x for x in df.columns if x not in exclude]

        results = []

        f = open(os.path.join(self.root, 'api', 'analysis', 'results', f'features_{name}.csv'), 'w')

        for combo in self.generate_combinations(features):

            if len(combo) > 6 or len(combo) <= 1:
                continue
            f.write(str(combo) + '\n')
            undersampler = RandomUnderSampler(random_state=42)
            X = df[list(combo)]

            X_resampled, y_resampled = undersampler.fit_resample(X, y)
            # Dividindo os dados em treino e teste
            X_train, X_test, y_train, y_test = train_test_split(X_resampled, y_resampled, test_size=0.2,
                                                                random_state=42)
            # LDA
            lda = LinearDiscriminantAnalysis()
            lda.fit(X_train, y_train)

            str_features = '_'.join(combo)
            modelpath = os.path.join(self.temp_results, f'lda_model_{name}__{str_features}.pkl')
            dump(lda, modelpath)

            y_prob = lda.predict_proba(X_test)[:, 1]

            # Curva ROC
            fpr, tpr, _ = roc_curve(y_test, y_prob, pos_label='G2')
            roc_auc = auc(fpr, tpr)
            scores = lda.transform(X)
            colname = '_'.join(combo)

            # Results só guarda os 5 maiores resultado, senão ficaria muito cheio
            if len(results) < 5:
                results.append([fpr, tpr, combo, roc_auc, colname, scores])
            else:
                # Se esse desempenho for maior que o menor, remover o menor e inserir esse
                lowest = sorted(results, key=lambda k: k[3])[0: 11]
                if roc_auc > lowest[0][3]:
                    results = lowest[1:] + [[fpr, tpr, combo, roc_auc, colname, scores]]

        # Imprime somente as 10 com melhores resultados
        sorted_result = sorted(results, key=lambda k: -k[3])[0: 6]
        # Plot
        for sr in sorted_result:
            plt.plot(sr[0], sr[1], label=f"{sr[2]} (AUC = {sr[3]:.2f})")
            df[sr[4]] = sr[5]
            # Copy fulldata to folder results
            source_file = os.path.join(self.root, 'api', 'analysis', 'results_temp', f'lda_model_{name}__{sr[4]}.pkl')
            target_file = os.path.join(self.root, 'api', 'analysis', 'results', f'lda_model_{name}__{sr[4]}.pkl')
            shutil.move(source_file, target_file)
        f.close()

        fulldata_lda = os.path.join(self.root, 'api', 'analysis', 'results', f'lda_traingdata_{name}.csv')
        df.to_csv(fulldata_lda)

        # Plot da curva ROC
        plt.plot([0, 1], [0, 1], 'k--', label="Random")
        plt.xlabel("FPR")
        plt.ylabel("TPR")
        plt.title("ROC curves of LDA for different combinations")
        plt.legend()
        plt.savefig(os.path.join(self.root, 'api', 'analysis', 'plots', f'lda_{name}.png'))

        return df

    @staticmethod
    def attributes(df):
        # 1
        df['FIB4'] = (df['AGE'] * df['ALT']) / (df['PL'] * np.sqrt(df['AST']))
        # 2
        df['AGE2'] = df['AGE'] ** 2
        # 3
        df['AGEsqrt'] = np.sqrt(df['AGE'])
        # 4
        df['AST2'] = df['AST'] ** 2
        # 5
        df['ASTsqrt'] = np.sqrt(df['AST'])
        # 6
        df['ALT2'] = df['ALT'] ** 2
        # 7
        df['ALTsqrt'] = np.sqrt(df['ALT'])
        # 8
        df['PL2'] = df['PL'] ** 2
        # 9
        df['PLsqrt'] = np.sqrt(df['PL'])
        # 10
        df['FIB42'] = df['FIB4'] ** 2
        # 11
        df['FIB4sqrt'] = np.sqrt(df['FIB4'])
        # 12
        df['AST--ALT'] = df['AST'] / df['ALT']
        # 13
        df['AST--AGE'] = df['AST'] / df['AGE']
        # 14
        df['ALT--AGE'] = df['ALT'] / df['AGE']
        # 15
        df['PL--AGE'] = df['PL'] / df['AGE']
        # 16
        df['PL*ALT'] = df['PL'] * df['ALT']
        # 17
        df['PL*AGE'] = df['PL'] * df['AGE']
        # 18
        df['PL*AST'] = df['PL'] * df['AST']
        # 19
        df['ALT*AST'] = df['ALT'] * df['AST']
        # 20
        df['ALT*AGE'] = df['ALT'] * df['AGE']
        # 21
        df['AGE*AST'] = df['AGE'] * df['AST']
        # 22
        df['PL-1'] = 1 / df['PL']
        # 23
        df['ALT^2'] = 1 / (df['ALT'] ** 2)

        return df

    def decision_tree(self, df, name):
        # Dividindo em variáveis independentes (X) e dependente (y)
        X = df.drop(['GROUP', 'DSE'], axis=1, errors='ignore')
        y = df['GROUP']

        # Balanceamento dos dados
        undersampler = RandomUnderSampler(random_state=42)
        X_resampled, y_resampled = undersampler.fit_resample(X, y)

        # Dividindo os dados em treino e teste
        X_train, X_test, y_train, y_test = train_test_split(
            X_resampled, y_resampled, test_size=0.2, random_state=42
        )

        base_model = ExtraTreeClassifier(random_state=42)

        param_grid = {
            'max_depth': [2, 3, 4, None],
            'min_samples_split': [2, 5, 10],
            'min_samples_leaf': [2, 4],
            'criterion': ['gini', 'entropy'],
            'splitter': ['best', 'random'],
            'max_features': [None, 'sqrt', 'log2'],
            'class_weight': [None, 'balanced'],
            'min_impurity_decrease': [0.0, 0.01, 0.1],
            'ccp_alpha': [0.0, 0.01, 0.1],
        }

        scoring = make_scorer(roc_auc_score, needs_proba=True)
        grid_search = GridSearchCV(
            estimator=base_model,
            param_grid=param_grid,
            scoring=scoring,
            cv=5,  # Validação cruzada com 5 divisões
            verbose=1,
            n_jobs=-1  # Usa todos os núcleos disponíveis
        )

        grid_search.fit(X_train, y_train)

        best_model = grid_search.best_estimator_
        modelpath = os.path.join(self.root, 'api', 'analysis', 'results', f'model1_{name}.pkl')
        dump(best_model, modelpath)

        y_pred = best_model.predict(X_test)
        y_pred_proba = best_model.predict_proba(X_test)[:, 1]

        # Métricas de avaliação

        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred, pos_label='G2')
        recall = recall_score(y_test, y_pred, pos_label='G2')
        f1 = f1_score(y_test, y_pred, pos_label='G2')
        roc_auc = roc_auc_score(y_test, y_pred_proba)

        report_path = os.path.join(self.root, 'api', 'analysis', 'results', f'tree_{name}.csv')
        with open(report_path, 'w') as f:
            f.write(f"Accuracy: {accuracy}\n")
            f.write(f"Precision: {precision}\n")
            f.write(f"Recall:{recall}\n")
            f.write(f"F1 Score: {f1}\n")
            f.write(f"Area under the curve (AUC): {roc_auc}\n")

        # Curva ROC
        fpr, tpr, thresholds = roc_curve(y_test, y_pred_proba, pos_label='G2')

        plt.figure(figsize=(10, 6))
        plt.plot(fpr, tpr, color='blue', lw=2, label=f'ROC Curve (AUC = {roc_auc:.2f})')
        plt.plot([0, 1], [0, 1], color='gray', linestyle='--', label='Random Guess')
        plt.xlabel('False positive rate (FPR)')
        plt.ylabel('True positive rate (TPR)')
        plt.title('ROC Curve')
        plt.legend(loc='lower right')
        plt.grid()
        roc_path = os.path.join(self.root, 'api', 'analysis', 'plots', f'tree_roc_{name}.png')
        plt.savefig(roc_path)

        # Plotando a árvore de decisão do melhor modelo
        plt.figure(figsize=(20, 12))
        plot_tree(
            best_model,
            filled=True,
            feature_names=X.columns,
            class_names=['Classe 0', 'Classe 1']  # Ajuste conforme suas classes
        )
        plt.title("Árvore de Decisão")
        tree_path = os.path.join(self.root, 'api', 'analysis', 'plots', f'tree_{name}.png')
        plt.tight_layout()
        plt.savefig(tree_path, dpi=300)
        print(f"Árvore de decisão salva em {tree_path}")

    def individual_model(self, df, name):
        df = df.drop('FIB4', axis=1, errors="ignore")
        df = self.attributes(df)
        # df = self.lda(df, name)
        df.to_csv(os.path.join(self.root, 'api', 'analysis', 'results', f'fulldata_{name}.csv'), index=False)
        self.decision_tree(df, name)
        return df

    def run(self):

        # 1. model fat
        print('iniciando FAT')
        df_fat_read = self.read('00_data_fat_n603.csv')
        df_fat = self.individual_model(df_fat_read, 'fat')

        # 2. model hbv
        print('iniciando HBV')
        df_hbv1 = self.read('00_data_hbv_n177.csv')
        df_hbv2 = self.read('00_data_hbv_n568.csv')
        df_hbv_read = pd.concat([df_hbv1, df_hbv2])
        df_hbv = self.individual_model(df_hbv_read, 'hbv')

        # 3. model hcv
        print('iniciando HCV')
        df_hcv1 = self.read('00_data_hcv_n73_proprio.csv')
        df_hcv2 = self.read('00_data_hcv_n230.csv')
        df_hcv_read = pd.concat([df_hcv1, df_hcv2])
        df_hcv = self.individual_model(df_hcv_read, 'hcv')

        # 4. model hbv + hcv
        print('iniciando HBV + HCV')
        df_hbv_read['DSE'] = 2
        df_hcv_read['DSE'] = 3
        df_hbc_read = pd.concat([df_hbv_read, df_hcv_read])
        df_hbcv = self.individual_model(df_hbc_read, 'hbcv')

        # Global
        print('iniciando Global')
        df_fat_read['DSE'] = 1
        df_hbv_read['DSE'] = 2
        df_hcv_read['DSE'] = 3
        df_global = pd.concat([df_fat_read, df_hbv_read, df_hcv_read])
        df_global = self.individual_model(df_global, 'global')

        try:
            shutil.rmtree(self.temp_results, ignore_errors=True)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    Analysis().run()
