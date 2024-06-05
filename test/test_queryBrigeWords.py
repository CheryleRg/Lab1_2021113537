# 作   者：林枭熠
# 开发时间:2024/6/5 下午3:05
import unittest
import WordFileGraph


class TestQueryBridgeWords(unittest.TestCase):
    def setUp(self):
        # 准备测试用例
        self.graph = WordFileGraph.WordFileGraph('../test1.txt')
        print("开始测试")

    def test_1(self):
        # 测试word1不在图中的情况
        result = self.graph.queryBridgeWords('sky', 'to')
        self.assertIsNone(result, "测试有误")
        print(f"测试1输出为{result}，测试通过")

    def test_2(self):
        # 测试word2不在图中的情况
        result = self.graph.queryBridgeWords('explore', 'sky')
        self.assertIsNone(result, "测试有误")
        print(f"测试2输出为{result}，测试通过")

    def test_3(self):
        # 测试没有桥接词的情况
        result = self.graph.queryBridgeWords('seek', 'to')
        self.assertEqual(result, [], "测试有误")
        print(f"测试3输出为{result}，测试通过")

    def test_4(self):
        # 测试存在桥接词的情况
        result = self.graph.queryBridgeWords('explore', 'new')
        self.assertEqual(result, ["strange"], "测试有误")
        print(f"测试4输出为{result}，测试通过")


if __name__ == '__main__':
    unittest.main()
