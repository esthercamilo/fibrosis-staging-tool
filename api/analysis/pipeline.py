import datetime
import os.path
import joblib
from imblearn.under_sampling import RandomUnderSampler
import numpy as np
from sklearn.metrics import confusion_matrix
from itertools import combinations
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor, plot_tree
from sklearn.metrics import accuracy_score, mean_squared_error
from sklearn.preprocessing import LabelEncoder
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.metrics import roc_curve, auc


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
        features = [x for x in df.columns if x not in exclude]
        combinations_features = sum([list(combinations(features, i)) for i in range(1, len(features) + 1)], [])

        results = []

        for combo in combinations_features:

            if len(combo) < 2:
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

        return df

    def decision_tree(self, df, name):

        # Dividindo em variáveis independentes (X) e dependente (y)
        X = df.drop(['GROUP', 'DSE', 'iGROUP'], axis=1, errors='ignore')
        y = df['iGROUP']

        undersampler = RandomUnderSampler(random_state=42)
        X_resampled, y_resampled = undersampler.fit_resample(X, y)
        # Dividindo os dados em treino e teste
        X_train, X_test, y_train, y_test = train_test_split(X_resampled, y_resampled, test_size=0.3, random_state=42)

        # Criando e treinando o modelo
        regressor = DecisionTreeRegressor(random_state=42)
        regressor.fit(X_train, y_train)

        # Fazendo previsões e avaliando o modelo
        y_pred = regressor.predict(X_test)
        print(f"Mean Squared Error {name}:", mean_squared_error(y_test, y_pred))

        # Treinando o modelo (usando DecisionTreeClassifier para classificação)
        model = DecisionTreeClassifier(random_state=42, max_depth=3)
        model.fit(X_train, y_train)

        joblib.dump(model, os.path.join(self.root, 'api', 'analysis', 'results', f'model1_{name}.pkl'))

        # Desenhando a árvore de decisão
        plt.figure(figsize=(20, 15))  # Ajuste o tamanho da figura
        plot_tree(model, filled=True, feature_names=X.columns, class_names=['G1', 'G2'], rounded=True, fontsize=12)
        plt.savefig(os.path.join(self.root, 'api', 'analysis', 'plots', f'tree_{name}.png'))

        # Gerar a matriz de confusão
        cm = confusion_matrix(y_test, y_pred)

        # Plotar a matriz de confusão usando Seaborn para visualização melhor
        plt.figure(figsize=(6, 4))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=model.classes_, yticklabels=model.classes_)
        plt.title('Matriz de Confusão')
        plt.xlabel('Previsões')
        plt.ylabel('Valores Reais')
        plt.savefig(os.path.join(self.root, 'api', 'analysis', 'plots', f'confusion_matrix_{name}.png'))

        # Extraindo os valores da matriz de confusão
        TP = cm[1, 1]  # Verdadeiro positivo (classe positiva)
        FN = cm[1, 0]  # Falso negativo (classe positiva, mas predito negativo)

        # Calculando as taxas
        TPR = TP / (TP + FN)  # Taxa de verdadeiro positivo
        FNR = FN / (TP + FN)  # Taxa de falso negativo

        # Imprimir as taxas
        print(f"Taxa de Verdadeiro Positivo (TPR)_{name}: {TPR:.2f}")
        print(f"Taxa de Falso Negativo (FNR)_{name}: {FNR:.2f}\n\n")

    def individual_model(self, df, name):
        df = self.attributes(df)
        df['iGROUP'] = self.le.fit_transform(df['GROUP'])
        df = self.lda(df, name)
        df.to_csv(os.path.join(self.root, 'api', 'analysis', 'results', f'fulldata_{name}.csv'), index=False)
        self.decision_tree(df, name)
        return df

    def run(self):

        # 1. model fat
        df_fat_read = self.read('00_data_fat_n603.csv')
        df_fat = self.individual_model(df_fat_read, 'fat')

        # 2. model hbv
        # df_hbv1 = self.read('00_data_hbv_n177.csv')
        # df_hbv2 = self.read('00_data_hbv_n568.csv')
        # df_hbv_read = pd.concat([df_hbv1, df_hbv2])
        # df_hbv = self.individual_model(df_hbv_read, 'hbv')

        # 3. model hcv
        # df_hcv1 = self.read('00_data_hcv_n74_proprio.csv')
        # df_hcv2 = self.read('00_data_hcv_n230.csv')
        # df_hcv_read = pd.concat([df_hcv1, df_hcv2])
        # df_hcv = self.individual_model(df_hcv_read, 'hcv')

        # Global



if __name__ == '__main__':
    Analysis().run()
