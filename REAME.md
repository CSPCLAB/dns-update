## DNS 관리
> godaddy DNS 자동 업데이트

`cspc.me`  goddady 유료 도메인 결재중

해당 도메인을 통해 여러 DNS들을 관리중인데 오픈소스 라이브러리인 certbot을 통해 SSL 인증서 발급

### certbot
현재 인증서 확인
```shell
certbot certificates
```

certbot은 한번 발급하면 인증서 만료기간이 3개월이라 반복해서 갱신해줘야함

인증서 갱신
```
certbot renew
```
일반적인 인증서들은 해당 명령어를 통해 인증서 재발급

> 인증서를 갱신할때는 80포트를 사용하므로 웹서버를 끄고 진행해야함 $apache2ctl stop

### wildcard 인증서 재발급
인증서중에 wildcard 인증서가 있는데 해당 renew 명령어로는 재발급 불가함

certbot이 발급한  `_acme-challenge` Text 를 godaddy에 등록해서 이를 확인하는 방식으로 인증서가 발급되는데

`godaddy-dns-update.py` 스크립트가 godaddy API를 통해 Text를 등록후 업데이트까지 기다림

```shell
./update_certificate.sh
```
해당 스크립트를 실행하여 자동으로 DNS 업데이트 진행

### Cron job
해당 스크립트는 한달마다 실행되도록 root cronjob 등록되어 있음

cronjob 수정
```
crontab -e
```