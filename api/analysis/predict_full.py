try:
    from api.predict import Predict
except Exception as e:
    print(e)


def predict(p, a, ast, alt, pl, model, lda=False):
    pred = Predict(root='/home/esther/GitProjects/fibrosis-staging-tool').run({'AGE': float(a), 'ALT': float(alt), 'AST': float(ast), 'PL': float(pl)}, model, lda=lda)
    return pred


def run():

    output = []

    with open('data/00_data_all_predictions.csv', 'r') as r:
        data = [x.split(';') for x in r.readlines()]
    for i, d in enumerate(data[1:]):
        pathology = d[0]
        age = int(d[1])
        ast = float(d[2].replace(',', '.'))
        alt = float(d[3].replace(',', '.'))
        pl = float(d[4].replace(',', '.'))

        partial = [pathology, age, ast, alt, pl]
        predictions = ['fat', 'hbv', 'hcv', 'hbcv', 'global']
        for p in predictions:
            pmodel = predict(pathology, age, ast, alt, pl, p)
            partial.append(pmodel['prediction'])
        for p in predictions:
            pmodel_lda = predict(pathology, age, ast, alt, pl, p, lda=True)
            partial.append(pmodel_lda['prediction'])
        output.append(partial)

    with open('prediction_table.csv', 'w') as p:
        p.write(';'.join(data[0]))
        for o in output:
            p.write(';'.join([str(x) for x in o]) + '\n')
            p.flush()
    return output


if __name__ == '__main__':
    import os
    import django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
    django.setup()
    from api.predict import Predict
    d = run()
    print(d)
