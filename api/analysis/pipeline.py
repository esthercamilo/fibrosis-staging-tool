# Importando bibliotecas
import os.path
import joblib
from imblearn.under_sampling import RandomUnderSampler
import numpy as np
from sklearn.metrics import confusion_matrix
import pandas
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor, plot_tree
from sklearn.metrics import accuracy_score, mean_squared_error
from sklearn.preprocessing import LabelEncoder


class Analysis:
    def __init__(self, root=None):
        self.root = os.path.abspath('../..')

    def read(self):
        root_path = self.root
        datapath = os.path.join(root_path, 'api', 'analysis', 'data')
        files = os.listdir(datapath)
        dfset = {}
        for f in files:
            df = pd.read_csv(os.path.join(datapath, f), sep='\t')
            name = '_'.join(f.split('.')[0].split('_')[2:4]).upper()
            df['DSE'] = name
            dfset[f.split('.')[0]] = df
        return dfset

    def description(self, df):
        path_plots = os.path.join(self.root, 'api', 'analysis', 'plots')
        path_results = os.path.join(self.root, 'api', 'analysis', 'results')

        sets = ['AGE', 'AST', 'ALT', 'PL', 'FIB4']

        for s in []:  # todo (sets):
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

    def attributes(self, df):
        """
        AGE2, AGE 1/2, AST 2, AST 1/2, ALT 2, ALT 1/2, PL 2, PL 1/2, FIB-4 2, FIB-4 1/2.
        """
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

    def decision_tree(self, df, include_dse=False):
        df = self.attributes(df)

        if include_dse:
            # Aplicando Label Encoding
            df = pd.get_dummies(df, columns=['DSE'], prefix='DSE')
        else:
            try:
                df = df.drop(['DSE'])
            except Exception as e:
                print(e)

        le = LabelEncoder()
        # Aplique o LabelEncoder na coluna 'GROUP'
        df['GROUP_encoded'] = le.fit_transform(df['GROUP'])

        # Dividindo em variáveis independentes (X) e dependente (y)
        X = df.drop(['GROUP', 'GROUP_encoded'], axis=1)
        y = df['GROUP_encoded']

        if include_dse:
            X.to_csv(os.path.join(self.root, 'api', 'analysis', 'results', 'fulldata.csv'), index=False)

        undersampler = RandomUnderSampler(random_state=42)
        X_resampled, y_resampled = undersampler.fit_resample(X, y)
        # Dividindo os dados em treino e teste
        X_train, X_test, y_train, y_test = train_test_split(X_resampled, y_resampled, test_size=0.3, random_state=42)

        # Criando e treinando o modelo
        regressor = DecisionTreeRegressor(random_state=42)
        regressor.fit(X_train, y_train)

        # Fazendo previsões e avaliando o modelo
        y_pred = regressor.predict(X_test)
        print("Mean Squared Error:", mean_squared_error(y_test, y_pred))

        # Treinando o modelo (usando DecisionTreeClassifier para classificação)
        model = DecisionTreeClassifier(random_state=42, max_depth=3)
        model.fit(X_train, y_train)

        joblib.dump(model, os.path.join(self.root, 'api', 'analysis', 'results', 'model1.pkl'))

        # Desenhando a árvore de decisão
        plt.figure(figsize=(20, 15))  # Ajuste o tamanho da figura
        plot_tree(model, filled=True, feature_names=X.columns, class_names=le.classes_, rounded=True, fontsize=12)
        plt.savefig(os.path.join(self.root, 'api', 'analysis', 'plots', 'tree.png'))

        # Gerar a matriz de confusão
        cm = confusion_matrix(y_test, y_pred)

        # Plotar a matriz de confusão usando Seaborn para visualização melhor
        plt.figure(figsize=(6, 4))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=model.classes_, yticklabels=model.classes_)
        plt.title('Matriz de Confusão')
        plt.xlabel('Previsões')
        plt.ylabel('Valores Reais')
        plt.savefig(os.path.join(self.root, 'api', 'analysis', 'plots', 'confusion_matrix.png'))

        # Extraindo os valores da matriz de confusão
        TP = cm[1, 1]  # Verdadeiro positivo (classe positiva)
        FN = cm[1, 0]  # Falso negativo (classe positiva, mas predito negativo)

        # Calculando as taxas
        TPR = TP / (TP + FN)  # Taxa de verdadeiro positivo
        FNR = FN / (TP + FN)  # Taxa de falso negativo

        # Imprimir as taxas
        print(f"Taxa de Verdadeiro Positivo (TPR): {TPR:.2f}")
        print(f"Taxa de Falso Negativo (FNR): {FNR:.2f}")

    def run(self):
        dfs = self.read()
        df_concat = pd.concat(dfs.values())
        self.description(df_concat)
        # 1. model with all conditions
        self.decision_tree(df_concat, include_dse=True)
        # 2. model fat
        # self.decision_tree(dfs['00_data_fat_n603'])
        # print()


if __name__ == '__main__':
    Analysis().run()
