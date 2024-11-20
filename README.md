## Objetivo

O objetivo desse repositório é prover uma solução para o [desafio](https://github.com/pier-cloud/vaga-engenheiro-de-software/blob/main/README.md) proposto pela PierCloud.

<!-- ## Visão geral -->

## Instalação

Este projeto utiliza [python](https://www.python.org/) e [rabbitmq](https://www.rabbitmq.com/). Para instalar as dependências é necessário que o [poetry](https://python-poetry.org/) esteja instalado.

```sh
poetry install
```

As configurações ficam em variáveis de ambiente e devem ser informadas no arquivo `.env`. O arquivo `.env-example` tem um exemplo de configuração.

## Uso

Aqui temos duas unidades.


![img](visao-geral.png)

- *Publisher* que é responsável por consumir a API de vendendores e publicar no rabbitmq. Depois de todo o envio, o serviço é finalizado
- *Consumer* que é responsável por consumir as mensagens enviadas pelo publisher, e para cada vendedor gerar um `CSV` com dados consolidados de vendas obtidos nas APIs de vendas, clientes e produtos. Uma vez iniciado, fica aguardando por novas mensagens.

Para rodar o publisher:
```sh
task publisher
```

Para rodar o consumer:
```sh
task consumer
```
Caso necessite, pode iniciar mais `consumers` executando o comando acima em outros terminais.

Executando o `docker-compose.yml` um container rabbitmq é iniciado.  

### Observações

- A variável de ambiente `DELAY_IN_SECONDS` está sendo utilizada para retardar novas requisições quando as APIs não estão ok (por exemplo retornando 429, 500, 503...). Como podem ser executados _n_ **consumers**, uma solução de requests/segundo não foi efetiva.
- Adicionar mais cenários de teste. 
