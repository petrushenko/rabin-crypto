from math import sqrt

# Криптосистема Рабина

#const
buff_size = 0x4000

#def fest_exp():


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
    Возвращает list с шифротекстом при успешном шифровании
    '''
    
    f_out = open(filename + ".enc", "w")
    out_data = []
    with open(filename, "rb") as f:
        #Бесконечный цикл чтения из файла
        while True: 
            fdata = f.read(buff_size)
            if fdata: #шифрование того, что прочитано: 
                for byte in fdata:
                    out_data.append((byte * (byte + b)) % n)
            else: #если ничего не прочитано - выход из цикла
                break
        for item in out_data:
            f_out.write(str(item) + " ")
        f.close()
        f_out.close()
    return out_data

def decrypt(c, p, q, b):
    '''
    Дешифровка одного элемента шифротекста
    Возвращает List исходных элементов
    '''
    n = p * q #открытый ключ
    # D - дискриминант
    D = (b ** 2 + 4 * c) % n
    # Нахождение корня квадратного из D (fast EXP)
    mp = (D ** ((p + 1)//4)) % p 
    mq = (D ** ((q + 1)//4)) % q

    #Расширенный алгоритм евклида
    yp, yq, _gcd = extended_euclid(p, q) #третий возвращаемый параметр не используется
    
    
    # di - корень из дискриминанта
    d1 = (yp * p * mq + yq * q * mp) % n 
    d2 = n - d1
    d3 = (yp * p * mq - yq * q * mp) % n
    d4 = n - d3

    d = (d1, d2, d3, d4)
    m = [] #исходные варианты сообщений
    for di in d:
        if (di - b) % 2 == 0:
            m.append(int(((-b + di) / 2) % n))
        else:
            m.append(int(((-b + di + n) / 2) % n))
    return m

def extended_euclid(a, b):
    '''
    Расширенный алгоритм Евклида
    НОД(a, b) = x * a + y * b
    Возвращает (x, y, gcd)
    '''

    #Индекс 1 - текущий элемет, 0 - предыдущий
    x0, x1 = 1, 0
    y0, y1 = 0, 1
    while b:
        # r2 = r0 - r1 * q
        # r - остаток от деления
        # q целая часть от a / b 
        q = a // b 

        a, b = b, a % b

        # чтобы не создавать промежуточные переменные, присваивание кортежем
        x0, x1 = x1, x0 - x1 * q
        y0, y1 = y1, y0 - y1 * q
    return (x0, y0, a)                

def file_decrypt(filename, p, q, b):
    '''
    Процедура дешифровки файла
    ******
    '''
    #замени расширения файла
    f_split = filename.split(".")
    f_expansion = f_split[len(f_split) - 1] # финт ушами: f_expansion = f_split[-1]
    if f_expansion == "enc":
        filename_out = filename.replace(f_expansion, "dec") 
    
    f_out = open(filename_out, "wb")
    out_data = bytearray([])
    with open(filename, "r") as f:
        #бесконечный цикл чтения из файла
        while True:
            fdata_str = f.read(buff_size)
            fdata_str = fdata_str.strip()
            if fdata_str:
                fdata = fdata_str.split(" ") #получение значений шифротекста из файла
                for item in fdata:
                    m = decrypt(int(item), p, q, b)
                    for i in range(len(m)):
                        if m[i] <= 255:
                            out_data.append(m[i])
            else:
                break
        f.close()

    f_out.write(out_data)
    f_out.close()
    return out_data    


file_encrypt("test.jpg", 11*31, 173)
file_decrypt("test.jpg.enc", 11, 31, 173)



    
    










    
            
    
