Link to project docs- https://docs.google.com/document/d/1V400O_kI9OInR3E6nqbkzn43qCVtPkT29pzhgIPvJ6A/edit?usp=sharing

DataSets-
https://mailtauacil-my.sharepoint.com/:f:/g/personal/estertkach_mail_tau_ac_il/IgCoo6KQJvaFRagY4IRDZW11AYesNT-0K6gkNcuXLhoHgOQ?e=VPvzd8


LIORA-
1) Add the 2 .parquet files Esty made to the /data folder.
2) To build the OFFLINE Content-Based Model, run: python api/ml/train_content_based.py
3) To get Content Based recommendations see functions in  file: api/ml/cb_recommender.py
4) To build the OFFLINE Item-Based Collaborative Filtering Model, run: python api/ml/train_item_cf.py
5) To get Collaborative Filtering recommendations, see functions in: api/ml/cf_recommender.py

AYA (if not docker)- 
1) Change config.py to allow data versoning
2) Created api folder - FastApi server, cold start run: python -m uvicorn api.main:app --reload
3) Added requirements.txt file. In order to install all: cd api, and only then, pip install -r requirements.txt 

Docker-
1) Make sure your docker app is open.
2) Open start.bat
3) Will open server, front and log if needed. 
4) First load takes half a minute. Future loads take a few seconds. 
5) To close follow console instructions. 

for mac users 😁
1) chmod +x start.sh
2) ./start.sh


Or, regular way will also work: 
cd api
python -m venv venv
source venv/bin/activate        # Mac/Linux
pip install -r requirements.txt
python -m uvicorn api.main:app --reload