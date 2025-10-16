import csv
import random
from datetime import datetime, timedelta

# --- 1. Tabela de Franquias ---
franquias_header = ['id_franquia', 'nome_franquia', 'cidade', 'estado']
franquias_data = [
    [1, 'Restaurante Matriz SP', 'São Paulo', 'SP'],
    [2, 'Filial Campinas', 'Campinas', 'SP'],
    [3, 'Filial Rio de Janeiro', 'Rio de Janeiro', 'RJ'],
    [4, 'Filial Curitiba', 'Curitiba', 'PR'],
    [5, 'Filial Belo Horizonte', 'Belo Horizonte', 'MG']
]

with open('franquias.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(franquias_header)
    writer.writerows(franquias_data)

print("franquias.csv gerado com sucesso.")

# --- 2. Tabela de Profissionais ---
profissionais_header = ['id_profissional', 'id_franquia', 'nome_profissional', 'cargo']
cargos = ['Cozinheiro', 'Garçom', 'Gerente', 'Caixa', 'Auxiliar de Cozinha']
profissionais_data = []
for i in range(1, 21):
    profissionais_data.append([
        i,
        random.randint(1, 5),
        f'Funcionario_{i}',
        random.choice(cargos)
    ])

with open('profissionais.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(profissionais_header)
    writer.writerows(profissionais_data)

print("profissionais.csv gerado com sucesso.")

# --- 3. Tabela de Ingredientes ---
ingredientes_header = ['id_ingrediente', 'nome_ingrediente']
ingredientes_data = [
    [101, 'Tomate'], [102, 'Queijo Muçarela'], [103, 'Farinha de Trigo'], [104, 'Carne Bovina'],
    [105, 'Alface'], [106, 'Pão de Hambúrguer'], [107, 'Batata'], [108, 'Frango'],
    [109, 'Arroz'], [110, 'Feijão'], [111, 'Cebola'], [112, 'Óleo Vegetal']
]

with open('ingredientes.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(ingredientes_header)
    writer.writerows(ingredientes_data)

print("ingredientes.csv gerado com sucesso.")


# --- 4. Tabela de Cardápio (Pratos) ---
cardapio_header = ['id_prato', 'nome_prato', 'preco', 'categoria']
cardapio_data = [
    [201, 'Prato Feito (PF)', 25.00, 'Principal'],
    [202, 'Hambúrguer Clássico', 30.50, 'Lanche'],
    [203, 'Pizza de Muçarela', 45.00, 'Pizza'],
    [204, 'Salada Caesar', 22.00, 'Salada'],
    [205, 'Porção de Batata Frita', 15.00, 'Acompanhamento'],
    [206, 'Frango Grelhado', 28.00, 'Principal'],
    [207, 'Refrigerante Lata', 6.00, 'Bebida'],
    [208, 'Suco Natural', 8.50, 'Bebida']
]

with open('cardapio.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(cardapio_header)
    writer.writerows(cardapio_data)

print("cardapio.csv gerado com sucesso.")

# --- 5. Tabela de Vendas (Fatos) ---
vendas_header = ['id_venda', 'id_franquia', 'id_profissional', 'id_prato', 'data_venda', 'quantidade', 'valor_total']
vendas_data = []
start_date = datetime(2024, 1, 1)

for i in range(1, 51): # Gerando 50 vendas
    prato = random.choice(cardapio_data)
    quantidade = random.randint(1, 3)
    vendas_data.append([
        i,
        random.randint(1, 5), # id_franquia
        random.randint(1, 20), # id_profissional
        prato[0], # id_prato
        (start_date + timedelta(days=random.randint(0, 300))).strftime('%Y-%m-%d'),
        quantidade,
        round(prato[2] * quantidade, 2)
    ])

with open('vendas.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(vendas_header)
    writer.writerows(vendas_data)

print("vendas.csv gerado com sucesso.")