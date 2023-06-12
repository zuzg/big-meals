# big-meals
The project is inspired on food saving concepts - toogoodtoogo and Foodsi.

## User interface
You can switch between four subpages:
* Admin - global view of all available meals and reservation. You can add more meals to the database or truncate tables.
* User Zuza - user view. You can reserve meals, add notes to reservations or cancel them
* User Agata - second user view. Same functionalities as User Zuza
* Stress tests - here you can run all stress tests

## Run
1. Prepare Cassandra clusters: run script `create.sh` from the docker directory.
2. Clone this repository.
3. Create environment (you can use `environment.yml` with conda)
4. Run from the project directory
```bash
streamlit run app.py
```