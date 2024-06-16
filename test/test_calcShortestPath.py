import unittest
import tempfile
from WordFileGraph import WordFileGraph


class TestCalcShortestPath(unittest.TestCase):

    def setUp(self):
        # 创建临时文件并写入内容
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False)
        self.temp_file.write("To @ explore strange new worlds, To seek out new life and new civilizations?")
        self.temp_file.close()
        # 使用临时文件路径初始化 WordFileGraph
        self.graph = WordFileGraph(self.temp_file.name)

    def tearDown(self):
        # 删除临时文件
        import os
        os.unlink(self.temp_file.name)

    def test_valid_word_in_graph(self):
        # word1 和 word2 都存在于图中，且存在一条最短路径
        shortest_path, path_weight = self.graph.calcShortestPath("To", "new")
        self.assertIsNotNone(shortest_path)
        self.assertIsNotNone(path_weight)
        # 将期望的最短路径列表中的单词转换为小写字母
        expected_shortest_path = [
            ['to', 'explore', 'strange', 'new'],
            ['to', 'seek', 'out', 'new']
        ]
        self.assertTrue(shortest_path in expected_shortest_path)
        self.assertEqual(path_weight, 3)
        print("测试1通过！")

    def test_word1_not_in_graph(self):
        # word1不在图中、word2存在于图中
        shortest_path, path_weight = self.graph.calcShortestPath("not_in_graph", "worlds")
        self.assertIsNone(shortest_path)
        self.assertIsNone(path_weight)
        print("测试2通过！")


    def test_words_all_not_in_graph(self):
        # word1和word2都不在图中
        shortest_path, path_weight = self.graph.calcShortestPath("not_in_graph", "not_in_graph_")
        self.assertIsNone(shortest_path)
        self.assertIsNone(path_weight)
        print("测试4通过！")

    def test_empty_word1(self):
        # word1为空字符串
        shortest_path, path_weight = self.graph.calcShortestPath("", "worlds")
        self.assertIsNone(shortest_path)
        self.assertIsNone(path_weight)
        print("测试5通过！")

    def test_empty_both_words(self):
        # word1和word2都为空字符串 ""
        shortest_path, path_weight = self.graph.calcShortestPath("", "")
        self.assertIsNone(shortest_path)
        self.assertIsNone(path_weight)
        print("测试6通过！")

    def test_no_path_exists(self):
        shortest_path, path_weight = self.graph.calcShortestPath("civilizations", "strange")
        self.assertIsNone(shortest_path)
        self.assertIsNone(path_weight)
        print("测试7通过！")


if __name__ == '__main__':
    unittest.main()
