class Solution(object):
    def intersection(self, nums1, nums2):
        """
        :type nums1: List[int]
        :type nums2: List[int]
        :rtype: List[int]
        """
        result = []
        for num in nums1:
            if num in nums2 and num not in result:
                result.append(num)
        return result