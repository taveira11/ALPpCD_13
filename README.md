<hl>ALPpCD_13</hl>
Pedro Taveira A103616
Duarte Neves A106870

# TP1
> Comandos disponíveis
##### 1. Mostrar ajuda para os comandos
Para obter os comandos disponíveis basta executar no terminal o seguinte comando: python jobscli.py help. Este comando fornecerá todos os comandos disponíveis.
#### 2. Mostrar as vagas mais recentes 
Para mostrar as 'n' vagas mais recentes necessitará de usar o seguinte comando: python jobscli.py top "n" : sendo o "n" o número de vagas que desejará procurar. Caso queira guardar o output fornecido num arquivo CSV basta utilizar o comando: python jobscli.py top "n" --export-csv.
#### 3. Procurar vagas de uma empresa numa localidade específica
Para procurar vagas para uma empresa específica em uma localidade específica, execute o seguinte comando: python jobscli.py search "Localidade" "Nome da Empresa" "Número de vagas". Para salvar os dados num arquivo CSV basta utilizar o comando --export-csv no final do código anterior.
#### 4. Exibir o saláraio de um determinado job_id
Para obtermos o salário de um determinado id de trabalho basta aplicar o comando: python jobscli.py salary "job_id". 
#### 5. Procurar vagas por capacidades dentro de um período de tempo
Para procurar determinadas vagas com determinadas características num determinado intervalo de tempo usamos o comando: python jobscli.py skills ["Capacidade1", "capacidade2"] <data_ini> <data_fim>. Sendo a "data_ini" e a "data_fim" com o formato YYYY-MM-DD. 


# TP2
