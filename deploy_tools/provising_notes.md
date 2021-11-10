## Pacotes necessários:

* nginx
* Python 3.6
* virtualenv + pip
* Git

Por exemplo, no Ubuntu:

    sudo apt-get install nginx git python36 python3.6-venv

## Configuração do Nginx Virtual Host

* veja nginx.template.conf
* substituir SITENAME, por seu domínio `(meu-dominio.com)`
* substituir USER, por seu `username`

## Serviço Systemd

* veja gunicorn-systemd.template.service
* substitua SITENAME, por seu domínio `(meu-dominio.com)`
* * substituir user, por seu `username`

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