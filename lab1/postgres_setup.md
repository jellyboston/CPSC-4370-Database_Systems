#### Startup Commands
```bash
conda activate 4370
docker start cpsc437-postgres1
```

Create a new database in the PostgreSQL container:
```bash
docker exec -i cpsc437-postgres-1 psql -U admin -d default_database -c "CREATE DATABASE library"
```