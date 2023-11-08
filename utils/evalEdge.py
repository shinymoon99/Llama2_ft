from scipy.optimize import linear_sum_assignment
import numpy as np
def span_similarity(span1, span2):
    # Define a similarity score between two spans.
    # You can use various metrics such as Jaccard similarity, overlap ratio, etc.
    # For example, you can calculate Jaccard similarity:
    intersection = len(set(span1) & set(span2))
    union = len(set(span1) | set(span2))
    return intersection / union if union > 0 else 0
def edge_similarity(edge1,edge2):
    startsim = span_similarity(edge1[0],edge2[0])
    endsim = span_similarity(edge1[1],edge2[1])

    return (startsim+endsim)/2
        
def calculate_similarity_matrix(test_list, gold_list):
    # Calculate a similarity matrix where each cell (i, j) represents
    # the similarity score between test_list[i] and gold_list[j].
    similarity_matrix = np.zeros((len(test_list), len(gold_list)))
    for i, test_span in enumerate(test_list):
        for j, gold_span in enumerate(gold_list):
            similarity_matrix[i][j] = edge_similarity(test_span, gold_span)
    return similarity_matrix

def find_best_matching(test_list, gold_list):
    # Example usage with different lengths:
    # test_list = [[(0, 5),], (10, 15), (20, 25)]
    # gold_list = [(2, 7), (11, 16)]

    # best_matching, match_rate = find_best_matching(test_list, gold_list)
    # print("Best Matching:", best_matching)
    # print("Overall Match Rate:", match_rate)


    # Calculate the similarity matrix.
    similarity_matrix = calculate_similarity_matrix(test_list, gold_list)
    
    # Use the Hungarian algorithm to find the optimal assignment that maximizes the overall match rate.
    row_indices, col_indices = linear_sum_assignment(-similarity_matrix)
    
    # Calculate the overall match rate.
    if len(test_list)>0:
        match_rate = similarity_matrix[row_indices, col_indices].sum()/len(test_list)
    else:
        match_rate = 0
    # Create a dictionary to represent the best matching.
    best_matching = {}
    # for i, j in zip(row_indices, col_indices):
    #     if i < len(test_list) and j < len(gold_list):
    #         best_matching[tuple(test_list[i])] = gold_list[j]
    
    return test_list, match_rate