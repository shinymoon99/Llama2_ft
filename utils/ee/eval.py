class DedupList(list):
    """定义去重的list
    """
    def append(self, x):
        if x not in self:
            super(DedupList, self).append(x)
def evaluate(data, threshold=0):
    """评估函数，计算f1、precision、recall
    """
    # event = [[((1,10),配置-内容),（(2,12),配置-地点)],[]]
    ex, ey, ez = 1e-10, 1e-10, 1e-10  # 事件级别
    ax, ay, az = 1e-10, 1e-10, 1e-10  # 论元级别
    for d in tqdm(data, ncols=0):
        pred_events = extract_events(d['text'], threshold, False)
        # 事件级别
        R, T = DedupList(), DedupList()
        for event in pred_events:
            if any([argu[1] == u'触发词' for argu in event]):
                R.append(list(sorted(event)))
        for event in d['events']:
            T.append(list(sorted(event)))
        for event in R:
            if event in T:
                ex += 1
        ey += len(R)
        ez += len(T)
        # 论元级别
        R, T = DedupList(), DedupList()
        for event in pred_events:
            for argu in event:
                if argu[1] != u'触发词':
                    R.append(argu)
        for event in d['events']:
            for argu in event:
                if argu[1] != u'触发词':
                    T.append(argu)
        for argu in R:
            if argu in T:
                ax += 1
        ay += len(R)
        az += len(T)
    e_f1, e_pr, e_rc = 2 * ex / (ey + ez), ex / ey, ex / ez
    a_f1, a_pr, a_rc = 2 * ax / (ay + az), ax / ay, ax / az
    return e_f1, e_pr, e_rc, a_f1, a_pr, a_rc
