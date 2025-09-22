#### Startup Commands
```bash
conda activate 4370
docker start cpsc437-postgres-1
```

Create a new database in the PostgreSQL container:
```bash
docker exec -i cpsc437-postgres-1 psql -U admin -d default_database -c "CREATE DATABASE library"
```

Ensure user has all privileges on the database:
```bash
docker exec -i cpsc437-postgres-1 psql -U admin -d library -c "GRANT ALL PRIVILEGES ON DATABASE library TO admin"
```

To query the database:
```bash
docker exec -it cpsc437-postgres-1 psql -U admin -d {db}
```