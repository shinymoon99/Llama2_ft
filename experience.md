模型似乎倾向于将第一个子句识别为条件
    #possible reason 可能与训练数据集上的样例分布有关。模型错误地学习到了这一特征。
    #possible reason 也有可能与few shot的例子分布有关(据说few shot的样例分布影响输出)
# ideas
## idea 
使用chatGPT产生指定类型流程。
尝试微调ChatGPT产生较好效果。
用ChatGPT对于自己产生的例子做标注，喂给llama2-7b
## idea
流程可能与ICT知识关系较少，可以尝试微调其他大模型。看能不能产生较好结果