from math import sqrt

# Криптосистема Рабина

def is_prime(num):
    '''
    Стандартная функция проверки на простоту числа
    '''
    if(num == 2):
        return True
    for i in range(2, int(sqrt(num))):
        if num % i == 0:
            return False
    return True

def sieve(num):
    '''
    Решето Эратосфена
    '''
    S = [1 for k in range(num+1)]
    S[1] = 0
    k = 2

    while (k * k <= num):
        if S[k] == 1:
            l = k*k
            while (l <= num):
                S[l] = 0
                l += k
        k += 1

    return S

def chek_input(*, p, q, b, n):
    ''' 
    Проверка на корректность введенных ключей
    '''
    if (p % 4 == 3 and q % 4 == 3 and 0 != b < n and is_prime(p) and is_prime(q) and n > 255):
        return True
    return False


def file_encrypt(filename, n, b):
    '''
    Шифрование файла открытыми ключами b и n
    Возвращает 0 при успешном шифровании
    '''
    #const
    buff_size = 0x4000
    
    f_out = open(filename + ".enc", "w")

    with open(filename, "rb") as f:
        #Бесконечный цикл чтения из файла
        while True: 
            fdata = f.read(buff_size)
            out_data = []
            if fdata: #шифрование того, что прочитано: 
                for byte in fdata:
                    f_out.write(str(((byte * (byte + b)) % n)))
                #    out_data.append((byte * (byte + b) % n))
                #f_out.write(out_data)
            else: #если ничего не прочитано - выход из цикла
                break
    f_out.close()
    f.close()
    return 0

file_encrypt("test.jpg", 39203, 13)
    



    
    










    
            
    
