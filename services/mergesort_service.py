"""
Merge Sort Service Implementation
Performs distributed sorting of students by CGPA or grade
"""

import time


class MergeSortService:
    """
    Implements Merge Sort algorithm for student ranking
    """
    
    # Grade ordering for sorting
    GRADE_ORDER = {
        'A': 1, 'A-': 2, 'B+': 3, 'B': 4, 'B-': 5,
        'C+': 6, 'C': 7, 'C-': 8, 'D': 9, 'F': 10
    }
    
    @staticmethod
    def merge(left, right, sort_by):
        """Merge two sorted lists"""
        result = []
        i = j = 0
        
        while i < len(left) and j < len(right):
            if sort_by == "cgpa":
                # Sort by CGPA descending
                if left[i].cgpa >= right[j].cgpa:
                    result.append(left[i])
                    i += 1
                else:
                    result.append(right[j])
                    j += 1
            elif sort_by == "grade":
                # Sort by grade ascending (A is better)
                left_order = MergeSortService.GRADE_ORDER.get(left[i].grade, 99)
                right_order = MergeSortService.GRADE_ORDER.get(right[j].grade, 99)
                if left_order <= right_order:
                    result.append(left[i])
                    i += 1
                else:
                    result.append(right[j])
                    j += 1
            elif sort_by == "name":
                # Sort by name alphabetically ascending
                if left[i].name.lower() <= right[j].name.lower():
                    result.append(left[i])
                    i += 1
                else:
                    result.append(right[j])
                    j += 1
            else:
                # Default: sort by CGPA
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
    def merge_sort(students, sort_by):
        """Recursive merge sort implementation"""
        if len(students) <= 1:
            return students
        
        mid = len(students) // 2
        left = MergeSortService.merge_sort(students[:mid], sort_by)
        right = MergeSortService.merge_sort(students[mid:], sort_by)
        
        return MergeSortService.merge(left, right, sort_by)
    
    @staticmethod
    def perform_sort(students, sort_by):
        """
        Perform merge sort on student data
        
        Args:
            students: List of student objects
            sort_by: "cgpa" or "grade"
        
        Returns:
            Dictionary with sorted students and processing time
        """
        start_time = time.time()
        
        sorted_students = MergeSortService.merge_sort(list(students), sort_by)
        
        processing_time = time.time() - start_time
        
        print(f"[MergeSort] Sort by: {sort_by}")
        print(f"[MergeSort] Sorted {len(sorted_students)} students")
        if sorted_students:
            print(f"[MergeSort] Top student: {sorted_students[0].name} ({sorted_students[0].grade}, CGPA: {sorted_students[0].cgpa})")
        print(f"[MergeSort] Processing time: {processing_time:.4f} seconds")
        
        return {
            'sorted_students': sorted_students,
            'processing_time': processing_time
        }
