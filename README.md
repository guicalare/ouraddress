# ouraddress

```
git clone https://github.com/guicalare/ouraddress.git
cd ouraddress
sudo docker build -t ouraddress .
sudo docker run -ti --network host ouraddress_v6:latest
cd ouraddress
python3 ui-server.py
```
