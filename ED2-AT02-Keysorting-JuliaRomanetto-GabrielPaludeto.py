import sys

# CLASSE HERÓI ==================================
class Heroi:
    def __init__(self, atributo):
        self.key = atributo[0]
        self.Name = atributo[1]
        self.Alignment = atributo[2]
        self.Gender = atributo[3]
        self.EyeColor = atributo[4]
        self.Race = atributo[5]
        self.HairColor = atributo[6]
        self.Publisher = atributo[7]
        self.SkinColor = atributo[8]
        self.Height = atributo[9]
        self.Weight = atributo[10]
        self.Intelligence = atributo[11]
        self.Strength = atributo[12]
        self.Speed = atributo[13]
        self.Durability = atributo[14]
        self.Power = atributo[15]
        self.Combat = atributo[16]
        self.Total = atributo[17]

    def get_key(self, campo_chave):
        valor = getattr(self, campo_chave, "")
        try:
            return int(valor)
        except ValueError:
            return valor.lower()

    def __str__(self):
        return '|'.join([
            self.key, self.Name, self.Alignment, self.Gender, self.EyeColor,
            self.Race, self.HairColor, self.Publisher, self.SkinColor,
            self.Height, self.Weight, self.Intelligence, self.Strength,
            self.Speed, self.Durability, self.Power, self.Combat, self.Total
        ])

# MÉTODOS DE ORDENAÇÃO ==========================
def quickSort(registros, chave, decrescente=False):
    if len(registros) <= 1:
        return registros
    pivo = registros[0]
    menores = [x for x in registros[1:] if x.get_key(chave) < pivo.get_key(chave)]
    iguais = [x for x in registros if x.get_key(chave) == pivo.get_key(chave)]
    maiores = [x for x in registros[1:] if x.get_key(chave) > pivo.get_key(chave)]
    resultado = quickSort(menores, chave) + iguais + quickSort(maiores, chave)
    return resultado[::-1] if decrescente else resultado

def insertionSort(registros, chave, decrescente=False):
    for i in range(1, len(registros)):
        atual = registros[i]
        j = i - 1
        while j >= 0 and ((registros[j].get_key(chave) > atual.get_key(chave)) ^ decrescente):
            registros[j + 1] = registros[j]
            j -= 1
        registros[j + 1] = atual
    return registros

def mergeSort(registros, chave, decrescente=False):
    if len(registros) <= 1:
        return registros
    meio = len(registros) // 2
    esquerda = mergeSort(registros[:meio], chave, decrescente)
    direita = mergeSort(registros[meio:], chave, decrescente)
    return merge(esquerda, direita, chave, decrescente)

def merge(esq, dir, chave, decrescente):
    resultado = []
    i = j = 0
    while i < len(esq) and j < len(dir):
        if (esq[i].get_key(chave) <= dir[j].get_key(chave)) ^ decrescente:
            resultado.append(esq[i])
            i += 1
        else:
            resultado.append(dir[j])
            j += 1
    resultado.extend(esq[i:])
    resultado.extend(dir[j:])
    return resultado

def heapify(registros, n, i, chave, decrescente):
    maior = i
    l = 2 * i + 1
    r = 2 * i + 2
    if l < n and (registros[l].get_key(chave) > registros[maior].get_key(chave)) ^ decrescente:
        maior = l
    if r < n and (registros[r].get_key(chave) > registros[maior].get_key(chave)) ^ decrescente:
        maior = r
    if maior != i:
        registros[i], registros[maior] = registros[maior], registros[i]
        heapify(registros, n, maior, chave, decrescente)

def heapSort(registros, chave, decrescente=False):
    n = len(registros)
    for i in range(n//2 - 1, -1, -1):
        heapify(registros, n, i, chave, decrescente)
    for i in range(n-1, 0, -1):
        registros[i], registros[0] = registros[0], registros[i]
        heapify(registros, i, 0, chave, decrescente)
    return registros

# FUNÇÃO PRINCIPAL ==============================
def main():

    if len(sys.argv) != 3:
        print("Para executar o programa: <nomearquivo.py> <arquivEntrada> <arquivoSaida>.\n")
        sys.exit(1)

    entrada = sys.argv[1]
    saida = sys.argv[2]

    with open (entrada, 'r', encoding='utf-8') as arqEntrada:
        try: 
            linhas = arqEntrada.readlines();
            if len(linhas) < 3:
                print("Erro: Arquivo de entrada deve conter pelo menos 3 linhas (metadados, cabeçalho e um registro).")
                sys.exit(1)
            meta_dados = dict(dado.strip().split('=') for dado in linhas[0].strip().split(',')) # faz com que os meta-atributos fiquem agrupados em pares ([sort, letra] e [order letra])
            atributos = linhas[1].split(',')
            registros = [Heroi(linha.strip().split('|')) for linha in linhas[2:]]
        except Exception as erro:
            print(f"Erro ao ler o arquivo: {erro}")
            sys.exit(1)

        metodoOrdenacao = meta_dados.get('SORT', '').upper()
        ordem = meta_dados.get('ORDER', '').upper()
        if ordem not in ('C', 'D'):
            print(f"ORDER inválido. Use 'C' para crescente ou 'D' para decrescente.")
            sys.exit(1)
        decrescente = ordem == 'D'
        chave = atributos[0]

    if metodoOrdenacao == 'Q':
        registros = quickSort(registros, chave, decrescente)
    elif metodoOrdenacao == 'M':
        registros = mergeSort(registros, chave, decrescente)
    elif metodoOrdenacao == 'H':
        registros = heapSort(registros, chave, decrescente)
    elif metodoOrdenacao == 'I':
        registros = insertionSort(registros, chave, decrescente)
    else:
        print(f"Método de ordenação inválido. Certifique-se que o mtodo escolhido é um dos abaixo:\n")
        print(f"Q - Quick Sort\nM - Merge Sort\nH - Heap Sort\n I - Insertion Sort\n")
        sys.exit(1)

    with open (saida, 'w', encoding='utf-8') as arqSaida:
        try: 
            arqSaida.write('|'.join(atributos))
            for heroi in registros:
                arqSaida.write(str(heroi) + '\n') #converte Heroi para uma string e escreve no arquivo
        except Exception as erro:
            print(f"Erro ao criar o arquivo: {erro}")
            sys.exit(1)

if __name__ == '__main__':
    main()