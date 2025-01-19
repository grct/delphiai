import os

folder_path = r'..\docs\vanna'

def training(vn):
    vn.connect_to_mysql(host=os.getenv('DB_HOST'), dbname=os.getenv('DB_NAME'), user=os.getenv('DB_USER'),
                        password=os.getenv('DB_PASSWORD'), port=3306)
    vn.train(
        documentation="Il database che stai visualizzando contiene tutti i ristoranti, piatti e tecniche utilizzati nei diversi pianeti del Ciclo Cosmico. ")

    for file_name in os.listdir(folder_path):
        if file_name.endswith('.txt'):
            full_path = os.path.join(folder_path, file_name)
            with open(full_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()
                for line in lines:
                    vn.train(documentation=line.strip())

    vn.train(question="Quali sono i piatti che includono le Chocobo Wings come ingrediente?",
             sql="""
                        SELECT id_piatto FROM PIATTI_INGREDIENTI PI
                        INNER JOIN INGREDIENTI I ON PI.id_ingrediente = I.id
                        WHERE I.nome LIKE '%Chocobo%' 
                    """)
    vn.train(question="Trova i piatti che utilizzano la tecnica Marinatura a Infusione",
             sql="""
                        select PT.id_piatto from PIATTI_TECNICHE PT
                        INNER JOIN TECNICHE T ON PT.id_tecnica = T.id
                         where T.descrizione LIKE '%Marinatura a infusione%'
                    """)
    vn.train(question="Dimmi tutti i telefoni Samsung con 12 GB di RAM.",
             sql="""
                        SELECT p.Brand,p.Model, p.id
                        FROM Product p
                        JOIN Product_Stats ps ON p.Product_Stats = ps.Id
                        WHERE p.Brand = 'SAMSUNG' AND ps.RAM = '12 GB';
                    """)
    vn.train(question="Mostra tutti i telefoni Google con più di 128 GB di memoria ROM",
             sql="""
                        SELECT p.Model, p.Price, ps.ROM, p.id
                        FROM Product p
                        JOIN Product_Stats ps ON p.Product_Stats = ps.Id
                        WHERE p.Brand = 'Google'
                        AND CAST(SUBSTRING_INDEX(ps.ROM, ' ', 1) AS UNSIGNED) > 128;
                    """)

    vn.train(documentation="Includi sempre nella risposta la colonna product.id")