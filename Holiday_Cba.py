from datetime import date
from workalendar.america import Brazil
from workalendar.america import BrazilMatoGrosso
from workalendar.america import BrazilCuiabaCity 
import holidays # lib para feriados estaduais e nacionais 
import cx_Oracle # lib para conexao com o banco oracle

cx_Oracle.init_oracle_client(lib_dir=r"C:\app\client\...")

conn = cx_Oracle.connect(user="...",password="...",dsn="host:port/service_name")
cursor = conn.cursor()

# criando uma instância para o calendário de cuiabá
cuiaba = BrazilCuiabaCity()

year = date.today().year # ano atual
cuiaba_feriados = cuiaba.holidays(year) # feriados municipais

feriados_pt = holidays.BR() # utilizando a biblioteca holidays eu instancio um objeto da classe holidays
                            # isso porque a classe holidays fornece o nome dos feriados nacionais em portugues

for holidays in sorted(cuiaba_feriados):
    nome_feriado = feriados_pt.get(holidays[0])
    
    if nome_feriado == None: # verifico se o nome_feriado esta vazio, se tiver é porque trata de um nome de um feriado municipal
        print(holidays[0], holidays[1])
    else:
        print(holidays[0], nome_feriado)



try:
    cursor.execute("select * from feriados")
except cx_Oracle.DatabaseError as e:
    cursor.execute("create table feriados (data_feriado date primary key, nome varchar2(50))")

for holidays in sorted(cuiaba_feriados):
    nome_feriado = feriados_pt.get(holidays[0])   # metodo para receber um nome de um feriado a partir de uma data
                                             # isso porque a classe holidays fornece o nome dos feriados nacionais em portugues

                                 # feriados municipais tem o nome em portugues usando a classe BrazilCuiabaCity
    if nome_feriado == None: # verifico se o nome_feriado esta vazio, se tiver é porque trata de um nome de um feriado municipal
        nome_feriado = holidays[1] # entao uso o nome do feriado vindo da classe BrazilCuiabaCity
    cursor.execute("insert into feriados (data_feriado, nome) values (to_date(:data, 'dd/mm/yyyy'), :nome)",{'data': holidays[0].strftime("%d/%m/%Y"), 'nome': nome_feriado})
    conn.commit()
