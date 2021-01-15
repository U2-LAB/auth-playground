# auth-playground
## Start services
1. Clone repo
2. Install docker and docker-compose
3. Run
```bash
docker-compose up -d
```
### Create super user for sourth-of-truth
1. Start bash in sourth-of-truth container
```bash
docker exec -it auth-playground_auth-portal bash
```
2. Create admin user
```bash
/bin/python3 source_of_truth/manage.py createsuperuser
```
3. Choose username and password
5. Exit from container
```bash
exit
```
