### 事件中的隐层含义(implicitly connoted by events)：
* [Universal Decompositional Semantics on Universal Dependencies. EMNLP2016][1] 提出了一个增加数据集的框架，Decomp（Universal Dependencies project，具有全局语义分解），提供多语言的句法标注标准和一个使用这个标准的语料库集合,在三个领域使用，语义角色分解（semantic role decomposition），事件分解（event decomposition）和word sense decomposition
* [Connotation Frames: A Data-Driven Investigation. ACL2016][2] 通过一个特定的谓语动词的选择(比如x violated y)，写作者巧妙的蕴含一系列关于实体x和y的情感和预设的事实，（1）写作者角度：将x视为敌人，y视为受害者，（2）实体角度：y可能不喜欢x，（3）效果：y发生了一些坏事（4）value:y是有价值的东西，（5）精神状态：y对这件事感到苦恼。这篇论文提出了一个基于词的分布式表示和不同类型隐含关系之间相互作用的预测谓语动词的内涵的框架
### 事件情感极性(sentiment polarities of events)
* [Acquiring knowledge of affective events from blogs using label propagation. AAAI2016][3]这篇文章从个人博客中获取带有成见的积极和消极事件的知识，从大量的博客文章中创建了一个事件上下文图并且使用情感分类器和半监督标签传播算法发现情感事件。本文探索了几种图的配置，使用局部上下文，话语距离和事件之间共现通过边来传递情感极性。最后从图中取较高的情感事件并评价和人评判的一致性
* [Weakly supervised induction of affective events by optimizing semantic consistency. AAAI2018][4]这篇文章调查了个人故事语料库中情感事件的普遍性，为大规模情感事件的归纳(large scale induction of affective events)引入了弱监督方法。文章提出一个迭代学习框架，构建一个图，节点表示事件，使用现有的情感分析工具初始化他们的情感极性作为弱监督。事件基于下列三个语义关系类型进行连接，（1）语义相似度（2）语义对立关系(semantic opposition)（3）共享组件(shared components)。这个学习算法迭代的改善极性值
 


  [1]: http://www.aclweb.org/anthology/D16-1177
  [2]: https://arxiv.org/pdf/1506.02739.pdf
  [3]: http://www.aaai.org/ocs/index.php/AAAI/AAAI16/paper/download/12488/12044
  [4]: http://www.cs.utah.edu/~hbding/papers/aaai2018_ding.pdf
