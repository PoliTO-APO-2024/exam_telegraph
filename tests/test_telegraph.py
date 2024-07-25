import unittest
from telegraph.telegraph_manager import TelegraphManager
from telegraph.exceptions import TelegraphException
from telegraph.elements import Symbol


class TestR1(unittest.TestCase):
    def setUp(self):
        self._mg = TelegraphManager()

    def test_add_station(self):
        self.assertEqual(1, self._mg.add_station("City1"))
        self.assertEqual(2, self._mg.add_station("City2"))
        self.assertEqual(3, self._mg.add_station("City3"))
        self.assertEqual(3, len(self._mg.stations))
        self.assertEqual({"City1", "City2", "City3"}, set(self._mg.stations))

    def test_add_station_duplicates(self):
        self.assertEqual(1, self._mg.add_station("City1"))
        self.assertEqual(2, self._mg.add_station("City2"))
        self.assertEqual(2, self._mg.add_station("City1"))
        self.assertEqual(2, len(self._mg.stations))
        self.assertEqual({"City1", "City2"}, set(self._mg.stations))

    def test_add_message(self):
        self._mg.add_station("City1")
        self._mg.add_station("City2")
        self._mg.add_station("City3")

        msg1 = self._mg.add_message("text1", "City1", "City2")
        msg2 = self._mg.add_message("text2", "City2", "City3")        
        
        self.assertEqual("text1", msg1.text)
        self.assertEqual("City1", msg1.sender)
        self.assertEqual("City2", msg1.receiver)

        self.assertEqual("text2", msg2.text)
        self.assertEqual("City2", msg2.sender)
        self.assertEqual("City3", msg2.receiver)
    
    def test_message_len(self):
        self._mg.add_station("City1")
        self._mg.add_station("City2")

        msg1 = self._mg.add_message("text1", "City1", "City2")
        msg2 = self._mg.add_message("text1234", "City1", "City2")

        self.assertEqual(5, len(msg1))
        self.assertEqual(8, len(msg2))

    def test_add_message_exceptions(self):
        self._mg.add_station("City1")
        self._mg.add_station("City2")
        msg1 = self._mg.add_message("text1", "City1", "City2")

        self.assertRaises(TelegraphException, self._mg.add_message, "text2", "City2", "City3")
        self.assertRaises(TelegraphException, self._mg.add_message, "text3", "City3", "City1")
        self.assertRaises(TelegraphException, self._mg.add_message, "text3", "City3", "City4")


class TestR2(unittest.TestCase):
    def setUp(self):
        self._mg = TelegraphManager()
        self._mg.add_station("City1")
        self._mg.add_station("City2")
        self._mg.add_station("City3")
        self._mg.add_station("City4")
        self._mg.add_station("City5")
        self._mg.add_station("City6")

    def test_destinations_by_frequency(self):
        self._mg.add_message("hello", "City2", "City1")
        self._mg.add_message("hello", "City3", "City1")
        self._mg.add_message("hello", "City4", "City1")
        self._mg.add_message("hello", "City1", "City2")
        self._mg.add_message("hello", "City3", "City2")
        self._mg.add_message("hello", "City1", "City3")
        self._mg.add_message("hello", "City2", "City3")
        self._mg.add_message("hello", "City3", "City4")
        self._mg.add_message("hello", "City5", "City4")
        self._mg.add_message("hello", "City6", "City5")
        self._mg.add_message("hello", "City5", "City6")

        freq = self._mg.get_destinations_by_frequency()
        self.assertEqual({1, 2, 3}, set(freq.keys()))
        self.assertEqual({"City1"}, set(freq[3]))
        self.assertEqual({"City2", "City3", "City4"}, set(freq[2]))
        self.assertEqual({"City5", "City6"}, set(freq[1]))

    def test_destinations_by_frequency_zero(self):
        self._mg.add_message("hello", "City2", "City1")
        self._mg.add_message("hello", "City3", "City1")
        self._mg.add_message("hello", "City4", "City1")
        self._mg.add_message("hello", "City1", "City2")
        self._mg.add_message("hello", "City3", "City2")
        self._mg.add_message("hello", "City3", "City4")
        self._mg.add_message("hello", "City5", "City4")
        self._mg.add_message("hello", "City6", "City5")

        freq = self._mg.get_destinations_by_frequency()
        self.assertEqual({0, 1, 2, 3}, set(freq.keys()))
        self.assertEqual({"City1"}, set(freq[3]))
        self.assertEqual({"City2", "City4"}, set(freq[2]))
        self.assertEqual({"City5"}, set(freq[1]))
        self.assertEqual({"City3", "City6"}, set(freq[0]))

    def test_destinations_by_frequency_sorted(self):
        self._mg.add_message("hello", "City3", "City4")
        self._mg.add_message("hello", "City5", "City4")
        self._mg.add_message("hello", "City2", "City1")
        self._mg.add_message("hello", "City1", "City3")
        self._mg.add_message("hello", "City2", "City3")
        self._mg.add_message("hello", "City1", "City2")
        self._mg.add_message("hello", "City3", "City2")        
        self._mg.add_message("hello", "City6", "City5")
        self._mg.add_message("hello", "City5", "City6")

        freq = self._mg.get_destinations_by_frequency()
        self.assertEqual({1, 2}, set(freq.keys()))
        self.assertEqual(["City1", "City5", "City6"], freq[1])
        self.assertEqual(["City2", "City3", "City4"], freq[2])

    def test_most_frequent_exchange(self):
        self._mg.add_message("hello", "City1", "City2")
        self._mg.add_message("hello", "City1", "City2")
        self._mg.add_message("hello", "City3", "City4")
        self._mg.add_message("hello", "City3", "City4")
        self._mg.add_message("hello", "City3", "City4")
        self._mg.add_message("hello", "City5", "City6")

        mf = self._mg.get_most_frequent_exchange()

        self.assertEqual(2, len(mf))
        self.assertEqual({"City3", "City4"}, set(mf))

    def test_most_frequent_exchange_bidir(self):
        self._mg.add_message("hello", "City1", "City2")
        self._mg.add_message("hello", "City1", "City2")
        self._mg.add_message("hello", "City1", "City2")
        self._mg.add_message("hello", "City3", "City4")
        self._mg.add_message("hello", "City4", "City3")
        self._mg.add_message("hello", "City3", "City4")
        self._mg.add_message("hello", "City4", "City3")
        self._mg.add_message("hello", "City5", "City6")

        mf = self._mg.get_most_frequent_exchange()

        self.assertEqual(2, len(mf))
        self.assertEqual({"City3", "City4"}, set(mf))


class TestR3(unittest.TestCase):
    def setUp(self):
        self._mg = TelegraphManager()

    def test_add_character_encoding(self):
        self.assertEqual(".", self._mg.add_character_encoding("h", Symbol.DOT, previous=None))
        self.assertEqual("..", self._mg.add_character_encoding("e", Symbol.DOT, previous="h"))
        self.assertEqual(".-", self._mg.add_character_encoding("l", Symbol.DASH, previous="h"))
        self.assertEqual("..-", self._mg.add_character_encoding("o", Symbol.DASH, previous="e"))
        self.assertEqual(".-.", self._mg.add_character_encoding("w", Symbol.DOT, previous="l"))
        self.assertEqual(".--", self._mg.add_character_encoding("a", Symbol.DASH, previous="l"))
        self.assertEqual("...", self._mg.add_character_encoding("r", Symbol.DOT, previous="e"))
        self.assertEqual("-", self._mg.add_character_encoding("y", Symbol.DASH, previous=None))
        self.assertEqual("-.", self._mg.add_character_encoding("u", Symbol.DOT, previous="y"))        

    def test_add_character_ecoding_exception(self):
        self._mg.add_character_encoding("h", Symbol.DOT, previous=None)
        self._mg.add_character_encoding("e", Symbol.DOT, previous="h")
        self._mg.add_character_encoding("l", Symbol.DASH, previous="h")
        self.assertRaises(TelegraphException, self._mg.add_character_encoding, "o", Symbol.DASH, previous="g")

    def test_encode_text(self):
        self._mg.add_character_encoding("h", Symbol.DOT, previous=None)
        self._mg.add_character_encoding("e", Symbol.DOT, previous="h")
        self._mg.add_character_encoding("l", Symbol.DASH, previous="h")
        self._mg.add_character_encoding("o", Symbol.DASH, previous="e")
        self._mg.add_character_encoding("w", Symbol.DOT, previous="l")
        self._mg.add_character_encoding("a", Symbol.DASH, previous="l")
        self._mg.add_character_encoding("r", Symbol.DOT, previous="e")
        self._mg.add_character_encoding("y", Symbol.DASH, previous=None)
        self._mg.add_character_encoding("u", Symbol.DOT, previous="y")
        
        enc_text = self._mg.encode_text("hello how are you")
        self.assertEqual([". .. .- .- ..-", ". ..- .-.", ".-- ... ..", "- ..- -."], enc_text)

class TestR4(unittest.TestCase):
    def setUp(self):
        self._mg = TelegraphManager()
        self._mg.add_station("City1")
        self._mg.add_station("City2")
        self._mg.add_station("City3")
        self._mg.add_station("City4")
        self._mg.add_station("City5")
        self._mg.add_station("City6")

    def test_are_connected(self):
        self._mg.add_connection("City4", "City6")
        self._mg.add_connection("City1", "City3")
        self.assertTrue(self._mg.are_connected("City4", "City6"))
        self.assertTrue(self._mg.are_connected("City1", "City3"))
        self.assertFalse(self._mg.are_connected("City4", "City5"))

    def test_are_connected_bidir(self):
        self._mg.add_connection("City4", "City6")
        self._mg.add_connection("City1", "City3")
        self.assertTrue(self._mg.are_connected("City4", "City6"))
        self.assertTrue(self._mg.are_connected("City1", "City3"))
        self.assertTrue(self._mg.are_connected("City6", "City4"))
        self.assertTrue(self._mg.are_connected("City3", "City1"))
        self.assertFalse(self._mg.are_connected("City4", "City5"))

    def test_link_neighbours(self):
        self._mg.add_connection("City1", "City2")
        self._mg.add_connection("City1", "City3")
        self._mg.add_connection("City2", "City3")
        self._mg.add_connection("City2", "City4")
        self._mg.add_connection("City3", "City5")
        self._mg.add_connection("City4", "City5")
        self._mg.add_connection("City5", "City6")
        
        self.assertEqual(["City5"], sorted(list(self._mg.get_connected_stations("City6"))))
        self.assertEqual(["City3", "City4", "City6"], sorted(list(self._mg.get_connected_stations("City5"))))
        self.assertEqual(["City2", "City5"], sorted(list(self._mg.get_connected_stations("City4"))))
        self.assertEqual(["City1", "City2", "City5"], sorted(list(self._mg.get_connected_stations("City3"))))
        self.assertEqual(["City1", "City3", "City4"], sorted(list(self._mg.get_connected_stations("City2"))))
        self.assertEqual(["City2", "City3"], sorted(list(self._mg.get_connected_stations("City1"))))


class TestR5(unittest.TestCase):
    def setUp(self):
        self._mg = TelegraphManager()
        self._mg.add_station("City1")
        self._mg.add_station("City2")
        self._mg.add_station("City3")
        self._mg.add_station("City4")
        self._mg.add_station("City5")
        self._mg.add_station("City6")


    def test_find_path(self):
        self._mg.add_connection("City1", "City2")
        self._mg.add_connection("City1", "City3")
        self._mg.add_connection("City2", "City3")
        self._mg.add_connection("City2", "City4")
        self._mg.add_connection("City3", "City5")
        self._mg.add_connection("City4", "City5")
        self._mg.add_connection("City5", "City6")

        path = self._mg.get_shortest_path("City1", "City6")

        all_paths = {
            ("City1", "City2", "City4", "City5", "City6"),
            ("City1", "City3", "City5", "City6"),
            ("City1", "City2", "City3", "City5", "City6"),
            ("City1", "City3", "City2", "City4", "City5", "City6"),
        }

        self.assertIn(tuple(path), all_paths)
        

    def test_find_shortest_path(self):
        self._mg.add_connection("City1", "City2")
        self._mg.add_connection("City1", "City3")
        self._mg.add_connection("City2", "City3")
        self._mg.add_connection("City2", "City4")
        self._mg.add_connection("City3", "City5")
        self._mg.add_connection("City4", "City5")
        self._mg.add_connection("City5", "City6")

        self.assertEqual(["City1", "City3", "City5", "City6"], self._mg.get_shortest_path("City1", "City6"))

    
    def test_find_path_tree(self):
        self._mg.add_connection("City1", "City2")
        self._mg.add_connection("City1", "City3")
        self._mg.add_connection("City2", "City4")
        self._mg.add_connection("City2", "City5")
        self._mg.add_connection("City3", "City6")

        path = self._mg.get_shortest_path("City1", "City6")
        self.assertEqual(["City1", "City3", "City6"], self._mg.get_shortest_path("City1", "City6"))
        