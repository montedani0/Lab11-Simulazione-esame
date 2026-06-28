from oauthlib.uri_validate import query

from database.DB_connect import DBConnect
from model.artista import Artista
from model.edge import Edge
from model.genre import Genre


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def AllGenre():
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        result = []
        query = """select *
                   from  genre g 
"""
        cursor.execute(query)
        for row in cursor:
            result.append(Genre(**row))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def allArtist():
        conn = DBConnect.get_connection()
        results = []
        cursor = conn.cursor(dictionary=True)
        query = ("""select ar.*
                 from artist ar
                      """)
        cursor.execute(query)
        for row in cursor:
            results.append(Artista(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllNodes(genre):
        conn = DBConnect.get_connection()
        results = []
        cursor = conn.cursor(dictionary=True)
        query = ("""
                     select distinct ar.*
                     from album a, track t , artist ar
                     where a.AlbumId = t.AlbumId and a.ArtistId = ar.ArtistId   and t.GenreId = %s
                     """)
        cursor.execute(query, (genre,))
        for row in cursor:
            results.append(Artista(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllEdge(genre, idMap):
        conn = DBConnect.get_connection()
        results = []
        cursor = conn.cursor(dictionary=True)
        query = ("""            
                select c1.artistid as a1 , c2.artistid as a2, c1.p1 + c2.p1  as peso
                 from (select i.CustomerId ,p.ArtistId , p.popolarity as p1
                       from invoice i , invoiceline il, track t , album al, 
                             (select ar.ArtistId , SUM(il.Quantity ) as popolarity
                             from artist ar,invoiceline il, track t , album al
                             where il.TrackId =t.TrackId  and al.AlbumId = t.AlbumId and al.ArtistId =ar.ArtistId and t.GenreId = %s 
                             group by ar.ArtistId ) as p
                     where i.InvoiceId = il.InvoiceId and il.TrackId =t.TrackId  and al.AlbumId = t.AlbumId 
                     and p.ArtistId = al.ArtistId and t.GenreId =%s  ) as c1, 
                     (select i.CustomerId ,p.ArtistId , p.popolarity as p1
                       from invoice i , invoiceline il, track t , album al, 
                             (select ar.ArtistId , SUM(il.Quantity ) as popolarity
                             from artist ar,invoiceline il, track t , album al
                             where il.TrackId =t.TrackId  and al.AlbumId = t.AlbumId and al.ArtistId =ar.ArtistId and t.GenreId =%s  
                             group by ar.ArtistId ) as p
                     where i.InvoiceId = il.InvoiceId and il.TrackId =t.TrackId  and al.AlbumId = t.AlbumId 
                     and p.ArtistId = al.ArtistId and t.GenreId =%s  ) as c2
                 where c1.customerid = c2.customerid and c1.artistid != c2.artistid
                 and c1.p1 >= c2.p1 
                 group by c1.artistid , c2.artistid
    """)
        cursor.execute(query, (genre, genre, genre, genre,))
        for row in cursor:
            results.append(Edge(idMap[row["a1"]], idMap[row["a2"]], row["peso"]))
        cursor.close()
        conn.close()
        return results



