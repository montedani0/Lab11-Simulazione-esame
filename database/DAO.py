from oauthlib.uri_validate import query

from database.DB_connect import DBConnect
from model.arco import Arco
from model.customer import Customer


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getNaz():
        conn = DBConnect.get_connection()
        results = []
        cursor = conn.cursor(dictionary=True)
        query = (""" select distinct c.Country 
                from customer c 
                 """)
        cursor.execute(query)
        for row in cursor:
            results.append(row['Country'])

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getCustomer(nazione):
        conn = DBConnect.get_connection()
        results = []
        cursor = conn.cursor(dictionary=True)
        query = ("""select c.CustomerId , c.FirstName , c.LastName ,c.Country 
from customer c 
where c.Country = %s
                    """)
        cursor.execute(query,(nazione,))
        for row in cursor:
            results.append(Customer(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getEdge(nazione, idMap):
        conn = DBConnect.get_connection()
        results = []
        cursor = conn.cursor(dictionary=True)
        query = ("""select C1.customerid as f1 , C2.customerid as f2 ,count(C1.genreid ) as peso
from (select distinct c.CustomerId, t.GenreId 
from customer c ,invoice i ,invoiceline il,track t  
where c.CustomerId =i.CustomerId and i.InvoiceId =il.InvoiceId and il.TrackId = t.TrackId
and c.Country = %s) as C1, (select distinct c.CustomerId, t.GenreId 
from customer c ,invoice i ,invoiceline il,track t  
where c.CustomerId =i.CustomerId and i.InvoiceId =il.InvoiceId and il.TrackId = t.TrackId
and c.Country =  %s) as C2
where C1.customerid > C2.customerid and C1.genreid = C2.genreid 
group by C1.customerid, C2.customerid 
                        """)
        cursor.execute(query, (nazione,nazione,))
        for row in cursor:
            results.append(Arco(idMap[row["f1"]], idMap[row["f2"]], row["peso"]))

        cursor.close()
        conn.close()
        return results



