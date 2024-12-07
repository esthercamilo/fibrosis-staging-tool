import os.path
import os.path
from itertools import combinations

# from sklearn.ensemble import RandomForestClassifier
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from imblearn.under_sampling import RandomUnderSampler
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import auc
from sklearn.metrics import (
    classification_report,
    roc_auc_score,
    roc_curve,
    precision_score,
    recall_score,
    accuracy_score,
    f1_score
)
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import PolynomialFeatures
from sklearn.tree import ExtraTreeClassifier, plot_tree
from joblib import dump, load


class Analysis:
    def __init__(self, root=None):
        self.le = LabelEncoder()
        if root:
            self.root = root
        else:
            self.root = os.path.abspath('../..')

    def read(self, f):
        root_path = self.root
        datapath = os.path.join(root_path, 'api', 'analysis', 'data')
        df = pd.read_csv(os.path.join(datapath, f), sep='\t')
        return df

    def description(self, df):
        path_plots = os.path.join(self.root, 'api', 'analysis', 'plots')
        path_results = os.path.join(self.root, 'api', 'analysis', 'results')

        sets = ['AGE', 'AST', 'ALT', 'PL']

        # Remove integer columns for description
        df = df.drop(['iGROUP', 'iDSE'], axis=1)

        for s in sets:
            sns.boxplot(data=df, x='GROUP', y=s, hue='DSE')  # Adiciona a variável 'DSE'
            plt.title(f'{s} distribution by Group and Condition')
            plt.legend(title='Condition')
            plt.savefig(os.path.join(path_plots, f'{s}_by_group_and_dse.png'))
            plt.close()  # Fecha o plot para evitar sobreposição em chamadas subsequentes

        # Plot Group and Condition
        tabela_contagem = df.groupby(['GROUP', 'DSE']).size().reset_index(name='COUNT')
        tabela_contagem.to_csv(os.path.join(path_results, 'count_table.csv'))
        plt.figure(figsize=(8, 6))
        sns.barplot(data=tabela_contagem, x='GROUP', y='COUNT', hue='DSE')
        plt.title('Count instances by GROUP and DSE')
        plt.ylabel('Instance number')
        plt.xlabel('GROUP')
        plt.legend(title='DSE')
        plt.tight_layout()
        path_plots = os.path.join(self.root, 'api', 'analysis', 'plots')
        plt.savefig(os.path.join(path_plots, 'count_by_group_and_dse.png'))

        # Plot Group only
        tabela_contagem = df.groupby(['GROUP']).size().reset_index(name='COUNT')
        tabela_contagem.to_csv(os.path.join(path_results, 'count_group_table.csv'))
        plt.figure(figsize=(8, 6))
        sns.barplot(data=tabela_contagem, x='GROUP', y='COUNT')
        plt.title('Count instances by GROUP')
        plt.ylabel('Instance number')
        plt.xlabel('GROUP')
        plt.tight_layout()
        path_plots = os.path.join(self.root, 'api', 'analysis', 'plots')
        plt.savefig(os.path.join(path_plots, 'count_by_group.png'))

        # Plot Condition only
        tabela_contagem = df.groupby(['DSE']).size().reset_index(name='COUNT')
        tabela_contagem.to_csv(os.path.join(path_results, 'count_group_table.csv'))
        plt.figure(figsize=(8, 6))
        sns.barplot(data=tabela_contagem, x='DSE', y='COUNT')
        plt.title('Count instances by Condition')
        plt.ylabel('Instance number')
        plt.xlabel('Condition')
        plt.tight_layout()
        path_plots = os.path.join(self.root, 'api', 'analysis', 'plots')
        plt.savefig(os.path.join(path_plots, 'count_by_condition.png'))

    def lda(self, df, name):
        """Discriminant function (DF) definition"""
        y = df['iGROUP']

        plt.figure(figsize=(10, 8))

        # Todas as combinações possíveis
        exclude = ['GROUP', 'DSE', 'iGROUP']
        features = [x for x in df.columns if x not in exclude][0:10]
        combinations_features = sum([list(combinations(features, i)) for i in range(1, len(features) + 1)], [])

        results = []

        for combo in combinations_features:

            if 1 < len(combo) < 6:
                continue
            undersampler = RandomUnderSampler(random_state=42)
            X = df[list(combo)]

            X_resampled, y_resampled = undersampler.fit_resample(X, y)
            # Dividindo os dados em treino e teste
            X_train, X_test, y_train, y_test = train_test_split(X_resampled, y_resampled, test_size=0.3,
                                                                random_state=42)
            # LDA
            lda = LinearDiscriminantAnalysis()
            lda.fit(X_train, y_train)
            y_prob = lda.predict_proba(X_test)[:, 1]

            # Curva ROC
            fpr, tpr, _ = roc_curve(y_test, y_prob)
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

        # Plot da curva ROC
        plt.plot([0, 1], [0, 1], 'k--', label="Random")
        plt.xlabel("FPR")
        plt.ylabel("TPR")
        plt.title("ROC curves of LDA for different combinations")
        plt.legend()
        plt.savefig(os.path.join(self.root, 'api', 'analysis', 'plots', f'lda_{name}.png'))
        return df

    def attributes(self, df):
        """
        AGE2, AGE 1/2, AST 2, AST 1/2, ALT 2, ALT 1/2, PL 2, PL 1/2, FIB-4 2, FIB-4 1/2 plus LDAs
        """

        df['FIB4'] = (df['AGE'] * df['ALT']) / (df['PL'] * np.sqrt(df['AST']))

        df['AGE2'] = df['AGE'] ** 2
        df['AGEsqrt'] = np.sqrt(df['AGE'])

        df['AST'] = df['AST'] ** 2
        df['ASTsqrt'] = np.sqrt(df['AST'])

        df['ALT2'] = df['ALT'] ** 2
        df['ALTsqrt'] = np.sqrt(df['ALT'])

        df['PL2'] = df['PL'] ** 2
        df['PLsqrt'] = np.sqrt(df['PL'])

        df['FIB42'] = df['FIB4'] ** 2
        df['FIB4sqrt'] = np.sqrt(df['FIB4'])

        df['AST/ALT'] = df['AST'] / df['ALT']
        df['AST/AGE'] = df['AST'] / df['AGE']
        df['ALT/AGE'] = df['ALT'] / df['AGE']
        df['PL/AGE'] = df['PL'] / df['AGE']

        df['PL*ALT'] = df['PL'] * df['ALT']
        df['PL*AGE'] = df['PL'] * df['AGE']
        df['PL*AST'] = df['PL'] * df['AST']
        df['ALT*AST'] = df['ALT'] * df['AST']
        df['ALT*AGE'] = df['ALT'] * df['AGE']
        df['AGE*AST'] = df['AGE'] * df['AST']

        df['PL-1'] = 1 / df['PL']
        df['ALT^2'] = 1 / (df['ALT'] ** 2)

        # X = df.drop(['GROUP', 'iGROUP'], axis=1, errors="ignore")
        # poly = PolynomialFeatures(degree=2, interaction_only=False, include_bias=False)
        # X_poly = poly.fit_transform(X)
        # feature_names = poly.get_feature_names_out()
        # df_poly = pd.DataFrame(X_poly, columns=feature_names)
        # df = df.reset_index(drop=True)
        # df_poly = df_poly.reset_index(drop=True)
        # df_poly['GROUP'] = df['GROUP']
        return df

    def decision_tree(self, df, name):
        # Dividindo em variáveis independentes (X) e dependente (y)
        X = df.drop(['GROUP', 'DSE', 'iGROUP'], axis=1, errors='ignore')
        y = df['iGROUP']

        # Balanceamento dos dados
        undersampler = RandomUnderSampler(random_state=42)
        X_resampled, y_resampled = undersampler.fit_resample(X, y)

        # Dividindo os dados em treino e teste
        X_train, X_test, y_train, y_test = train_test_split(
            X_resampled, y_resampled, test_size=0.3, random_state=42
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
            'ccp_alpha': [0.0, 0.01, 0.1]
        }

        grid_search = GridSearchCV(
            estimator=base_model,
            param_grid=param_grid,
            scoring='f1',  # Altere a métrica conforme necessário
            cv=5,  # Validação cruzada com 5 divisões
            verbose=1,
            n_jobs=-1  # Usa todos os núcleos disponíveis
        )

        grid_search.fit(X_train, y_train)

        best_model = grid_search.best_estimator_
        modelpath = os.path.join(self.root, 'api', 'analysis', 'results', 'model1.pkl')
        dump(best_model, modelpath)

        y_pred = best_model.predict(X_test)
        y_pred_proba = best_model.predict_proba(X_test)[:, 1]

        # Métricas de avaliação
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        roc_auc = roc_auc_score(y_test, y_pred_proba)

        report_path = os.path.join(self.root, 'api', 'analysis', 'results', f'tree_{name}.csv')
        with open(report_path, 'w') as f:
            f.write(f"Accuracy: {accuracy}\n")
            f.write(f"Precision: {precision}\n")
            f.write(f"Recall:{recall}\n")
            f.write(f"F1 Score: {f1}\n")
            f.write(f"Area under the curve (AUC): {roc_auc}\n")

        # Curva ROC
        fpr, tpr, thresholds = roc_curve(y_test, y_pred_proba)

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
        df['iGROUP'] = self.le.fit_transform(df['GROUP'])
        df = self.lda(df, name)
        df.to_csv(os.path.join(self.root, 'api', 'analysis', 'results', f'fulldata_{name}.csv'), index=False)
        self.decision_tree(df, name)
        return df

    def run(self):

        # 1. model fat
        df_fat_read = self.read('00_data_fat_n603.csv')
        # df_fat = self.individual_model(df_fat_read, 'fat')

        # 2. model hbv
        df_hbv1 = self.read('00_data_hbv_n177.csv')
        df_hbv2 = self.read('00_data_hbv_n568.csv')
        df_hbv_read = pd.concat([df_hbv1, df_hbv2])
        # df_hbv = self.individual_model(df_hbv_read, 'hbv')

        # 3. model hcv
        df_hcv1 = self.read('00_data_hcv_n74_proprio.csv')
        df_hcv2 = self.read('00_data_hcv_n230.csv')
        df_hcv_read = pd.concat([df_hcv1, df_hcv2])
        # df_hcv = self.individual_model(df_hcv_read, 'hcv')

        # 4. model hbv + hcv
        df_hbv_read['DSE'] = 2
        df_hcv_read['DSE'] = 3
        df_hbc_read = pd.concat([df_hbv_read, df_hcv_read])
        # df_hbcv = self.individual_model(df_hbc_read, 'hbcv')

        # Global
        df_fat_read['DSE'] = 1
        df_hbv_read['DSE'] = 2
        df_hcv_read['DSE'] = 3
        df_global = pd.concat([df_fat_read, df_hbv_read, df_hcv_read])
        df_global = self.individual_model(df_global, 'global')


if __name__ == '__main__':
    Analysis().run()
