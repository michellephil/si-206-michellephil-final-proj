import unittest
import json
import sqlite3
import proj4_cherrios as proj4

file_name = open('cache.json', 'r')
sample_json = json.load(file_name)
file_name.close()

DBNAME = 'cheerios.db'

class TestProducts(unittest.TestCase):
    def test_constructor(self):
        m1 = proj4.Products('Honey Nut Cheerios Medley Crunch', 'Crispy flakes and crunchy clusters come together to create a delicious breakfast cereal.', '120 calories 17g Whole Grains*', 'https://www.cheerios.com/~/media/06C09DA13BAD4DCFA718DE4863A8D9EE.ashx', '8')

        self.assertEqual(m1.product_name, 'Honey Nut Cheerios Medley Crunch')
        self.assertEqual(m1.product_description, 'Crispy flakes and crunchy clusters come together to create a delicious breakfast cereal.')
        self.assertEqual(m1.product_calories_and_wg, '120 calories 17g Whole Grains*')
        self.assertEqual(m1.product_pic, 'https://www.cheerios.com/~/media/06C09DA13BAD4DCFA718DE4863A8D9EE.ashx')

    def test_str(self):
        m1 = proj4.Products('Honey Nut Cheerios Medley Crunch', 'Crispy flakes and crunchy clusters come together to create a delicious breakfast cereal.', '120 calories 17g Whole Grains*', 'https://www.cheerios.com/~/media/06C09DA13BAD4DCFA718DE4863A8D9EE.ashx', '8')

class TestTwitterTable(unittest.TestCase):
    def test_constructor(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()
        sql = '''
            SELECT TweetId, TweetText, RetweetCount, UserId, ScreenName, Location, FollowerCount FROM Tweets '''
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertEqual(len(result_list), 100)
        self.assertEqual(result_list[2][4], 'JAIMON777')
        conn.close()

    def test_2(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()
        sql = 'SELECT UserId FROM Tweets'
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertIn(('99783978',), result_list)
        self.assertEqual(len(result_list), 100)

class TestDatabase(unittest.TestCase):
    def test_products_table(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()

        sql = 'SELECT ProductName FROM Products'
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertIn(('Original Cheerios',), result_list)
        self.assertEqual(len(result_list), 18)

        sql = '''
            SELECT ProductId, ProductName, ProductDesc,
                   Calories, Picture
            FROM Products
        '''
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertEqual(len(result_list), 18)
        self.assertEqual(result_list[0][3], '110\ncalories\n\n\n17g\nWhole Grains*')
        conn.close()

    def test_products_table(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()

        sql = 'SELECT ProductDesc FROM Products'
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertIn(('A family favorite for years now has more protein with a taste your whole family will love.',), result_list)
        self.assertEqual(len(result_list), 18)

    def test_tweets_table(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()
        sql = 'SELECT UserId FROM Tweets'
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertIn(('99783978',), result_list)
        self.assertEqual(len(result_list), 100)

        sql = '''
            SELECT TweetId, TweetText, RetweetCount, UserId, ScreenName, Location, FollowerCount FROM Tweets '''
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertEqual(len(result_list), 100)
        self.assertEqual(result_list[1][3], '508320794')
        conn.close()

    def test_tweets_table_location(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()
        sql = 'SELECT Location FROM Tweets'
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertEqual(len(result_list), 100)

    def test_tweets_table_retweets(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()
        sql = 'SELECT RetweetCount FROM Tweets'
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertEqual(len(result_list), 100)

unittest.main()
