## Pacotes necessários:

* nginx
* Python 3.8
* virtualenv + pip
* Git

Por exemplo, no Ubuntu:

    sudo apt-get install nginx git python38 python3.8-venv

## Configuração do Nginx Virtual Host

* veja nginx.template.conf
* substitua SITENAME, por seu domínio `(meu-dominio.com)`
* substitua dantas, por seu `username`

## Serviço Systemd

* veja gunicorn-systemd.template.service
* substitua SITENAME, por seu domínio `(meu-dominio.com)`
* substitua dantas, por seu `username`

## Estrutura de pastas:
Supondo que temos um usuário em /home/username

```
/home/username
└─ sites
   └─ SITENAME
      └─ database
      └─ source
      └─ static
      └─ virtualenv
```