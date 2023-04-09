# 二分查找的实现
def binary_search(arr, target):
    """
    :param arr: 有序数组
    :param target: 目标值
    :return: 目标值在数组中的索引，若不存在则返回-1
    """
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1

