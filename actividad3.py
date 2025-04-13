import pandas as pd
import numpy as np

# 1. Crear un conjunto de datos de ejemplo (transporte masivo)
data = {
    'Hora': [9, 12, 17, 6, 13, 19, 15, 8, 18, 7],
    'Distancia': [10, 15, 20, 5, 25, 30, 18, 7, 22, 5],
    'Tráfico': ['Bajo', 'Alto', 'Alto', 'Bajo', 'Medio', 'Medio', 'Bajo', 'Alto', 'Bajo', 'Medio'],
    'Pasajeros': [5, 20, 25, 3, 30, 35, 22, 8, 28, 7],
    'Llegada_Tiempo': [12, 14, 19, 9, 15, 20, 17, 10, 18, 9]  # Variable objetivo (en horas)
}

# Convertir el dataset a un DataFrame
df = pd.DataFrame(data)

# 2. Preprocesar los datos (convertir 'Tráfico' a valores numéricos)
df['Tráfico'] = df['Tráfico'].map({'Bajo': 0, 'Medio': 1, 'Alto': 2})

# Mostrar los primeros registros del DataFrame
print("Datos de entrenamiento:")
print(df.head())

# 3. Función para calcular el índice de Gini
def gini_index(groups, classes):
    total_instances = float(sum([len(group) for group in groups]))
    gini = 0.0
    for group in groups:
        size = float(len(group))
        if size == 0:
            continue
        score = 0.0
        for class_val in classes:
            proportion = [row[-1] for row in group].count(class_val) / size
            score += proportion * proportion
        gini += (1.0 - score) * (size / total_instances)
    return gini

# 4. Función para dividir los datos según un atributo
def test_split(index, value, dataset):
    left, right = [], []
    for row in dataset:
        if row[index] < value:
            left.append(row)
        else:
            right.append(row)
    return left, right

# 5. Función para elegir el mejor atributo para dividir el conjunto de datos
def get_best_split(dataset):
    class_values = list(set(row[-1] for row in dataset))
    b_score, b_index, b_value, b_left, b_right = float('inf'), None, None, None, None
    for index in range(len(dataset[0]) - 1):
        for row in dataset:
            groups = test_split(index, row[index], dataset)
            gini = gini_index(groups, class_values)
            if gini < b_score:
                b_score, b_index, b_value, b_left, b_right = gini, index, row[index], groups[0], groups[1]
    return {'index': b_index, 'value': b_value, 'left': b_left, 'right': b_right}

# 6. Función recursiva para construir el árbol de decisión
def build_tree(dataset, max_depth, min_size, depth=1):
    if len(dataset) == 0:
        return None

    class_values = list(set(row[-1] for row in dataset))
    if len(class_values) == 1:  # Si solo hay una clase, ya no es necesario dividir más
        return {'label': class_values[0]}
    
    # Si alcanzamos el máximo de profundidad o el tamaño mínimo
    if depth >= max_depth or len(dataset) <= min_size:
        return {'label': np.mean([row[-1] for row in dataset])}
    
    node = get_best_split(dataset)
    
    left_tree = build_tree(node['left'], max_depth, min_size, depth + 1)
    right_tree = build_tree(node['right'], max_depth, min_size, depth + 1)
    
    node['left'] = left_tree
    node['right'] = right_tree
    
    return node

# 7. Convertir el DataFrame a lista para procesar
dataset = df.values.tolist()

# 8. Construir el árbol de decisión
tree = build_tree(dataset, max_depth=5, min_size=2)

# Función para imprimir el árbol de decisión de forma legible
def print_tree(node, depth=0):
    if isinstance(node, dict):
        if 'label' in node:
            print(f"{'  ' * depth}Predict: {node['label']}")
        else:
            print(f"{'  ' * depth}X{node['index']} < {node['value']} ?")
            print(f"{'  ' * (depth+1)}Left:")
            print_tree(node['left'], depth + 2)
            print(f"{'  ' * (depth+1)}Right:")
            print_tree(node['right'], depth + 2)
    else:
        print(f"{'  ' * depth}Predict: {node['label']}")

# Mostrar el árbol de decisión
print("\nÁrbol de decisión:")
print_tree(tree)
