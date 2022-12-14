# Gerador/Verificador de Assinaturas - RSA
# Trabalho 2 de Segurança Computacional
# Alunos:
# * Gabriel Rodrigues Pacheco - 17/0058280
# * Théo Henrique Gallo - 17/0080781

# Etapas do trabalho:
# * Parte I: Geracao de chaves
# ** Geracao de chaves (p e q primos com no minimo de 1024 bits)
# * Parte II: Cifra simetrica
# ** Geracao de chaves simetrica
# ** Cifracao simetrica de mensagem (AES modo CTR),
# * Parte III: Geracao da assinatura
# ** Calculo de hashes da mensagem em claro (funcao de hash SHA-3)
# ** Assinatura da mensagem (cifracao do hash da mensagem usando OAEP)
# ** Formatação do resultado (caracteres especiais e informações para verificação em BASE64)
# * Parte IV: Verificação:
# ** Parsing do documento assinado e decifração da mensagem (de acordo com a formatação usada, no caso BASE64)
# ** Decifracao da assinatura (decifração do hash)
# ** Verificacao (calculo e comparação do hash do arquivo)

import random
from hashlib import sha512
from pickle import dump, load


sbox = [
        0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
        0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
        0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
        0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
        0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
        0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
        0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
        0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
        0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
        0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
        0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
        0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
        0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,
        0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,
        0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
        0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16
]
sbox_Inv = [
        0x52, 0x09, 0x6a, 0xd5, 0x30, 0x36, 0xa5, 0x38, 0xbf, 0x40, 0xa3, 0x9e, 0x81, 0xf3, 0xd7, 0xfb,
        0x7c, 0xe3, 0x39, 0x82, 0x9b, 0x2f, 0xff, 0x87, 0x34, 0x8e, 0x43, 0x44, 0xc4, 0xde, 0xe9, 0xcb,
        0x54, 0x7b, 0x94, 0x32, 0xa6, 0xc2, 0x23, 0x3d, 0xee, 0x4c, 0x95, 0x0b, 0x42, 0xfa, 0xc3, 0x4e,
        0x08, 0x2e, 0xa1, 0x66, 0x28, 0xd9, 0x24, 0xb2, 0x76, 0x5b, 0xa2, 0x49, 0x6d, 0x8b, 0xd1, 0x25,
        0x72, 0xf8, 0xf6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xd4, 0xa4, 0x5c, 0xcc, 0x5d, 0x65, 0xb6, 0x92,
        0x6c, 0x70, 0x48, 0x50, 0xfd, 0xed, 0xb9, 0xda, 0x5e, 0x15, 0x46, 0x57, 0xa7, 0x8d, 0x9d, 0x84,
        0x90, 0xd8, 0xab, 0x00, 0x8c, 0xbc, 0xd3, 0x0a, 0xf7, 0xe4, 0x58, 0x05, 0xb8, 0xb3, 0x45, 0x06,
        0xd0, 0x2c, 0x1e, 0x8f, 0xca, 0x3f, 0x0f, 0x02, 0xc1, 0xaf, 0xbd, 0x03, 0x01, 0x13, 0x8a, 0x6b,
        0x3a, 0x91, 0x11, 0x41, 0x4f, 0x67, 0xdc, 0xea, 0x97, 0xf2, 0xcf, 0xce, 0xf0, 0xb4, 0xe6, 0x73,
        0x96, 0xac, 0x74, 0x22, 0xe7, 0xad, 0x35, 0x85, 0xe2, 0xf9, 0x37, 0xe8, 0x1c, 0x75, 0xdf, 0x6e,
        0x47, 0xf1, 0x1a, 0x71, 0x1d, 0x29, 0xc5, 0x89, 0x6f, 0xb7, 0x62, 0x0e, 0xaa, 0x18, 0xbe, 0x1b,
        0xfc, 0x56, 0x3e, 0x4b, 0xc6, 0xd2, 0x79, 0x20, 0x9a, 0xdb, 0xc0, 0xfe, 0x78, 0xcd, 0x5a, 0xf4,
        0x1f, 0xdd, 0xa8, 0x33, 0x88, 0x07, 0xc7, 0x31, 0xb1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xec, 0x5f,
        0x60, 0x51, 0x7f, 0xa9, 0x19, 0xb5, 0x4a, 0x0d, 0x2d, 0xe5, 0x7a, 0x9f, 0x93, 0xc9, 0x9c, 0xef,
        0xa0, 0xe0, 0x3b, 0x4d, 0xae, 0x2a, 0xf5, 0xb0, 0xc8, 0xeb, 0xbb, 0x3c, 0x83, 0x53, 0x99, 0x61,
        0x17, 0x2b, 0x04, 0x7e, 0xba, 0x77, 0xd6, 0x26, 0xe1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0c, 0x7d
]
k_ex = [
        0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36, 0x6c, 0xd8, 0xab, 0x4d, 0x9a,
        0x2f, 0x5e, 0xbc, 0x63, 0xc6, 0x97, 0x35, 0x6a, 0xd4, 0xb3, 0x7d, 0xfa, 0xef, 0xc5, 0x91, 0x39,
        0x72, 0xe4, 0xd3, 0xbd, 0x61, 0xc2, 0x9f, 0x25, 0x4a, 0x94, 0x33, 0x66, 0xcc, 0x83, 0x1d, 0x3a,
        0x74, 0xe8, 0xcb, 0x8d, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36, 0x6c, 0xd8,
        0xab, 0x4d, 0x9a, 0x2f, 0x5e, 0xbc, 0x63, 0xc6, 0x97, 0x35, 0x6a, 0xd4, 0xb3, 0x7d, 0xfa, 0xef,
        0xc5, 0x91, 0x39, 0x72, 0xe4, 0xd3, 0xbd, 0x61, 0xc2, 0x9f, 0x25, 0x4a, 0x94, 0x33, 0x66, 0xcc,
        0x83, 0x1d, 0x3a, 0x74, 0xe8, 0xcb, 0x8d, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b,
        0x36, 0x6c, 0xd8, 0xab, 0x4d, 0x9a, 0x2f, 0x5e, 0xbc, 0x63, 0xc6, 0x97, 0x35, 0x6a, 0xd4, 0xb3,
        0x7d, 0xfa, 0xef, 0xc5, 0x91, 0x39, 0x72, 0xe4, 0xd3, 0xbd, 0x61, 0xc2, 0x9f, 0x25, 0x4a, 0x94,
        0x33, 0x66, 0xcc, 0x83, 0x1d, 0x3a, 0x74, 0xe8, 0xcb, 0x8d, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20,
        0x40, 0x80, 0x1b, 0x36, 0x6c, 0xd8, 0xab, 0x4d, 0x9a, 0x2f, 0x5e, 0xbc, 0x63, 0xc6, 0x97, 0x35,
        0x6a, 0xd4, 0xb3, 0x7d, 0xfa, 0xef, 0xc5, 0x91, 0x39, 0x72, 0xe4, 0xd3, 0xbd, 0x61, 0xc2, 0x9f,
        0x25, 0x4a, 0x94, 0x33, 0x66, 0xcc, 0x83, 0x1d, 0x3a, 0x74, 0xe8, 0xcb, 0x8d, 0x01, 0x02, 0x04,
        0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36, 0x6c, 0xd8, 0xab, 0x4d, 0x9a, 0x2f, 0x5e, 0xbc, 0x63,
        0xc6, 0x97, 0x35, 0x6a, 0xd4, 0xb3, 0x7d, 0xfa, 0xef, 0xc5, 0x91, 0x39, 0x72, 0xe4, 0xd3, 0xbd,
        0x61, 0xc2, 0x9f, 0x25, 0x4a, 0x94, 0x33, 0x66, 0xcc, 0x83, 0x1d, 0x3a, 0x74, 0xe8, 0xcb, 0x8d
]
exp = []


# Calcular chave publica e
def find_e(n, phi_n):
    while True:
        if verifica_eh_primo(n):
            if verifica_eh_coprimo(n, phi_n):
                return n
        n = n+1


# Calcular chave privada d
def find_d(prime1, n, e, phi_n):
    for i in range(prime1, n):
        if ((i * e) % phi_n) == 1:
            return i


# Verifica se um numero e primo percorrendo todos os numeros até ele
def verifica_eh_primo(n):
    for valor in range(2, n):
        # print(f"Valor = {valor}, n={n}")
        if n % valor == 0:
            return False
    return True


# Verifica se dois numeros sao coprimos
def verifica_eh_coprimo(numero_1, numero_2):
    numero_1_fatores = encontrar_fatores(numero_1)
    numero_2_fatores = encontrar_fatores(numero_2)

    if set(numero_1_fatores).isdisjoint(set(numero_2_fatores)):
        return True
    return False


# Usa a funcao de identificar primos para percorrer um valor ate encontrar um valor primo proximo a ele
def encontrar_primo(num, maximo_chave):
    while num < maximo_chave:
        if verifica_eh_primo(num):
            return num
        num += 1
    else:
        return encontrar_primo(num/2, maximo_chave)


def encontrar_fatores(num):
    fatores = list()
    for i in range(2, num):
        if (num % i) == 0:
            fatores.append(i)
    return fatores


# Funcao para gerar chaves publica e privada
def gerar_chaves():
    print("Geração de chaves (p e q primos com no mínimo de 1024 bits)")
    # Ajuste aqui o tamahho dos numeros primos desejados (impacto grande no tempo de execucao)
    maximo_chave = 1000
    p = encontrar_primo(random.randint(0, maximo_chave), maximo_chave)
    q = encontrar_primo(random.randint(0, maximo_chave), maximo_chave)

    # Funcao totiente
    phi_n = (p-1) * (q-1)
    n = p * q

    e = find_e(n, phi_n)
    d = find_d(p, n, e, phi_n)

    return [[n, e], [n, d]]


# Funcao para gerar a criptografia RSA
def criptografar_rsa(msg, nome_arquivo):
    # ***** AES *****
    # Cifração simétrica de mensagem (AES modo CTR)
    # bloco fixo de 128 bits e um tamanho de chave de 128, 192 ou 256 bits
    # 10 rodadas para chaves de 128 bits.
    # KeyExpansion, AddRoundKey, SubBytes, ShiftRows, MixColumns, AddRoundKey, SubBytes, ShiftRows, AddRoundKey

    # * Parte I: Geracao de chaves
    key = random.getrandbits(128)
    print(f"Chave gerada: {(hex(key))}")
    # TODO: Implementar isso


    # ***** RSA *****
    # Calcular hash (SHA-3) da mensagem
    hash = int.from_bytes(sha512(str.encode(msg)).digest(), byteorder='big')
    print("Hash: ", hex(hash))

    # Vamos gerar um par de chaves (p e q) de numeros primos (privada e publica) de 1024 bits
    [chave_publica, chave_privada] = gerar_chaves()
    print(f"Chave publica:  (n={chave_publica[0]}, e={chave_publica[1]})")
    print(f"Chave privada: (n={chave_privada[0]}, d={chave_privada[1]})")
    mensagem_cifrada = list()
    hash_cifrado = list()
    for i in range(len(msg)):
        print(f"Cifrando letra msg: {i+1}/{len(msg)}")
        asc = ord(msg[i])
        mensagem_cifrada.append((asc ** chave_publica[1]) % chave_publica[0])
    hash_str = str(hash)
    for i in range(len(hash_str)):
        print(f"Cifrando letra hash: {i+1}/{len(hash_str)}")
        asc = ord(hash_str[i])
        hash_cifrado.append((asc ** chave_publica[1]) % chave_publica[0])
    print(f"Mensagem cifrada: {mensagem_cifrada}")
    print(f"Hash cifrado: {hash_cifrado}")

    # Salvar resultado no arquivo
    Data = {
        "mensagem_cifrada": mensagem_cifrada,
        "chave_privada": chave_privada,
        "hash": hash,
        "hash_cifrado": hash_cifrado,
    }
    arquivo = open(nome_arquivo, "wb")
    dump(Data, arquivo)
    arquivo.close()
    print(f"Dados salvos no arquivo {nome_arquivo}")

def decifrar_mensagem(msg_cifrada, chave_privada_n, chave_privada_d):
    print(f"Decifrando a mensagem")
    msg = list()
    for i in range(len(msg_cifrada)):
        print(f"Decifrando letra: {i + 1}/{len(msg_cifrada)}")
        letra = ((msg_cifrada[i] ** chave_privada_d) % chave_privada_n)
        msg.append(chr(letra))

    return ''.join(msg)


# Funcao para ler a criptografia RSA
def ler_rsa(nome_arquivo):
    # Inicialmente ler os dados do arquivo gerado
    mensagem_cifrada = list()
    chave_privada = list()
    hash = 0
    hash_cifrado = 0
    try:
        arquivo = open(nome_arquivo, "rb")
        fileRead = load(arquivo)
        arquivo.close()
        mensagem_cifrada = fileRead["mensagem_cifrada"]
        chave_privada = fileRead["chave_privada"]
        hash = fileRead["hash"]
        hash_cifrado = fileRead["hash_cifrado"]
        print(f"Mensagem cifrada para ser decifrada: {mensagem_cifrada}")
        print(f"Chave Privada: {chave_privada}")
        print(f"Hash: {hash}")
        print(f"Hash cifrado: {hash_cifrado}")
        print(f"Arquivo lido com sucesso {nome_arquivo}")

        # Decifra a mensagem
        mensagem_decifrada = decifrar_mensagem(mensagem_cifrada, chave_privada[0], chave_privada[1])
        hash_cifrado_decifrado = decifrar_mensagem(hash_cifrado, chave_privada[0], chave_privada[1])
        print(f"Mensagem decifrada: {mensagem_decifrada}")
        print(f"Hash decifrado: {hash_cifrado_decifrado}")
        print(f"Hash esperado : {hash}")

        # Calcula e compara os hashes
        hash_msg_decifrada = int.from_bytes(sha512(str.encode(mensagem_decifrada)).digest(), byteorder='big')
        print(f"Hash msg      : {hash_msg_decifrada}")
        if str(hash_msg_decifrada) == str(hash_cifrado_decifrado):
            print(f"Os hashes são iguais")
        else:
            print(f"Os hashes são diferentes")
    except Exception as e:
        print("Não foi possível ler o arquivo. Execute primeiramente a parte de criação dele e verifique se o arquivo gerado está na pasta correta")
        print(e)


# Usamos o comeco do codigo para que o usuario escolha qual operacao deve ser feita: Gerador ou verificar assinatura
if __name__ == '__main__':
    nome_arquivo = "dados.pkl"
    print("Seja bem-vindo!")
    print("Selecione a opção:")
    print("1 - Gerar assinatura")
    print("2 - Verificar assinatura")
    resposta = '0'
    while resposta != '1' and resposta != '2':
        resposta = input("Escolha: ")
    if resposta == '1':
        msg = input("Qual sua mensagem? ")
        criptografar_rsa(msg, nome_arquivo)
    elif resposta == '2':
        ler_rsa(nome_arquivo)
