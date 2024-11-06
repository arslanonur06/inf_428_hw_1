class Solution(object):
    def findLengthOfLCIS(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        if not nums:
            return 0

        max_length = 1
        current_length = 1
        for i in range(1, len(nums)):
            if nums[i] > nums[i - 1]:
                current_length += 1
            else:
                current_length = 1  # Reset count for a new subsequence
            max_length = max(max_length, current_length)

        return max_length