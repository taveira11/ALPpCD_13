<hl>ALPpCD_13</hl>
Pedro Taveira A103616
Duarte Neves A106870



##### Mostrar ajuda para os comandos
Para obter os comandos disponíveis basta executar no terminal o seguinte comando: python jobscli.py help. Este comando fornecerá todos os comandos disponíveis.

# TP1
> Comandos disponíveis
##### 1. Mostrar ajuda para os comandos
Para obter os comandos disponíveis basta executar no terminal o seguinte comando: python jobscli.py --help. Este comando fornecerá todos os comandos disponíveis.
#### 2. Mostrar as vagas mais recentes 
Para mostrar as 'n' vagas mais recentes necessitará de usar o seguinte comando: python jobscli.py top "n" : sendo o "n" o número de vagas que desejará procurar. Caso queira guardar o output fornecido num arquivo CSV basta utilizar o comando: python jobscli.py top "n" --export-csv.
#### 3. Procurar vagas de uma empresa numa localidade específica
Para procurar vagas para uma empresa específica em uma localidade específica, execute o seguinte comando: python jobscli.py search "Localidade" "Nome da Empresa" "Número de vagas". Para salvar os dados num arquivo CSV basta utilizar o comando --export-csv no final do código anterior.
#### 4. Exibir o saláraio de um determinado job_id
Para obtermos o salário de um determinado id de trabalho basta aplicar o comando: python jobscli.py salary "job_id". 
#### 5. Procurar vagas por capacidades dentro de um período de tempo
Para procurar determinadas vagas com determinadas características num determinado intervalo de tempo usamos o comando: python jobscli.py skills ["Capacidade1", "capacidade2"] <data_ini> <data_fim>. Sendo a "data_ini" e a "data_fim" com o formato YYYY-MM-DD. 


# TP2
> Comandos disponíveis
##### 1. Mostrar ajuda para os comandos
Para obter os comandos disponíveis basta executar no terminal o seguinte comando: python jobscli2.py --help. Este comando fornecerá todos os comandos disponíveis.
##### 2. Rating / Descrição / Principais benefícios de trabalhar na empresa
Para obtermos o rating, a decrição e os principais benefícios do site ambitionbox.com através de um JOBID específico  precisamos de usar o seguinte comando: python jobscli2.py get JOB_ID.
Caso queira guardar o output em cima num arquivo CSV basta usar o comando --export-csv no final do código anterior.
#### 3. Criar uma contagem de vagas por localidade 
Para sabermos quais são os trabalhos disponíveis naquela localidade e qual o regime de trabalho (part-time ou full-time) usamos o comando: python jobscli2.py statistics "Distrito".
#### 4. Principais skills do TOP 10 de cada tipo de trabalho
Para sabermos quais as principais skills de um certo trabalho precisamos de recorrer ao site https://www.ambitionbox.com/jobs?campaign=desktop_nav , escrever o nome da profissão que desejamos e pesquisarmos, de seguida vamos à CLI e usamos o comando : python jobscli2.py list-skills "url".
Sendo o url : https://www.ambitionbox.com/jobs/data-scientist-jobs-prf, por exemplo.
#### 5. Rating/ Descrição / Principais benefícios de trabalhar na empresa 
Para fazermos o mesmo que no ponto 2. mas para o site https://pt.indeed.com/ necessitamos de utilizar o seguinte comando: python jobscli2.py get2 JOB_ID
