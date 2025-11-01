"""
Merge Sort Service Implementation
Performs distributed sorting of students by CGPA
"""

import time


class MergeSortService:
    """
    Implements Merge Sort algorithm for student ranking by CGPA
    """
    
    @staticmethod
    def merge(left, right):
        """Merge two sorted lists by CGPA (descending)"""
        result = []
        i = j = 0
        
        while i < len(left) and j < len(right):
            # Sort by CGPA descending (highest first)
            if left[i].cgpa >= right[j].cgpa:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        
        result.extend(left[i:])
        result.extend(right[j:])
        return result
    
    @staticmethod
    def merge_sort(students):
        """Recursive merge sort implementation for CGPA"""
        if len(students) <= 1:
            return students
        
        mid = len(students) // 2
        left = MergeSortService.merge_sort(students[:mid])
        right = MergeSortService.merge_sort(students[mid:])
        
        return MergeSortService.merge(left, right)
    
    @staticmethod
    def perform_sort(students):
        """
        Perform merge sort on student data by CGPA
        
        Args:
            students: List of student objects
        
        Returns:
            Dictionary with sorted students and processing time
        """
        start_time = time.time()
        
        sorted_students = MergeSortService.merge_sort(list(students))
        
        processing_time = time.time() - start_time
        
        return {
            'sorted_students': sorted_students,
            'processing_time': processing_time
        }
