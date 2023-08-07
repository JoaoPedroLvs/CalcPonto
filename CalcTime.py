import os, platform, psycopg2

totalHour
totalMinute
totalDays
system = platform.system()
option = 0;

def calc(hour, min, multiplier):
    global totalHour, totalMinute, totalDays
    totalHour += int(hour) * multiplier
    totalMinute += int(min) * multiplier
    
    if (totalMinute < 0):
        totalHour -= 1
        totalMinute += 60
    
    if (totalHour < 0):
        totalDays -= 1
        totalHour += 24
    
    if (totalMinute >= 60):
        totalHour += 1
        totalMinute -= 60
    
    if (totalHour >= 24):
        totalDays += 1
        totalHour -= 24
    

def setTime():
    
    global totalHour, totalMinute, totalDays
    
    try:
        conn = psycopg2.connect(host="localhost",database="ponto", user="postgres", password="postgres")
        cur = conn.cursor()
        totalDays = cur.execute("SELECT days FROM saldo ORDER BY id DESC LIMIT 1")
        totalHour = cur.execute("SELECT hours FROM saldo ORDER BY id DESC LIMIT 1")
        totalMinute = cur.execute("SELECT minutes FROM saldo ORDER BY id DESC LIMIT 1")
        cur.close()
        conn.close()
        
    except (Exception, psycopg2.DatabaseError) as error:
        print('Não foi possível salvar no banco: ', error)

    
def getTime():
    global totalHour, totalMinute, totalDays
    
    return str(totalDays) + 'd ' + str(totalHour) + 'h ' + str(totalMinute) + 'm'
    

setTime()
print('1 - Calcular horas')
print('2 - Ver saldo atual')
print('3 - Sair')
option = input('Digite sua opção: ')

while  option != '3':
    
    if option == '1':
        multiplier = 1
        hour, min = input('Digite o tempo que você fez na semana: ').split(' ')
        
        if '-' in hour:
            hour.replace('-', '')
            multiplier = -1
        
        calc(hour, min, multiplier)
        
        
        if system == 'Windows':
            os.system('cls')
        elif system == 'Linux':
            os.system('clear')
        
        print('Seu saldo atual de horas é: ', getTime())
            
    elif option == '2':
        print('Seu saldo atual de horas é: ', getTime())

    else:
        print('Opção inválida!')
    
    print('1 - Calcular horas')
    print('2 - Ver saldo atual')
    print('3 - Sair')
    option = input('Digite sua opção: ')
    
save = input('Deseja salvar o saldo atual? (s/n) ')

if save == 's':
    try:
        conn = psycopg2.connect(host="localhost",database="ponto", user="postgres", password="postgres")
        cur = conn.cursor()
        cur.execute("INSERT INTO saldo (days, hour, minutes) VALUES (%s, %s, %s)", (totalDays, totalHour, totalMinute))
        conn.commit()
        cur.close()
        conn.close()
        print('Saldo salvo com sucesso!')
    except (Exception, psycopg2.DatabaseError) as error:
        print('Não foi possível salvar no banco: ', error)