from sklearn.model_selection    import train_test_split
from sklearn.datasets           import load_iris
from sklearn.metrics            import accuracy_score, confusion_matrix
from tabnanny                   import verbose
from cvxpy                      import Variable, Minimize, Problem, multiply, pos, sum_squares

import numpy as np

# dicionario que relaciona nome da especie ao valor no vetor y
especies = {
    'setosa' : 0,
    'versicolor' : 1,
    'virginica' : 2
}

classesValidas = [0, 1, 2]

iris = load_iris()

def identificadorQuadradosMinimos(t, y, x_test):
    
    yBinSetosa      = np.where(y == especies['setosa'], 1, -1)
    yBinVersicolor  = np.where(y == especies['versicolor'], 1, -1)
    yBinVirginica   = np.where(y == especies['virginica'], 1, -1)
    
    m = t.shape[1]
    x_train = t

    t = t.T    
    

    # Identificar setosas
    a = Variable(m)
    b = Variable()
    funcao      = yBinSetosa - (a.T @ t) - b
    objective   = Minimize(sum_squares(funcao))
    problema    = Problem(objective)
    problema.solve()
    a = a.value
    a.reshape(-1,1)

    yPredSetosaTeste = np.sign(x_test @ a + b.value)
    yPredSetosaTeste = np.where(yPredSetosaTeste == 1, especies['setosa'], -1)

    yPredSetosaTreino = np.sign(x_train @ a + b.value)
    yPredSetosaTreino = np.where(yPredSetosaTreino == 1, especies['setosa'], -1)

    # Identificar versicolor
    a = Variable(m)
    b = Variable()
    funcao      = yBinVersicolor - (a.T @ t) - b
    objective   = Minimize(sum_squares(funcao))
    problema    = Problem(objective)
    problema.solve()
    a = a.value
    a.reshape(-1,1)
    
    yPredVersicolorTeste = np.sign(x_test @ a + b.value)
    yPredVersicolorTreino = np.sign(x_train @ a + b.value)

    # Identificar virginica
    a = Variable(m)
    b = Variable()
    funcao      = yBinVirginica - (a.T @ t) - b
    objective   = Minimize(sum_squares(funcao))
    problema    = Problem(objective)
    problema.solve()
    a = a.value
    a.reshape(-1,1)
    
    yPredVirginicaTeste = np.sign(x_test @ a + b.value)
    yPredVirginicaTeste = np.where(yPredVirginicaTeste == 1, especies['virginica'], -1)

    yPredVirginicaTreino = np.sign(x_train @ a + b.value)
    yPredVirginicaTreino = np.where(yPredVirginicaTreino == 1, especies['virginica'], -1)

    yPredTeste  = []
    yPredTreino = []

    for item in range(len(yPredSetosaTeste)):
        yPredTeste.append(max(yPredSetosaTeste[item], yPredVersicolorTeste[item], yPredVirginicaTeste[item]))
        if yPredTeste[item] == -1:
            if y[item] > 0:
                yPredTeste[item] = 0
            else:
                yPredTeste[item] = 2

    for item in range(len(yPredSetosaTreino)):
        yPredTreino.append(max(yPredSetosaTreino[item], yPredVersicolorTreino[item], yPredVirginicaTreino[item]))
        if yPredTreino[item] == -1:
            if y[item] > 0:
                yPredTreino[item] = 0
            else:
                yPredTreino[item] = 2

    print('Quantidade de amostras treino: ', len(x_train))
    print('Quantidade de amostras teste: ', len(x_test))

    return yPredTeste, yPredTreino

def encontraCoeficientesSVM(t, y, especie):
    yBinario = np.where(y == especies[especie], 1, -1)
    
    m = t.shape[1]
    
    t = t.T

    a = Variable(m)
    b = Variable()

    funcao = pos(1 - multiply(yBinario, (a.T @ t + b)))
    objective = Minimize(sum(funcao))
    problema = Problem(objective)

    problema.solve()

    return a.value, b.value

# print(type(iris))
x = iris.data
y = iris.target

# print('\nx: ',x)
# print('\ny: ',y)

xTrain, xTest, yTrain, yTest = train_test_split(
    x, y,
    test_size= 50,
    random_state= 42,
    stratify= y
)

yTestSetosa     = np.where(yTest == especies['setosa'], 1, -1)
yTestVirginica  = np.where(yTest == especies['virginica'], 1, -1)
yTestVersicolor = np.where(yTest == especies['versicolor'], 1, -1)

yTrainSetosa     = np.where(yTrain == especies['setosa'], 1, -1)
yTrainVirginica  = np.where(yTrain == especies['virginica'], 1, -1)
yTrainVersicolor = np.where(yTrain == especies['versicolor'], 1, -1)

y_predTeste, y_predTreinamento = identificadorQuadradosMinimos(xTrain, yTrain, xTest)

y_predTeste         = [int(val) for val in y_predTeste]
y_predTreinamento   = [int(val) for val in y_predTreinamento]

# print(y_predTeste)
# print(y_predTreinamento)

matrizConfusaoTeste = confusion_matrix(
    y_true= yTest,
    y_pred= y_predTeste,
    labels= classesValidas
)

matrizConfusaoTreinamento = confusion_matrix(
    y_true= yTrain,
    y_pred= y_predTreinamento,
    labels= classesValidas
)

print('\nMatriz de Confusão QM -> Variáveis de teste:')
print(matrizConfusaoTeste)

elementosTeste = matrizConfusaoTeste.sum()
print('Soma dos elementos da matriz de teste: ', elementosTeste)

print('\nMatriz de Confusão QM -> Variáveis de treinamento:')
print(matrizConfusaoTreinamento)

elementosTreinamento = matrizConfusaoTreinamento.sum()
print('Soma dos elementos da matriz de treinamento: ', elementosTreinamento)