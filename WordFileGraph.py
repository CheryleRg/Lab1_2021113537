# 作   者：林枭熠
# 开发时间:2024/5/17 下午4:07
import copy
import re
import random
import networkx as nx
import matplotlib.pyplot as plt


class WordFileGraph:
    def __init__(self, file_path):
        """
        功能需求1：初始化WordFileGraph类，先解析文本文件，然后创建有向图
        :param file_path: 用户输入的文本文件路径
        """
        self.file_path = file_path
        self.words = []
        self.graph = nx.DiGraph()
        self.parseTextFile()
        self.createGraph()

    def parseTextFile(self):
        """
        解析文本文件，提取单词并存储在self.words中
        """
        # 以只读方式打开文件
        with open(self.file_path, 'r') as file:
            # 读取文件内容并去除换行符和回车符
            text = file.read().replace('\n', ' ').replace('\r', ' ')
            # 使用正则表达式找到文本中的单词并存储在self.words中
            self.words = re.findall(r'[a-zA-Z]+', text)

    def createGraph(self):
        """
        根据单词关系创建图，并设置边的权重
        """
        for i in range(len(self.words) - 1):
            # 转换为小写字母，以便忽略大小写进行处理
            current_word = self.words[i].lower()
            next_word = self.words[i + 1].lower()
            # 如果图中没有当前单词节点，则添加节点
            if not self.graph.has_node(current_word):
                self.graph.add_node(current_word)
            # 如果图中没有下一个单词节点，则添加节点
            if not self.graph.has_node(next_word):
                self.graph.add_node(next_word)
            # 如果图中没有当前单词到下一个单词的边，则添加边并设置权重为1
            if not self.graph.has_edge(current_word, next_word):
                self.graph.add_edge(current_word, next_word, weight=1)
            # 如果已经存在当前单词到下一个单词的边，则增加权重计数
            else:
                self.graph[current_word][next_word]['weight'] += 1

    def showDirectedGraph(self):
        """
        功能需求2：展示有向图
        :return: 无
        """
        # 使用有向图的Kamada-Kawai布局
        pos = nx.kamada_kawai_layout(self.graph)
        # 获取边的权重标签
        labels = nx.get_edge_attributes(self.graph, 'weight')
        # 绘制节点和边
        nx.draw(self.graph, pos, with_labels=True, node_size=1000, node_color='skyblue', edge_color='gray')
        # 在边上绘制权重标签
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=labels, font_color='red')
        # 保存图表为base_graph.png
        plt.savefig('base_graph.png')
        # 显示图表
        plt.show()

    def queryBridgeWords(self, word1, word2):
        """
        功能需求3：用户输入任意两个英文单词word1、 word2，程序从图中查询它们的“桥接词”
        :param word1: word1
        :param word2: word2
        :return: 桥接词列表
        """
        bridge_words = []
        # 如果word1或word2不在图中，则返回None
        if word1.lower() not in self.graph.nodes or word2.lower() not in self.graph.nodes:
            return None
        # 遍历图中的所有节点，找到word1和word2之间存在的桥接词
        for node in self.graph.nodes:
            if node != word1.lower() and node != word2.lower():
                if self.graph.has_edge(word1.lower(), node) and self.graph.has_edge(node, word2.lower()):
                    bridge_words.append(node)
        return bridge_words

    def generateNewText(self, inputText):
        """
        功能需求4：用户输入一行新文本，程序根据图中桥接词生成新文本
        :param inputText: 用户输入的新文本
        :return: 生成的新文本
        """
        # 去除输入文本中的标点符号和空格
        input_words = re.findall(r'[a-zA-Z]+', inputText)
        output_text = ""
        # 遍历输入文本中的每个单词，查找其与下一个单词之间的桥接词，并随机选择一个作为输出文本中的单词
        for i in range(len(input_words) - 1):
            current_word = input_words[i].lower()
            next_word = input_words[i + 1].lower()
            bridge_words = self.queryBridgeWords(current_word, next_word)
            # 如果当前单词和下一个单词之间存在桥接词，则随机选择一个桥接词加上当前单词，作为输出文本中的单词，没有桥接词则直接输出当前单词
            if bridge_words is not None and len(bridge_words) > 0:
                bridge_word = random.choice(bridge_words)
                output_text += current_word + " " + bridge_word + " "
            else:
                output_text += current_word + " "
        # 输出最后一个单词
        output_text += input_words[-1]
        return output_text

    @staticmethod
    def custom_shortest_path(graph, start, end):
        """
        自定义的 Dijkstra 最短路径算法
        :param graph: 求最短路径的图：nx.DiGraph()
        :param start: 源节点
        :param end: 目的节点
        :return: shortest_path, path_weight
        """

        # 初始化最短路径和路径长度
        shortest_path = []
        path_weight = 0

        # 如果起始节点和目标节点相同，则返回空路径和路径长度 0
        if start == end:
            shortest_path = [start]
            return shortest_path, path_weight

        # 使用 Dijkstra 算法计算最短路径
        # 初始化距离和前驱节点
        distance = {node: float('inf') for node in graph.nodes()}
        predecessor = {node: None for node in graph.nodes()}
        distance[start] = 0

        # 定义一个辅助函数，用于从未访问的节点中选择距离最短的节点
        def min_distance_node(nodes, distance):
            return min(nodes, key=lambda node: distance[node])

        # 遍历所有节点
        unvisited_nodes = set(graph.nodes())
        # 直到所有节点都访问完毕
        while unvisited_nodes:
            # 从未访问的节点中选择距离最短的节点
            current_node = min_distance_node(unvisited_nodes, distance)
            unvisited_nodes.remove(current_node)

            # 更新与当前节点相邻节点的距离和前驱节点
            for neighbor in graph.neighbors(current_node):
                weight = graph[current_node][neighbor]['weight']
                new_distance = distance[current_node] + weight
                if new_distance < distance[neighbor]:
                    distance[neighbor] = new_distance
                    predecessor[neighbor] = current_node

        # 如果目标节点没有被访问（即没有路径），则抛出异常或返回None
        if distance[end] == float('inf'):
            raise ValueError("No path between the given nodes.")

        # 构建最短路径
        current_node = end
        path_weight = distance[end]  # 直接使用计算得到的距离作为路径权重
        while predecessor[current_node] is not None:
            shortest_path.insert(0, current_node)
            current_node = predecessor[current_node]
        shortest_path.insert(0, start)  # 确保起始节点在路径中

        return shortest_path, path_weight

    def calcShortestPath(self, word1, word2):
        """
        功能需求5：计算两个单词之间的最短路径，并将其展示在图中
        :param word1: word1
        :param word2: word2
        :return: 最短路径列表和路径长度
        """
        # 如果word1与word2之间可达，则计算最短路径并展示在图中
        try:
            # 计算最短路径和长度
            shortest_path, path_weight = self.custom_shortest_path(self.graph, word1.lower(), word2.lower())
            local_graph = copy.deepcopy(self.graph)
            # 标记最短路径的边
            for i in range(len(shortest_path) - 1):
                current_word = shortest_path[i]
                next_word = shortest_path[i + 1]
                local_graph[current_word][next_word]['highlight'] = 'red'
            # 展示图表
            pos = nx.kamada_kawai_layout(local_graph)
            edge_colors = [local_graph[u][v]['highlight'] if 'highlight' in local_graph[u][v] else 'gray' for u, v in
                           local_graph.edges()]
            labels = nx.get_edge_attributes(local_graph, 'weight')
            nx.draw(local_graph, pos, with_labels=True, node_size=1000, node_color='skyblue', edge_color=edge_colors)
            nx.draw_networkx_edge_labels(local_graph, pos, edge_labels=labels, font_color='red')
            plt.show()
            return shortest_path, path_weight
        # 如果word1与word2之间不可达，则返回None
        except ValueError:
            return None, None

    def randomWalk(self):
        """
        功能需求6：随机游走算法，随机选择图中的节点进行游走，直到出现第一条重复的边为止，或者进入的某个节点不存在出边为止。
        :return: 随机游走经过的节点列表
        """
        # 随机选择一个节点作为起始节点
        start_node = random.choice(list(self.graph.nodes()))
        # 定义一个集合来记录已经访问过的边，一个列表来记录随机游走经过的节点
        visited_nodes_list = []
        visited_edges_set = set()
        current_node = start_node
        visited_nodes_list.append(current_node)
        # 随机游走循环
        while True:
            # 随机选择当前节点的出边
            next_nodes = list(self.graph.successors(current_node))
            # 如果当前节点不存在出边，则退出循环
            if not next_nodes:
                break
            # 随机选择一个出边作为下一个节点
            next_node = random.choice(next_nodes)
            # 如果为重复的边，则退出循环
            if (current_node, next_node) in visited_edges_set:
                break
            # 否则，标记当前边为已访问，加入集合
            visited_edges_set.add((current_node, next_node))
            # 将出边的节点加入列表
            visited_nodes_list.append(next_node)
            current_node = next_node
        return visited_nodes_list


def main():
    file_path = input("请输入文本文件的路径和文件名：")
    graph_generator = WordFileGraph(file_path)

    while True:
        print("\n请选择功能：")
        print("1. 展示有向图")
        print("2. 查询桥接词")
        print("3. 根据桥接词生成新文本")
        print("4. 计算两个单词之间的最短路径")
        print("5. 随机游走")
        print("6. 退出程序")

        choice = input("请输入数字进行选择：")
        if choice == "1":
            graph_generator.showDirectedGraph()
        elif choice == "2":
            word1 = input("请输入word1：")
            word2 = input("请输入word2：")
            bridge_words = graph_generator.queryBridgeWords(word1, word2)
            if bridge_words is not None:
                if len(bridge_words) >= 1:
                    bridge_words_str = ", ".join(bridge_words)
                    print("{} 与 {} 之间的桥接词为：{}.".format(word1, word2, bridge_words_str))
                else:
                    print("{} 与 {} 之间没有桥接词".format(word1, word2))
            else:
                print("word1 或 word2 未在图中")
        elif choice == "3":
            input_text = input("请输入一行新文本：")
            output_text = graph_generator.generateNewText(input_text)
            print("生成的新文本: ", output_text)
        elif choice == "4":
            word1 = input("请输入word1：")
            word2 = input("请输入word2：")
            shortest_path, path_weight = graph_generator.calcShortestPath(word1, word2)
            if shortest_path and path_weight is not None:
                shortest_path_str = "->".join(shortest_path)
                print("{} 与 {} 之间的最短路径为：{}".format(word1, word2, shortest_path_str))
                print("最短路径的长度为: {}".format(path_weight))
            else:
                print("两个单词之间没有最短路径。")
        # elif choice == "5":
        #     visited_nodes = graph_generator.randomWalk()
        #     visited_nodes_str = " ".join(visited_nodes)
        #     print("随机游走经过的节点生成的文本: {}".format(visited_nodes_str))
        # elif choice == "6":
        #     break
        else:
            print("无效选择。请重新输入。")


if __name__ == '__main__':
    main()
