提示工程

条目
讨论

大陆简体
阅读
编辑
查看历史

工具
外观 隐藏
文本

小

标准

大
宽度

标准

宽
颜色 （测试版）

自动

浅色

深色
维基百科，自由的百科全书
提示工程
技术、​工作领域
上级分类	writing、​计算机程序设计 编辑
用途	人工智能艺术、​生成式人工智能 编辑
话题方面	人工智能 编辑
产品	AI提示 编辑
从业者	提示工程师、​AI prompter 编辑
提示工程（Prompt engineering）是人工智能中的一个概念，特别是自然语言处理（NLP）。 在提示工程中，任务的描述会被嵌入到输入中。例如，不是隐含地给予模型一定的参数，而是以问题的形式直接输入。 提示工程的典型工作方式是将一个或多个任务转换为基于提示的数据集，并通过所谓的“基于提示的学习（prompt-based learning）”来训练语言模型。[1][2] 提示工程可以从一个大型的“冻结”预训练语言模型开始工作，其中只学习了提示的表示方法，即所谓的“前缀调整（prefix-tuning）”或“提示调整（prompt tuning）”。[3][4] 语言模型GPT-2和GPT-3[5]是提示工程的重要步骤。

历史
2021年，使用多个NLP数据集的多任务提示工程在新任务上显示出良好的性能。[6] 在小样本学习的例子中，包含思维链的提示在语言模型中显示出更好的推理能力。[7]零样本学习中，在提示中预留鼓励思考链的语句（如“让我们一步一步地思考”）可能会提高语言模型在多步骤推理问题中的表现。[8]这些工具的广泛可及性由几个开源笔记和社区主导的图像合成项目的发布所推动。[9]

一份关于处理提示的描述报告称，在2022年2月，约有170个数据集的2000多个公共提示可用。[10]

2022年，DALL-E、Stable Diffusion、Midjourney等机器学习模型得到公开发布。这些模型以文本提示为输入，并使用其生成图像，这影响了一个与文生图提示有关的新品种提示工程。[11]

文字到文字
思路链
思路链（Chain-of-thought）(CoT) 是文字提示（Textual prompting）的一种技术，该技术通过提示 LLM 生成一系列中间步骤来提高 LLM 的推理能力，这些中间步骤会导致多步骤问题的最终答案。[12] 该技术由谷歌研究人员于 2022 年首次提出。[13][14]

提示链接
提示链接（Prompt chaining）是一种在对话式AI中文本提示使用的一种技术，用于创建更具动态性和上下文感知的聊天机器人。它涉及使用一个提示的输出作为下一个提示或对话的一部分的输入。通过将提示链接在一起，您的对话助手可以更轻松地适应您没有设计的情况，同时保持良好的对话。[15][16]

文字到图像
2022 年，DALL-E 2、Stable Diffusion 和 Midjourney 等文本到图像模型向公众发布。[17]

文字到影片
文本到影片生成 (TTV) 是一项新兴技术，可以直接根据文本描述创建影片。这个新颖的领域具有显着改变影片制作、动画和故事讲述的潜力。通过利用人工智能的力量，TTV 允许用户绕过传统的影片编辑工具，将他们的想法转化为移动图像。

非文字提示
一些方法用非文本输入来增强或替换自然语言文本提示。

提示注入
参见：SQL注入、跨站脚本和后门
提示注入(英语：Prompt injection)，是一系列相关的计算机安全漏洞，通过让经过训练的机器学习模型（如大型语言模型）遵循人类给出的指令来遵循恶意用户提供的指令，这与指令遵循系统的预期操作形成对比，其中机器学习模型只遵循机器学习模型操作员所提供的可信指令（提示）。[18][19][20]

提示性注入可以被看作是一种使用对抗性提示工程的代码注入攻击。2022年，NCC集团将提示注入定性为AI/ML系统的一类新漏洞。[21]

在2023年左右，提示注入在针对ChatGPT和类似的聊天机器人的次要漏洞中出现，例如揭示系统隐藏的初始提示，[22]或者欺骗聊天机器人参与到违反聊天机器人内容政策的对话。 [23]

根据OWASP有关大型语言模型的安全漏洞报告指出，提示注入是大型语言模型十大安全漏洞之首。 [24][25]

参见
icon	语言主题
	技术主题
机器学习
深度学习
通用人工智能
生成式人工智能
图灵测试
外部链接
Prompt engineering （Six strategies for getting better results） （页面存档备份，存于互联网档案馆）
Prompt examples （Explore what's possible with some example prompts） （页面存档备份，存于互联网档案馆）
A systematic overview of prompt engineering through programming （页面存档备份，存于互联网档案馆）
参考文献

Scholia上有关提示工程的信息
 Alec Radford; Jeffrey Wu; Rewon Child; David Luan; Dario Amodei; 伊尔亚·苏茨克维, Language Models are Unsupervised Multitask Learners (PDF), 2019, Wikidata Q95726769 （英语）
 Pengfei Liu; Weizhe Yuan; Jinlan Fu; Zhengbao Jiang; Hiroaki Hayashi; Graham Neubig, Pre-train, Prompt, and Predict: A Systematic Survey of Prompting Methods in Natural Language Processing (PDF), 2021-07-28, arXiv:2107.13586 可免费查阅, Wikidata Q109286554 （英语）
 Xiang Lisa Li; Percy Liang. Prefix-Tuning: Optimizing Continuous Prompts for Generation. Proceedings of the 59th Annual Meeting of the Association for Computational Linguistics and the 11th International Joint Conference on Natural Language Processing (Volume 1: Long Papers). 2021-08: 4582–4597. doi:10.18653/V1/2021.ACL-LONG.353. Wikidata Q110887424 （英语）.
 Brian Lester; Rami Al-Rfou; Noah Constant. The Power of Scale for Parameter-Efficient Prompt Tuning. Proceedings of the 2021 Conference on Empirical Methods in Natural Language Processing. 2021-11: 3045–3059. arXiv:2104.08691 可免费查阅. doi:10.18653/V1/2021.EMNLP-MAIN.243. Wikidata Q110887400 （英语）.
 Tom Brown; Benjamin Mann; Nick Ryder; et al. Language Models are Few-Shot Learners. arXiv, Advances in Neural Information Processing Systems 33. Advances in Neural Information Processing Systems. 2020-05-28. ISSN 2331-8422. S2CID 218971783. arXiv:2005.14165 可免费查阅. doi:10.48550/ARXIV.2005.14165. Wikidata Q95727440 （英语）.
 Victor Sanh; Albert Webson; Colin Raffel; et al, Multitask Prompted Training Enables Zero-Shot Task Generalization (PDF), 2021-10-15, arXiv:2110.08207 可免费查阅, Wikidata Q108941092 （英语）
 Jason Wei; Xuezhi Wang; Dale Schuurmans; Maarten Bosma; Ed Chi; 黎曰国; Denny Zhou, Chain of Thought Prompting Elicits Reasoning in Large Language Models (PDF), 2022-01-28, arXiv:2201.11903 可免费查阅, doi:10.48550/ARXIV.2201.11903, Wikidata Q111971110 （英语）
 Takeshi Kojima; Shixiang Shane Gu; Machel Reid; Yutaka Matsuo; Yusuke Iwasawa. Large Language Models are Zero-Shot Reasoners (PDF). Advances in Neural Information Processing Systems. 2022-05-24. ISBN 978-1-7138-7108-8. arXiv:2205.11916 可免费查阅. doi:10.48550/ARXIV.2205.11916. Wikidata Q112124882 （英语）. |journal=被忽略 (帮助)
 Liu, Vivian; Chilton, Lydia. Design Guidelines for Prompt Engineering Text-to-Image Generative Models. ACM Digital Library. Association for Computing Machinery. [2022-10-26]. （原始内容存档于2022-10-26）.
 Stephen H. Bach; Victor Sanh; Zheng-Xin Yong; et al, PromptSource: An Integrated Development Environment and Repository for Natural Language Prompts (PDF), 2022-02-02, arXiv:2202.01279 可免费查阅, Wikidata Q110839490 （英语）
 Monge, Jim Clyde. Dall-E2 VS Stable Diffusion: Same Prompt, Different Results. MLearning.ai. 2022-08-25 [2022-08-31]. （原始内容存档于2022-08-26） （英语）.
 McAuliffe, Zachary. Google's Latest AI Model Can Be Taught How to Solve Problems. CNET. [10 March 2023]. （原始内容存档于2023-05-26） （英语）.
 Wei, Jason; Wang, Xuezhi; Schuurmans, Dale; Bosma, Maarten; Ichter, Brian; Xia, Fei; Chi, Ed H.; Le, Quoc V.; Zhou, Denny. Chain-of-Thought Prompting Elicits Reasoning in Large Language Models. 31 October 2022 [2023-06-12]. arXiv:2201.11903 可免费查阅. （原始内容存档于2023-06-07） （英语）.
 Wei, Jason; Zhou. Language Models Perform Reasoning via Chain of Thought. ai.googleblog.com. [10 March 2023]. （原始内容存档于2023-08-11） （英语）.
 Prompt Chaining & Large Language Models. [2023-06-13]. （原始内容存档于2023-07-08）.
 Voiceflow: The Future of AI-Powered Conversational Interfaces. [2023-06-13]. （原始内容存档于2023-06-13）.
 Monge, Jim Clyde. Dall-E2 VS Stable Diffusion: Same Prompt, Different Results. MLearning.ai. 2022-08-25 [2022-08-31]. （原始内容存档于2022-08-26） （英语）.
 Willison, Simon. 针对GPT-3的提示注入攻击. simonwillison.net. 12 September 2022 [2023-02-09]. （原始内容存档于2023-05-03） （英国英语）.
 Papp, Donald. What's Old Is New Again:. Hackaday. 2022-09-17 [2023-02-09]. （原始内容存档于2023-05-02） （美国英语）.
 Vigliarolo, Brandon. GPT-3 'prompt injection' attack causes bot bad manners. 19 September 2022 [2023-02-09]. （原始内容存档于2023-03-29） （英语）.
 Selvi, Jose. 探索提示注入攻击. NCC集团研究. 2022-12-05 [2023-02-09]. （原始内容存档于2023-05-03） （美国英语）.
 Edwards, Benj. AI-powered Bing Chat lost its mind when fed Ars Technica article. Ars Technica. 14 February 2023 [16 February 2023]. （原始内容存档于2023-02-22） （美国英语）.
 将ChatGPT变成其邪恶双胞胎的巧妙技巧. Washington Post. 2023 [2023年2月16日]. （原始内容存档于2023年3月6日）.
 OWASP Top 10 for Large Language Model Applications. OWASP. （原始内容存档于2023-09-07）.
 对抗性提示. （原始内容存档于2023-06-11）.